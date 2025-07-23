import customtkinter
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox  # Use the standard messagebox for modal feedback
import functions as module

# --- Add Entry ---
class AddEntry(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)        
        self.geometry("400x400")
        self.title("Add entry")

        self.my_frame = customtkinter.CTkFrame(master=self)
        self.my_frame.pack(pady=20, padx=60, fill="both", expand=True)

        customtkinter.CTkLabel(master=self.my_frame, text="Username").pack(pady=(10, 0), padx=5, anchor="w")
        self.username_entry = customtkinter.CTkEntry(master=self.my_frame, width=150)
        self.username_entry.pack(pady=(5, 2), padx=5, fill="x")

        customtkinter.CTkLabel(master=self.my_frame, text="Password").pack(pady=(10, 0), padx=5, anchor="w")
        self.password_entry = customtkinter.CTkEntry(master=self.my_frame, width=150, show="*")
        self.password_entry.pack(pady=(4, 5), padx=5, fill="x")

        customtkinter.CTkLabel(master=self.my_frame, text="Website").pack(pady=(10, 0), padx=5, anchor="w")
        self.website_entry = customtkinter.CTkEntry(master=self.my_frame, width=150)
        self.website_entry.pack(pady=(4, 5), padx=5, fill="x")

        customtkinter.CTkButton(master=self.my_frame, text="Submit", command=self.get_inputs).pack(pady=10, padx=5)

        self.grab_set()
        self.focus()

    def get_inputs(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        website = self.website_entry.get().strip()
        add_entry = module.add_entry(website=website, username=username, password=password)
        if add_entry:
            messagebox.showinfo("Success", "Successfully added!")

# --- Delete Entry ---
class DeleteEntry(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)        
        self.geometry("400x250")
        self.title("Delete entry")

        self.my_frame = customtkinter.CTkFrame(master=self)
        self.my_frame.pack(pady=20, padx=60, fill="both", expand=True)

        customtkinter.CTkLabel(master=self.my_frame, text="Username").pack(pady=(10, 0), padx=5, anchor="w")
        self.username_entry = customtkinter.CTkEntry(master=self.my_frame, width=150)
        self.username_entry.pack(pady=(5, 2), padx=5, fill="x")

        customtkinter.CTkLabel(master=self.my_frame, text="Password").pack(pady=(10, 0), padx=5, anchor="w")
        self.password_entry = customtkinter.CTkEntry(master=self.my_frame, width=150, show="*")
        self.password_entry.pack(pady=(4, 5), padx=5, fill="x")

        customtkinter.CTkButton(master=self.my_frame, text="Submit", command=self.get_inputs).pack(pady=10, padx=5)
        self.grab_set()
        self.focus()

    def get_inputs(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        delete_entry = module.delete_entry(username, password)
        if not delete_entry:
            messagebox.showinfo("Info", str(delete_entry))
        else:
            messagebox.showinfo("Success", "Successfully deleted!")

# --- View Entry ---
class ViewEntry(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("600x250")
        self.title("View entry")

        results = module.view_entry()  # Your data source

        self.my_frame = customtkinter.CTkFrame(master=self)
        self.my_frame.pack(pady=20, padx=20, fill="both", expand=True)
        table_frame = tk.Frame(self.my_frame)
        table_frame.pack(fill="both", expand=True)

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview",
            background="#2a2d2e", foreground="white", rowheight=25,
            fieldbackground="#343638", bordercolor="#343638", borderwidth=0)
        self.style.map('Treeview', background=[('selected', '#22559b')])
        self.style.configure("Treeview.Heading",
            background="#565b5e", foreground="white", relief="flat")
        self.style.map("Treeview.Heading", background=[('active', '#3484F0')])

        columns = ("username", "password", "website")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        self.table.heading("username", text="Username")
        self.table.heading("password", text="Password")
        self.table.heading("website", text="Website")
        self.table.column("username", width=100, anchor=tk.CENTER)
        self.table.column("password", width=100, anchor=tk.CENTER)
        self.table.column("website", width=120, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for credentials in results:
            self.username = credentials.get("credentials", {}).get("username", "")
            self.password = credentials.get("credentials", {}).get("password", "")  # actual password
            self.website = credentials.get("website", "")
            self.table.insert("", tk.END, values=(self.username, "***", self.website))

        self.table.bind("<<TreeviewSelect>>", self.on_row_selected)
        self.grab_set()
        self.focus()

    def on_row_selected(self, event):
        selected_items = self.table.selection()
        if not selected_items:
            return
        item_id = selected_items[0]
        values = self.table.item(item_id, "values")
        username, masked_password, website = values
        # Assuming you can get the real password via module
        
        messagebox.showinfo("Info", f"Website: {website}\nUsername: {username}\nPassword: {module.decrypt(self.password)}")

# --- Update Entry ---
class UpdateEntry(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("600x250")
        self.title("Update entry")

        self.original_results = module.view_entry()

        self.my_frame = customtkinter.CTkFrame(master=self)
        self.my_frame.pack(pady=20, padx=20, fill="both", expand=True)
        table_frame = tk.Frame(self.my_frame)
        table_frame.pack(fill="both", expand=True)

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview",
            background="#2a2d2e", foreground="white", rowheight=25,
            fieldbackground="#343638", bordercolor="#343638", borderwidth=0)
        self.style.map('Treeview', background=[('selected', '#22559b')])
        self.style.configure("Treeview.Heading",
            background="#565b5e", foreground="white", relief="flat")
        self.style.map("Treeview.Heading", background=[('active', '#3484F0')])

        columns = ("username", "password", "website")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        self.table.heading("username", text="Username")
        self.table.heading("password", text="Password")
        self.table.heading("website", text="Website")
        self.table.column("username", width=100, anchor=tk.CENTER)
        self.table.column("password", width=100, anchor=tk.CENTER)
        self.table.column("website", width=120, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for i, credentials_data in enumerate(self.original_results):
            username_display = credentials_data.get("credentials", {}).get("username", "")
            website_display = credentials_data.get("website", "")
            self.table.insert("", tk.END, values=(username_display, "***", website_display), iid=str(i))

        self.table.bind("<<TreeviewSelect>>", self.on_row_selected)
        self.grab_set()
        self.focus()

    def on_row_selected(self, event):
        selected_items = self.table.selection()
        if not selected_items:
            return
        item_iid = selected_items[0]
        try:
            original_index = int(item_iid)
            original_data = self.original_results[original_index]
        except (ValueError, IndexError):
            return
        original_username = original_data.get("credentials", {}).get("username", "")
        original_password = original_data.get("credentials", {}).get("password", "")
        original_website = original_data.get("website", "")
        self.open_update_dialog(original_username, original_password, original_website)

    def open_update_dialog(self, original_username, original_password, original_website):
        update_dialog = customtkinter.CTkToplevel(self)
        self.center_window(update_dialog, 400, 350)
        update_dialog.title("Edit Entry")
        update_dialog.transient(self)
        update_dialog.grab_set()
        update_dialog.focus_set()

        dialog_frame = customtkinter.CTkFrame(master=update_dialog)
        dialog_frame.pack(pady=20, padx=20, fill="both", expand=True)

        customtkinter.CTkLabel(master=dialog_frame, text="Username").pack(pady=(10, 0), padx=5, anchor="w")
        username_entry = customtkinter.CTkEntry(master=dialog_frame, width=300)
        username_entry.insert(0, original_username)
        username_entry.pack(pady=(5, 2), padx=5, fill="x")

        customtkinter.CTkLabel(master=dialog_frame, text="Password").pack(pady=(10, 0), padx=5, anchor="w")
        password_entry = customtkinter.CTkEntry(master=dialog_frame, width=300, show="*")
        password_entry.insert(0, original_password)
        password_entry.pack(pady=(4, 5), padx=5, fill="x")

        customtkinter.CTkLabel(master=dialog_frame, text="Website").pack(pady=(10, 0), padx=5, anchor="w")
        website_entry = customtkinter.CTkEntry(master=dialog_frame, width=300)
        website_entry.insert(0, original_website)
        website_entry.pack(pady=(4, 5), padx=5, fill="x")

        button_frame = customtkinter.CTkFrame(master=dialog_frame, fg_color="transparent")
        button_frame.pack(pady=10, padx=5)

        update_button = customtkinter.CTkButton(
            master=button_frame,
            text="Update",
            command=lambda: self.perform_update(
                original_website, original_username,
                username_entry.get(), password_entry.get(), website_entry.get(),
                update_dialog
            )
        )
        update_button.pack(side="left", padx=5)
        cancel_button = customtkinter.CTkButton(master=button_frame, text="Cancel", command=update_dialog.destroy)
        cancel_button.pack(side="right", padx=5)

    def perform_update(self, original_website, original_username, new_username, new_password, new_website, dialog_to_close):
        success = module.update_entry(original_website, original_username, new_username, new_password, new_website)
        if success:
            messagebox.showinfo("Success", "Entry updated successfully!")
            dialog_to_close.destroy()
            self.refresh_table()
        else:
            messagebox.showerror("Error", "Failed to update entry.")

    def refresh_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
        self.original_results = module.view_entry()
        for i, credentials_data in enumerate(self.original_results):
            username_display = credentials_data.get("credentials", {}).get("username", "")
            website_display = credentials_data.get("website", "")
            self.table.insert("", tk.END, values=(username_display, "***", website_display), iid=str(i))

    def center_window(self, window, width, height):
        window.update_idletasks()
        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_w = self.winfo_width()
        parent_h = self.winfo_height()
        x = parent_x + (parent_w - width) // 2
        y = parent_y + (parent_h - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

# --- Main App ---
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(self.center_to_screen(400, 250))
        self.title("Password Manager")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = customtkinter.CTkFrame(master=self)
        self.my_frame.grid(row=0, column=0, pady=15, padx=60, sticky="nsew")
        self.my_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.my_frame.grid_columnconfigure(0, weight=1)

        customtkinter.CTkButton(master=self.my_frame, text="Add", command=self.add_entry).grid(row=0, column=0, pady=10, padx=10, sticky="ew") 
        customtkinter.CTkButton(master=self.my_frame, text="Delete", command=self.delete_entry).grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        customtkinter.CTkButton(master=self.my_frame, text="View", command=self.view_entry).grid(row=2, column=0, pady=10, padx=10, sticky="ew")
        customtkinter.CTkButton(master=self.my_frame, text="Update", command=self.update_entry).grid(row=3, column=0, pady=10, padx=10, sticky="ew")
        self.my_frame.grid_rowconfigure(4, weight=1)

    def center_to_screen(self, width, height):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        return f"{width}x{height}+{x}+{y}"

    def center_to_parent(self, parent, width, height):
        parent.update_idletasks()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        return f"{width}x{height}+{x}+{y}"
    
    def add_entry(self):
        add_dialog = AddEntry(self)
        add_dialog.geometry(self.center_to_parent(self, 400, 400))

    def delete_entry(self):
        delete_dialog = DeleteEntry(self)
        delete_dialog.geometry(self.center_to_parent(self, 400, 250))

    def view_entry(self):
        view_dialog = ViewEntry(self)
        view_dialog.geometry(self.center_to_parent(self, 600, 250))

    def update_entry(self):
        update_dialog = UpdateEntry(self)
        update_dialog.geometry(self.center_to_parent(self, 600, 250))

if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("blue")
    app = App()
    app.mainloop()
