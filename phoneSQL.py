import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from operation import CRUD

app = tk.Tk()

def open_delete():
    app.withdraw()
    page_D = tk.Toplevel(app)

    def close():
        page_D.destroy()
        app.deiconify()

    page_D.protocol("WM_DELETE_WINDOW", close)

    # page_D SETTINGS
    page_D.geometry("1000x700")
    page_D.resizable(False, False)
    page_D.config(bg="#F3F6F4")
    page_D.title("Delete Contact")

    # PAGE_D ELEMENTS
    db = CRUD()

    lab_D = tk.Label(
        master=page_D,
        text="Select a contact",
        font=["Arial", 35],
        bg="#F3F6F4",
        fg="#FF5A22"
    )
    lab_D.pack(pady=20)

    cols = ("ID", "Firstname", "Lastname", "Age", "Phone1", "Phone2", "Phone3", "Relation")
    tree_D = ttk.Treeview(
        master=page_D,
        columns=cols,
        show="headings",
        height=15
    )
    for column in cols:
        tree_D.heading(column, text=column)
        tree_D.column(column, width=130, anchor="center")

    tree_D.column("ID", width=50)

    tree_D.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    contacts = db.read()
    for contact in contacts:
        tree_D.insert("", "end", values=contact)

    def delete_contact():
        selected = tree_D.selection()

        if not selected:
            messagebox.showerror("Error", "you have to select one contact!")
            return

        confirm_delete = messagebox.askyesno("Deletion", "do you realy want to delete this contact?")
        if not confirm_delete:
            return

        con = tree_D.item(selected[0], "values")
        db.delete(con[0])
        tree_D.delete(selected[0])

        messagebox.showinfo("deleted", "Contact successfully deleted!")
    
    btn_Delete = tk.Button(
        master=page_D,
        text="Delete",
        font=["Arial", 18],
        bg="#5B6E2C",
        fg="white",
        width=15,
        command=delete_contact
        )
    btn_Delete.pack(pady=15)

