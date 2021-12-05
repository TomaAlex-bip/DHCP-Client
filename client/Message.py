import struct


class Message:

    @staticmethod
    def discover(client_mac):
        op = 1
        htype = 1
        hlen = 6
        hops = 0
        xid = 0  # ??? Transaction ID for this message exchange.
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
        option1 = ([53, 1, 1])
        package = struct.pack(f'!bbbblh2s4s4s4s4s16s4sbbb',
                              op, htype, hlen, hops, xid, secs, flags,
                              ciaddr, yiaddr, siaddr, giaddr, chaddr, magic_cookie,
                              option1[0], option1[1], option1[2])

        return package


    @staticmethod
    def request(old_ipaddr, client_mac):
        op = 1
        htype = 1
        hlen = 6
        hops = 0
        xid = 0  # ??? Transaction ID for this message exchange.
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
        xid = 0  # ??? Transaction ID for this message exchange.
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
        xid = 0  # ??? Transaction ID for this message exchange.
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
    def inform(client_mac):
        op = 1
        htype = 1
        hlen = 6
        hops = 0
        xid = 0  # ??? Transaction ID for this message exchange.
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
        option1 = ([53, 1, 8])
        package = struct.pack(f'!bbbblh2s4s4s4s4s16s4sbbb',
                              op, htype, hlen, hops, xid, secs, flags,
                              ciaddr, yiaddr, siaddr, giaddr, chaddr, magic_cookie,
                              option1[0], option1[1], option1[2])

        return package
