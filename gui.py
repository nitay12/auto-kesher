import tkinter as tk
from tkinter import ttk,filedialog,messagebox
import json

from app import *
from sensitive import *
def start(sortFunc,sendFunc):
    #Buttons Functions
    file_path = [""]
    def on_open():
        path = filedialog.askopenfilename()
        file_path[0] = path
        print(file_path[0])

    def on_sort():
        def edit_txt(Text,addresses):
            Text['state']='normal'
            Text.delete(1.0,tk.END)
            Text.insert(tk.END,addresses,'tag-right')
            Text['state']='disabled'
        try:
            print("file path = ", file_path[0])
            addresses = sortFunc(file_path[0])
            print(addresses)
            edit_txt(north_txt,addresses["north"])
            edit_txt(south_txt,addresses["south"])
            edit_txt(east_txt,addresses["east"])
            edit_txt(west_txt,addresses["west"])
        except:
            if file_path[0]=="":
                messagebox.showerror(message="לא נבחר קובץ")
            else:
                messagebox.showerror(message="קובץ אינו נתמך")
    def on_settings():
        north_var = tk.StringVar()
        south_var = tk.StringVar()
        west_var = tk.StringVar()
        east_var = tk.StringVar()
        with open ("emails.json") as emails:
            data = json.load(emails)
            north_email = data["north_email"]
            south_email = data["south_email"]
            east_email = data["east_email"]
            west_email = data["west_email"]
        def on_save():
            print(data)
            print(north_var.get())
            data["north_email"] = north_var.get()
            data["south_email"] = south_var.get()
            data["east_email"] = east_var.get()
            data["west_email"] = west_var.get()
            with open ("emails.json", "w") as emails:
                json.dump(data,emails)
            settings_win.destroy()
        settings_win = tk.Toplevel(master = window)
        emails_frame = tk.Frame(master =settings_win)
        emails_frame.pack()
        north_ent = ttk.Entry(master = emails_frame, textvariable = north_var)
        south_ent = ttk.Entry(master = emails_frame, textvariable = south_var)
        west_ent = ttk.Entry(master = emails_frame, textvariable = west_var)
        east_ent = ttk.Entry(master = emails_frame, textvariable = east_var)
        def add_mail_entry(region, entry, email):
            label = tk.Label(master = emails_frame, text ="כתובת מייל " + region)
            entry
            entry.insert(0, email)
            label.pack()
            entry.pack()
        add_mail_entry("צפון",north_ent, north_email)
        add_mail_entry("דרום",south_ent, south_email)
        add_mail_entry("מרכז",west_ent, west_email)
        add_mail_entry("מזרח",east_ent,east_email)
        save_btn = tk.Button(master = emails_frame,text="שמור", command = on_save)
        save_btn.pack()
    def on_send():
        try:
            with open ("emails.json") as emails:
                data = json.load(emails)
                north_email = data["north_email"]
                south_email = data["south_email"]
                east_email = data["east_email"]
                west_email = data["west_email"]
            north_addresses = north_txt.get(1.0,tk.END)
            east_addresses = east_txt.get(1.0,tk.END)
            west_addresses = west_txt.get(1.0,tk.END)
            south_addresses = south_txt.get(1.0,tk.END)
            print ("sending mail to:", north_email)
            sendFunc(north_email,north_addresses, " צפון ")
            print("mail sent to north Worker")
            sendFunc(east_email,east_addresses, " מזרח ")
            print("mail sent to east Worker")
            sendFunc(west_email,west_addresses, " מרכז ")
            print("mail sent to west Worker")
            sendFunc(south_email,south_addresses, " דרום ")
            messagebox.showinfo(message="המיילים נשלחו")
        except:
            messagebox.showerror(title="תקלה",message="משהו השתבש, לא ניתן היה לשלוח את המיילים")
            raise

    #Main Window
    window = tk.Tk()
    window.title('אוטומציה קשר של אמת') 
    #Title
    title_frame = tk.Frame(master=window)
    title_frame.pack()
    title = tk.Label(master=title_frame, text="אוטומציה \nקשר של אמת")
    title.pack()
    #Buttons
    buttons_frame = tk.Frame(master=window)
    buttons_frame.pack()
    # Open File Button
    file_btn = tk.Button(master=buttons_frame, text="פתח קובץ", command=on_open)
    file_btn.pack()
    n = ttk.Notebook(window)
    f1 = tk.Frame(n)   
    f2 = tk.Frame(n)   
    f3 = tk.Frame(n)
    f4 = tk.Frame(n)
    #Sort Button
    sort_btn = tk.Button(master=buttons_frame,command=on_sort,text="מיין כתובות")
    sort_btn.pack()
    #Settings Button
    settings_btn = tk.Button(master=buttons_frame,command=on_settings,text="הגדרות")
    settings_btn.pack()
    #Addresses Text
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
    
    send_btn = tk.Button(text="שלח לכולם", command=on_send)
    send_btn.pack()
    
    window.mainloop()
start(addresses_sort,send_mail)