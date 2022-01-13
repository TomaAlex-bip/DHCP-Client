import random
import struct


def generatexid():
    return random.randbytes(4)


# TODO: codificare mesaje
# codifica fiecare mesaj cum trebuie
# captura de date cu wireshark si se vede cum arata un pachet


# 1     DHCPDISCOVER
# 2     DHCPOFFER
# 3     DHCPREQUEST
# 4     DHCPDECLINE
# 5     DHCPACK
# 6     DHCPNAK
# 7     DHCPRELEASE
# 8     DHCPINFORM



class Message:

    # pentru a trimite alte optiuni se face cu opt 52 si dupa in value se trec mai multe optiuni cerute


    @staticmethod
    def discover(client_mac, requested_ip):
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

        requested_ip_address_option = bytes([50, 4, requested_ip[0], requested_ip[1], requested_ip[2], requested_ip[3]])


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
    def request(client_mac, server_ip, old_ipaddr):
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
        sname = bytes([0x00] * 64)
        file = bytes([0x00] * 128)

        magic_cookie = bytes([0x63, 0x82, 0x53, 0x63])

        message_option = bytes([53, 1, 3])

        client_identifier_option = bytes([61, 7, 0x01, client_mac[0], client_mac[1],
                                          client_mac[2], client_mac[3], client_mac[4], client_mac[5]])


        server_identifier_option = bytes([54, 4, server_ip[0], server_ip[1], server_ip[2], server_ip[3]])
        # TODO: aici se pune adresa ip a serverului ales

        # optiunea care precizeaza ce optiuni se cer de la server(addr IP, Gateway, Mask, DNS, lease time)
        # 3 -> gateway
        # 1 -> mask
        # 6 -> DNS
        # 51 -> lease time
        request_option = bytes([55, 4, 0x01, 0x03, 0x06, 0x2a])
        # TODO: sa aiba lungime variabila, doar optiunile cerute
        request_option_length = len(request_option) + 2

        end_option = bytes([0xff])

        padding = bytes([0x00])  # TODO: sa fie de lungime variablia cum trebuie
        padding_length = len(padding)

        requested_ip_address_option = bytes([50, 4, old_ipaddr[0], old_ipaddr[1], old_ipaddr[2], old_ipaddr[3]])
        package = struct.pack(f'!ssss4s2s2s4s4s4s4s16s64s128s4s3s9s6s6s{request_option_length}ss{padding_length}s',
                              op, htype, hlen, hops, xid, secs, flags,
                              ciaddr, yiaddr, siaddr, giaddr, chaddr, sname, file,
                              magic_cookie, message_option, client_identifier_option,
                              requested_ip_address_option, server_identifier_option,
                              request_option, end_option, padding
                              )

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
