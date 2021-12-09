import tkinter as tk
import tkinter.font as font
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



        mac_label = tk.Label(self.__window, text='MAC address of the client\nPlease use format FF:FF:FF:FF:FF:FF')
        mac_label.place(relx=0.15, y=20)

        self.__mac_addr_text = tk.Text(self.__window, height=1, width=25)
        self.__mac_addr_text.place(relx=0.15, y=60)
        self.__mac_addr_text.insert('1.0', '8F:45:A7:90:BA:C4')

        mac_label = tk.Label(self.__window, text='old IP address of the client\nPlease use format 255.255.255.255')
        mac_label.place(relx=0.6, y=20)

        self.__old_ip_addr_text = tk.Text(self.__window, height=1, width=25)
        self.__old_ip_addr_text.place(relx=0.6, y=60)
        self.__old_ip_addr_text.insert('1.0', '0.0.0.0')

        start_button_font = font.Font(family='Helvetica', size=14, weight='bold')
        self.__connect_button = tk.Button(
            self.__window,
            text="Start the client",
            font=start_button_font,
            command=self.on_connect_button_callback
        )
        self.__connect_button.place(x=320, y=120)

        current_ip_addr_label = tk.Label(self.__window, text='Your IP address:')
        current_ip_addr_label.place(x=50, y=250)
        self.__current_ip_addr_text = tk.Text(self.__window, height=1, width=20)
        self.__current_ip_addr_text.place(x=145, y=250)
        self.__current_ip_addr_text['state'] = 'disabled'
        self.__current_ip_addr_text.insert('1.0', '0.0.0.0')

        lease_time_label = tk.Label(self.__window, text='Lease time:')
        lease_time_label.place(x=75, y=300)
        self.__lease_time_text = tk.Text(self.__window, height=1, width=10)
        self.__lease_time_text.place(x=145, y=300)
        self.__lease_time_text['state'] = 'disabled'
        self.__lease_time_text.insert('1.0', '99')

        options_label = tk.Label(self.__window, text='Available options:')
        options_label.place(x=40, y=350)
        self.__selected_option = tk.StringVar()
        self.__options_combobox = ttk.Combobox(
            self.__window,
            textvariable=self.__selected_option
        )
        self.__options_combobox.place(x=145, y=350)
        self.__options_combobox.bind('<<ComboboxSelected>>', self.on_connect_server_chosen)
        self.__options_combobox['values'] = ('option 1',
                                             'option 2',
                                             'option 3',
                                             'option 4',
                                             'option 5')

        self.__send_option_button = tk.Button(
            self.__window,
            text="Send the option to the server",
            command=self.on_send_option_button_callback
        )
        self.__send_option_button.place(x=100, y=380)



        client_console_label = tk.Label(self.__window, text="Console:")
        client_console_label.place(x=500, y=215)

        self.__client_console_text = tk.Text(self.__window, height=20, width=45)
        self.__client_console_text.place(x=400, y=250)
        self.__client_console_text['state'] = 'disabled'
        self.__client_console_text.insert('1.0', '99')



    def on_send_option_button_callback(self):
        print("incercam dar nu putem")


    def on_connect_button_callback(self):
        print("inca nu se poate gigele")


    def on_connect_server_chosen(self, ceva):
        print("o alegere minunata")


    def run_interface(self):
        self.__window.mainloop()
