import socket
import sys
import select
import threading

from Message import *


serverPort = 67
clientPort = 68
localIP = "127.0.0.1"

running = False


class NetworkInterface:

    def __init__(self):
        # Creare socket UDP
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        self.__socket.bind(('0.0.0.0', clientPort))

        # creare de threaduri separate pentru trimitere si pentru primire de date
        self.__receive_thread = threading.Thread(target=self.__receive_function)
        self.__send_thread = threading.Thread(target=self.__send_function)

        print('UDP Client created')


    def start(self):
        global running
        try:
            running = True
            self.__receive_thread.start()
            self.__send_thread.start()
        except:
            print()
            print("Eroare la pornirea threadului")
            sys.exit()

        # trimitere mesaj de discover

        mac_addr = bytes([0x69, 0x69, 0x69, 0x69, 0x69, 0x69])
        old_addr = bytes([192, 168, 45, 6])

        discover_message = Message.discover(mac_addr)

        request_message = Message.request(old_addr, mac_addr)


        # self.send_package(test_message)
        self.send_package(discover_message)
        self.send_package(request_message)


    def __receive_function(self):
        contor = 0
        while running:
            # Apelam la functia sistem IO -select- pentru a verifca daca socket-ul are date in bufferul de receptie
            # Stabilim un timeout de 1 secunda
            r, _, _ = select.select([self.__socket], [], [], 1)
            if not r:
                contor = contor + 1
            else:
                data, address = self.__socket.recvfrom(1024)
                self.__receive_package(data)
                # print("contor = ", contor, "\nTrimite mesaj catre server: ")



    def __send_function(self):
        global running
        while True:
            try:
                data = input("Trimite mesaj catre server: ")
                self.__socket.sendto(str.encode(data), (localIP, serverPort))
            except KeyboardInterrupt:
                running = False
                self.__receive_thread.join()
                print("Closing thread...")
                break


    def send_package(self, package):
        self.__socket.sendto(package, (localIP, serverPort))


    def __receive_package(self, package):

        size = sys.getsizeof(package)  # 81 pana la magic inclusiv
        # print("\nSize: ", size)
        options_length = size - 81

        try:
            message = struct.unpack(f'!bbbblh2s4s4s4s4s16s4s{options_length}s', package)
        except:
            return

        self.__process_package(message)


    def __process_package(self, message):
        read_options = message[len(message) - 1]
        processed_options = []

        options_index = 0
        while options_index < options_length:
            opcode = read_options[options_index]
            length = read_options[options_index + 1]

            aux = 0
            value = []
            while aux < length:
                value.append(read_options[options_index + 2 + aux])
                aux = aux + 1

            options_index += length + 2

            tuple_temp = (opcode, length, value)
            processed_options.append(tuple_temp)

        print("\nS-a receptionat ", message, " de la server")
        i = 0
        while i < len(processed_options):
            print("\n cu optiunea: ", processed_options[i])
            i = i + 1