def open_update():
    app.withdraw()
    page_U = tk.Toplevel()

    def close():
        page_U.destroy()
        app.deiconify()

    page_U.protocol("WM_DELETE_WINDOW", close)

    # PAGE_U SETTINGS
    page_U.geometry("1000x700")
    page_U.resizable(False, False)
    page_U.config(bg="#F3F6F4")
    page_U.title("Edit Contact")

    db = CRUD()
    lab_U = tk.Label(
        master=page_U,
        text="Select a contact",
        font=["Arial", 35],
        bg="#F3F6F4",
        fg="#FF5A22"
    )
    lab_U.pack(pady=20)


    columns = ("ID", "Firstname", "Lastname", "Age", "Phone1", "Phone2", "Phone3", "Relation")
    tree_U = ttk.Treeview(
        master=page_U,
        columns=columns,
        show="headings",
        height=15
    )

    for column in columns:
        tree_U.heading(column, text=column)
        tree_U.column(column, width=130, anchor="center")

    tree_U.column("ID", width=50)

    tree_U.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    contacts = db.read()

    for contact in contacts:
        tree_U.insert("", "end", values=contact)

    def select_contact():
        selected = tree_U.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a contact!"
            )
            return

        contact = tree_U.item(selected[0], "values")

        page_U.withdraw()

        page_edit = tk.Toplevel()
        page_edit.geometry("600x600")
        page_edit.resizable(False, False)
        page_edit.config(bg="#F3F6F4")
        page_edit.title("Update Contact")

        def close_edit():
            page_edit.destroy()
            page_U.deiconify()

        page_edit.protocol("WM_DELETE_WINDOW", close_edit)

        ent_fname = tk.Entry(page_edit, font=["Arial", 16])
        ent_fname.pack(pady=10)

        ent_lname = tk.Entry(page_edit, font=["Arial", 16])
        ent_lname.pack(pady=10)

        ent_age = tk.Entry(page_edit, font=["Arial", 16])
        ent_age.pack(pady=10)

        ent_phone1 = tk.Entry(page_edit, font=["Arial", 16])
        ent_phone1.pack(pady=10)

        ent_phone2 = tk.Entry(page_edit, font=["Arial", 16])
        ent_phone2.pack(pady=10)

        ent_phone3 = tk.Entry(page_edit, font=["Arial", 16])
        ent_phone3.pack(pady=10)

        combo_relation = ttk.Combobox(
            page_edit,
            values=["Family", "Friend", "Co-Worker", "Other"],
            state="readonly",
            font=["Arial", 16]
        )
        combo_relation.pack(pady=10)

        ent_fname.insert(0, contact[1])
        ent_lname.insert(0, contact[2])
        ent_age.insert(0, contact[3])
        ent_phone1.insert(0, contact[4])
        ent_phone2.insert(0, contact[5])
        ent_phone3.insert(0, contact[6])
        combo_relation.set(contact[7])

        def getdata():
            fname = ent_fname.get().strip()
            lname = ent_lname.get().strip()
            age = ent_age.get().strip()
            phone1 = ent_phone1.get().strip()
            phone2 = ent_phone2.get().strip()
            phone3 = ent_phone3.get().strip()
            relative = combo_relation.get()

            if not fname or not lname or not age or not phone1 or not phone2 or not phone3:
                messagebox.showerror("Error", "you have to fill all fields!")
                return
            
            if not age.isdigit() or int(age) <= 0:
                messagebox.showerror("Error", "Invalid age!")
                return

            if relative not in ["Family", "Friend", "Co-Worker", "Other"]:
                messagebox.showerror("Error", "Please select one option of the relation list!")
                return

            db.update(
                contact[0],
                fname,
                lname,
                int(age),
                phone1,
                phone2,
                phone3,
                relative
            )

            close_edit()

            for item in tree_U.get_children():
                tree_U.delete(item)

            for row in db.read():
                tree_U.insert("", "end", values=row)

            messagebox.showinfo("Success", "Contact updated successfully!")
        
        btn_update = tk.Button(
        master=page_edit,
        text="Update",
        font=["Arial", 18],
        bg="#5B6E2C",
        fg="white",
        width=15,
        command=getdata
        )
        btn_update.pack(pady=15)

    btn_select = tk.Button(
    master=page_U,
    text="Select",
    font=["Arial", 18],
    bg="#5B6E2C",
    fg="white",
    width=15,
    command=select_contact
    )
    btn_select.pack(pady=10)

def open_read():
    app.withdraw()
    page_R = tk.Toplevel(app)

    def close():
        page_R.destroy()
        app.deiconify()

    page_R.protocol("WM_DELETE_WINDOW", close)

    # PAGE_R SETTINGS
    page_R.geometry("1000x700")
    page_R.resizable(False, False)
    page_R.config(bg="#F3F6F4")
    page_R.title("View contacts")

    # PAGE ELEMENTS
    lab_R = tk.Label(
    master=page_R,
    text="View contacts",
    font=["Arial", 60],
    bg="#F3F6F4",
    fg="#FF5A22"
    )
    lab_R.pack(
    anchor="center"
    )

    columns = ("ID", "Firstname", "Lastname", "Age", "Phone1", "Phone2", "Phone3", "Relation")
    tree_R = ttk.Treeview(
        master=page_R,
        columns=columns,
        show="headings",
        height=15
    )

    for column in columns:
        tree_R.heading(column, text=column)
        tree_R.column(column, width=130, anchor="center")

    tree_R.column("ID", width=50)

    tree_R.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    scrollbar_R = ttk.Scrollbar(
        master=page_R,
        orient="vertical",
        command=tree_R.yview
    )

    tree_R.configure(yscrollcommand=scrollbar_R.set)

    scrollbar_R.place(
        relx=0.97,
        rely=0.23,
        relheight=0.65
    )

    contacts = CRUD().read()
    for contact in contacts:
        tree_R.insert(
            "",
            "end",
            values=contact
        )


