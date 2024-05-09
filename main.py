from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_pass():
    password_list = ([choice(letters) for _ in range(randint(8, 10))]
                     + [choice(symbols) for _ in range(randint(2, 4))]
                     + [choice(numbers) for _ in range(randint(2, 4))])

    shuffle(password_list)
    pw = "".join(password_list)

    password_input.delete(0, END)
    password_input.insert(0, pw)
    pyperclip.copy(pw)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def field_refresh():
    website_input.delete(0, END)
    password_input.delete(0, END)
    username_input.delete(0, END)
    username_input.insert(0, "placeholder@gmail.com")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    web_in = website_input.get()
    user_in = username_input.get()
    pass_in = password_input.get()
    new_data = {
        web_in: {
            "email": user_in,
            "password": pass_in
        }
    }

    if len(web_in) == 0 or len(user_in) == 0 or len(pass_in) == 0:
        messagebox.showinfo(title="Error", message="Please do not leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            field_refresh()


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def find_pass():
    web_in = website_input.get()

    if len(web_in) == 0:
        messagebox.showinfo(title="Error", message="Please enter website to retrieve password.")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No Data File Found")
        else:
            if web_in in data:
                messagebox.showinfo(title="Login Details", message=f"Website: {web_in}\n"
                                                                   f"Username: {data[web_in]['email']}\n"
                                                                   f"Password: {data[web_in]['password']}\n\n"
                                                                   f"(Password saved to clipboard)")
                pyperclip.copy(data[web_in]['password'])
            else:
                messagebox.showinfo(title="Error", message=f"No details for {web_in} exist.")
        finally:
            field_refresh()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title = "Password Manager"
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
lock = PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=lock)
canvas.grid(column=1, row=0)

# Labels
website = Label(text="Website:")
website.grid(column=0, row=1)

username = Label(text="Email/Username:")
username.grid(column=0, row=2)

password = Label(text="Password:")
password.grid(column=0, row=3)

# Inputs
website_input = Entry(width=18)
website_input.grid(column=1, row=1)
website_input.focus()

username_input = Entry(width=31)
username_input.grid(column=1, row=2, columnspan=2)
username_input.insert(index=0, string="aaron@gmail.com")

password_input = Entry(width=18)
password_input.grid(column=1, row=3)

# Buttons
search_button = Button(width=9, text="Search", command=find_pass)
search_button.grid(column=2, row=1)

gen_pass_button = Button(width=9, text="Generate", command=generate_pass)
gen_pass_button.grid(column=2, row=3)

add_button = Button(width=28, text="Add", command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
