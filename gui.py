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
            if file_path[0]=="":
                messagebox.showerror(message="לא נבחר קובץ")
            else:
                print("file path = ", file_path[0])
                addresses = sortFunc(file_path[0])
                print(addresses)
                edit_txt(north_txt,addresses["north"])
                edit_txt(south_txt,addresses["south"])
                edit_txt(east_txt,addresses["east"])
                edit_txt(west_txt,addresses["west"])
        except:
            messagebox.showerror(message="קובץ אינו נתמך")
            raise
    def on_settings():
        with open ("config.json") as config:
            settings = json.load(config)
            emails = settings["emails"]
            north_email = emails["north_email"]
            south_email = emails["south_email"]
            east_email = emails["east_email"]
            west_email = emails["west_email"]

            columns = settings["columns"]
            date_col = columns["dateDead"]
            family_col = columns["familyName"]
            name_col = columns["firstName"]
            street_col = columns["street"]
            street_num_col = columns["street_num"]
            city_col = columns["city"]
            conection_col = columns["deadConection"]
            phone_col = columns["phone"]
        def on_save():
            print(north_ent.get())
            emails = settings["emails"]
            emails["north_email"] = north_ent.get()
            emails["south_email"] = south_ent.get()
            emails["east_email"] = east_ent.get()
            emails["west_email"] = west_ent.get()
            columns = settings["columns"]
            columns["dateDead"] = date_ent.get()
            columns["familyName"] = family_ent.get()
            columns["firstName"] = name_ent.get()
            columns["street"] = street_ent.get()
            columns["street_num"] = street_num_ent.get()
            columns["city"] = city_ent.get()
            columns["deadConection"] = conection_ent.get()
            columns["phone"] = phone_ent.get()
            with open ("config.json", "w") as config:
                json.dump(settings,config)
            settings_win.destroy()
        
        settings_win = tk.Toplevel(master = window)
        emails_frame = ttk.Frame(master = settings_win,padding =5)
        emails_frame.grid(row = 0,column =1)
        emails_label = ttk.Label(master =emails_frame, text = "מיילים",background ="red")
        emails_label.pack()
        columns_frame = ttk.Frame(master =settings_win, padding =5)
        columns_frame.grid(row=0,column=0)
        columns_label = ttk.Label(master = columns_frame, text = "עמודות", background ="red")
        columns_label.pack()
        save_btn = tk.Button(master = settings_win,text="שמור", command = on_save)
        save_btn.grid(row=1)

        north_ent = ttk.Entry(master = emails_frame)
        south_ent = ttk.Entry(master = emails_frame)
        west_ent = ttk.Entry(master = emails_frame)
        east_ent = ttk.Entry(master = emails_frame)

        date_ent = ttk.Entry(master = columns_frame)
        family_ent = ttk.Entry(master = columns_frame)
        name_ent = ttk.Entry(master = columns_frame)
        street_ent = ttk.Entry(master = columns_frame)
        street_num_ent = ttk.Entry(master = columns_frame)
        city_ent = ttk.Entry(master = columns_frame)
        conection_ent = ttk.Entry(master = columns_frame)
        phone_ent = ttk.Entry(master = columns_frame)
        def add_ent(label, entry, master, content):
            label = tk.Label(master = master, text = label)
            entry
            entry.insert(0, content)
            label.pack()
            entry.pack()
        add_ent("כתובת מייל צפון",north_ent,emails_frame, north_email)
        add_ent("כתובת מייל דרום",south_ent,emails_frame ,south_email)
        add_ent("כתובת מייל מרכז",west_ent,emails_frame,west_email)
        add_ent("כתובת מייל מזרח",east_ent,emails_frame,east_email)

        add_ent("תאריך",date_ent,columns_frame,date_col)
        add_ent("שם משפחה",family_ent,columns_frame,family_col)
        add_ent("שם פרטי",name_ent,columns_frame,name_col)
        add_ent("רחוב",street_ent,columns_frame,street_col)
        add_ent("מספר דירה", street_num_ent,columns_frame,street_num_col)
        add_ent("עיר",city_ent,columns_frame,city_col)
        add_ent("קרבה",conection_ent,columns_frame,conection_col)
        add_ent("טלפון",phone_ent,columns_frame,phone_col)
    def on_send():
        try:
            with open ("config.json") as config:
                settings = json.load(config)
                emails = settings["emails"]
                north_email = emails["north_email"]
                south_email = emails["south_email"]
                east_email = emails["east_email"]
                west_email = emails["west_email"]
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
    file_btn = tk.Button(master=buttons_frame, text="פתח קובץ", command=on_open, height = 2, width = 16)
    file_btn.grid(row=0,column=2)
    #Sort Button
    sort_btn = tk.Button(master=buttons_frame,command=on_sort,text="מיין כתובות", height = 2, width = 16)
    sort_btn.grid(row=1,column=2)
    #Settings Button
    settings_btn = tk.Button(master=buttons_frame,command=on_settings,text="הגדרות", height = 2, width = 16)
    settings_btn.grid(row=0,column=0)
    #Addresses Text
    addresses_frame = tk.Frame(window)
    addresses_frame.pack()
    #Addresses Notebook
    n = ttk.Notebook(addresses_frame)
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
    n.add(f4, text='מרכז')
    n.pack()
    
    send_btn = tk.Button(text="שלח לכולם", command=on_send)
    send_btn.pack()
    
    window.mainloop()
start(addresses_sort,send_mail)