from colorama import Fore, Style

class color:
    def __init__(self, text):
        self.text = text

    def red(self):
        return f"{Fore.RED}{self.text}{Style.RESET_ALL}"

    def green(self):
        return f"{Fore.GREEN}{self.text}{Style.RESET_ALL}"

    def yellow(self):
        return f"{Fore.YELLOW}{self.text}{Style.RESET_ALL}"

    def blue(self):
        return f"{Fore.BLUE}{self.text}{Style.RESET_ALL}"

    def magenta(self):
        return f"{Fore.MAGENTA}{self.text}{Style.RESET_ALL}"

    def cyan(self):
        return f"{Fore.CYAN}{self.text}{Style.RESET_ALL}"

    def white(self):
        return f"{Fore.WHITE}{self.text}{Style.RESET_ALL}"

    def black(self):
        return f"{Fore.BLACK}{self.text}{Style.RESET_ALL}"

    def light_black(self):
        return f"{Fore.LIGHTBLACK_EX}{self.text}{Style.RESET_ALL}"

    def light_red(self):
        return f"{Fore.LIGHTRED_EX}{self.text}{Style.RESET_ALL}"

    def light_green(self):
        return f"{Fore.LIGHTGREEN_EX}{self.text}{Style.RESET_ALL}"

    def light_yellow(self):
        return f"{Fore.LIGHTYELLOW_EX}{self.text}{Style.RESET_ALL}"

    def light_blue(self):
        return f"{Fore.LIGHTBLUE_EX}{self.text}{Style.RESET_ALL}"

    def light_magenta(self):
        return f"{Fore.LIGHTMAGENTA_EX}{self.text}{Style.RESET_ALL}"

    def light_cyan(self):
        return f"{Fore.LIGHTCYAN_EX}{self.text}{Style.RESET_ALL}"

    def light_white(self):
        return f"{Fore.LIGHTWHITE_EX}{self.text}{Style.RESET_ALL}"