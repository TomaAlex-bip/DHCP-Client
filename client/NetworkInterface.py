import socket
import sys
import select
import threading

from Message import *

serverPort = 67
clientPort = 68
clientAddress = '192.168.0.107'
broadcastAddress = '255.255.255.255'

running = False


class NetworkInterface:

    def __init__(self, mac_addr, old_ip_addr):

        self.__mac_addr = mac_addr
        self.__old_ip_addr = old_ip_addr

        # Creare socket UDP
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__socket.bind((clientAddress, clientPort))
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


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

        # creare mesaj DISCOVER
        discover_message = Message.discover(self.__mac_addr)

        # trimitere mesaj DISCOVER la pornire
        # cat timp nu s-a primit raspuns de la server se trimit mesaje DISCOVER
        r, _, _ = select.select([self.__socket], [], [], 1)
        received_message = False
        while not r and not received_message:
            received_message = True
            self.send_package(discover_message)
            print("S-a trimis mesajul DISCOVER:")

        data, address = self.__socket.recvfrom(1024)
        self.__receive_package(data)



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




    # TODO: contor lease time
    # contorizeaza fiecare secunda
    # ca sa se poata trimite un mesaj de reinnoire a adresei la lease time T1 si T2
    # din cate observ, se poate folosi si acel contor din functia de receive
    # astfel, nici nu ar mai trebui functia de send
    def __send_function(self):
        global running
        while True:
            try:
                pass
                # data = input("Trimite mesaj catre server: ")
                # self.__socket.sendto(str.encode(data), (broadcastAddress, serverPort))
            except KeyboardInterrupt:
                running = False
                self.__receive_thread.join()
                print("Closing thread...")
                break



    def send_package(self, package):
        self.__socket.sendto(package, (broadcastAddress, serverPort))



    def __receive_package(self, package):
        size = len(package)  # 240 de octeti pana la magic cookie(inclusiv)
        # print("\nSize: ", size)
        options_length = size - 240

        try:
            # print(package)
            message = struct.unpack(f'!ssss4s2s2s4s4s4s4s16s64s128s4s{options_length}s', package)
        except:
            print("\n Mesajul nu a putut fi decodificat!!!")
            return

        if len(message) > 0:
            self.__process_package(message, options_length)


    # TODO: vezi ca nu merge :)
    def __process_package(self, message, options_length):

        op = message[0].hex()
        htype = message[1].hex()
        hlen = message[2].hex()
        hops = message[3].hex()
        xid = message[4].hex()
        secs = message[5].hex()
        flags = message[6].hex()
        ciaddr = message[7].hex()
        yiaddr = message[8].hex()
        siaddr = message[9].hex()
        giaddr = message[10].hex()
        chaddr = message[11].hex()
        sname = message[12].hex()
        file = message[13].hex()
        magic_cookie = message[14]
        read_options = message[15]

        # print("\nMessage:")
        # print("op: " + message[0].hex())
        # print("htype: " + message[1].hex())
        # print("hlen: " + message[2].hex())
        # print("hops: " + message[3].hex())
        # print("xid: " + message[4].hex())
        # print("secs: " + message[5].hex())
        # print("flags: " + message[6].hex())
        # print("ciaddr: " + message[7].hex())
        # print("yiaddr: " + message[8].hex())
        # print("siaddr: " + message[9].hex())
        # print("giaddr: " + message[10].hex())
        # print("chaddr: " + message[11].hex())
        # print("sname: " + message[12].hex())
        # print("file: " + message[13].hex())
        # print("magic cookie: " + message[14].hex())
        # print("options: " + message[15].hex())

        # option1: 35 01 02
        # option2: 36 04 c0 a8 00 01
        # option3: 33 04 00 00 1c 20
        # option4: 01 04 ff ff ff 00
        # option5: 03 04 c0 a8 00 01
        # option6: 06 04 c0 a8 00 01
        # end option: ff
        # padding: 00 x multi

        # print("read_options = ")
        # split_strings = [read_options.hex()[index: index + 2] for index in range(0, len(read_options), 2)]
        # print(split_strings)

        processed_options = []
        options_index = 0
        while options_index < options_length and read_options[options_index] != 255:
            op_code = read_options[options_index]
            op_length = read_options[options_index + 1]

            op_value_index = 0
            op_value = []
            while op_value_index < op_length:
                op_value.append(read_options[options_index + 2 + op_value_index])
                op_value_index = op_value_index + 1

            options_index += op_length + 2

            temp_tuple = (op_code, op_length, op_value)
            processed_options.append(temp_tuple)

        print("\nS-a receptionat ", message, " \nde la server")
        options_index = 0
        while options_index < len(processed_options):
            print("   cu optiunea " + str(options_index) + ": ", processed_options[options_index])
            options_index = options_index + 1

        # decide what to do based on the received package

        # 1     DHCPDISCOVER    c
        # 2     DHCPOFFER       s
        # 3     DHCPREQUEST     c
        # 4     DHCPDECLINE     c
        # 5     DHCPACK         s
        # 6     DHCPNAK         s
        # 7     DHCPRELEASE     c
        # 8     DHCPINFORM      c


        # this verifies if the message is an OFFER MESSAGE from the server
        if processed_options[0][0] == 53 and processed_options[0][2][0] == 2:
            print("Serverul a raspuns cu un mesaj de OFFER")

            # sends an REQUEST MESSAGE to the server
            request_message = Message.request(self.__old_ip_addr, self.__mac_addr)
            self.send_package(request_message)

            # TODO: should unpack the message and get the configuration parameters


        if processed_options[0][0] == 53 and processed_options[0][2][0] == 5:
            print("Serverul a raspuns cu un mesaj de ACK")


        if processed_options[0][0] == 53 and processed_options[0][2][0] == 6:
            print("Serverul a raspuns cu un mesaj de NAK")





















