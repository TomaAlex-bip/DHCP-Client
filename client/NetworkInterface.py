import queue
import socket
import sys
import select
import threading
from time import sleep

from Message import *

serverPort = 67
clientPort = 68

'''In cazul in care sunt instalate masini virtuale pe statie
trebuie dat disable la conexiuni (din Control Panel \ Network and Internet \ Network Connections)
pentru ca functia gethostbyname sa returneze ip-ul corect'''
# interfaceAddress = socket.gethostbyname(socket.gethostname())

interfaceAddress = '192.168.0.107'
# interfaceAddress = '192.168.0.126'

broadcastAddress = '255.255.255.255'


offer_wait_time = 20
ack_wait_time = 15

running = False


class NetworkInterface:

    def __init__(self, mac_addr, old_ip_addr):

        print(interfaceAddress)

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

        self.__options_list = [1, 3, 6, 51]  # default options

        self.__server_ip_addr = bytes([0x00, 0x00, 0x00, 0x00])

        self.__contor_lease_time = 0
        self.__offer_messages_queue = queue.Queue()

        self.__sent_renew_t1 = False
        self.__sent_renew_t2 = False

        self.__client_is_on = False

        # Creare socket UDP
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__socket.bind((interfaceAddress, clientPort))
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # creare de threaduri separate pentru trimitere si pentru primire de date
        self.__receive_thread = threading.Thread(target=self.__receive_function)
        self.__offer_wait_thread = threading.Thread(target=self.__offer_wait_function)
        self.__send_requests_thread = threading.Thread(target=self.__send_requests_function)

        # creare thread pentru reinnoire de adresa, se va porni abia dupa ce se primeste un mesaj de ACK
        self.__lease_time_renew_thread = threading.Thread(target=self.__lease_time_renew_function)

        print('UDP Client created')



    def start(self):
        global running

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__socket.bind((interfaceAddress, clientPort))
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # creare de threaduri separate pentru trimitere si pentru primire de date
        self.__receive_thread = threading.Thread(target=self.__receive_function)
        self.__offer_wait_thread = threading.Thread(target=self.__offer_wait_function)
        self.__send_requests_thread = threading.Thread(target=self.__send_requests_function)

        # creare thread pentru reinnoire de adresa, se va porni abia dupa ce se primeste un mesaj de ACK
        self.__lease_time_renew_thread = threading.Thread(target=self.__lease_time_renew_function)

        try:
            running = True
            # self.__receive_thread.start()
            self.__offer_wait_thread.start()  # pornire thread pentru primire de maseje OFFER
        except :
            print()
            print("Eroare la pornirea threadului", )
            sys.exit()

        # trimitere mesaj DISCOVER la pornire
        self.send_discover()


    def __receive_function(self):
        print("Receive messages thread started")
        self.__offer_wait_thread.join()
        while running:
            # Apelam la functia sistem IO -select- pentru a verifca daca socket-ul are date in bufferul de receptie
            # Stabilim un timeout de 1 secunda
            r, _, _ = select.select([self.__socket], [], [], 1)
            if not r:
                pass
            else:
                data, address = self.__socket.recvfrom(1024)
                message, options_length, options = Message.unpack_package(data)
                self.__process_package(message, options_length, options)


    def __lease_time_renew_function(self):
        print("Lease tine renew thread started")
        self.__contor_lease_time = 0
        while running:
            print("time passed: ", self.__contor_lease_time)
            sleep(1)
            self.__contor_lease_time = self.__contor_lease_time + 1
            if not self.__sent_renew_t1 and self.__contor_lease_time >= self.__lease_time * 50.0/100.0:  # T1
                # trimitere mesaj de request pentru reiinoire
                self.send_request()
                self.__sent_renew_t1 = True

            if not self.__sent_renew_t2 and self.__contor_lease_time >= self.__lease_time * 87.5/100.0:  # T2
                # trimitere mesaj de request pentru reiinoire
                self.send_request()
                self.__sent_renew_t2 = True

            if self.__contor_lease_time > self.__lease_time:
                # stop using the current_p_addres
                # TODO: fie oprim clientul, fie cumva dar complicat reincepem secventa de discover
                raise NotImplementedError


    def __offer_wait_function(self):
        print("Offer wait thread started")
        stop = False
        contor = 0
        while not stop:
            # print("asteptam mesaj: ", contor)
            r, _, _ = select.select([self.__socket], [], [], 1)
            if r:
                print("primit mesaj")
                data, address = self.__socket.recvfrom(1024)
                message, options_length, options = Message.unpack_package(data)
                if Message.package_type(options) == 'OFFER':
                    print("S-a pus in coada un mesaj de OFFER")
                    self.__offer_messages_queue.put((message, options_length, options))
            if contor >= offer_wait_time and stop is False:
                print("Oprire asteptare mesaje OFFER")
                if not self.__receive_thread.is_alive():
                    self.__receive_thread.start()
                if not self.__send_requests_thread.is_alive():
                    self.__send_requests_thread.start()
                stop = True
                sys.exit()


            contor = contor + 1


    def __send_requests_function(self):

        print("Send requests thread started")
        print("coada: ", self.__offer_messages_queue.qsize())
        while self.__offer_messages_queue.qsize() > 0:
            print("se proceseaza un mesaj din coada")
            message, options_length, options = self.__offer_messages_queue.get()
            self.__process_package(message, options_length, options)
            sleep(ack_wait_time)




    def send_discover(self):
        print("\nS-a trimis un mesaj DISCOVER cu adresa: ", self.__old_ip_addr.hex())
        self.__socket.sendto(Message.discover(self.__mac_addr, self.__old_ip_addr), (broadcastAddress, serverPort))

    def send_request(self):
        server_ip = str(int(self.__server_ip_addr[0])) + '.' + str(int(self.__server_ip_addr[1])) + '.' + \
                   str(int(self.__server_ip_addr[2])) + '.' + str(int(self.__server_ip_addr[3]))
        options_list = [1, 3, 6, 51, 58, 59]  # TODO: get the options from inteface
        request_message = Message.request(self.__mac_addr, self.__server_ip_addr, self.__received_ip_addr, options_list)
        self.__socket.sendto(request_message, (server_ip, serverPort))
        print("\nS-a trimis un mesaj REQUEST catre " + server_ip + " cu adresa: " + self.__received_ip_addr.hex())
        print(options_list)

    def send_decline(self, server_ip_addr):
        server_ip = str(int(server_ip_addr[0])) + '.' + str(int(server_ip_addr[1])) + '.' + \
                    str(int(server_ip_addr[2])) + '.' + str(int(server_ip_addr[3]))
        decline_message = Message.decline(self.__mac_addr, server_ip_addr)
        self.__socket.sendto(decline_message, (server_ip, serverPort))
        print("\nS-a trimis un mesaj DECLINE catre " + server_ip)

    def send_release(self):
        server_ip = str(int(self.__server_ip_addr[0])) + '.' + str(int(self.__server_ip_addr[1])) + '.' + \
                    str(int(self.__server_ip_addr[2])) + '.' + str(int(self.__server_ip_addr[3]))
        release_message = Message.release(self.__mac_addr, self.__server_ip_addr)
        self.__socket.sendto(release_message, (server_ip, serverPort))
        print("\nS-a trimis un mesaj RELEASE catre " + server_ip + " cu adresa: " + self.__received_ip_addr.hex())

    def send_inform(self):
        server_ip = str(int(self.__server_ip_addr[0])) + '.' + str(int(self.__server_ip_addr[1])) + '.' + \
                    str(int(self.__server_ip_addr[2])) + '.' + str(int(self.__server_ip_addr[3]))
        options_list = [51, 58, 59]  # TODO: get the options from inteface
        inform_message = Message.inform(self.__mac_addr, self.__server_ip_addr, options_list)
        self.__socket.sendto(inform_message, (server_ip, serverPort))
        print("\nS-a trimis un mesaj INFORM catre " + server_ip + " cu adresa: " + self.__received_ip_addr.hex())

    def send_options(self):
        server_ip = str(int(self.__server_ip_addr[0])) + '.' + str(int(self.__server_ip_addr[1])) + '.' + \
                    str(int(self.__server_ip_addr[2])) + '.' + str(int(self.__server_ip_addr[3]))
        options_list = [1, 3, 6, 51, 58, 59]  # TODO: get the options from inteface
        options_message = Message.get_options(self.__mac_addr, self.__server_ip_addr, options_list)
        self.__socket.sendto(options_message, (server_ip, serverPort))
        print("\nS-a trimis un mesaj OPTIONS catre " + server_ip + " cu adresa: " + self.__received_ip_addr.hex())


    # def __receive_package(self, package):
        # size = len(package)  # 240 de octeti pana la magic cookie(inclusiv)
        # # print("\nSize: ", size)
        # options_length = size - 240
        #
        # try:
        #     # print(package)
        #     message = struct.unpack(f'!ssss4s2s2s4s4s4s4s16s64s128s4s{options_length}s', package)
        # except:
        #     print("\n Mesajul nu a putut fi decodificat!!!")
        #     return
        #
        # if len(message) > 0:
        #     if self.__verify_if_offer(message, options_length):
        #         self.__offer_servers_queue.put((message, options_length))
        #     else:
        #         self.__process_package(message, options_length)


    def __process_package(self, message, options_length, processed_options):

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


        print("\nS-a receptionat ", message, " \nde la server adresa: ", yiaddr.hex())
        options_index = 0
        while options_index < len(processed_options):
            print("   cu optiunea " + str(options_index) + ": ", processed_options[options_index])
            if processed_options[options_index][0] == 54:
                received_server_ip_addr = bytes([processed_options[options_index][2][0],
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
        if Message.package_type(processed_options) == 'OFFER':
            print("Serverul a raspuns cu un mesaj de OFFER")

            # sends an REQUEST MESSAGE to the server
            self.__received_ip_addr = bytes([yiaddr[0], yiaddr[1], yiaddr[2], yiaddr[3]])
            self.__server_ip_addr = received_server_ip_addr
            self.send_request()

            # send DECLINE messages to the other servers
            while self.__offer_messages_queue.qsize() > 0:
                decline_message, decline_options_length, decline_options = self.__offer_messages_queue.get()

                options_index = 0
                while options_index < len(decline_options):
                    if decline_options[options_index][0] == 54:
                        decline_server_address = bytes([decline_options[options_index][2][0],
                                                        decline_options[options_index][2][1],
                                                        decline_options[options_index][2][2],
                                                        decline_options[options_index][2][3]])
                    options_index = options_index + 1

                self.send_decline(decline_server_address)


            # stops the thread that replies to OFFER messages
            # self.__send_requests_thread.join()
            sys.exit()



        # this verifies if the message is an ACK MESSAGE from the server
        if Message.package_type(processed_options) == 'ACK':
            print("Serverul a raspuns cu un mesaj de ACK")

            if not self.__lease_time_renew_thread.is_alive():
                self.__lease_time_renew_thread.start()

            if self.__sent_renew_t1:
                self.__contor_lease_time = 0
                self.__sent_renew_t1 = False
                self.reset_client()

            if self.__sent_renew_t2:
                self.__contor_lease_time = 0
                self.__sent_renew_t2 = False

            options_index = 0
            while options_index < len(processed_options):
                # print("   cu optiunea " + str(options_index) + ": ", processed_options[options_index])
                if processed_options[options_index][0] == 51:
                    self.__lease_time = int("0x" + (bytes([processed_options[options_index][2][0],
                                                           processed_options[options_index][2][1],
                                                           processed_options[options_index][2][2],
                                                           processed_options[options_index][2][3]])).hex(), base=16)
                    self.__lease_time = 30

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


            print("\nIP address:" + self.__current_ip_addr.hex())
            print("subnet mask:" + self.__subnet_mask.hex())
            print("gateway address:" + self.__gateway.hex())
            print("dns address:" + self.__dns.hex())
            print("lease time:" + str(self.__lease_time))

            # self.send_decline()
            # self.send_release()
            # self.send_inform()
            # self.send_options()


        # this verifies if the message is an NAK MESSAGE from the server
        if Message.package_type(processed_options) == 'NAK':
            print("Serverul a raspuns cu un mesaj de NAK")


    def reset_client(self):
        global running
        print("Performig RESET")

        self.send_release()
        self.__socket.close()

        running = False

        if self.__lease_time_renew_thread.is_alive():
            print("STOP lease time renew thread")
            self.__lease_time_renew_thread.join()

        if self.__send_requests_thread.is_alive():
            self.__send_requests_thread.join()
            print("STOP send requests thread")

        if self.__offer_wait_thread.is_alive():
            self.__offer_wait_thread.join()
            print("STOP offer wait thread")

        if self.__receive_thread.is_alive():
            # self.__receive_thread.join()
            print("STOP receive thread (current) thread")
            self.start()
            print("Start the client again")
            sys.exit()


    def get_ip(self):
        return self.__current_ip_addr

    def get_sm(self):
        return self.__subnet_mask

    def get_gw(self):
        return self.__gateway

    def get_dns(self):
        return self.__dns

    def get_lease(self):
        return self.__lease_time

    def get_mac(self):
        return self.__mac_addr

    def get_old_ip(self):
        return self.__old_ip_addr

    def update_options_list(self, options_list):
        self.__options_list = options_list


















