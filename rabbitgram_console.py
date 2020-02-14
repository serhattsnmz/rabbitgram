import json
import argparse
import colorama

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

class RabbitgramConsole:

    def __init__(self):
        self.rabbitgram = Rabbitgram()

        self.args = self.parse_args()
        self.username = getattr(self.args, "username", None)
        self.password = getattr(self.args, "password", None)
        self.account  = getattr(self.args, "account", None)

        self.login(self.username, self.password)

    def parse_args(self):
        parser = argparse.ArgumentParser(description="Rabbitgram : The Fastest Instagram Scrapper")
        parser.add_argument("-u", "--username", metavar="", required=True, help="User username")
        parser.add_argument("-p", "--password", metavar="", required=True, help="User password")
        parser.add_argument("-a", "--account",  metavar="", required=True, help="Account username for scrapping")
        parser.add_argument("-P", "--path",     metavar="", help="The path for saving media.")
        parser.add_argument("-v", "--video",    action='store_true', help="Download user video. Default : False")
        return parser.parse_args()

    def login(self, username, password):
        print_info("Logging in...")
        result = self.rabbitgram.login(username, password)

        if result["status"]:
            print_success("Successfully logged in.")
        else:
            print_error(result["error"])

    def print_user_information(self):
        print_info("Getting user information...")
        result = self.rabbitgram.get_user_information(self.account)

        if result["status"]:
            print_success("User information successfully scrapped.", "\n\n")
            message = f"    User Information For '{self.account}'    "
            print_magenta(message)
            print_magenta("-" * len(message))

            user_info = [[f"{colorama.Fore.GREEN}{k} :" , f"{colorama.Fore.CYAN}{v}"] for k, v in result["user_info"].items()]
            print(tabulate(user_info, tablefmt="plain", colalign=("right", "left")))

        else:
            print_error(result["error"])

if __name__ == "__main__":
    colorama.init(autoreset=True)

    console = RabbitgramConsole()
    console.print_user_information()