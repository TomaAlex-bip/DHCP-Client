import socket
import threading
import time
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Style

import op_list

# mac_addr_client = bytes([0x00, 0x0b, 0x82, 0x01, 0xfc, 0x42])
# old_ip_addr_client = bytes([0xc0, 0xa8, 0x00, 0x71])

# ni = NetworkInterface(mac_addr_client, old_ip_addr_client)

global opt1, opt3, opt4, opt6, opt12, opt15, opt28, opt50, opt51, opt53, opt58, opt59, opt184, enabled


class Interface:

    def __init__(self, width, height, ni):
        self.__window = Tk()
        self.__window.title("DHCP Client")

        self.__networkInterface = ni

        self.__refresh_gui_interface_thread = threading.Thread(target=self.refresh_gui_interface)

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

        self.opt1 = IntVar()
        self.opt3 = IntVar()
        self.opt4 = IntVar()
        self.opt6 = IntVar()
        self.opt12 = IntVar()
        self.opt15 = IntVar()
        self.opt28 = IntVar()
        self.opt50 = IntVar()
        self.opt51 = IntVar()
        self.opt53 = IntVar()
        self.opt58 = IntVar()
        self.opt59 = IntVar()
        self.opt184 = IntVar()

        self.__options_button.menu.add_checkbutton(label="1", variable=self.opt1, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="3", variable=self.opt3, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="4", variable=self.opt4, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="6", variable=self.opt6, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="12", variable=self.opt12, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="15", variable=self.opt15, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="28", variable=self.opt28, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="50", variable=self.opt50, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="51", variable=self.opt51, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="53", variable=self.opt53, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="58", variable=self.opt58, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="59", variable=self.opt59, onvalue=1, offvalue=0)
        self.__options_button.menu.add_checkbutton(label="184", variable=self.opt184, onvalue=1, offvalue=0)

        self.__options_button.pack()

        self.__apply = Button(
            self.right_list,
            text='Apply',
            command=self.Item_test)

        self.__apply.place(relx=0.84, rely=0.6)

        def showTableini():
            self.listBox.insert('', 'end', text="1",
                                values=((ni.get_mac().hex()).upper(), socket.inet_ntoa(ni.get_old_ip())))

        self.s = Style()
        self.s.configure('Treeview', rowheight=8)
        Label(self.left_list, text="DHCP Client Table", font=("Arial", 15)).place(relx=0.4, y=15)
        self.client_table = ['MAC Address', 'IP Address']
        self.listBox = Treeview(self.left_list, columns=self.client_table, show='headings')
        for i in self.client_table:
            self.listBox.column(i, width=200)
            self.listBox.heading(i, text=i)
        self.listBox.place(relx=0.5, rely=0.5, anchor="center")
        showTableini()

    def Item_test(self):
        opt_list = []
        if self.opt1.get() == 1:
            opt_list.append(1)
        if self.opt3.get() == 1:
            opt_list.append(3)
        if self.opt4.get() == 1:
            opt_list.append(4)
        if self.opt6.get() == 1:
            opt_list.append(6)
        if self.opt12.get() == 1:
            opt_list.append(12)
        if self.opt15.get() == 1:
            opt_list.append(15)
        if self.opt28.get() == 1:
            opt_list.append(28)
        if self.opt50.get() == 1:
            opt_list.append(50)
        if self.opt51.get() == 1:
            opt_list.append(51)
        if self.opt53.get() == 1:
            opt_list.append(53)
        if self.opt58.get() == 1:
            opt_list.append(58)
        if self.opt59.get() == 1:
            opt_list.append(59)
        if self.opt184.get() == 1:
            opt_list.append(184)
        self.__networkInterface.update_options_list(opt_list)



    #def return_op(self):
    #    op_list.op_list = self.Item_test()
    #    print(op_list.op_list)


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
        # time.sleep(22)



    def on_connect_button_callback(self):
        if self.enabled.get() == 1:
            self.__networkInterface.start()
            print("DHCP enabled")

            self.__refresh_gui_interface_thread.start()

            for i in self.listBox.get_children():
                self.listBox.delete(i)
            self.__window.update()
            self.add_col()
        elif self.enabled.get() == 0:
            self.__networkInterface.reset_client(False)
            self.__refresh_gui_interface_thread.join()
            print("DHCP disabled")

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
                                              '184 - opțiune rezervată, se poate configura informația care să fie '
                                              'transmisă în această opțiune\n')

    def run_interface(self):
        self.__window.mainloop()


    def refresh_gui_interface(self):
        while True:
            temp = self.__networkInterface.get_lease() - self.__networkInterface.get_lease_time_contor()
            self.listBox.insert('', 'end', text="1",
                                values=(
                                    (self.__networkInterface.get_mac().hex()).upper(),
                                    socket.inet_ntoa(self.__networkInterface.get_ip()),
                                    socket.inet_ntoa(self.__networkInterface.get_sm()),
                                    socket.inet_ntoa(self.__networkInterface.get_gw()),
                                    socket.inet_ntoa(self.__networkInterface.get_dns()),
                                    str(temp) + 's'))

            mins, secs = divmod(temp, 60)
            hours = 0
            if mins > 60:
                hours, mins = divmod(mins, 60)

            for i in self.listBox.get_children():
                self.listBox.delete(i)
            self.listBox.insert('', 'end', values=(self.__networkInterface.get_mac().hex().upper(),
                                                   socket.inet_ntoa(self.__networkInterface.get_ip()),
                                                   socket.inet_ntoa(self.__networkInterface.get_sm()),
                                                   socket.inet_ntoa(self.__networkInterface.get_gw()),
                                                   socket.inet_ntoa(self.__networkInterface.get_dns()),
                                                   '{:d}:{:02d}:{:02d}'.format(hours, mins, secs)))
            self.__window.update()
            time.sleep(1)

            # when temp value = 0; then a messagebox pop's up
            # with a message:"Time's up"
            temp -= 1
            if temp == 0:
                messagebox.showinfo(title="Lease Time", message="Lease time's up! Starting renewal...")
                # TODO asteapta pana la primirea de informatii noi dupa renew si reincepe timerul...

