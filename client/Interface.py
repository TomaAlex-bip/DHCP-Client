import socket
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Style

from NetworkInterface import NetworkInterface

mac_addr_client = bytes([0x00, 0x0b, 0x82, 0x01, 0xfc, 0x42])
old_ip_addr_client = bytes([0xc0, 0xa8, 0x00, 0x71])

ni = NetworkInterface(mac_addr_client, old_ip_addr_client )
ni.start()


global opt1, opt3, opt4, opt6, opt12, opt15, opt28, opt50, opt51, opt53, opt58, opt59, opt184, enabled


class Interface:

    def __init__(self, width, height):
        self.__window = Tk()
        self.__window.title("DHCP Client")

        s_width = self.__window.winfo_screenwidth()
        s_height = self.__window.winfo_screenheight()
        x_centre = int(s_width / 2 - width / 2)
        y_centre = int(s_height / 2 - height / 2)
        self.__window.geometry(f'{width}x{height}+{x_centre}+{y_centre}')
        self.__window.resizable(False, False)

        self.pw = PanedWindow(orient=VERTICAL, bg="black")

        # Left listbox
        self.left_list = Listbox(self.__window)
        self.left_list.pack(side=LEFT)
        self.pw.add(self.left_list)

        # Right listbox
        self.right_list = Listbox(self.__window)
        self.right_list.pack(side=LEFT)
        self.pw.add(self.right_list)

        # place the panedwindow on the root window
        self.pw.pack(fill=BOTH, expand=True)

        self.enabled = IntVar()

        self.__connect_button = Checkbutton(
            self.right_list,
            text="Enable DHCP", font=("Arial", 15),
            command=self.on_connect_button_callback, variable=self.enabled,
            onvalue=1,
            offvalue=0
        )
        self.__connect_button.pack(ipadx=0, ipady=0, expand=True, side='left')

        self.__legend_button = Button(
            self.right_list,
            text="Option legend",
            command=self.on_legend_button_callback
        )
        self.__legend_button.pack(ipadx=0, ipady=0, expand=True, side='left')

        self.__options_button = Menubutton(
            self.right_list,
            text="Choose options",
            relief=RAISED
        )

        self.__options_button.menu = Menu(self.__options_button, tearoff=0)
        self.__options_button["menu"] = self.__options_button.menu
        self.__options_button.pack(ipadx=0, ipady=0, expand=True, side='left')

        opt1 = IntVar()
        opt3 = IntVar()
        opt4 = IntVar()
        opt6 = IntVar()
        opt12 = IntVar()
        opt15 = IntVar()
        opt28 = IntVar()
        opt50 = IntVar()
        opt51 = IntVar()
        opt53 = IntVar()
        opt58 = IntVar()
        opt59 = IntVar()
        opt184 = IntVar()

        self.__options_button.menu.add_checkbutton(label="1", variable=opt1, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="3", variable=opt3, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="4", variable=opt4, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="6", variable=opt6, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="12", variable=opt12, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="15", variable=opt15, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="28", variable=opt28, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="50", variable=opt50, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="51", variable=opt51, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="53", variable=opt53, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="58", variable=opt58, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="59", variable=opt59, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="184", variable=opt184, onvalue=1, offvalue=0)

        self.__options_button.pack()

        def Item_test():
            if opt1.get() == 1:
                print("1")
            if opt3.get() == 1:
                print("3")
            if opt4.get() == 1:
                print("4")
            if opt6.get() == 1:
                print("6")
            if opt12.get() == 1:
                print("12")
            if opt15.get() == 1:
                print("15")
            if opt28.get() == 1:
                print("28")
            if opt50.get() == 1:
                print("50")
            if opt51.get() == 1:
                print("51")
            if opt53.get() == 1:
                print("53")
            if opt58.get() == 1:
                print("58")
            if opt59.get() == 1:
                print("59")
            if opt184.get() == 1:
                print("184")

        self.__apply = Button(
            self.right_list,
            text='Apply',
            command=Item_test)

        self.__apply.place(relx=0.84, rely=0.6)

        def showTableini(self):
            self.listBox.insert('', 'end', text="1",
                                values=((mac_addr_client.hex()).upper(), socket.inet_ntoa(old_ip_addr_client)))

        self.s = Style()
        self.s.configure('Treeview', rowheight=8)
        Label(self.left_list, text="DHCP Client Table", font=("Arial", 15)).place(relx=0.4, y=15)
        self.client_table = ['MAC Address', 'IP Address']
        self.listBox = Treeview(self.left_list, columns=self.client_table, show='headings')
        for i in self.client_table:
            self.listBox.column(i, width=200)
            self.listBox.heading(i, text=i)
        self.listBox.place(relx=0.5, rely=0.5, anchor="center")
        showTableini(self)

    def add_col(self):
        self.client_table.append('Subnet Mask')
        self.client_table.append('Gateway Address')
        self.client_table.append('DNS Address')
        self.client_table.append('Lease time')
        self.listBox = Treeview(self.left_list, columns=self.client_table, show='headings')
        for i in self.client_table:
            self.listBox.column(i, width=100)
            self.listBox.heading(i, text=i)
        self.listBox.place(relx=0.5, rely=0.5, anchor="center")
        self.listBox.insert('', 'end', text="1",
                            values=(
                            (mac_addr_client.hex()).upper(), socket.inet_ntoa(ni.get_ip()), socket.inet_ntoa(ni.get_sm()), socket.inet_ntoa(ni.get_gw()),
                            socket.inet_ntoa(ni.get_dns()), str(ni.get_lease()) + 's'))



    def on_connect_button_callback(self):
        if self.enabled.get() == 1:
            print("DHCP enabled")
        elif self.enabled.get() == 0:
            print("DHCP disabled")
        self.add_col()

    def on_legend_button_callback(self):
        messagebox.showinfo('Options Legend', 'Cele mai folosite optiuni sunt: \n'
                                              '1  - specifică masca subrețelei\n'
                                              '3  - specifică adresa gateway\n'
                                              '4  - specifică timpul serverului\n'
                                              '6  - specifică adresa IP a serverului DNS\n'
                                              '12 - specifică numele dispozitivului a unui client DHCP\n'
                                              '15 - specifică numele domeniului\n'
                                              '28 - specifică o adresă de difuzie\n'
                                              '50 - specifică adresa IP cerută\n'
                                              '51 - specifică timpul de împrumut a unei adrese\n'
                                              '53 - specifică un tip de mesaj DHCP\n'
                                              '58 - specifică timpul de reînnoire (T1)\n'
                                              '59 - specifică timpul de reînnoire (T2)\n'
                                              '184 - opțiune rezervată, se poate configura informația care să fie transmisă în această opțiune\n')

    def run_interface(self):
        self.__window.mainloop()
