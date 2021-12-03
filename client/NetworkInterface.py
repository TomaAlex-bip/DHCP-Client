import socket
import sys
import select
import threading


serverPort = 20001
clientPort = 8888
serverAddress = "127.0.0.1"

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
            print("Eroare la pornirea threadului")
            sys.exit()


    def __receive_function(self):
        contor = 0
        while running:
            # Apelam la functia sistem IO -select- pentru a verifca daca socket-ul are date in bufferul de receptie
            # Stabilim un timeout de 1 secunda
            r, _, _ = select.select([self.__socket], [], [], 1)
            if not r:
                contor = contor + 1
                # print(contor)
            else:
                data, address = self.__socket.recvfrom(1024)
                print("\nS-a receptionat ", str(data), " de la serverul ", address)
                print("contor = ", contor, "\nTrimite mesaj catre server: ")


    def __send_function(self):
        global running
        while True:
            try:
                data = input("Trimite mesaj catre server: ")
                self.__socket.sendto(str.encode(data), (serverAddress, serverPort))
            except KeyboardInterrupt:
                running = False
                self.__receive_thread.join()
                print("Closing thread...")
                break

