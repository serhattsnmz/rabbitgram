import os
import sys
import time
import json
import argparse
import yaml
import colorama

from datetime               import datetime
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
print_dialog    = lambda message, end="\n" : print_yellow("[>] " + message, end)

capitalize_all  = lambda sentences : " ".join([k.capitalize() for k in sentences.split(" ")])
is_path_file    = lambda path : True if len([k for k in path.split("/")[-1].split(".") if k != ""]) == 2 else False
is_path_dir     = lambda path : True if len([k for k in path.split("/")[-1].split(".") if k != ""]) == 1 else False

LOGGER = Logger().create_logger("console")

class RabbitgramConsole:
    
    def exception_handler(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as exp:
                LOGGER.exception("System Error!")
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

        self.get_settings()
        self.login(self.username, self.password)

    @exception_handler
    def parse_args(self):
        parser = argparse.ArgumentParser(description="Rabbitgram : The Fastest Instagram Scraper")

        parser.add_argument("-u", "--username", metavar="",          help="User username")
        parser.add_argument("-p", "--password", metavar="",          help="User password")
        parser.add_argument("-a", "--account",  metavar="",          help="Account username for scraping")

        parser.add_argument("-s", "--settings", metavar="",          help="The user settings file path")

        parser.add_argument("--info",           action='store_true', help="Get account general information")
        parser.add_argument("--posts",          action='store_true', help="Get user posts' information")
        parser.add_argument("--media",          action='store_true', help="Get user media information")
        parser.add_argument("-l", "--list",     metavar="",          help="Download from account list file")
        
        parser.add_argument("-o", "--output",   metavar="",          help="The file/directory path for saving result")
        parser.add_argument("--save",           action='store_true', help="Save the media or information")
        parser.add_argument("--download",       action='store_true', help="Download the media")
        parser.add_argument("--video",          action='store_true', help="Include videos for download. Default : False")

        args = parser.parse_args()
        return {
            "username"  : getattr(args, "username", None),
            "password"  : getattr(args, "password", None),
            "account"   : getattr(args, "account",  None),

            "settings"  : getattr(args, "settings", None),
            
            "info"      : getattr(args, "info",     False),
            "posts"     : getattr(args, "posts",    False),
            "media"     : getattr(args, "media",    False),
            "list"      : getattr(args, "list",     None),

            "output"    : getattr(args, "output",   None),
            "save"      : getattr(args, "save",     False),
            "download"  : getattr(args, "download", False),
            "video"     : getattr(args, "video",    False),
        }

    @exception_handler
    def get_settings(self):
        """
            Parse args and set attributes. These are required parameters.
            They must be given either args or in settings file.
            Include >> username - password - account
        """
        settings_path = self.args["settings"]
        settings = None

        username  = self.args["username"]
        password  = self.args["password"]
        account   = self.args["account"]

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
        if self.args["save"]:
            file_path = self.args["output"]
            if not file_path or not is_path_file(file_path):
                file_path = "./output.json" if type(content) in [dict, list] else "./output.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                if type(content) in [dict, list]:
                    json.dump(content, f, indent=4, sort_keys=True)
                else:
                    f.write(content)
                print_success(f"Result is saved in '{file_path}'.")

    @exception_handler
    def login(self, username, password):
        print_info("Logging in...")
        result = self.rabbitgram.login(username, password)

        if result["status"]:
            print_success("Successfully logged in.")
        else:
            raise Exception(result["error"])


    @exception_handler
    def user_information(self):
        print_info("Getting user information...")
        result = self.rabbitgram.get_user_information(self.account)

        if result["status"]:
            # Print user information
            print_success("User information successfully scraped.", "\n\n")
            message = f"User Information For '{self.account}'"
            print_magenta(message)
            print_magenta("-" * len(message))

            max_string_lenght = max([len(k) for k in result['user_info'].keys()])

            user_info = [
                [f"{colorama.Fore.GREEN}{capitalize_all(k.replace('_', ' ')).ljust(max_string_lenght, '.')} :" , f"{colorama.Fore.CYAN}{v}"] 
                    for k, v in result["user_info"].items()]

            user_info_without_color = [
                [f"{capitalize_all(k.replace('_', ' ')).ljust(max_string_lenght, '.')} :" , f"{v}"] 
                    for k, v in result["user_info"].items()]
            
            # Print table
            print(tabulate(user_info, tablefmt="plain"), end="\n\n")

            # Save output to file
            self.save_to_output_file(f'{message}\n{"-" * len(message)}\n{tabulate(user_info_without_color, tablefmt="plain")}')

        else:
            print_error(result["error"])
            print_error("User information could not be retrieved!")

    @exception_handler
    def post_list(self):        
        print_info("Getting account media links...")
        result = self.rabbitgram.get_user_media(self.account)
        if result["status"]:
            print_success("Account media successfully scraped.")

            images = []
            videos = []

            for post in result["user_media"]:
                for media in post["media_list"]:
                    if media["is_video"] : videos.append(media["video_url"])
                    else                 : images.append(media["picture_url"])

            message = f"""
            Total Found Media   : {len(result["user_media"])}
            Total Images        : {len(images)}
            Total Videos        : {len(videos)}
            """
            print_cyan(message)

            self.save_to_output_file(result["user_media"])
        else:
            print_error(result["error"])
            print_error("Account media links could not be retrieved.")

    @exception_handler
    def user_media(self):
        print_info("Getting account media links...")
        result = self.rabbitgram.get_user_media(self.account)

        if result["status"]:
            print_success("Account media successfully scraped.")

            # Get images and videos
            images = []
            videos = []

            for post in result["user_media"]:
                for media in post["media_list"]:
                    if media["is_video"] : videos.append(media["video_url"])
                    else                 : images.append(media["picture_url"])

            # Print account information to console
            message = f"""
            Total Found Media   : {len(result["user_media"])}
            Total Images        : {len(images)}
            Total Videos        : {len(videos)}
            """
            print_cyan(message)

            # Save to file
            if self.args["save"]:
                self.save_to_output_file({"images" : images, "videos" : videos})

            # Download media
            if self.args["download"]:

                # Create folder
                path = None
                if self.args["output"] and is_path_dir(self.args["output"]):
                    path = self.args["output"] + "/" + self.account
                else:
                    path = "./" + self.account

                if not os.path.exists(path) : os.makedirs(path)
                print_success("Folders are created.")

                # Download media
                _total = len(images) + len(videos)
                _downloaded = _error = _replica = 0

                message = "Total : {} | Downloaded : {} | Replica : {} | Error : {}"
                
                for media in result["user_media"]:
                    taken_time = datetime.fromtimestamp(media["timestamp"]).strftime("%Y-%m-%d-%H-%M-%S")
                    for inner_media in media["media_list"]:

                        # Create media path
                        media_path = path + "/" + taken_time + "-" + inner_media["id"]
                        media_path += ".jpg" if not inner_media["is_video"] else ".mp4"

                        # Replica
                        if os.path.isfile(media_path):
                            _replica += 1
                        else:
                            # Download video
                            if inner_media["is_video"] and self.args["video"]:
                                _r = self.rabbitgram.download_media(media_path, inner_media["video_url"])
                                if _r["status"] : _downloaded += 1
                                else : _error += 1

                            # Download photo
                            if not inner_media["is_video"]:
                                _r = self.rabbitgram.download_media(media_path, inner_media["picture_url"])
                                if _r["status"] : _downloaded += 1
                                else : _error += 1

                        print_info(message.format(_total, _downloaded, _replica, _error), end="\r")

                print("")
                print_success(f"All media are donwloaded in '{path}'.")
        else:
            print_error(result["error"])
            print_error("Account media could not be retrieved.")
        

if __name__ == "__main__":
    colorama.init(autoreset=True)
    console = RabbitgramConsole()

    # Show Account Information
    if console.args["info"]:
        console.user_information()

    # Save Media List
    if console.args["posts"]:
        console.post_list()

    # Save Media
    if console.args["media"]:
        console.user_media()
    