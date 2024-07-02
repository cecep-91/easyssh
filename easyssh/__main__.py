import easyssh
# Below is modules I needed when I want to build package using pyinstaller
import json
import os
import sys
import paramiko
import subprocess
from getpass import getpass
from tools.cert import cert
from tools.color import color
from tabulate import tabulate
from colorama import Fore, Style

if __name__ == "__main__":
    try:
        easyssh.main()
    except KeyboardInterrupt:
        quit()
