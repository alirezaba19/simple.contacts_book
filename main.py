from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk

root = Tk()
root.title("contacts")
root.geometry("970x550")
background_color = "#1d6ecf"
root.configure(bg=background_color)
root.iconbitmap("main_icon.ico")
font_color = "#ffffff"
sub_font_color = "#ffffff"
font = "#Times 18 normal"
sub_font = "#Times 12 normal"
design_row = 0


# create a main_frame
main_frame = Frame(root, bg=background_color)
main_frame.pack(fill=BOTH, expand=1)
# create a canvas
my_canvas = Canvas(main_frame, bg=background_color)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
#  add scrollbar to canvas
my_scrollbar = ttk.Scrollbar(
    main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)
# config scrollbar
my_canvas.configure(yscrollcommand=my_scrollbar.set, bg=background_color)
my_canvas.bind("<Configure>", lambda e: my_canvas.configure(
    scrollregion=my_canvas.bbox("all")))
# create another frame in canvas
second_frame = Frame(my_canvas, bg=background_color)
# add that new frame in the canvas
my_canvas.create_window((0, 0), window=second_frame, anchor="nw")


class User():
    def __init__(self, name, last_name, phone_number, email, id, row):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.id_label = Label(
            second_frame, text=id, font=sub_font, bg=background_color, fg=sub_font_color)
        self.id_label.grid(row=row, column=0)
        self.name_label = Label(
            second_frame, text=name, font=sub_font, bg=background_color, fg=sub_font_color)
        self.name_label.grid(row=row, column=1)
        self.last_name_label = Label(
            second_frame, text=last_name, font=sub_font, bg=background_color, fg=sub_font_color)
        self.last_name_label.grid(row=row, column=2)
        self.phone_number_label = Label(second_frame, text=str(
            0)+str(phone_number), font=sub_font, bg=background_color, fg=sub_font_color)
        self.phone_number_label.grid(row=row, column=3)
        self.email_label = Label(
            second_frame, text=email, font=sub_font, bg=background_color, fg=sub_font_color)
        self.email_label.grid(row=row, column=4)
        self.all_entities = [self.id_label, self.name_label,
                             self.last_name_label, self.phone_number_label, self.email_label]
        self.delete_button = Button(second_frame, text="Delete", command=self.delete_user,
                                    bg=background_color, fg=font_color, font=sub_font)
        self.delete_button.grid(row=row, column=5)
        self.edit_button = Button(second_frame, text="Edit", command=self.edit_user,
                                  bg=background_color, fg=font_color, font=sub_font)
        self.edit_button.grid(row=row, column=6)

    def delete_user(self):
        delete_or_not = messagebox.askokcancel(
            "Delete Contact?", "Are you sure you want to delete this contact?")
        if delete_or_not == True or delete_or_not == 1:
            conn = sqlite3.connect("contacts_book.db")
            cursor = conn.cursor()
            cursor.execute("DELETE from contacts WHERE oid = " +
                           str(self.id_label["text"]))
            conn.commit()
            conn.close()
            show_contacts()

    def grid_f(self):
        self.id_label.grid_forget()
        self.id_label.destroy()
        self.name_label.grid_forget()
        self.name_label.destroy()
        self.last_name_label.grid_forget()
        self.last_name_label.destroy()
        self.phone_number_label.grid_forget()
        self.phone_number_label.destroy()
        self.email_label.grid_forget()
        self.email_label.destroy()
        self.delete_button.grid_forget()
        self.delete_button.destroy()
        self.edit_button.grid_forget()
        self.edit_button.destroy()

    def edit_user(self):
        def save_edit():
            conn = sqlite3.connect("contacts_book.db")
            cursor = conn.cursor()
            ask_edit = messagebox.askokcancel(
                "Edit contact", "Are you sure you want to save changes?")
            if ask_edit == True or ask_edit == 1:

                cursor.execute("""UPDATE contacts SET
                    first_name = :first,
                    last_name = :last,
                    phone_number = :phone,
                    email = :email_
                    WHERE oid = :oid""",
                               {
                                   'first': self.first_name_entry.get(),
                                   'last': self.last_name_entry.get(),
                                   'phone': self.phone_number_entry.get(),
                                   'email_': self.email_entry.get(),
                                   'oid': self.id
                               }
                               )
                self.edit_screen.destroy()
            conn.commit()
            conn.close()
            show_contacts()

        def discard_edit():
            self.edit_screen.destroy()

        self.edit_screen = Toplevel()
        self.edit_screen.title(f"Edit {self.name} {self.last_name}")
        self.edit_screen.geometry("400x400")
        self.edit_screen.iconbitmap("main_icon.ico")
        self.edit_screen.configure(bg=background_color)

        self.first_name_entry = Entry(
            self.edit_screen, font="arial 12 normal", width=25)
        self.first_name_entry.grid(row=0, column=1, padx=20)
        self.last_name_entry = Entry(
            self.edit_screen, font="arial 12 normal", width=25)
        self.last_name_entry.grid(row=1, column=1)
        self.phone_number_entry = Entry(
            self.edit_screen, font="arial 12 normal", width=25)
        self.phone_number_entry.grid(row=2, column=1)
        self.email_entry = Entry(
            self.edit_screen, font="arial 12 normal", width=25)
        self.email_entry.grid(row=3, column=1)
        first_name_edit_label = Label(self.edit_screen, bg=background_color,
                                      fg=sub_font_color, text="Fisrt name:", font="arial 12 bold")
        first_name_edit_label.grid(row=0, column=0, pady=20)
        last_name_edit_label = Label(self.edit_screen, bg=background_color,
                                     fg=sub_font_color, text="Last name:", font="arial 12 bold")
        last_name_edit_label.grid(row=1, column=0, pady=20)
        phone_number_edit_label = Label(self.edit_screen, bg=background_color,
                                        fg=sub_font_color, text="Phone number: ", font="arial 12 bold")
        phone_number_edit_label.grid(row=2, column=0, pady=20)
        email_edit_label = Label(self.edit_screen, bg=background_color,
                                 fg=sub_font_color, text="Email:", font="arial 12 bold")
        email_edit_label.grid(row=3, column=0, pady=20)
        save_button = Button(self.edit_screen, text="Save", bg=background_color,
                             fg=sub_font_color, width=20, border=3, command=save_edit)
        save_button.grid(row=4, column=0, columnspan=2, pady=20)
        discard_button = Button(self.edit_screen, text="Discard", bg=background_color,
                                fg=sub_font_color, width=20, border=3, command=discard_edit)
        discard_button.grid(row=5, column=0, columnspan=2, pady=5)
        self.first_name_entry.insert(0, self.name)
        self.last_name_entry.insert(0, self.last_name)
        self.phone_number_entry.insert(0, self.phone_number)
        self.email_entry.insert(0, self.email)

        self.edit_screen.mainloop()


