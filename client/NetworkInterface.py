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
        self.__current_ip_addr = old_ip_addr
        self.__received_ip_addr = old_ip_addr

        self.__subnet_mask = bytes([0x00, 0x00, 0x00, 0x00])
        self.__gateway = bytes([0x00, 0x00, 0x00, 0x00])
        self.__lease_time = 0
        self.__lease_t1 = 0
        self.__lease_t2 = 0
        self.__dns = bytes([0x00, 0x00, 0x00, 0x00])

        self.__contor_lease_time = 0


        self.__server_ip_addr = bytes([0x00, 0x00, 0x00, 0x00])

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

        # trimitere mesaj DISCOVER la pornire
        # cat timp nu s-a primit raspuns de la server se trimit mesaje DISCOVER
        r, _, _ = select.select([self.__socket], [], [], 1)
        received_message = False
        while not r and not received_message:
            received_message = True
            self.send_discover()


        data, address = self.__socket.recvfrom(1024)
        self.__receive_package(data)



    def __receive_function(self):
        while running:
            # Apelam la functia sistem IO -select- pentru a verifca daca socket-ul are date in bufferul de receptie
            # Stabilim un timeout de 1 secunda
            r, _, _ = select.select([self.__socket], [], [], 1)
            if not r:
                self.__contor_lease_time = self.__contor_lease_time + 1

                if self.__contor_lease_time >= self.__lease_t1:
                    pass
                    # trimitere mesaj de request pentru reiinoire

                if self.__contor_lease_time >= self.__lease_t2:
                    pass
                    # trimitere mesaj de request pentru reiinoire

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



    def send_discover(self):
        self.__socket.sendto(Message.discover(self.__mac_addr, self.__old_ip_addr), (broadcastAddress, serverPort))
        print("\nS-a trimis un mesaj DISCOVER cu adresa: ", self.__old_ip_addr.hex())


    def send_request(self):
        server_ip = str(int(self.__server_ip_addr[0])) + '.' + str(int(self.__server_ip_addr[1])) + '.' + \
                   str(int(self.__server_ip_addr[2])) + '.' + str(int(self.__server_ip_addr[3]))
        request_message = Message.request(self.__mac_addr, self.__server_ip_addr, self.__received_ip_addr)
        self.__socket.sendto(request_message, (server_ip, serverPort))
        print("\nS-a trimis un mesaj REQUEST catre " + server_ip + " cu adresa: " + self.__received_ip_addr.hex())


    def send_decline(self):
        server_ip = str(int(self.__server_ip_addr[0])) + '.' + str(int(self.__server_ip_addr[1])) + '.' + \
                    str(int(self.__server_ip_addr[2])) + '.' + str(int(self.__server_ip_addr[3]))
        decline_message = Message.decline(self.__mac_addr, self.__server_ip_addr)
        self.__socket.sendto(decline_message, (server_ip, serverPort))
        print("\nS-a trimis un mesaj DECLINE catre " + server_ip + " cu adresa: " + self.__received_ip_addr.hex())



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


    def __process_package(self, message, options_length):

        op = message[0].hex()
        htype = message[1].hex()
        hlen = message[2].hex()
        hops = message[3].hex()
        xid = message[4].hex()
        secs = message[5].hex()
        flags = message[6].hex()
        ciaddr = message[7].hex()
        yiaddr = message[8]
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

        print("\nS-a receptionat ", message, " \nde la server adresa: ", yiaddr.hex())
        options_index = 0
        while options_index < len(processed_options):
            print("   cu optiunea " + str(options_index) + ": ", processed_options[options_index])
            if processed_options[options_index][0] == 54:
                self.__server_ip_addr = bytes([processed_options[options_index][2][0],
                                               processed_options[options_index][2][1],
                                               processed_options[options_index][2][2],
                                               processed_options[options_index][2][3]])
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
            self.__received_ip_addr = bytes([yiaddr[0], yiaddr[1], yiaddr[2], yiaddr[3]])
            self.send_request()

        # this verifies if the message is an ACK MESSAGE from the server
        if processed_options[0][0] == 53 and processed_options[0][2][0] == 5:
            print("Serverul a raspuns cu un mesaj de ACK")
            options_index = 0
            while options_index < len(processed_options):
                # print("   cu optiunea " + str(options_index) + ": ", processed_options[options_index])

                if processed_options[options_index][0] == 51:
                    self.__lease_time = int("0x"+(bytes([processed_options[options_index][2][0],
                                                   processed_options[options_index][2][1],
                                                   processed_options[options_index][2][2],
                                                   processed_options[options_index][2][3]])).hex(), base=16)

                if processed_options[options_index][0] == 1:
                    self.__subnet_mask = bytes([processed_options[options_index][2][0],
                                               processed_options[options_index][2][1],
                                               processed_options[options_index][2][2],
                                               processed_options[options_index][2][3]])

                if processed_options[options_index][0] == 3:
                    self.__gateway = bytes([processed_options[options_index][2][0],
                                           processed_options[options_index][2][1],
                                           processed_options[options_index][2][2],
                                           processed_options[options_index][2][3]])

                if processed_options[options_index][0] == 6:
                    self.__dns = bytes([processed_options[options_index][2][0],
                                       processed_options[options_index][2][1],
                                       processed_options[options_index][2][2],
                                       processed_options[options_index][2][3]])


                options_index = options_index + 1

            print("\n IP address:" + self.__current_ip_addr.hex())
            print("\n subnet mask:" + self.__subnet_mask.hex())
            print("\n gateway address:" + self.__gateway.hex())
            print("\n dns address:" + self.__dns.hex())
            print("\n lease time:" + str(self.__lease_time))

            # self.send_decline()


        # this verifies if the message is an NAK MESSAGE from the server
        if processed_options[0][0] == 53 and processed_options[0][2][0] == 6:
            print("Serverul a raspuns cu un mesaj de NAK")























