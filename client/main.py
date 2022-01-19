

import tkinter as tk
import Interface
from NetworkInterface import *



if __name__ == '__main__':
    print("Gigel")

    gui = Interface.Interface(800, 600)

    gui.run_interface()  # thread separat

    mac_addr_client = bytes([0x00, 0x0b, 0x82, 0x01, 0xfc, 0x42])
    old_ip_addr_client = bytes([0xc0, 0xa8, 0x00, 0x71])
    #client = NetworkInterface(mac_addr_client, old_ip_addr_client)
    #client.start()


# ponturi
#
# trebuie sa folosim codificari la nivel de pachet
# cand le compunem trebuie sa avem grija la network order
# stivele de comm folosesc big endian
# pentru partea de impachetare ar fi bine sa folosim modulul struct (pack si unpack)
# functia pack functioneaza astfel:
# primeste ca prim parametru un specificator de format, apoi sirul de octeti










