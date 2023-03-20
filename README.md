## Simple network scanner and port 22 brute force script in python

Both scripts perform a port scan on a user-specified IP address and identifi open ports. 
If port 22 is open, it prompts the user to perform a brute force attack to gain unauthorized access to the SSH server.


# Script_1

How does it work.

1.  Imports the necessary libraries - scapy, paramiko.
2.  Defines the target IP address, port range, and an empty list to store open ports.
3.  Defines functions for scanning a single port, checking the reachability of the target IP address, and performing a brute force attack using a password list.
4.  Calls the main function, which scans for open ports on the specified IP address.
5.  If port 22 is open, it prompts the user to perform a brute force attack. If the user agrees, the script performs a brute force attack using a list of passwords from a file named "PasswordList.txt".


## Script_2

1. Libraries - argparse, socket, paramiko

The program starts by parsing the command line arguments and constructing a list of ports to scan. It then scans each port using the `scan_port` function and builds a list of open ports. If port 22 (the SSH port) is open, it reads the list of passwords from the specified file and attempts to brute-force the SSH login using the `ssh_brute_force` function.

The `scan_port` function uses the Python `socket` module to create a TCP socket and attempts to connect to the specified port on the target host. If the connection is successful, it returns `True`, indicating that the port is open. Otherwise, it returns `False`.

The `ssh_brute_force` function uses the Paramiko library to attempt to connect to the SSH service on the target host using the specified username and a list of passwords. It loops through the password list and tries each one until it finds one that works, at which point it prints a message indicating that the login was successful and returns `True`. If none of the passwords work, it returns `False`.


## Note

Script appears to be a security vulnerability scanner, and the brute force attack is potentially harmful and illegal if used without permission. Therefore, it is important to use such scripts ethically and legally.
