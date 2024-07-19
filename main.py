import customtkinter as ctk
import os
import json
from PIL import Image, ImageTk
from password_generator import generate

class PasswordManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager App")
        self.resizable(False, False)

        self.lock_img = ImageTk.PhotoImage(Image.open("./ui_elements/locked.png").resize((200, 200), Image.LANCZOS))
        self.copy_img = ctk.CTkImage(Image.open("./ui_elements/copy.png"), size=(20, 20))
        self.search_img = ctk.CTkImage(Image.open("./ui_elements/search.png"), size=(20, 20))

        self.create_widgets()
        self.check_json_exists()

    def create_widgets(self):
        self.canvas_frame = ctk.CTkFrame(self, fg_color="#242424")
        self.canvas_frame.grid(row=0, column=0, padx=50, pady=0, sticky="nsew")

        self.canvas = ctk.CTkCanvas(self.canvas_frame, width=200, height=200, bg="#242424", highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=120, pady=20)
        self.canvas.create_image(0, 0, image=self.lock_img, anchor="nw")

        self.text_frame = ctk.CTkFrame(self, fg_color="#242424")
        self.text_frame.grid(row=1, column=0, padx=50, pady=0, sticky="nsew")

        self.website_label = ctk.CTkLabel(self.text_frame, text="Website", font=("Arial", 15), bg_color="transparent")
        self.website_label.grid(row=1, column=0, padx=20, pady=5)
        self.website_entry = ctk.CTkEntry(self.text_frame, width=205, placeholder_text="Enter Website")
        self.website_entry.grid(row=1, column=1, padx=20, pady=5, sticky="w")

        self.search_button = ctk.CTkButton(self.text_frame, text="", image=self.search_img, width=30,
                                           command=self.search_data)
        self.search_button.grid(row=1, column=1, padx=20, pady=5, sticky="e")

        self.email_label = ctk.CTkLabel(self.text_frame, text="Email/Username", font=("Arial", 15), bg_color="transparent")
        self.email_label.grid(row=2, column=0, padx=20, pady=5)
        self.email_entry = ctk.CTkEntry(self.text_frame, width=250, placeholder_text="Enter Email/Username")
        self.email_entry.grid(row=2, column=1, padx=20, pady=5)

        self.password_label = ctk.CTkLabel(self.text_frame, text="Password", font=("Arial", 15), bg_color="transparent")
        self.password_label.grid(row=3, column=0, padx=20, pady=5)
        self.password_entry = ctk.CTkEntry(self.text_frame, width=205, placeholder_text="Enter Password or Click Generate")
        self.password_entry.grid(row=3, column=1, padx=20, pady=5, sticky="w")

        self.copy_password_button = ctk.CTkButton(self.text_frame, text="", image=self.copy_img, width=30,
                                                  command=lambda: self.copy_text(self.password_entry.get()))
        self.copy_password_button.grid(row=3, column=1, padx=20, pady=5, sticky="e")

        self.button_frame = ctk.CTkFrame(self, fg_color="#242424")
        self.button_frame.grid(row=2, column=0, padx=100, pady=20, sticky="nsew")
        self.button_frame.columnconfigure(0, weight=1)

        self.add_password_button = ctk.CTkButton(self.button_frame, text="Add Password", command=self.add_password)
        self.add_password_button.grid(row=0, column=1, padx=20, pady=10)

        self.generate_password_button = ctk.CTkButton(self.button_frame, text="Generate Password", command=self.generate_password)
        self.generate_password_button.grid(row=0, column=2, padx=20, pady=10)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=3, column=0, columnspan=2, pady=5, sticky='ew')

    def check_json_exists(self):
        if not os.path.exists("data.json"):
            with open("data.json", "w") as f:
                json.dump({}, f)

    def search_data(self):
        with open("data.json", "r") as f:
            data = json.load(f)
        website = self.website_entry.get().lower()
        if website == "":
            self.error_label.configure(text="Website field should not be empty")
        elif website not in data:
            self.error_label.configure(text="Website does not exist")
        else:
            self.search_popup(website, data)

    def search_popup(self, website, data):
        search_popup = ctk.CTkToplevel()
        search_popup.title("data")
        search_popup.attributes("-topmost", True)
        search_popup.resizable(False, False)

        message = f"EMAIL/USERNAME: {data[website]['email/username']}\nPASSWORD: {data[website]['password']}"
        label = ctk.CTkLabel(search_popup, text=message, wraplength=350, justify="left", font=("Arial", 12))
        label.pack(pady=10, padx=10)

        button_frame = ctk.CTkFrame(search_popup, fg_color="#242424")
        button_frame.pack(pady=10)

        copy_pass_button = ctk.CTkButton(button_frame, text="Copy Password", image=self.copy_img, command=lambda: self.copy_text(data[website]['password']))
        copy_pass_button.grid(row=0, column=0, padx=10, pady=5)

        copy_email_button = ctk.CTkButton(button_frame, text="Copy Email", image=self.copy_img, command=lambda: self.copy_text(data[website]['email/username']))
        copy_email_button.grid(row=0, column=1, padx=10, pady=5)

        search_popup.wait_window()

    def add_password(self):
        website, email_username, password = (self.website_entry.get().lower(),
                                             self.email_entry.get().lower(),
                                             self.password_entry.get())
        if "" in (website, email_username, password):
            self.error_label.configure(text="No field should be empty")
        elif not self.confirmation_popup(website, email_username, password):
            pass
        else:
            with open("data.json", "r") as f:
                data = json.load(f)

            new_data = {
                "email/username": email_username,
                "password": password
            }
            data[website] = new_data

            with open("data.json", "w") as f:
                json.dump(data, f, indent=4)

            self.clear_entryboxes()

    def clear_entryboxes(self):
        self.website_entry.delete(0, ctk.END)
        self.email_entry.delete(0, ctk.END)
        self.password_entry.delete(0, ctk.END)

    def confirmation_popup(self, website, email_username, password):
        result = None

        def on_yes():
            nonlocal result
            result = True
            popup.destroy()

        def on_no():
            nonlocal result
            result = False
            popup.destroy()

        popup = ctk.CTkToplevel()
        popup.title("Confirmation")
        popup.attributes("-topmost", True)
        popup.resizable(False, False)

        message = f"WEBSITE: {website}\nEMAIL/USERNAME: {email_username}\nPASSWORD: {password}\nDo you want to proceed?"
        label = ctk.CTkLabel(popup, text=message, wraplength=350, justify="left", font=("Arial", 12))
        label.pack(pady=10, padx=10)

        button_frame = ctk.CTkFrame(popup, fg_color="#242424")
        button_frame.pack(pady=10)

        yes_button = ctk.CTkButton(button_frame, text="Yes", command=on_yes)
        yes_button.grid(row=0, column=0, padx=10, pady=5)

        no_button = ctk.CTkButton(button_frame, text="No", command=on_no, fg_color="white", hover_color="#ccc", text_color="black")
        no_button.grid(row=0, column=1, padx=10, pady=5)

        popup.wait_window()

        return result

    def generate_password(self):
        self.password = generate()
        self.password_entry.delete(0, ctk.END)
        self.password_entry.insert(0, self.password)

    def copy_text(self, copy):
        try:
            self.clipboard_clear()
            self.clipboard_append(copy)
        except Exception as e:
            self.error_label.configure(text=f"Error copying password: {str(e)}")

if __name__ == "__main__":
    pss = PasswordManager()
    pss.mainloop()