def open_create():
    app.withdraw()
    page_C = tk.Toplevel()

    def close():
        page_C.destroy()
        app.deiconify()
    
    page_C.protocol("WM_DELETE_WINDOW", close)

    # PAGE_C SETTINGS
    page_C.geometry("600x800")
    page_C.resizable(False, False)
    page_C.config(bg="#F3F6F4")
    page_C.title("Add a contact")

    # PAGE_C ELEMENTS
    lab_C = tk.Label(
    master=page_C,
    text="Add a contact",
    font=["Arial", 60],
    bg="#F3F6F4",
    fg="#FF5A22"
    )
    lab_C.pack(
    anchor="center"
    )

    ent_C_fname = tk.Entry(
        master=page_C,
        width=20,
        bg="#7D8D39",
        fg="white",
        font=["Arial", 17],
        border=4
    )
    ent_C_fname.place(
        relx=0.5,
        y=300,
        anchor="center"
    )

    ent_C_lname = tk.Entry(
        master=page_C,
        width=20,
        bg="#7D8D39",
        fg="white",
        font=["Arial", 17],
        border=4   
    )
    ent_C_lname.place(
        relx=0.5,
        y=350,
        anchor="center"
    )

    ent_C_age = tk.Entry(
        master=page_C,
        width=20,
        bg="#7D8D39",
        fg="white",
        font=["Arial", 17],
        border=4   
    )
    ent_C_age.place(
        relx=0.5,
        y=400,
        anchor="center"
    )

    ent_C_phone1 = tk.Entry(
        master=page_C,
        width=20,
        bg="#7D8D39",
        fg="white",
        font=["Arial", 17],
        border=4   
    )
    ent_C_phone1.place(
        relx=0.5,
        y=450,
        anchor="center"
    )

    ent_C_phone2 = tk.Entry(
        master=page_C,
        width=20,
        bg="#7D8D39",
        fg="white",
        font=["Arial", 17],
        border=4   
    )
    ent_C_phone2.place(
        relx=0.5,
        y=500,
        anchor="center"
    )

    ent_C_phone3 = tk.Entry(
        master=page_C,
        width=20,
        bg="#7D8D39",
        fg="white",
        font=["Arial", 17],
        border=4   
    )
    ent_C_phone3.place(
        relx=0.5,
        y=550,
        anchor="center"
    )

    comb_C_values = ["Family", "Friend", "Co-Worker", "Other"]
    combo_C_relation = ttk.Combobox(
        master=page_C,
        width=19,
        font=["Arial", 17],
        background="white",
        foreground="black",
        values=comb_C_values,
        state="readonly"
    )
    combo_C_relation.place(
        relx=0.5,
        y=600,
        anchor="center"
    )
    combo_C_relation.set("Select a relation...")

    lab_C_fname = tk.Label(
        master=page_C,
        text="Firstname:",
        font=["Arial", 15],
        bg="#F3F6F4",
        fg="#FF5A22"
    )
    lab_C_fname.place(
        relx=0.156,   
        y=300, 
        anchor="center"
    )

    lab_C_lname = tk.Label(
        master=page_C,
        text="Lastname:",
        font=["Arial", 15],
        bg="#F3F6F4",
        fg="#FF5A22"
    )
    lab_C_lname.place(
        relx=0.156,   
        y=350, 
        anchor="center"
    )

    lab_C_age = tk.Label(
        master=page_C,
        text="Age:",
        font=["Arial", 15],
        bg="#F3F6F4",
        fg="#FF5A22"
    )
    lab_C_age.place(
        relx=0.156,   
        y=400, 
        anchor="center"
    )

    lab_C_phone1 = tk.Label(
        master=page_C,
        text="Phone 1:",
        font=["Arial", 15],
        bg="#F3F6F4",
        fg="#FF5A22"
    )
    lab_C_phone1.place(
        relx=0.156,   
        y=450, 
        anchor="center"
    )

    lab_C_phone2 = tk.Label(
        master=page_C,
        text="Phone 2:",
        font=["Arial", 15],
        bg="#F3F6F4",
        fg="#FF5A22"
    )
    lab_C_phone2.place(
        relx=0.156,   
        y=500, 
        anchor="center"
    )

    lab_C_phone3 = tk.Label(
        master=page_C,
        text="Phone 3:",
        font=["Arial", 15],
        bg="#F3F6F4",
        fg="#FF5A22"
    )
    lab_C_phone3.place(
        relx=0.156,   
        y=550, 
        anchor="center"
    )

    lab_C_relation = tk.Label(
        master=page_C,
        text="Relation:",
        font=["Arial", 15],
        bg="#F3F6F4",
        fg="#FF5A22"
    )
    lab_C_relation.place(
        relx=0.156,   
        y=600, 
        anchor="center"
    )

    btn_C_Enter = tk.Button(
        master=page_C,
        text="Add",
        bg="#5B6E2C",
        fg="white",
        font=["Arial", 20],
        width=15,
        height=1
    )
    btn_C_Enter.place(
        relx=0.5,
        y=670,
        anchor="center"
    )

    def add_contact():
        fname = ent_C_fname.get().strip()
        lname = ent_C_lname.get().strip()
        age = ent_C_age.get().strip()
        phone1 = ent_C_phone1.get().strip()
        phone2 = ent_C_phone2.get().strip()
        phone3 = ent_C_phone3.get().strip()
        relation = combo_C_relation.get()

        if not fname or not lname or not age or not phone1 or not phone2 or not phone3:
            messagebox.showerror("Error", "Please fill all fields!")
            return

        if not age.isdigit() or int(age) <= 0:
            messagebox.showerror("Error", "Age must be a number!")
            return

        if not relation or relation == "Select a relation...":
            messagebox.showerror("Error", "Please select a relation!")
            return

        CRUD().create(fname, lname, int(age), phone1, phone2, phone3, relation)

        messagebox.showinfo("Success", "Contact added successfully!")

        close()

    btn_C_Enter.config(
        command=add_contact
    )

