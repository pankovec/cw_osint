from colorama import Fore, Back, Style
from rich.console import Console
from time import sleep
import itertools
import threading

class ProgressBar(threading.Thread):
    def __init__(self):
        super(ProgressBar, self).__init__()
        self.do_run = True

    def run(self):
        for char in itertools.cycle('|/-\\'):
            if not self.do_run:
                break
            print(Fore.LIGHTMAGENTA_EX + Back.WHITE + char + Style.RESET_ALL, end='\r')
            sleep(0.1)

class Menu:
    def __init__(self):
        self.console = Console()

    def print_main_menu(self):
        print('\n')
        print(Fore.MAGENTA + Back.WHITE + '[MAIN MENU]' + Style.RESET_ALL)
        print(Fore.CYAN + "1. Determine target and start scan")
        print(Fore.CYAN + "2. Manage/create report storage database")
        print(Fore.LIGHTRED_EX + "3. Exit" + Style.RESET_ALL + '\n')

    def print_db_menu(self):
        print(Fore.MAGENTA + Back.WHITE + '[DATABASE MENU]' + Style.RESET_ALL)
        print(Fore.CYAN + "1. Show database content")
        print(Fore.CYAN + "2. Recreate report from database")
        print(Fore.LIGHTRED_EX + "3. Return to main menu" + Style.RESET_ALL + '\n')
