import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Function to run queries
def run_query(query, params=()):
    conn = sqlite3.connect('donation_system.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
    except Exception as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        conn.commit()
        conn.close()
    return result

# Function to refresh the tree view after operations (Add/Delete/Search)
def refresh_tree(tree, table_name, columns):
    rows = run_query(f"SELECT * FROM {table_name}")
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", tk.END, values=row)

# Function to add a new entry
def add_entry(entries, tree, table_name, columns):
    values = [e.get() for e in entries]
    placeholders = ", ".join(["?"] * len(columns))
    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
    try:
        run_query(query, values)
        refresh_tree(tree, table_name, columns)
        for e in entries: e.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to delete an entry by ID
def delete_entry(entry_id, tree, table_name, id_column, columns):
    try:
        run_query(f"DELETE FROM {table_name} WHERE {id_column} = ?", (entry_id.get(),))
        refresh_tree(tree, table_name, columns)
        entry_id.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to search an entry by ID
def search_entry(entry_id, tree, table_name, columns, id_column):
    try:
        entry_id_value = entry_id.get()
        rows = run_query(f"SELECT * FROM {table_name} WHERE {id_column} = ?", (entry_id_value,))
        tree.delete(*tree.get_children())
        if rows:
            for row in rows:
                tree.insert("", tk.END, values=row)
        else:
            messagebox.showinfo("No Results", f"No records found with {id_column} = {entry_id_value}.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create main window
root = tk.Tk()
root.title("Donation System Management")
root.geometry("900x600")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# ---------- Tab: Users ----------
tab_users = ttk.Frame(notebook)
notebook.add(tab_users, text="Users")

cols_users = ["User_ID", "Name", "Address", "Phone"]
tree_users = ttk.Treeview(tab_users, columns=cols_users, show='headings')
for col in cols_users:
    tree_users.heading(col, text=col)
tree_users.pack(fill='x')

refresh_tree(tree_users, "Users", cols_users)

# Form to add new user
frame_form_users = tk.Frame(tab_users)
frame_form_users.pack()

entries_users = []
for col in cols_users:
    lbl = tk.Label(frame_form_users, text=col)
    lbl.pack(side='left')
    entry = tk.Entry(frame_form_users, width=15)
    entry.pack(side='left')
    entries_users.append(entry)

btn_add_user = tk.Button(tab_users, text="Add User", command=lambda: add_entry(entries_users, tree_users, "Users", cols_users))
btn_add_user.pack(pady=5)

# Delete and Search for Users
frame_action_users = tk.Frame(tab_users)
frame_action_users.pack()

entry_id_users = tk.Entry(frame_action_users, width=10)
entry_id_users.pack(side='left')
btn_delete_user = tk.Button(frame_action_users, text="Delete by ID", command=lambda: delete_entry(entry_id_users, tree_users, "Users", "User_ID", cols_users))
btn_delete_user.pack(side='left', padx=5)
btn_search_user = tk.Button(frame_action_users, text="Search by ID", command=lambda: search_entry(entry_id_users, tree_users, "Users", cols_users, "User_ID"))
btn_search_user.pack(side='left', padx=5)

# ---------- Tab: Medicine ----------
tab_medicine = ttk.Frame(notebook)
notebook.add(tab_medicine, text="Medicine")

cols_medicine = ["Medicine_ID", "Name", "Expiry_Date", "Quantity", "Category"]
tree_medicine = ttk.Treeview(tab_medicine, columns=cols_medicine, show='headings')
for col in cols_medicine:
    tree_medicine.heading(col, text=col)
tree_medicine.pack(fill='x')

refresh_tree(tree_medicine, "Medicine", cols_medicine)

# Form to add new medicine
frame_form_medicine = tk.Frame(tab_medicine)
frame_form_medicine.pack()

entries_medicine = []
for col in cols_medicine:
    lbl = tk.Label(frame_form_medicine, text=col)
    lbl.pack(side='left')
    entry = tk.Entry(frame_form_medicine, width=15)
    entry.pack(side='left')
    entries_medicine.append(entry)

btn_add_medicine = tk.Button(tab_medicine, text="Add Medicine", command=lambda: add_entry(entries_medicine, tree_medicine, "Medicine", cols_medicine))
btn_add_medicine.pack(pady=5)

# Delete and Search for Medicine
frame_action_medicine = tk.Frame(tab_medicine)
frame_action_medicine.pack()

entry_id_medicine = tk.Entry(frame_action_medicine, width=10)
entry_id_medicine.pack(side='left')
btn_delete_medicine = tk.Button(frame_action_medicine, text="Delete by ID", command=lambda: delete_entry(entry_id_medicine, tree_medicine, "Medicine", "Medicine_ID", cols_medicine))
btn_delete_medicine.pack(side='left', padx=5)
btn_search_medicine = tk.Button(frame_action_medicine, text="Search by ID", command=lambda: search_entry(entry_id_medicine, tree_medicine, "Medicine", cols_medicine, "Medicine_ID"))
btn_search_medicine.pack(side='left', padx=5)

# ---------- Tab: Pharmacy ----------
tab_pharmacy = ttk.Frame(notebook)
notebook.add(tab_pharmacy, text="Pharmacy")

cols_pharmacy = ["Pharmacy_ID", "Name", "Address"]
tree_pharmacy = ttk.Treeview(tab_pharmacy, columns=cols_pharmacy, show='headings')
for col in cols_pharmacy:
    tree_pharmacy.heading(col, text=col)
tree_pharmacy.pack(fill='x')

refresh_tree(tree_pharmacy, "Pharmacy", cols_pharmacy)

# Form to add new pharmacy
frame_form_pharmacy = tk.Frame(tab_pharmacy)
frame_form_pharmacy.pack()

entries_pharmacy = []
for col in cols_pharmacy:
    lbl = tk.Label(frame_form_pharmacy, text=col)
    lbl.pack(side='left')
    entry = tk.Entry(frame_form_pharmacy, width=15)
    entry.pack(side='left')
    entries_pharmacy.append(entry)

btn_add_pharmacy = tk.Button(tab_pharmacy, text="Add Pharmacy", command=lambda: add_entry(entries_pharmacy, tree_pharmacy, "Pharmacy", cols_pharmacy))
btn_add_pharmacy.pack(pady=5)

# Delete and Search for Pharmacy
frame_action_pharmacy = tk.Frame(tab_pharmacy)
frame_action_pharmacy.pack()

entry_id_pharmacy = tk.Entry(frame_action_pharmacy, width=10)
entry_id_pharmacy.pack(side='left')
btn_delete_pharmacy = tk.Button(frame_action_pharmacy, text="Delete by ID", command=lambda: delete_entry(entry_id_pharmacy, tree_pharmacy, "Pharmacy", "Pharmacy_ID", cols_pharmacy))
btn_delete_pharmacy.pack(side='left', padx=5)
btn_search_pharmacy = tk.Button(frame_action_pharmacy, text="Search by ID", command=lambda: search_entry(entry_id_pharmacy, tree_pharmacy, "Pharmacy", cols_pharmacy, "Pharmacy_ID"))
btn_search_pharmacy.pack(side='left', padx=5)

# ---------- Tab: Donation ----------
tab_donation = ttk.Frame(notebook)
notebook.add(tab_donation, text="Donation")

cols_donation = ["Donation_ID", "User_ID", "Medicine_ID", "Pharmacy_ID", "Donation_Date", "Status"]
tree_donation = ttk.Treeview(tab_donation, columns=cols_donation, show='headings')
for col in cols_donation:
    tree_donation.heading(col, text=col)
tree_donation.pack(fill='x')

refresh_tree(tree_donation, "Donation", cols_donation)

# Form to add new donation
frame_form_donation = tk.Frame(tab_donation)
frame_form_donation.pack()

entries_donation = []
for col in cols_donation:
    lbl = tk.Label(frame_form_donation, text=col)
    lbl.pack(side='left')
    entry = tk.Entry(frame_form_donation, width=15)
    entry.pack(side='left')
    entries_donation.append(entry)

btn_add_donation = tk.Button(tab_donation, text="Add Donation", command=lambda: add_entry(entries_donation, tree_donation, "Donation", cols_donation))
btn_add_donation.pack(pady=5)

# Delete and Search for Donation
frame_action_donation = tk.Frame(tab_donation)
frame_action_donation.pack()

entry_id_donation = tk.Entry(frame_action_donation, width=10)
entry_id_donation.pack(side='left')
btn_delete_donation = tk.Button(frame_action_donation, text="Delete by ID", command=lambda: delete_entry(entry_id_donation, tree_donation, "Donation", "Donation_ID", cols_donation))
btn_delete_donation.pack(side='left', padx=5)
btn_search_donation = tk.Button(frame_action_donation, text="Search by ID", command=lambda: search_entry(entry_id_donation, tree_donation, "Donation", cols_donation, "Donation_ID"))
btn_search_donation.pack(side='left', padx=5)

# ---------- Tab: Distribution ----------
tab_distribution = ttk.Frame(notebook)
notebook.add(tab_distribution, text="Distribution")

cols_distribution = ["Distribution_ID", "Donation_ID", "Pharmacy_ID", "Distribution_Date"]
tree_distribution = ttk.Treeview(tab_distribution, columns=cols_distribution, show='headings')
for col in cols_distribution:
    tree_distribution.heading(col, text=col)
tree_distribution.pack(fill='x')

refresh_tree(tree_distribution, "Distribution", cols_distribution)

# Form to add new distribution
frame_form_distribution = tk.Frame(tab_distribution)
frame_form_distribution.pack()

entries_distribution = []
for col in cols_distribution:
    lbl = tk.Label(frame_form_distribution, text=col)
    lbl.pack(side='left')
    entry = tk.Entry(frame_form_distribution, width=15)
    entry.pack(side='left')
    entries_distribution.append(entry)

btn_add_distribution = tk.Button(tab_distribution, text="Add Distribution", command=lambda: add_entry(entries_distribution, tree_distribution, "Distribution", cols_distribution))
btn_add_distribution.pack(pady=5)

# Delete and Search for Distribution
frame_action_distribution = tk.Frame(tab_distribution)
frame_action_distribution.pack()

entry_id_distribution = tk.Entry(frame_action_distribution, width=10)
entry_id_distribution.pack(side='left')
btn_delete_distribution = tk.Button(frame_action_distribution, text="Delete by ID", command=lambda: delete_entry(entry_id_distribution, tree_distribution, "Distribution", "Distribution_ID", cols_distribution))
btn_delete_distribution.pack(side='left', padx=5)
btn_search_distribution = tk.Button(frame_action_distribution, text="Search by ID", command=lambda: search_entry(entry_id_distribution, tree_distribution, "Distribution", cols_distribution, "Distribution_ID"))
btn_search_distribution.pack(side='left', padx=5)

# Start the application
root.mainloop()