number_design = Label(second_frame, text="Id", font=font.replace(
    "18", "12"), bg=background_color, fg=font_color)
number_design.grid(row=design_row, column=0, pady=15, padx=4)
first_name_design = Label(second_frame, text="Name", font=font,
                          bg=background_color, fg=font_color)
first_name_design.grid(row=design_row, column=1, padx=8)
last_name_design = Label(second_frame, text="Last Name", font=font,
                         bg=background_color, fg=font_color)
last_name_design.grid(row=design_row, column=2, padx=8)
phone_number_design = Label(
    second_frame, text="phone number", font=font, bg=background_color, fg=font_color)
phone_number_design.grid(row=design_row, column=3, padx=8)
email_number_design = Label(
    second_frame, text="Email", font=font, bg=background_color, fg=font_color)
email_number_design.grid(row=design_row, column=4, padx=8)

all_contacts = []


def show_contacts(bind_var=None):
    global all_contacts
    global cont
    if len(all_contacts) != 0:
        for contact in all_contacts:
            contact.grid_f()
    all_contacts = []
    conn = sqlite3.connect("contacts_book.db")
    cursor = conn.cursor()
    cursor.execute("SELECT *,oid FROM contacts")
    contacts = cursor.fetchall()
    sub_row = design_row + 1
    for contact in contacts:
        cont = User(contact[0], contact[1], contact[2],
                    contact[3], contact[4], sub_row)
        sub_row += 1
        all_contacts.append(cont)
    print(len(all_contacts))
    conn.commit()
    conn.close()


