from tkinter import *
from tkinter import messagebox
import random
import string
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    length = 16  # Total password length

    letters = string.ascii_letters
    digits = string.digits
    special_chars = '@#$%&*!'

    # Ensure at least one character from each category
    word = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(digits),
        random.choice(special_chars)
    ]

    all_chars = letters + digits + special_chars
    word += random.choices(all_chars, k=length - 4)
    random.shuffle(word)

    return ''.join(word)

def fill_password():
    pw = generate_password()
    final.delete(0, END)
    final.insert(0, pw)
    pyperclip.copy(pw)


# ---------------------------- SAVE AND FIND PASSWORD ------------------------------- #
def find_password():
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
        web = url.get()
        if web in data:
            messagebox.showinfo(title="Your Credentials", message=f"{web}:\nEmail: {data[web]["email"]}\nPassword: {data[web]["password"]}")
        else:
            messagebox.showinfo(title="Oopsie", message=f"Oops! no match found for {web}")

    except FileNotFoundError:
        messagebox.showinfo(title="Oopsie", message=f"No data file found")


def save():

    website = url.get()
    email = mail.get()
    passw = final.get()

    new_data = {
        website: {
            "email": email,
            "password": passw
        }
    }

    if len(website) == 0 or len(email) == 0 or website == "Enter website":
        messagebox.showinfo(title="Oops!", message="Please don't leave any fields empty!")
        return

    is_ok = messagebox.askokcancel(
        title=website,
        message=f"These are the details entered:\nEmail: {email}\nPassword: {passw}\n\nSave it?"
    )

    if is_ok:
        # Save to text file
        with open("data.txt", mode="a") as file:
            file.write(f"{website} | {email} | {passw}\n")

        # Save to JSON file
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except (FileNotFoundError, json.JSONDecodeError):
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            url.delete(0, END)
            final.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("PASSWORD MANAGER")
#window.config(height=240,width = 240)
window.config(padx=50,pady=50)

canvas = Canvas(width=200, height=200)
lock = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock)
canvas.image = lock
canvas.grid(column=1,row=0)

web = Label(text = "Website:",font=("Courier",10,"bold"))
web.grid(column=0,row=1,sticky="e")

name = Label(text = "Email/Username:",font=("Courier",10,"bold"))
name.grid(column=0,row=2,sticky="e")

password = Label(text = "Password:",font=("Courier",10,"bold"))
password.grid(column=0,row=3,sticky="e")

# url = Entry(width=35)
# url.grid(column =1,row=1)
# url.focus()

mail = Entry(width=35)
mail.grid(column =1,row=2,columnspan=2,sticky="ew")
mail.insert(END,"verze@gmail.com")

final = Entry(width=21)
final.grid(column =1,row=3,sticky="ew")

generate = Button(text="Generate Password",highlightthickness=0,command=fill_password)
generate.grid(column=2,row=3)

add = Button(text="Add",highlightthickness=0,width=36,command=save)
add.grid(column=1,row=4,columnspan=2,sticky="ew")

search = Button(text="Search",width=15,highlightthickness=0,command=find_password)
search.grid(column=2,row=1)


placeholder_url = "Enter website"
def on_url_click(event):
    if url.get() == placeholder_url:
        url.delete(0, END)
        url.config(fg='black')

def on_url_focusout(event):
    if url.get() == "":
        url.insert(0, placeholder_url)
        url.config(fg='grey')

url = Entry(width=35, fg='grey')
url.insert(0, placeholder_url)
url.bind("<FocusIn>", on_url_click)
url.bind("<FocusOut>", on_url_focusout)
url.grid(column=1, row=1)


window.mainloop()

