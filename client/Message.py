import random
import struct


def generatexid():
    return random.randbytes(4)
    # xid_0 = randint(0, 0xFF)
    # xid_1 = randint(0, 0xFF)
    # xid_2 = randint(0, 0xFF)
    # xid_3 = randint(0, 0xFF)
    # return bytes([xid_0, xid_1, xid_2, xid_3])


# TODO: codificare mesaje
# codifica fiecare mesaj cum trebuie
# captura de date cu wireshark si se vede cum arata un pachet

class Message:

    # pentru a trimute alte optiuni se face cu opt 52 si dupa in value se trec mai multe optiuni cerute


    @staticmethod
    def discover(client_mac):
        op = bytes([0x01])
        htype = bytes([0x01])
        hlen = bytes([0x06])
        hops = bytes([0x00])
        xid = generatexid()  # Transaction ID for this message exchange.
        # A DHCP client generates a random number, which the client and server use to identify their message exchange.
        secs = bytes([0x00, 0x00])
        flags = bytes([0x80, 0x00])
        ciaddr = bytes([0x00, 0x00, 0x00, 0x00])
        yiaddr = bytes([0x00, 0x00, 0x00, 0x00])
        siaddr = bytes([0x00, 0x00, 0x00, 0x00])
        giaddr = bytes([0x00, 0x00, 0x00, 0x00])
        chaddr = bytes([client_mac[0], client_mac[1], client_mac[2], client_mac[3],
                        client_mac[4], client_mac[5], 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00])
        sname = bytes([0x00]*64)
        file = bytes([0x00]*128)

        magic_cookie = bytes([0x63, 0x82, 0x53, 0x63])

        # optiunea care precizeaza ca acesta este un mesaj de tip DISCOVER
        message_option = bytes([53, 1, 1])

        client_identifier_option = bytes([61, 7, 0x01, client_mac[0], client_mac[1],
                                          client_mac[2], client_mac[3], client_mac[4], client_mac[5]])

        requested_ip_address_option = bytes([50, 4, 0x00, 0x00, 0x00, 0x00])  # TODO: fill with ce trebuie


        # optiunea care precizeaza ce optiuni se cer de la server(addr IP, Gateway, Mask, DNS, lease time)
        # 3 -> gateway
        # 1 -> mask
        # 6 -> DNS
        # 51 -> lease time
        request_option = bytes([52, 4, 1, 3, 6, 42])  # TODO: sa aiba lungime variabila, doar optiunile cerute

        end_options = bytes([0xff])

        padding = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])  # TODO: sa fie de lungime variablia cum trebuie

        package = struct.pack(f'!ssss4s2s2s4s4s4s4s16s64s128s4s3s9s6s6ss7s',
                              op, htype, hlen, hops, xid, secs, flags,
                              ciaddr, yiaddr, siaddr, giaddr, chaddr, sname, file,
                              magic_cookie, message_option, client_identifier_option,
                              requested_ip_address_option, request_option, end_options, padding)

        return package



    @staticmethod
    def request(old_ipaddr, client_mac):
        op = 1
        htype = 1
        hlen = 6
        hops = 0
        xid = generatexid()  # Transaction ID for this message exchange.
        # A DHCP client generates a random number, which the client and server use to identify their message exchange.
        secs = 0
        flags = bytes([0x00, 0x00])
        ciaddr = bytes([0x00, 0x00, 0x00, 0x00])
        yiaddr = bytes([0x00, 0x00, 0x00, 0x00])
        siaddr = bytes([0x00, 0x00, 0x00, 0x00])
        giaddr = bytes([0x00, 0x00, 0x00, 0x00])
        chaddr = bytes([client_mac[0], client_mac[1], client_mac[2], client_mac[3],
                        client_mac[4], client_mac[5], 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00])
        magic_cookie = bytes([0x63, 0x82, 0x53, 0x63])
        option1 = ([53, 1, 3])
        option2_code = 50
        option2_length = 4
        option2_values = bytes([old_ipaddr[0], old_ipaddr[1], old_ipaddr[2], old_ipaddr[3]])

        # TO DO:
        # daca se primeste offer de la mai multe servere, o sa se trimita acest mesaj ca o "confirmare" ca
        # s-a ales serverul asta

        package = struct.pack(f'!bbbblh2s4s4s4s4s16s4sbbbbb{option2_length}s',
                              op, htype, hlen, hops, xid, secs, flags,
                              ciaddr, yiaddr, siaddr, giaddr, chaddr, magic_cookie,
                              option1[0], option1[1], option1[2],
                              option2_code, option2_length, option2_values)

        return package

    @staticmethod
    def decline(client_mac):
        op = 1
        htype = 1
        hlen = 6
        hops = 0
        xid = generatexid()  # Transaction ID for this message exchange.
        # A DHCP client generates a random number, which the client and server use to identify their message exchange.
        secs = 0
        flags = bytes([0x00, 0x00])
        ciaddr = bytes([0x00, 0x00, 0x00, 0x00])
        yiaddr = bytes([0x00, 0x00, 0x00, 0x00])
        siaddr = bytes([0x00, 0x00, 0x00, 0x00])
        giaddr = bytes([0x00, 0x00, 0x00, 0x00])
        chaddr = bytes([client_mac[0], client_mac[1], client_mac[2], client_mac[3],
                        client_mac[4], client_mac[5], 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00])
        magic_cookie = bytes([0x63, 0x82, 0x53, 0x63])
        option1 = ([53, 1, 6])
        package = struct.pack(f'!bbbblh2s4s4s4s4s16s4sbbb',
                              op, htype, hlen, hops, xid, secs, flags,
                              ciaddr, yiaddr, siaddr, giaddr, chaddr, magic_cookie,
                              option1[0], option1[1], option1[2])

        return package

    @staticmethod
    def release(client_mac):
        op = 1
        htype = 1
        hlen = 6
        hops = 0
        xid = generatexid() # Transaction ID for this message exchange.
        # A DHCP client generates a random number, which the client and server use to identify their message exchange.
        secs = 0
        flags = bytes([0x00, 0x00])
        ciaddr = bytes([0x00, 0x00, 0x00, 0x00])
        yiaddr = bytes([0x00, 0x00, 0x00, 0x00])
        siaddr = bytes([0x00, 0x00, 0x00, 0x00])
        giaddr = bytes([0x00, 0x00, 0x00, 0x00])
        chaddr = bytes([client_mac[0], client_mac[1], client_mac[2], client_mac[3],
                        client_mac[4], client_mac[5], 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00])
        magic_cookie = bytes([0x63, 0x82, 0x53, 0x63])
        option1 = ([53, 1, 7])
        package = struct.pack(f'!bbbblh2s4s4s4s4s16s4sbbb',
                              op, htype, hlen, hops, xid, secs, flags,
                              ciaddr, yiaddr, siaddr, giaddr, chaddr, magic_cookie,
                              option1[0], option1[1], option1[2])

        return package

    @staticmethod
    def inform(client_mac, client_ip_addr, options_list):
        op = bytes([0x01])
        htype = bytes([0x01])
        hlen = bytes([0x06])
        hops = bytes([0x00])
        xid = generatexid()  # Transaction ID for this message exchange.
        # A DHCP client generates a random number, which the client and server use to identify their message exchange.
        secs = bytes([0x00, 0x00])
        flags = bytes([0x00, 0x00])
        ciaddr = bytes([client_ip_addr[0], client_ip_addr[1], client_ip_addr[2], client_ip_addr[3]])
        yiaddr = bytes([0x00, 0x00, 0x00, 0x00])
        siaddr = bytes([0x00, 0x00, 0x00, 0x00])
        giaddr = bytes([0x00, 0x00, 0x00, 0x00])
        chaddr = bytes([client_mac[0], client_mac[1], client_mac[2], client_mac[3],
                        client_mac[4], client_mac[5], 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00])
        sname = bytes([0x00] * 64)
        file = bytes([0x00] * 128)

        magic_cookie = bytes([0x63, 0x82, 0x53, 0x63])

        # optiunea care precizeaza ca acesta este un mesaj de tip DISCOVER
        message_option = bytes([53, 1, 8])

        # optiunea care precizeaza ce optiuni se cer de la server
        request_option_length = len(options_list)
        request_option = bytes([52, request_option_length])
        requested_options = bytes(options_list)

        package = struct.pack(f'!ssss4s2s2s4s4s4s4s16s64s128s4s3s2s{request_option_length}s',
                              op, htype, hlen, hops, xid, secs, flags,
                              ciaddr, yiaddr, siaddr, giaddr, chaddr, sname, file,
                              magic_cookie, message_option, request_option, requested_options)

        return package
