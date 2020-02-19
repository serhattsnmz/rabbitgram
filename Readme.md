# 🐇RABBITGRAM

Rabbitgram is Instagram scrapper which you can get accounts informations and download accounts' photos/videos.

### Requirements

1. [Python 3.4+](https://www.python.org/downloads/)
2. [Pip](https://pip.pypa.io/en/stable/)

### Installation

1. Clone this repo,
2. Install required libraries with pip,
3. Start `rabbitgram_console.py` with python. 

```bash
$ git clone https://github.com/serhattsnmz/rabbitgram.git
$ cd rabbitgram/
$ python -m pip install -r requirements.txt
$ python rabbitgram_console.py
```

### Usage

```
usage: rabbitgram_console.py [-h] [-u] [-p] [-a] [-P] [-o] [-s] [--info]
                             [--video]

Rabbitgram : The Fastest Instagram Scrapper

optional arguments:
  -h, --help        show this help message and exit
  -u , --username   User username
  -p , --password   User password
  -a , --account    Account username for scrapping
  -P , --path       The directory path for saving media
  -o , --output     The file path for saving result
  -s , --settings   The settings file path
  --info            Show account info
  --video           Download user video. Default : False
```

### Save The Result In A File

If you use `--output` parameter, rabbitgram will create a file and save the result in it.  
Following results can be taken as a file;

1. User informations, if rabbitgram is used with `--info`
2. User media lists, if rabbitgram is used with `--list`

Example usage;

```
$ python rabbitgram_console.py -u user -p pass -a acc -o ./output.txt --info
>>> Save user information as output.txt

$ python rabbitgram_console.py -u user -p pass -a acc -o ./output.txt --list
>>> Save user media list as output.txt
```

### Create Settings File

If you prefer rabbitgram to get your information from file instead of parameters, you can create a settings file as yaml format.  
Example yaml file must be like that :

```
username : user_username
password : user_s3cr3t_p4ss
account  : the_account_name_wish_to_get_info
```

Remember that, none of the keys above is **not required**. You can define any of them and can give the others as parameter. Beside that, if you give a parameter which is already defined in settings file, **rabbitgram will take the parameter instead of defination in the settings file**. 

After creating settings file, you can use it like that;

```
$ python rabbitgram_console.py -s ./user_settings.yml
$ python rabbitgram_console.py -s ./user_settings.yml -u new_username
$ python rabbitgram_console.py -s ./user_settings.yml -p new password
$ python rabbitgram_console.py -s ./user_settings.yml -u new_username -p new password
$ python rabbitgram_console.py -s ./user_settings.yml -a new_account
etc...
```
