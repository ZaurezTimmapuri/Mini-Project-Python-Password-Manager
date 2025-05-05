import random
from tkinter import *
from tkinter import messagebox
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
    number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbol = ['!', '@', '#', '$', '%', '&', '*', ')', '(', '+', '-']

    password_generated = ''

    letters_1 = [random.choice(alphabets) for _ in range(random.randint(8, 10))]
    letters_2 = [random.choice(number) for _ in range(random.randint(2, 4))]
    letters_3 = [random.choice(symbol) for _ in range(random.randint(2, 4))]
    complete = letters_1 + letters_2 + letters_3

    for _ in range(len(complete)):
        password_generated += random.choice(complete)
    Entry.config(password, password.delete(0, END))
    Entry.config(password, password.insert(0, password_generated))
    pyperclip.copy(password_generated)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def write():
    website_name = website.get().title()
    password_output = password.get()
    email_name = email.get()

    new_data = {
        website_name:
            {
                "email": email_name,
                "password": password_output
            }
    }

    if website_name == '' or password_output == '' or email_name == '':
        messagebox.showwarning(title='Empty input', message='Please fill all required details')
    else:
        is_ok = messagebox.askokcancel(title='User confirmation\n',
                                       message=f'Website = {website_name}\n Password = {password_output}'
                                               f'\n Email = {email_name}'
                                               f'\n Are the entered details to be saved?')
        if is_ok:
            try:
                file = open('data.json', 'r')
            except FileNotFoundError:
                # file.write(f"{website_name} | {email_name} | {password_output} \n")   how we normally do
                with open('data.json', 'w') as file:
                    json.dump(new_data, file, indent=4)
            else:
                data = json.load(file)
                new_data.update(data)
                with open('data.json', 'w') as file:
                    json.dump(new_data, file, indent=4)
            finally:
                file.close()
                Entry.config(password, password.delete(0, END))
                Entry.config(website, website.delete(0, END))


# ---------------------------- LOOK PASSWORD ------------------------------- #

def look():
    try:
        with open('data.json') as file:
            data_dict = json.load(file)
            website_search = website.get().title()
    except FileNotFoundError:
        messagebox.showwarning(title="No file", message="No Data file found!")
    else:
        if website_search in data_dict:
            email_searched = data_dict[website_search]["email"]
            password_searched = data_dict[website_search]["password"]
            messagebox.askokcancel(title="Password and email asked!",
                                   message=f"Email = {email_searched}\n"
                                           f"Password = {password_searched}\n")
            pyperclip.copy(password_searched)
        else:
            messagebox.showwarning(title="No entry",
                                   message=f"No details of the {website_search} exists!")
    finally:
        Entry.config(website, website.delete(0, END))


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password manager")
window.config(padx=70, pady=70)

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file='logo.png')
image = canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

website_label = Label(text='Website:    ', font=('Courier', 14, 'bold'))
website_label.grid(row=1, column=0)

website = Entry(width=33)
website.focus()
website.grid(row=1, column=1)

search_button = Button(width=8, text='search', font=('Courier', 10, 'bold'), command=look)
search_button.grid(row=1, column=2)

email_label = Label(text='Email/Username:   ', font=('Courier', 14, 'bold'))
email_label.grid(row=2, column=0)

email = Entry(width=47)
email.insert(0, 'zaurezsakheebbode@gmail.com')
email.grid(row=2, column=1, columnspan=2)

password_label = Label(text='Password:   ', font=('Courier', 14, 'bold'))
password_label.grid(row=3, column=0)

password = Entry(width=33)
password.grid(row=3, column=1)

password_button = Button(width=8, text='Generate', font=('Courier', 10, 'bold'), command=generate)
password_button.grid(row=3, column=2)

submit_button = Button(width=35, text='Apply', font=('Courier', 10, 'bold'), command=write)
submit_button.grid(row=4, column=1, columnspan=2, rowspan=2)

window.mainloop()
