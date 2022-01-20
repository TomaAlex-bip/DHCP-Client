import Interface
from NetworkInterface import *

if __name__ == '__main__':
    print("Gigel")

    mac_addr_client = bytes([0x00, 0x0b, 0x82, 0x01, 0xfc, 0x42])
    old_ip_addr_client = bytes([0x00, 0x00, 0x00, 0x00])
    network_interface = NetworkInterface(mac_addr_client, old_ip_addr_client)
    # network_interface.start()

    gui = Interface.Interface(800, 600, network_interface)
    # passed the networkInterface to the GUI interface constructor,
    # after that, for getting or setting the variables use getters and setters

    gui.run_interface()

