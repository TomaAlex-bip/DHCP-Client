import socket
import sys
import select
import threading


class NetworkInterface:

    def __init__(self, sport, dport, dip):

        self.__s_port = sport
        self.__d_port = dport
        self.__d_ip = dip

        # Creare socket UDP
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        self.__socket.bind(('0.0.0.0', int(self.__s_port)))

        self.__running = True

        # Creare thread pentru receptie de date
        self.__receive_thread = threading.Thread(target=self.__receive_fct())


    def start(self):
        try:
            self.__receive_thread.start()
        except:
            print("Eroare la pornirea thread‐ului")
            sys.exit()

        while True:
            try:
                data = input("Trimite: ")
                self.__socket.sendto(bytes(data, encoding="ascii"), (self.__d_ip, int(self.__d_port)))
            except KeyboardInterrupt:
                self.__running = False
                print("Waiting for the thread to close...")
                self.__receive_thread.join()
                break


    def __receive_fct(self):
        contor = 0
        while self.__running:
            # Apelam la functia sistem IO -select- pentru a verifca daca socket-ul are date in bufferul de receptie
            # Stabilim un timeout de 1 secunda
            r, _, _ = select.select([self.__socket], [], [], 1)
            if not r:
                contor = contor + 1
            else:
                data, address = self.__socket.recvfrom(1024)
                print("S-a receptionat ", str(data), " de la ", address)
                print("Contor= ", contor)




