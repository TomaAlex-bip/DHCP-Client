import tkinter as tk
from tkinter import ttk


class Interface:

    def __init__(self, width, height):
        self.__window = tk.Tk()
        self.__window.title("DHCP Client")

        s_width = self.__window.winfo_screenwidth()
        s_height = self.__window.winfo_screenheight()
        x_centre = int(s_width/2 - width/2)
        y_centre = int(s_height/2 - height/2)
        self.__window.geometry(f'{width}x{height}+{x_centre}+{y_centre}')
        self.__window.resizable(False, False)


        self.__connect_button = tk.Button(
            self.__window,
            text="Search for a server",
            command=self.on_connect_button_callback
        )
        self.__connect_button.pack(ipadx=0, ipady=0, expand=True, side='left')

        self.__selectedServer = tk.StringVar()
        self.__server_options_combobox = ttk.Combobox(
            self.__window,
            textvariable=self.__selectedServer
        )
        self.__server_options_combobox.pack(ipadx=0, ipady=0, expand=True, side='right')
        self.__server_options_combobox.bind('<<ComboboxSelected>>', self.on_connect_server_chosen)
        self.__server_options_combobox['values'] = ('Test server 1',
                                                    'Test server 2',
                                                    'Test server 3',
                                                    'Test server 4',
                                                    'Test server 5')




    def on_connect_button_callback(self):
        print("inca nu se poate gigele")


    def on_connect_server_chosen(self, ceva):
        print("o alegere minunata")


    def run_interface(self):
        self.__window.mainloop()
