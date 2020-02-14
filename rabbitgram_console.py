from rabbitgram.rabbitgram  import Rabbitgram
from rabbitgram.logger      import Logger
import json

USERNAME                = ""
PASSWORD                = ""

if __name__ == "__main__":
    r = Rabbitgram()
    r.login(USERNAME, PASSWORD)