
import paramiko
import socket
from getpass import getpass

class Raspberry_pi_manager(object):
    def __init__(self,ip,password):
        self.ip = ip
        self.password = password
        # self.client = paramiko.SSHClient()
        # self.client.load_system_host_keys()
        # self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_client(self):
        # self.client.connect(self.ip,"22","pi",self.password)
        self.client.connect((self.ip,12345))
        print("CLIENT: connected")
        msg = "test"
        self.client.send(msg.encode())
        from_server = self.client.recv(4096).decode()
        # print("Recieved: "+ from_server)

    def send_command(self,command):
        self.client.send(command.encode())
        from_server = self.client.recv(4096).decode()
        # print("Recieved: "+ from_server)
        return from_server

    def run_file(self):
        try:
            self.client.connect(self.ip,"22","pi",self.password)
            # dir = "/var/www/dmx"
            # command = "sudo python raspberry_pi_connection_test2.py"
            stdin, stdout, stderr = self.client.exec_command('sudo  fuser -k 12345/tcp')
            # stdin, stdout, stderr = self.client.exec_command(f'cd {dir}; {command}',get_pty=True)
            stdout.channel.set_combine_stderr(True)
            self.test = stdout
        except paramiko.ssh_exception.AuthenticationException:
            raise Exception("Incorrect password. Please try again")
        except TimeoutError:
            raise Exception("Could not connect. Please try again later")
        except paramiko.ssh_exception.NoValidConnectionsError: #this happend when the address is of something else so you cannot ssh into it
            raise Exception("The ipv4 is incorrect. Please try again.")

    def send_stop(self):
        self.client.send("stop".encode())
        from_server = self.client.recv(4096).decode()
        # print("Recieved: "+ from_server)

    def __del__(self):
        try:
            self.client.send("stop".encode())
        except Exception as e:
            print(e)
        # try:
        #     self.client.exec_command(chr(3))
        # except Exception as e:
        #     print(e)
        try:
            self.client.close()
            self.client.shutdown(1)
            self.client.close()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    from getpass import getpass
    password = "getpass()"
    m = Raspberry_pi_manager("192.168.0.79", password)
    m.connect_client()
    while True:
        command = input("Enter command:")
        m.send_command(command)