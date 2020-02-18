import json
import argparse
import colorama
import yaml
import os
import sys

from termcolor              import cprint
from tabulate               import tabulate

from rabbitgram.rabbitgram  import Rabbitgram
from rabbitgram.logger      import Logger

print_red       = lambda message, end="\n" : cprint(message, "red",     end=end, attrs=['blink'])
print_green     = lambda message, end="\n" : cprint(message, "green",   end=end, attrs=['blink'])
print_magenta   = lambda message, end="\n" : cprint(message, "magenta", end=end, attrs=['blink'])
print_yellow    = lambda message, end="\n" : cprint(message, "yellow",  end=end, attrs=['blink'])
print_cyan      = lambda message, end="\n" : cprint(message, "cyan",    end=end, attrs=['blink'])

print_error     = lambda message, end="\n" : print_red("[x] " + message, end)
print_info      = lambda message, end="\n" : print_yellow("[i] " + message, end)
print_success   = lambda message, end="\n" : print_green("[\u2713] " + message, end)

capitalize_all  = lambda sentences : " ".join([k.capitalize() for k in sentences.split(" ")])

class RabbitgramConsole:
    
    def exception_handler(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as exp:
                print_error(str(exp))
                sys.exit(1)
        return wrapper

    @exception_handler
    def __init__(self):
        self.rabbitgram = Rabbitgram()

        self.args       = self.parse_args()
        self.username   = None
        self.password   = None
        self.account    = None
        self.file_path  = None

        self.get_settings()
        self.login(self.username, self.password)

    @exception_handler
    def parse_args(self):
        parser = argparse.ArgumentParser(description="Rabbitgram : The Fastest Instagram Scrapper")

        parser.add_argument("-u", "--username", metavar="", help="User username")
        parser.add_argument("-p", "--password", metavar="", help="User password")
        parser.add_argument("-a", "--account",  metavar="", help="Account username for scrapping")

        parser.add_argument("-P", "--path",     metavar="", help="The directory path for saving media")
        parser.add_argument("-o", "--output",   metavar="", help="The file path for saving result")
        parser.add_argument("-s", "--settings", metavar="", help="The settings file path")

        parser.add_argument("--info",     action='store_true', help="Show account info")
        parser.add_argument("--video",    action='store_true', help="Download user video. Default : False")
        return parser.parse_args()

    @exception_handler
    def get_settings(self):
        """
            Parse args and set attributes. These are required parameters.
            They must be given either args or in settings file.
            Include >> username - password - account
        """
        settings_path = getattr(self.args, "settings", None)
        settings = None

        username  = getattr(self.args, "username", None)
        password  = getattr(self.args, "password", None)
        account   = getattr(self.args, "account", None)

        # Open >> settings file
        if settings_path and os.path.isfile(settings_path):
            with open(settings_path) as f:
                settings = yaml.load(f, Loader=yaml.FullLoader)

        # Get >> username
        if not username and not (settings and settings.get("username", None)):
            raise Exception("Username must be given!")
        self.username = username if username else settings.get("username")

        # Get >> password
        if not password and not (settings and settings.get("password", None)):
            raise Exception("Password must be given!")
        self.password = password if password else settings.get("password") 

        # Get >> account name
        if not account and not (settings and settings.get("account", None)):
            raise Exception("Account name must be given!")
        self.account  = account if account else setting.get("account")

    @exception_handler
    def save_to_output_file(self, content):
        file_path = getattr(self.args, "output", None)
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                if type(content) == dict:
                    json.dump(content, f)
                else:
                    f.write(content)

    @exception_handler
    def login(self, username, password):
        print_info("Logging in...")
        result = self.rabbitgram.login(username, password)

        if result["status"]:
            print_success("Successfully logged in.")
        else:
            raise Exception(result["error"])

    @exception_handler
    def print_user_information(self):
        print_info("Getting user information...")
        result = self.rabbitgram.get_user_information(self.account)

        if result["status"]:
            print_success("User information successfully scrapped.", "\n\n")
            message = f"    User Information For '{self.account}'    "
            print_magenta(message)
            print_magenta("-" * len(message))

            max_string_lenght = max([len(k) for k in result['user_info'].keys()])

            user_info = [
                [f"{colorama.Fore.GREEN}{capitalize_all(k.replace('_', ' ')).ljust(max_string_lenght, '.')} :" , f"{colorama.Fore.CYAN}{v}"] 
                    for k, v in result["user_info"].items()]

            user_info_without_color = [
                [f"{capitalize_all(k.replace('_', ' ')).ljust(max_string_lenght, '.')} :" , f"{v}"] 
                    for k, v in result["user_info"].items()]
            
            print(tabulate(user_info, tablefmt="plain"))
            self.save_to_output_file(
                f'{message}\n{"-" * len(message)}\n{tabulate(user_info_without_color, tablefmt="plain")}'
                )

        else:
            raise Exception(result["error"])

if __name__ == "__main__":
    colorama.init(autoreset=True)
    console = RabbitgramConsole()

    # Show Account Information
    arg_info  = getattr(console.args, "info", None)
    if arg_info:
        console.print_user_information()
    