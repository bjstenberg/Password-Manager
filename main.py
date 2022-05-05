from tkinter import *
from tkinter import messagebox
import secrets
import pyperclip
import json


# ---------------------------- WEBSITE SEARCH ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        elif website not in data:
            messagebox.showwarning(title="Error", message=f"No Data Saved for {website}")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#password = ""


def password():
    global password
    password_length = 13
    password = (secrets.token_urlsafe(password_length))
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
# TODO Create a function called save()
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {
        "email": email,
        "password": password,
    }}

    if len(password) == 0 or len(website) == 0:
        messagebox.showwarning(title="Warning", message="Please don't leave any fields empty!")
    else:
        # Create a messagebox
        # is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} \n"
        # f"Password: {password}\nIs this OK to be saved?")
        # if is_ok:
        # TODO 2. Write to the data inside the entries toa a data.txt file when the Add button is clicked.
        try:
            with open("data.json", "r") as data:
                # TODO 3. Each website, email and password combination should be on a new line inside the file
                # data.write(f"{website} | {email} | {password}\n")

                # Json.dump() - how to write (dump) to a json file in "w" - stores information into a dict
                # json.dump(new_data, data, indent=4)

                # json.load() - how to read (load) from a json file, change "w" to "r"
                #                               - retrieves information from a type dict
                # data_file = json.load(data)
                # print(data_file)

                # json.update() - "w", update existing data with new data.
                # Reading old data
                data_file = json.load(data)
                if website in data_file:
                    update = messagebox.askyesno(title="Warning!", message=f"There is already a password saved for"
                                                                           f" {website}\nWould you like to overwrite?")
                    if update:
                        pass
                    else:
                        return
                data_file.update(new_data)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open("data.json", "w") as data:
                json.dump(new_data, data, indent=4)
        else:
            # Updating old data with new data
            data_file.update(new_data)

            with open("data.json", "w") as data:
                # Saving the updated data
                json.dump(data_file, data, indent=4)
        finally:
            # TODO 4. All files need to be cleared after add button is pressed
            # Deletes from first character to the end of the string
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Generator")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
pw_logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=pw_logo)
canvas.grid(column=1, row=0)

# Generate the Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Generate Entries
website_entry = Entry(width=21)
website_entry.grid(column=1, row=1, sticky="EW")
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
email_entry.insert(END, "bjorn.p.stenberg@gmail.com")

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3, sticky="EW")

# Generate buttons
generate_pw_button = Button(text="Generate Password", command=password)
generate_pw_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(row=1, column=2)

window.mainloop()
