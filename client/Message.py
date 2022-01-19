import random
import struct


def generatexid():
    return random.randbytes(4)



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
        sname = bytes([0x00] * 64)
        file = bytes([0x00] * 128)

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
    def request(client_mac, server_ip, old_ipaddr, options_list):
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

        # optiunea care precizeaza ce optiuni se cer de la server(addr IP, Gateway, Mask, DNS, lease time)
        # 3 -> gateway
        # 1 -> mask
        # 6 -> DNS
        # 51 -> lease time
        request_option = bytes([55, len(options_list)])

        i = 0
        while i < len(options_list):
            request_option += bytes([options_list[i]])
            i = i + 1

        request_option_length = len(request_option)

        # 260 de octeti pana la server_identifier inclusiv + end_option
        message_length = 260

        if message_length % 16 == 0:
            padding_length = 16
        else:
            good_length = (int(message_length / 16) + 1) * 16
            padding_length = good_length - message_length + 1

        padding = bytes([0x00] * padding_length)

        end_option = bytes([0xff])

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
    def decline(client_mac, server_ip):
        op = bytes([0x01])
        htype = bytes([0x01])
        hlen = bytes([0x06])
        hops = bytes([0x00])
        xid = generatexid()  # Transaction ID for this message exchange.
        # A DHCP client generates a random number, which the client and server use to identify their message exchange.
        secs = bytes([0x00, 0x00])
        flags = bytes([0x00, 0x00])
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
        message_option = bytes([53, 1, 4])

        client_identifier_option = bytes([61, 7, 0x01, client_mac[0], client_mac[1],
                                          client_mac[2], client_mac[3], client_mac[4], client_mac[5]])

        server_identifier_option = bytes([54, 4, server_ip[0], server_ip[1], server_ip[2], server_ip[3]])

        end_option = bytes([0xff])

        padding = bytes([0x00] * 13)
        padding_length = len(padding)

        package = struct.pack(f'!ssss4s2s2s4s4s4s4s16s64s128s4s3s9s6ss{padding_length}s',
                              op, htype, hlen, hops, xid, secs, flags, ciaddr, yiaddr, siaddr, giaddr,
                              chaddr, sname, file, magic_cookie, message_option, client_identifier_option,
                              server_identifier_option, end_option, padding)

        return package


    @staticmethod
    def release(client_mac, server_ip):
        op = bytes([0x01])
        htype = bytes([0x01])
        hlen = bytes([0x06])
        hops = bytes([0x00])
        xid = generatexid()  # Transaction ID for this message exchange.
        # A DHCP client generates a random number, which the client and server use to identify their message exchange.
        secs = bytes([0x00, 0x00])
        flags = bytes([0x00, 0x00])
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
        message_option = bytes([53, 1, 7])

        client_identifier_option = bytes([61, 7, 0x01, client_mac[0], client_mac[1],
                                          client_mac[2], client_mac[3], client_mac[4], client_mac[5]])

        server_identifier_option = bytes([54, 4, server_ip[0], server_ip[1], server_ip[2], server_ip[3]])

        end_option = bytes([0xff])

        padding = bytes([0x00] * 13)
        padding_length = len(padding)

        package = struct.pack(f'!ssss4s2s2s4s4s4s4s16s64s128s4s3s9s6ss{padding_length}s',
                              op, htype, hlen, hops, xid, secs, flags, ciaddr, yiaddr, siaddr, giaddr,
                              chaddr, sname, file, magic_cookie, message_option, client_identifier_option,
                              server_identifier_option, end_option, padding)

        return package


    @staticmethod
    def inform(client_mac, server_ip, options_list):
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

        message_option = bytes([53, 1, 8])

        client_identifier_option = bytes([61, 7, 0x01, client_mac[0], client_mac[1],
                                          client_mac[2], client_mac[3], client_mac[4], client_mac[5]])

        server_identifier_option = bytes([54, 4, server_ip[0], server_ip[1], server_ip[2], server_ip[3]])

        # optiunea care precizeaza ce optiuni se cer de la server(addr IP, Gateway, Mask, DNS, lease time, etc...)
        request_option = bytes([55, len(options_list)])
        i = 0
        while i < len(options_list):
            request_option += bytes([options_list[i]])
            i = i + 1

        request_option_length = len(request_option)

        end_option = bytes([0xff])

        # 260 de octeti pana la server_identifier inclusiv + end_option
        message_length = 260 + request_option_length

        # TODO: TEST cu wireshark !!!

        if message_length % 16 == 0:
            padding_length = 16
        else:
            good_length = (int(message_length / 16) + 1) * 16
            padding_length = good_length - message_length + 1

        padding = bytes([0x00] * padding_length)


        print("request_option: " + request_option.hex())

        package = struct.pack(f'!ssss4s2s2s4s4s4s4s16s64s128s4s3s9s6s{request_option_length}ss{padding_length}s',
                              op, htype, hlen, hops, xid, secs, flags,
                              ciaddr, yiaddr, siaddr, giaddr, chaddr, sname, file,
                              magic_cookie, message_option, client_identifier_option,
                              server_identifier_option, request_option, end_option, padding
                              )

        return package


    @staticmethod
    def get_options(client_mac, server_ip, options_list):
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

        client_identifier_option = bytes([61, 7, 0x01, client_mac[0], client_mac[1],
                                          client_mac[2], client_mac[3], client_mac[4], client_mac[5]])

        server_identifier_option = bytes([54, 4, server_ip[0], server_ip[1], server_ip[2], server_ip[3]])

        # optiunea care precizeaza ce optiuni se cer de la server(addr IP, Gateway, Mask, DNS, lease time, etc...)
        request_option = bytes([55, len(options_list)])
        i = 0
        while i < len(options_list):
            request_option += bytes([options_list[i]])
            i = i + 1

        request_option_length = len(request_option)

        end_option = bytes([0xff])

        # 260 de octeti pana la server_identifier inclusiv + end_option
        message_length = 257 + request_option_length

        # TODO: TEST cu wireshark !!!

        if message_length % 16 == 0:
            padding_length = 16
        else:
            good_length = (int(message_length / 16) + 1) * 16
            padding_length = good_length - message_length + 1

        padding = bytes([0x00] * padding_length)


        print("request_option: " + request_option.hex())

        package = struct.pack(f'!ssss4s2s2s4s4s4s4s16s64s128s4s9s6s{request_option_length}ss{padding_length}s',
                              op, htype, hlen, hops, xid, secs, flags,
                              ciaddr, yiaddr, siaddr, giaddr, chaddr, sname, file,
                              magic_cookie, client_identifier_option,
                              server_identifier_option, request_option, end_option, padding
                              )

        return package


    @staticmethod
    def unpack_package(package):
        size = len(package)  # 240 de octeti pana la magic cookie(inclusiv)
        options_length = size - 240

        try:
            message = struct.unpack(f'!ssss4s2s2s4s4s4s4s16s64s128s4s{options_length}s', package)
            read_options = message[15]
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

            return message, options_length, processed_options

        except:
            return None


    @staticmethod
    def package_type(options):
        if options[0][0] == 53 and options[0][2][0] == 2:
            return 'OFFER'
        elif options[0][0] == 53 and options[0][2][0] == 6:
            return 'ACK'
        elif options[0][0] == 53 and options[0][2][0] == 7:
            return 'NAK'
        else:
            return 'unknown'



























