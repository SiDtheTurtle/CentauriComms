import asyncio
import json
import argparse
import sys
from CentauriComms import CentauriClient

    # Example wrapper to excute commands for CentauriComms client

async def main():
    try:
        client = CentauriClient()
    except (FileNotFoundError, ValueError) as e:
        print(e)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Send a command to an ELEGOO Centauri Carbon", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("command", nargs='?', choices=sorted(client.commands.keys()), help="The command code to send.")
    parser.add_argument("parameter", nargs='?', default=None, help="Optional parameter for commands that require one (e.g., a filename for 128).")
    
    args = parser.parse_args()
  
    try:
        response = await client.send_command(args.command, args.parameter)
        print(json.dumps(response, indent=4))
    except (ConnectionError, ValueError, RuntimeError) as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())