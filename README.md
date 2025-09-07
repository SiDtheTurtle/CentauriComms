# Centauri Comms
A simple Python library to communicate with the ELEGOO Centauri Carbon 3D printer over websockets

# Preamble
I'd like to use OctoPrint and others with my ELEGOO Centauri Carbon 3D printer, but as of writing the printer doesn't supoprt or allow it. So I will code something myself!

To do this, I needed a library that encapsulates how to send commands to the printer. Another user has already figured out how to send websocket messages over a proprietry protocol called SDCP to do this here:  https://github.com/WalkerFrederick/sdcp-centauri-carbon. You could use this as a crib with Postman, however part of the request message is a UUID and a timestamp, and it's a pain to have to keep editing it every time.

So I decided to create a library. This could be used as is, or as part of another project. Please take note of the AI section below before you use it in your own code.

# AI Disclosure
This project was also an experiment into how far AI has come in its coding ability. I can write Python, but I haven't worked with websockets before, and for a relatively simple project I thought it would be quicker to see if an AI code do it for me! Therefore I used Google Gemini Pro v2.5 to write it. The short answer is that it can do it, if you have a programmer's mindset to start with, but it does make errors that are not easy to spot if you are not a progrmmer- the code looks correct but it's not. Here's some key points:

- You need a programmer's head to frame the problem, and to to decide how to break up script into a library in the first place.
- I asked it to scrape the commands from the afformentioned GitHub page, but it continually daydreamed a set of made up codes, even though it insisted it got it from that page. The codes were close enough to reality that if you weren't reviewing the script, it would compile, but nothing would return from the printer.
- Sometimes it would just go nuts and we-write stuff that was working, into non-working code.

For full disclosure, you can see the 'vibe coding' session that created this code here: https://gemini.google.com/share/ab5c890f2540.

# Set-up
1. Install Python.
2. Install websockets and asyncio via pip.
3. Download this repo.
4. Edit config.json with your printer IP and mainboard ID. You can find the mainboard ID by inspecting the messages on the ELEGOO web UI through dev tools.
5. Run cli.py for an example of how to use the library.

# cli.py - Usage
`cli.py [-h] [-l] [--clean] [{0,1,128,129,130,131,134,258,320,386,403}] [parameter]`

Options:
- `-h, --help` Standard help output
- `-l, --list-commands` List all available commands and their descriptions.
- `--clean` Provides simplified, clean output removing JSON noise.
- `[parameter]` If the command code requires any parmeters, enter them here.
