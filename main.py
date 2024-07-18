import customtkinter as ctk
import pandas as pd
import os
from PIL import Image, ImageTk
from password_generator import generate


class PasswordManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager App")
        # Disable window resizing
        self.resizable(False, False)

        lock_image = Image.open("locked.png")
        # Resizing the image
        lock_image = lock_image.resize((200, 200), Image.LANCZOS)
        self.lock_img = ImageTk.PhotoImage(lock_image)

        copy_image = Image.open("copy.png")
        # Resizing the image
        self.copy_img = ctk.CTkImage(copy_image, size=(20, 20))

        # Frame for canvas
        self.canvas_frame = ctk.CTkFrame(self, fg_color="#242424")
        self.canvas_frame.grid(row=0, column=0, padx=50, pady=0, sticky="nsew")

        # create canvas and add image to it
        self.canvas = ctk.CTkCanvas(self.canvas_frame, width=200, height=200,
                                    bg="#242424", highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=120, pady=20)
        self.canvas.create_image(0, 0, image=self.lock_img, anchor="nw")

        # Frame for Labels and Entry boxes
        self.text_frame = ctk.CTkFrame(self, fg_color="#242424")
        self.text_frame.grid(row=1, column=0, padx=50, pady=0, sticky="nsew")

        # Website label and entry box
        self.website_label = ctk.CTkLabel(self.text_frame, text="Website", font=(
            "Arial", 15), bg_color="transparent")
        self.website_label.grid(row=1, column=0, padx=20, pady=5)

        self.website_entry = ctk.CTkEntry(self.text_frame, width=250,
                                          placeholder_text="Enter Website")
        # self.website_entry.bind("<Button-1>",
        #                       command=lambda event: self.enable_entry(event, self.website_entry))
        self.website_entry.grid(row=1, column=1, padx=20, pady=5)

        # Email label and entry box
        self.email_label = ctk.CTkLabel(self.text_frame, text="Email/Username", font=(
            "Arial", 15), bg_color="transparent")
        self.email_label.grid(row=2, column=0, padx=20, pady=5)

        self.email_entry = ctk.CTkEntry(self.text_frame, width=250,
                                        placeholder_text="Enter Email/Username")
        # self.email_entry.bind("<Button-1>",
        #                          command=lambda event: self.enable_entry(event, self.email_entry))
        self.email_entry.grid(row=2, column=1, padx=20, pady=5)

        # password label and entry box
        self.password_label = ctk.CTkLabel(self.text_frame, text="Password", font=(
            "Arial", 15), bg_color="transparent")
        self.password_label.grid(row=3, column=0, padx=20, pady=5)

        self.password_entry = ctk.CTkEntry(self.text_frame, width=205,
                                           placeholder_text="Enter Password or Click Generate")
        # self.password_entry.bind("<Button-1>",
        #                          command=lambda event: self.enable_entry(event, self.password_entry))
        self.password_entry.grid(row=3, column=1, padx=20, pady=5, sticky="w")

        # copy password to clipboard button
        self.copy_password_button = ctk.CTkButton(self.text_frame, text="", image=self.copy_img,
                                                  width=30, command=self.copy_password)
        self.copy_password_button.grid(
            row=3, column=1, padx=20, pady=5, sticky="e")

        # Frame for buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="#242424")
        self.button_frame.grid(row=2, column=0, padx=100,
                               pady=20, sticky="nsew")
        self.button_frame.columnconfigure(0, weight=1)

        # Add Password button
        self.add_password_button = ctk.CTkButton(self.button_frame, text="Add Password",
                                                 command=self.add_password)
        self.add_password_button.grid(row=0, column=1, padx=20, pady=10)

        # Generate Password button
        self.generate_password_button = ctk.CTkButton(self.button_frame, text="Generate Password",
                                                      command=self.generate_password)
        self.generate_password_button.grid(row=0, column=2, padx=20, pady=10)

        # error label
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(
            row=3, column=0, columnspan=2, pady=5, sticky='ew')

    def add_password(self):
        website, email_username, password = self.website_entry.get(
        ), self.email_entry.get(), self.password_entry.get()
        if "" in (website, email_username, password):
            self.error_label.configure(text="No field should be empty")
        elif not self.open_popup(website, email_username, password):
            pass
        else:
            df = pd.read_csv("data.csv")
            new_data = {
                "WEBSITES": [self.website_entry.get()],
                "EMAIL/USERNAME": [self.email_entry.get()],
                "PASSWORD": [self.password_entry.get()]
            }
            new_data = pd.DataFrame(new_data)
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv('data.csv', index=False)
            self.clear_entryboxes()

    def clear_entryboxes(self):
        self.website_entry.delete(0, ctk.END)
        self.email_entry.delete(0, ctk.END)
        self.password_entry.delete(0, ctk.END)

    def open_popup(self, website, email_username, password):
        result = None  # To store the result from the popup

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
        popup.geometry("350x150")
        # Make the popup window always on top
        popup.attributes("-topmost", True)
        popup.resizable(False, False)

        message = f"WEBSITE: {website}\nEMAIL/USERNAME: {email_username}\nPASSWORD: {password}\nDo you want to proceed?"
        label = ctk.CTkLabel(popup, text=message, wraplength=350, justify="left", font=(
            "Arial", 15))
        label.pack(pady=10)

        button_frame = ctk.CTkFrame(popup, fg_color="#242424")
        button_frame.pack(pady=10)

        yes_button = ctk.CTkButton(button_frame, text="Yes", command=on_yes)
        yes_button.grid(row=0, column=0, padx=10, pady=5)

        no_button = ctk.CTkButton(button_frame, text="No", command=on_no, fg_color="white",
                                  hover_color="#ccc", text_color="black")
        no_button.grid(row=0, column=1, padx=10, pady=5)

        popup.wait_window()  # Wait until the popup window is closed

        return result

    def generate_password(self):
        self.password = generate()
        self.password_entry.delete(0, ctk.END)
        self.password_entry.insert(0, self.password)

    def copy_password(self):
        try:
            # Clear the clipboard
            self.clipboard_clear()
            # Append the text to the clipboard
            self.clipboard_append(self.password)
        except AttributeError:
            self.error_label.configure(text="Password field is empty")


if __name__ == "__main__":
    pss = PasswordManager()
    pss.mainloop()
