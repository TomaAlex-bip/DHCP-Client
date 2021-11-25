import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Entry


class Interface:

    def __init__(self, width, height):
        self.__window = tk.Tk()
        self.__window.title("DHCP Client")

        s_width = self.__window.winfo_screenwidth()
        s_height = self.__window.winfo_screenheight()
        x_centre = int(s_width / 2 - width / 2)
        y_centre = int(s_height / 2 - height / 2)
        self.__window.geometry(f'{width}x{height}+{x_centre}+{y_centre}')
        self.__window.resizable(False, False)

        self.__connect_button = tk.Button(
            self.__window,
            text="Search for a server",
            command=self.on_connect_button_callback
        )
        self.__connect_button.pack(ipadx=0, ipady=0, expand=True, side='left')

        self.__legend_button = tk.Button(
            self.__window,
            text="Option legend",
            command=self.on_legend_button_callback
        )
        self.__legend_button.pack(ipadx=0, ipady=0, expand=True, side='left')

        self.__options_button = tk.Button(
            self.__window,
            text="Insert options",
            command=self.on_options_button_callback
        )
        self.__options_button.pack(ipadx=0, ipady=0, expand=True, side='left')

        self.__selectedServer = tk.StringVar()
        self.__server_options_combobox = ttk.Combobox(
            self.__window,
            textvariable=self.__selectedServer
        )

        self.t = tk.StringVar(self.__window)
        self.e = Entry(self.__window, textvariable=self.t)
        self.e.pack(ipadx=0, ipady=0, expand=True, side='left')

        self.__server_options_combobox.pack(ipadx=0, ipady=0, expand=True, side='right')
        self.__server_options_combobox.bind('<<ComboboxSelected>>', self.on_connect_server_chosen)
        self.__server_options_combobox['values'] = ('Test server 1',
                                                    'Test server 2',
                                                    'Test server 3',
                                                    'Test server 4',
                                                    'Test server 5')

    def on_connect_button_callback(self):
        print("inca nu se poate gigele")

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

    def on_options_button_callback(self):
        op = self.t.get()
        op_list = op.split(',')
        print(op_list)


    def on_connect_server_chosen(self, ceva):
        print("o alegere minunata")

    def run_interface(self):
        self.__window.mainloop()