# MAIN APP SETTINGS
app.geometry("600x700")
app.resizable(False, False)
app.config(bg="#F3F6F4")
app.title("PhoneSQL")

# MAIN APP ELEMENTS
lab_app1 = tk.Label(
    master=app,
    text="PhoneSQL",
    font=["Arial", 60],
    bg="#F3F6F4",
    fg="#FF5A22"
)
lab_app1.pack(
    anchor="center"
)

btn_C = tk.Button(
    master=app,
    text="Add a contact",
    width=12,
    font=["Arial", 35],
    bg="#5B6E2C",
    fg="#F3F6F4",
    command=open_create
)
btn_C.place(
    relx=0.5,
    y=275,
    anchor="center"
)

btn_R = tk.Button(
    master=app,
    text="View contacts",
    width=12,
    font=["Arial", 35],
    bg="#5B6E2C",
    fg="#F3F6F4",
    command=open_read
)
btn_R.place(
    relx=0.5,
    y=370,
    anchor="center"
)

btn_U = tk.Button(
    master=app,
    text="Edit",
    width=12,
    font=["Arial", 35],
    bg="#5B6E2C",
    fg="#F3F6F4",
    command=open_update
)
btn_U.place(
    relx=0.5,
    y=465,
    anchor="center"
)

btn_D = tk.Button(
    master=app,
    text="Delete",
    width=12,
    font=["Arial", 35],
    bg="#5B6E2C",
    fg="#F3F6F4",
    command=open_delete
)
btn_D.place(
    relx=0.5,
    y=560,
    anchor="center"
)

app.mainloop()