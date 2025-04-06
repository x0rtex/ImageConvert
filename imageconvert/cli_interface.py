import os

from colorama import Fore, Style, init
from tqdm import tqdm
from imageconvert.image_converter import ImageConverter

init(autoreset=True)


class CLIInterface:
    @staticmethod
    def print_header():
        """Print header"""
        header: str = r"""
   ____                    _____                      __ 
  /  _/_ _  ___ ____ ____ / ___/__  ___ _  _____ ____/ /_
 _/ //  ' \/ _ `/ _ `/ -_) /__/ _ \/ _ \ |/ / -_) __/ __/
/___/_/_/_/\_,_/\_, /\__/\___/\___/_//_/___/\__/_/  \__/ 
               /___/                                     
        """
        print(Fore.CYAN + header)
        print(Fore.YELLOW + "✨ Image Conversion Wizard ✨" + Style.RESET_ALL)
        print(Fore.CYAN + "-" * 40 + Style.RESET_ALL)

    @staticmethod
    def get_input(prompt, color=Fore.CYAN, validator=None):
        """Get user input"""
        while True:
            value = input(color + prompt + Style.RESET_ALL).strip()
            if validator and not validator(value):
                print(Fore.RED + "❌ Invalid input, please try again")
                continue
            return value

    @staticmethod
    def get_confirmation(prompt):
        """Get user confirmation"""
        response = CLIInterface.get_input(
            f"{Fore.YELLOW}{prompt} (y/n): ",
            validator=lambda x: x.lower() in ['y', 'n']
        )
        return response.lower() == 'y'

    @staticmethod
    def handle_conversion():
        """Handle image conversion"""
        CLIInterface.print_header()

        directory = CLIInterface.get_input(
            "📂 Enter directory to search: ",
            validator=lambda x: os.path.isdir(x)
        )

        source_ext = CLIInterface.get_input("📤 Enter source extension (e.g., jpg): ")
        target_ext = CLIInterface.get_input("📥 Enter target extension (e.g., webp): ")

        compression = int(CLIInterface.get_input(
            "🎚  Enter compression (1-100): ",
            validator=lambda x: x.isdigit() and 1 <= int(x) <= 100
        ))

        converter = ImageConverter(directory, source_ext, target_ext, compression)

        try:
            with tqdm(desc=Fore.GREEN + "Converting images", unit="file") as pbar:
                converter.convert()
                pbar.total = converter.source_count
                pbar.update(converter.conversion_count)

            print(Fore.CYAN + "\n" + "=" * 40)
            print(Fore.YELLOW + f"🎉 Conversion complete! {converter.conversion_count} files converted")

            if CLIInterface.get_confirmation("\n🗑️  Would you like to manage files now?"):
                CLIInterface.handle_file_management(converter)

        except Exception as e:
            print(Fore.RED + f"\n❌ Error: {str(e)}")

    @staticmethod
    def handle_file_management(converter):
        """Handle file management after conversion"""
        print(Fore.CYAN + "\n1) Delete original source files")
        print("2) Delete newly converted files")
        print("3) Keep all files")

        choice = CLIInterface.get_input(
            Fore.YELLOW + "\nEnter choice (1-3): ",
            validator=lambda x: x in ['1', '2', '3']
        )

        if choice == '1':
            CLIInterface.delete_files(converter, 'source')
        elif choice == '2':
            CLIInterface.delete_files(converter, 'converted')
        else:
            print(Fore.BLUE + "🤝 Keeping all files")

    @staticmethod
    def delete_files(converter, file_type):
        """Delete files of specified type (source/converted)"""
        if CLIInterface.get_confirmation(f"⚠️  Confirm delete ALL {file_type} files?"):
            try:
                success, total = converter.delete_files(file_type)
                print(Fore.GREEN + f"\n✅ Successfully deleted {success}/{total} {file_type} files")
            except Exception as e:
                print(Fore.RED + f"\n❌ Deletion failed: {str(e)}")