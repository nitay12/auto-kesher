import tkinter as tk
from tkinter import ttk
from app import *
from sensitive import *
def start(sortFunc,sendFunc):
    
    window = tk.Tk()
    window.title('אוטומציה קשר של אמת')
    title_frame = tk.Frame(master=window)
    grid_frame = tk.Frame(master=window)

    title = tk.Label(master=title_frame, text="אוטומציה קשר של אמת")
    
    #auto_sort_cbx = tk.Checkbutton(master=title_frame, text="מיון מהיר")
    title.pack()
    
    #auto_sort_cbx.pack()


    title_frame.pack()
    n = ttk.Notebook(window)
    f1 = tk.Frame(n)   
    f2 = tk.Frame(n)   
    f3 = tk.Frame(n)
    f4 = tk.Frame(n)

    north_txt = tk.Text(master=f1, width=30, height=15, font=["ariel",12], state="disabled", bg="#F0F0F0")
    north_txt.tag_configure("tag-right", justify="right")
    south_txt = tk.Text(master=f2,width = 30, height=15, font=["ariel",12], state="disabled", bg="#F0F0F0")
    south_txt.tag_configure("tag-right", justify="right")
    east_txt = tk.Text(master=f3,width= 30,height=15, font=["ariel",12], state="disabled", bg="#F0F0F0")
    east_txt.tag_configure("tag-right", justify="right")
    west_txt = tk.Text(master=f4,width= 30,height=15, font=["ariel",12], state="disabled", bg="#F0F0F0")
    west_txt.tag_configure("tag-right", justify="right")
    def add_scroll(Frame, Text):
        Scroll = ttk.Scrollbar(master=Frame, command=Text.yview, orient="vertical")
        Scroll.grid(column=1, row=0, sticky=("n,s"))
        Text.configure(yscrollcommand=Scroll.set)
    add_scroll(f1,north_txt)
    add_scroll(f2,south_txt)
    add_scroll(f3,east_txt)
    add_scroll(f4,west_txt)
    north_txt.grid(column=0,row=0)
    east_txt.grid(column=0,row=0)
    west_txt.grid(column=0,row=0)
    south_txt.grid(column=0,row=0)


    n.add(f1, text='צפון')
    n.add(f2, text='דרום')
    n.add(f3, text='מזרח')
    n.add(f4, text='מערב')
    n.pack()
    def on_send():
        north_addresses = north_txt.get(1.0,tk.END)
        east_addresses = east_txt.get(1.0,tk.END)
        west_addresses = west_txt.get(1.0,tk.END)
        south_addresses = south_txt.get(1.0,tk.END)
        print ("sending mails")
        sendFunc(north_email,north_addresses, " צפון ")
        print("mail sent to north Worker")
        sendFunc(north_email,east_addresses, " מזרח ")
        print("mail sent to east Worker")
        #sendFunc(west_email,west_addresses, " מרכז ")
        #print("mail sent to west Worker")
        #sendFunc(south_email,south_addresses, " דרום ")

    send_btn = tk.Button(text="שלח לכולם", command=on_send)
    send_btn.pack()
    def on_sort():
        def edit_txt(Text,addresses):
            Text['state']='normal'
            Text.delete(1.0,tk.END)
            Text.insert(tk.END,addresses,'tag-right')
            Text['state']='disabled'
        addresses = sortFunc()
        print(addresses)
        edit_txt(north_txt,addresses["north"])
        edit_txt(south_txt,addresses["south"])
        edit_txt(east_txt,addresses["east"])
        edit_txt(west_txt,addresses["west"])
    sort_btn = tk.Button(master=title_frame,command=on_sort, text="מיין כתובות", width=25, height=5)
    sort_btn.pack()
    window.mainloop()
start(addresses_sort,send_mail)