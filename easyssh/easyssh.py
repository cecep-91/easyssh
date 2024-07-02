import json
import os
import sys
import time
import subprocess
from getpass import getpass
from tools.cert import cert
from tools.color import color
from tabulate import tabulate

metadata_file = os.path.expanduser('~/.easyssh/hosts.json')
private_key_path = os.path.expanduser('~/.easyssh/.rsa_key_temp')

def isYesNo(msg):
    while True:
        is_yes_no = input(msg + color(" (y/n) ").green())
        if len(is_yes_no) == 1:
            if is_yes_no in 'Yy':
                return True
                break
            elif is_yes_no in 'Nn':
                return False
                break
            else:
                continue
        else:
            continue

def getHostByNumber(msg):
    metadata = readMetadataFile()
    while True:
        hostnum = input(msg + color(f" (1-{len(metadata)})").green() + ": ")
        if hostnum.isdigit() and 0 < int(hostnum) <= len(metadata):
            host = list(metadata.keys())[int(hostnum) - 1]
            return host
            break

def checkMetadataFileExsistance():
    metadata_dir=os.path.dirname(metadata_file)
    if not os.path.exists(metadata_dir):
        os.mkdir(metadata_dir)
 
    if not os.path.exists(metadata_file):
        with open(metadata_file, 'a'):
            os.utime(metadata_file, None)

def readMetadataFile():
    with open(metadata_file, 'r') as f:
        try:
            return json.load(f)
        except:
            return {}

def getHostCredentials(host):
    metadata = readMetadataFile()
    if host in metadata:
        return metadata[host]
    else:
        return None

def printHostCredentials():
    host = getHostByNumber("Enter the host's number you want to get credentials for")
    credentials = getHostCredentials(host)
    if credentials:
        print(f"\n{color(host).light_blue()}:")
        print(f"  - user: {color(credentials['user']).light_blue()}")
        print(f"  - pass: {color(credentials['pass']).light_blue()}")

def listMetadata():
    metadata = readMetadataFile()
    if metadata:
        metadata_table = [[i + 1, host, credentials['user']] for i, (host, credentials) in enumerate(metadata.items())]
        table_headers = ["No", "Host", "User"]
        print(tabulate(metadata_table, table_headers, tablefmt="rounded_outline"))

def tryConnectToHost(host, user, password):
    certificate = cert(private_key_path)
    certificate.create()

    options = "-o IdentitiesOnly=yes -o PreferredAuthentications=password -o PubkeyAuthentication=no -o PasswordAuthentication=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
    cmd = f"sshpass -p {password} ssh {user}@{host} -i '{private_key_path}' {options} 'whoami'"

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    stdout, stderr = process.communicate()

    certificate.delete()
    if (len(stdout) - 1 == len(user)) and (user in stdout): 
        return True
    else:
        return False

def connectToHost(host):
    data = getHostCredentials(host)
    user = data['user']
    password = data['pass']
    os.system(f"sshpass -p '{password}' ssh {user}@{host} -o StrictHostKeyChecking=no 2> /dev/null")

def dirrectConnect():
    metadata = readMetadataFile()
    ssh_connect = sys.argv[1]
    if '@' in ssh_connect:
        user, host = ssh_connect.split('@')
        if host in metadata:
            if user == metadata[host]['user']:
                connectToHost(host)
            else:
                print(f"No user '{color(user).light_blue()}' for {color(host).light_blue()}, but user '{color(metadata[host]['user']).light_blue()}' is found.")
                if isYesNo(f"Want to connect to {color(host).light_blue()} as user '{color(metadata[host]['user']).light_blue()}'?"):
                    connectToHost(host)
        else:
            print(f'Host {color(host).light_blue()} not found.')
            if isYesNo(f"Want to add credentials for host {color(host).light_blue()} with user '{color(user).light_blue()}'?"):
                addHostEntry(host,user)
    else:
        host = ssh_connect
        if host in metadata:
            connectToHost(host)
        else:
            print(f'Host {color(host).light_blue()} not found.')
            if isYesNo(f"Want to add credentials for host {color(host).light_blue()}?"):
                addHostEntry(host)

