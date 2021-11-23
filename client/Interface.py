import tkinter as tk
from tkinter import ttk


def on_connect_button_callback():
    print("inca nu se poate gigele")


def on_connect_server_chosen():
    print("o alegere minunata")



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
            command=on_connect_button_callback()
        )
        self.__connect_button.pack(ipadx=0, ipady=0, expand=True, side='left')

        self.__server_options_combobox = ttk.Combobox(
            self.__window,
            textvariable="Servers available"
        )
        self.__server_options_combobox.pack(ipadx=0, ipady=0, expand=True, side='right')
        self.__server_options_combobox.bind('<<ComboboxSelected>>', on_connect_server_chosen())


    def run_interface(self):
        self.__window.mainloop()


