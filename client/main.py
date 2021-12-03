

import tkinter as tk
import Interface
from NetworkInterface import *



if __name__ == '__main__':
    print("Gigel")

    gui = Interface.Interface(800, 600)

    # gui.run_interface()

    client = NetworkInterface()
    client.start()


# ponturi
#
# trebuie sa folosim codificari la nivel de pachet
# cand le compunem trebuie sa avem grija la network order
# stivele de comm folosesc big endian
# pentru partea de impachetare ar fi bine sa folosim modulul struct (pack si unpack)
# functia pack functioneaza astfel:
# primeste ca prim parametru un specificator de format, apoi sirul de octeti










