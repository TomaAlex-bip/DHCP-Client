

import tkinter as tk
import Interface
from NetworkInterface import *



if __name__ == '__main__':
    print("Gigel")


    mac_addr_client = bytes([0x00, 0x0b, 0x82, 0x01, 0xfc, 0x42])
    old_ip_addr_client = bytes([0xc0, 0xa8, 0x00, 0x71])
    network_interface = NetworkInterface(mac_addr_client, old_ip_addr_client)
    # network_interface.start()


    gui = Interface.Interface(800, 600, network_interface)
    # passed the networkInterface to the GUI interface constructor,
    # after that, for getting or setting the variables use getters and setters

    gui.run_interface()


# ponturi
#
# trebuie sa folosim codificari la nivel de pachet
# cand le compunem trebuie sa avem grija la network order
# stivele de comm folosesc big endian
# pentru partea de impachetare ar fi bine sa folosim modulul struct (pack si unpack)
# functia pack functioneaza astfel:
# primeste ca prim parametru un specificator de format, apoi sirul de octeti