def add():
    add_window = Toplevel()
    add_window.title("contacts")
    add_window.iconbitmap("main_icon.ico")
    add_window.geometry("400x400")
    add_window.configure(bg=background_color)

    def save():
        if (first_name_entry.get() != "" and last_name_entry.get() != "" and phone_number_entry.get() != "" and email_entry.get() != ""):
            try:
                int(phone_number_entry.get())
            except:
                messagebox.showerror("please enter a valid phone number")
            else:
                if len(phone_number_entry.get()) == 11:
                    email = email_entry.get()
                    email_2 = email.split(".")
                    if "@" in email and len(email.split(".")) == 2 and email_2[1] != "":
                        conn = sqlite3.connect("contacts_book.db")
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO contacts VALUES(:first_name, :last_name, :phone_number, :email)",
                                       {
                                           'first_name': first_name_entry.get(),
                                           'last_name': last_name_entry.get(),
                                           'phone_number': phone_number_entry.get(),
                                           'email': email_entry.get()
                                       })
                        first_name_entry.delete(0, END)
                        last_name_entry.delete(0, END)
                        phone_number_entry.delete(0, END)
                        email_entry.delete(0, END)

                        conn.commit()
                        conn.close()
                        show_contacts()
                    else:
                        messagebox.showwarning(
                            "invalid email!", "please enter a valid email.")
                else:
                    messagebox.showwarning(
                        "please enter a valid phone number", "phone number must have 11 characters!")
        else:
            messagebox.showerror("please check your entries!",
                                 "please check if everithing is all right then press add")

    def discard():
        add_window.destroy()
        show_contacts()

    first_name_entry = Entry(add_window, font="arial 12 normal", width=25)
    first_name_entry.grid(row=0, column=1, padx=20)
    last_name_entry = Entry(add_window, font="arial 12 normal", width=25)
    last_name_entry.grid(row=1, column=1)
    phone_number_entry = Entry(add_window, font="arial 12 normal", width=25)
    phone_number_entry.grid(row=2, column=1)
    email_entry = Entry(add_window, font="arial 12 normal", width=25)
    email_entry.grid(row=3, column=1)
    first_name_label = Label(add_window, bg=background_color,
                             fg=sub_font_color, text="Fisrt name:", font="arial 12 bold")
    first_name_label.grid(row=0, column=0, pady=20)
    last_name_label = Label(add_window, bg=background_color,
                            fg=sub_font_color, text="Last name:", font="arial 12 bold")
    last_name_label.grid(row=1, column=0, pady=20)
    phone_number_label = Label(add_window, bg=background_color,
                               fg=sub_font_color, text="Phone number: ", font="arial 12 bold")
    phone_number_label.grid(row=2, column=0, pady=20)
    email_label = Label(add_window, bg=background_color,
                        fg=sub_font_color, text="Email:", font="arial 12 bold")
    email_label.grid(row=3, column=0, pady=20)
    save_button = Button(add_window, text="Save", bg=background_color,
                         fg=sub_font_color, width=20, border=3, command=save)
    save_button.grid(row=4, column=0, columnspan=2, pady=20)
    discard_button = Button(add_window, text="Discard", bg=background_color,
                            fg=sub_font_color, width=20, border=3, command=discard)
    discard_button.grid(row=5, column=0, columnspan=2, pady=5)


main_menu = Menu()
root.configure(menu=main_menu)
options_menu = Menu()
options_menu.add_command(label="New contact", command=add)

options_menu.add_separator()
options_menu.add_command(label="Exit", command=root.quit)
main_menu.add_cascade(label="options", menu=options_menu)

show_contacts()

root.mainloop()
