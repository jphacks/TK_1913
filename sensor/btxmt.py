from time import sleep
import bluetooth

class BTClient:
    def __init__(self, addr, port):
        """Initial setting.

        Args:
            addr (str): Server mac address
            port (int): Server port number
        """
        self.__addr = addr
        self.__port = port
        self.__sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)


    def connect(self):
        """Connect server.
        """
        while True:
            try:
                self.__sock.connect((self.__addr, self.__port))
                sleep(1)
                break
            except bluetooth.btcommon.BluetoothError:
                self.__sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                sleep(1)
            except Exception as e:
                print(e)
                break


    def disconnect(self):
        """Disconnect.
        """
        self.__sock.close()


    def send(self, msg):
        """Send `msg` to server.

        Args:
            msg (str): Message sent to server
        """
        self.__sock.send(msg)


class BTServer:
    def __init__(self, port):
        """Initial setting.

        Args:
            port (int): Server (listen) port number
        """
        self.__server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.__server_sock.bind(('', port))
        self.__server_sock.listen(1)


    def accept(self):
        """Listening for connection.

        Returns:
            str: Client mac address
        """
        client_sock, client_addr = self.__server_sock.accept()
        self.__client_sock = client_sock
        return client_addr


    def disconnect(self):
        """Disconnect.
        """
        self.__client_sock.close()
        self.__server_sock.close()


    def recv(self, recv_size):
        """Send `msg` to server.

        Returns:
            bytes: Message recieved from client
        """
        return self.__client_sock.recv(recv_size)
