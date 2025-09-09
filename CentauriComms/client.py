import asyncio
import json
import uuid
import time
import websockets
import os

class CentauriClient:
    # A client for sending commands to an ELEGOO Centauri Carbon 3D printer.

    def __init__(self):
        # Class entrypoint

        # Get the path to this script
        abs_path = os.path.dirname(os.path.abspath(__file__))

        # Define location for required json files
        config_file = os.path.join(abs_path,"config.json")
        commands_file = os.path.join(abs_path,"commands.json")

        # Load json files
        self.config = self._load_json_file(config_file)
        self.commands = self._load_json_file(commands_file)

    def _load_json_file(self, filename):
        # Simple wrapper to load json file with error handling

        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File '{filename}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error: The file '{filename}' contains invalid JSON.")

    def _create_printer_command(self, command_code: int, command_data: dict = None) -> dict:
        """Creates a message payload in the printer's specific format."""
        
        # Some commands have no data, just the code, if so send an empty data message
        if command_data is None: command_data = {}

        # Each message needs a unique uuid4 hex code
        request_id = uuid.uuid4().hex

        # Each message needs the correct maindboard id, or it will ignore the message
        mainboard_id = self.config.get("mainboard_id", "")
        
        # Each message needs a timestamp, have not experimented if this needs to be anywhere near the actual machine time
        timestamp = int(time.time())

        # Build up the request message
        message = {
            #"Id": "", # Doesn't seem to be required, commenting until proven
            "Data": {
                "Cmd": command_code, "Data": command_data, "RequestID": request_id, "MainboardID": mainboard_id, "TimeStamp": timestamp, "From": 1
            }
        }

        # Send the message back up to the command function
        return message

    async def send_command(self, command, parameter=None, output_format='raw'):
        # Send command to the printer and returns whatever response, if any
        # command (str): the numerical command code
        # parameter (str, optional): any parameter text for that code, for example the filename for a print command

        # Get the printer's IP address from the config file
        ip_address = self.config.get("printer_ip")
        if not ip_address:
            raise ValueError("Printer IP adress setting not found in config.json!")

        # Configure the websocket URL
        address = f"ws://{ip_address}/websocket"
        
        # Get the chosen command's json from the commands file
        chosen_command = self.commands.get(command)
        if not chosen_command:
            raise ValueError(f"Command '{command}' not found in commands.json!")

        command_data = chosen_command.get("data", {}).copy()

        # If the chosen command requires a paremter, set it in the message json
        if chosen_command.get("parameter") == "Filename" and parameter:
            command_data['Filename'] = f"/local/{parameter}.gcode"

        # Send the json message over websockets
        try:
            async with websockets.connect(address) as websocket:
                message = self._create_printer_command(chosen_command['code'], command_data)
                await websocket.send(json.dumps(message))
                response_str = await websocket.recv()
                response_json = json.loads(response_str)

                return response_json

        except ConnectionRefusedError:
            raise ConnectionError(f"Connection refused. Is the printer on at {ip_address}?")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e}")