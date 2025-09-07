import asyncio
import json
import argparse
import sys
from CentauriComms import CentauriClient

async def main():
    """Parses arguments and uses the CentauriClient to execute commands."""
    try:
        client = CentauriClient(config_path="config.json")
    except (FileNotFoundError, ValueError) as e:
        print(e)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Send a command to a 3D printer via WebSocket.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("command", nargs='?', choices=sorted(client.commands.keys()), help="The command code to send.")
    parser.add_argument("parameter", nargs='?', default=None, help="Optional parameter for commands that require one (e.g., a filename for 128).")
    parser.add_argument('-l', '--list-commands', action='store_true', help="List all available commands and their descriptions.")
    parser.add_argument('--clean', action='store_true', help="Provide simplified, clean output by extracting the nested 'Data' object from the response.")
    
    args = parser.parse_args()
    
    if args.list_commands:
        print("Available Commands:")
        for key in sorted(client.commands.keys(), key=int):
            value = client.commands[key]
            print(f"  {key:<5} - {value['description']}")
        sys.exit(0)

    if not args.command:
        parser.print_help()
        sys.exit(0)

    chosen_command = client.commands[args.command]
    
    command_to_run = args.command
    output_format = 'clean' if args.clean else 'raw'

    print(f"Executing command: '{chosen_command['description']}'...")
    print("-" * 50)

    try:
        response = await client.send_command(command_to_run, args.parameter, output_format=output_format)
        print("\nReceived response:")
        print(json.dumps(response, indent=4))
    except (ConnectionError, ValueError, RuntimeError) as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

