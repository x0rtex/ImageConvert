from colorama import Fore
from imageconvert.cli_interface import CLIInterface

if __name__ == "__main__":
    try:
        CLIInterface.handle_conversion()
    except KeyboardInterrupt:
        print(Fore.RED + "\n🚫 Operation cancelled by user")