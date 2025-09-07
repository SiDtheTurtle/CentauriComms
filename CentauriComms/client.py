import asyncio
import json
import uuid
import time
import websockets
import os

class CentauriClient:
    """A client for sending commands to an ELEGOO Centauri Carbon 3D printer."""

    def __init__(self, config_path="config.json"):
        """
        Initializes the client.
        
        Args:
            config_path (str): Path to the user's config.json file.
        """
        self.config = self._load_json_file(config_path)
        
        # Load commands.json from the same directory as this client.py file
        here = os.path.dirname(os.path.abspath(__file__))
        commands_path = os.path.join(here, "commands.json")
        self.commands = self._load_json_file(commands_path)

    def _load_json_file(self, filename):
        """Loads data from a JSON file."""
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File '{filename}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error: The file '{filename}' contains invalid JSON.")

    def _create_printer_command(self, command_code: int, command_data: dict = None) -> dict:
        """Creates a message payload in the printer's specific format."""
        if command_data is None: command_data = {}
        request_id = uuid.uuid4().hex
        mainboard_id = self.config.get("mainboard_id", "")
        
        message = {
            "Id": "",
            "Data": {
                "Cmd": command_code, "Data": command_data, "RequestID": request_id,
                "MainboardID": mainboard_id, "TimeStamp": int(time.time() * 1000), "From": 1
            }
        }
        return message

    async def send_command(self, command, parameter=None, output_format='raw'):
        """
        Connects to the printer, sends a command, and returns the response.
        
        Args:
            command (str): The command code (e.g., '258').
            parameter (str, optional): An optional parameter for the command.
            output_format (str): 'raw' for the full response, 'clean' for a simplified version.
            
        Returns:
            A dictionary containing the printer's response.
        """
        ip_address = self.config.get("printer_ip")
        if not ip_address:
            raise ValueError("printer_ip not found in config.json")
            
        address = f"ws://{ip_address}/websocket"
        
        chosen_command = self.commands.get(command)
        if not chosen_command:
            raise ValueError(f"Command '{command}' not found in commands.json")

        command_data = chosen_command.get("data", {}).copy()

        if chosen_command.get("requires_parameter") == "filename" and parameter:
            command_data['Filename'] = f"/local/{parameter}.gcode"

        try:
            async with websockets.connect(address) as websocket:
                message = self._create_printer_command(chosen_command['code'], command_data)
                await websocket.send(json.dumps(message))
                response_str = await websocket.recv()
                response_json = json.loads(response_str)

                # --- UPDATED: Generic clean logic ---
                if output_format == 'clean':
                    try:
                        # Extract the nested 'Data' object
                        data_payload = response_json['Data']['Data']
                        
                        # If it's a dictionary, remove the 'Ack' field and return the rest
                        if isinstance(data_payload, dict):
                            cleaned_data = data_payload.copy()
                            cleaned_data.pop('Ack', None) # Safely remove 'Ack'
                            return cleaned_data
                        
                        # If it's not a dictionary (e.g., just a number), return it as is
                        return data_payload

                    except (KeyError, TypeError):
                        # If the structure is unexpected, fall back to the raw response
                        return response_json 
                else:
                    return response_json

        except ConnectionRefusedError:
            raise ConnectionError(f"Connection refused. Is the printer on at {ip_address}?")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e}")