def writeMetadata(metadata):
    try:
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=4)
        return True
    except:
        return False

def writeEntryToMetadata(host, user, password):
    metadata = readMetadataFile()
    metadata[host] = {"user": user, "pass": password}
    try:
        writeMetadata(metadata)
        return True
    except:
        return False
    
def addHostEntry(host=None,user=None):
    password = None
    print("\nDefine host you want to add and its credentials:")
    while True:
        if host == None:
            while True:
                host = input("Enter host: ")
                data = getHostCredentials(host)
                if data:
                    print(f"{color(host).light_blue()} found in metadata with user {color(data['user']).light_blue()}")
                    if isYesNo("Continue to add? The host's credentials will be overridden."):
                        break
                    else:
                        print(f"Skipping {color(host).light_blue()}. Enter another host.")
                        continue
                else:
                    if host: break
        else:
            pass
        while not user:
            user = input(f"Enter {color(host).light_blue()}'s user: ")
        while not password:
            password = getpass(f"Enter {color(host).light_blue()} {color(user).light_blue()}'s password: ")

        print("\nVerifying. Trying to connect to the host...", end = " ")

        if tryConnectToHost(host, user, password):
            print(color("Success.").green())
            print(f"Adding {color(host).light_blue()} to the metadata...", end = " ")

            if writeEntryToMetadata(host, user, password):
                print(color("Success.").green())
            else:
                print(color("Failed.").red())
                quit()

            if isYesNo(f"Immediately connect to {color(host).light_blue()}?"):
                connectToHost(host)
                break
            else:
                break
        
        else:
            print(color("Failed.").red())
            print(f"Cannot connect to {color(host).light_blue()}. Make sure you enter the correct credentials.")
            user, password = None, None
            continue

def removeHostFromMetadata(host):
    metadata = readMetadataFile()
    try:
        del metadata[host]
        writeMetadata(metadata)
        return True
    except:
        return False

def removeHost():
    host = getHostByNumber("Enter the host's number you want to remove")
    print(f"Are you sure to remove this host? Enter '{color(host).green()}' to verify or " + color("(n)").green() + " to cancel.")
    while True:
        verify = input(": ")
        if verify == host:
            print(f"Removing host {color(host).light_blue()}... ", end="")
            if removeHostFromMetadata(host):
                print(color("Success.").green())
            else:
                print(color("Failed.").red())
            break
        elif not len(verify) >= 1:
            continue
        elif verify in 'Nn':
            quit()

def menu():
    listMetadata()
    metadata = readMetadataFile()
    print(color(f"\n(1-{len(metadata)})").green(), "Connect to host,", color("(a)").green(), "Add host,", color("(g)").green(), "Get host's credentials,", color("(r)").green(), "Remove host,", color("(q)").green(), "Quit")
    if metadata:
        while True:
            user_option = input(color(f"(1-{len(metadata)})").green() + " or " + color("(a/g/r/q)").green() + ": ")
            if user_option.isdigit() and 0 < int(user_option) <= len(metadata):
                break
            elif len(user_option) >= 1 and user_option in 'AaGgRrQq':
                break
        if user_option in 'Aa':
            addHostEntry()
        elif user_option in 'Gg':
            printHostCredentials()
        elif user_option in 'Rr':
            removeHost()
        elif user_option in 'Qq':
            quit()
        else:
            host = list(metadata.keys())[int(user_option) - 1]
            connectToHost(host)
    else:
        if isYesNo("\nNo host found. Want to add your first host?"):
            addHostEntry()

def main():
    checkMetadataFileExsistance()
    if len(sys.argv) > 1:
        dirrectConnect()
    else:
        menu()
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        quit()