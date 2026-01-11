import tkinter as tk
from tkinter import ttk, messagebox
import openpyxl

# Load client names from Excel
def load_client_names(file_path="data/Client_data.xlsx"):
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        clients = set()
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Assuming row 1 has headers
            client_name = row[0]  # Assuming "Client" is in column A
            if client_name:
                clients.add(client_name.strip())
        return sorted(list(clients))
    except Exception as e:
        print(f"Error loading clients: {e}")
        return []

def start_ui():
    root = tk.Tk()
    root.title("Automation Framework UI")
    root.geometry("520x460")
    root.resizable(True, True)
    root.configure(bg="#f4f4f4")

    LABEL_FONT = ("Segoe UI", 10)
    BUTTON_FONT = ("Segoe UI", 10, "bold")

    main_frame = tk.Frame(root, bg="#f4f4f4", padx=20, pady=20)
    main_frame.pack(expand=True, fill="both")

    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)

    # ====== Client Name Dropdown ======
    tk.Label(main_frame, text="Select Client", font=("Segoe UI", 11, "bold"),
             bg="#f4f4f4", fg="#333").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

    client_names = load_client_names()
    client_dropdown = ttk.Combobox(main_frame, values=client_names, state="readonly", width=40)
    client_dropdown.set("Select Client")
    client_dropdown.grid(row=1, column=0, columnspan=2, pady=(0, 15), sticky="ew")

# Dummy test functions (replace these with actual logic)
def run_plan_change(customer_id, plan_name):
    return f"Plan change test run for {customer_id} with plan {plan_name}"

def run_plan_renew(customer_id, plan_name):
    return f"Plan renew test run for {customer_id} with plan {plan_name}"

def start_ui():
    root = tk.Tk()
    root.title("Automation Framework UI")
    root.geometry("500x420")  # Initial window size
    root.resizable(True, True)  # Enable both horizontal and vertical resizing
    root.configure(bg="#f4f4f4")

    LABEL_FONT = ("Segoe UI", 10)
    BUTTON_FONT = ("Segoe UI", 10, "bold")

    main_frame = tk.Frame(root, bg="#f4f4f4", padx=20, pady=20)
    main_frame.pack(expand=True, fill="both")

    # ========== Configure Grid to be Responsive ==========
    main_frame.grid_rowconfigure(0, weight=0)  # Customer selection header
    main_frame.grid_rowconfigure(1, weight=0)  # Customer ID entry
    main_frame.grid_rowconfigure(2, weight=0)  # Radio options
    main_frame.grid_rowconfigure(7, weight=0)  # Plan selection
    main_frame.grid_rowconfigure(8, weight=0)  # Plan dropdown
    main_frame.grid_rowconfigure(9, weight=1)  # Action buttons

    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)

    # ========== Customer Option Selection ==========
    tk.Label(main_frame, text="Customer Selection Options", font=("Segoe UI", 11, "bold"),
             bg="#f4f4f4", fg="#333").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

    customer_option = tk.StringVar(value="manual")

    # Customer ID entry (initially enabled)
    customer_id_entry = tk.Entry(main_frame, width=40, fg='grey')
    placeholder_text = "Enter Customer ID"
    customer_id_entry.insert(0, placeholder_text)
    customer_id_entry.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")

    def clear_placeholder(event):
        if customer_id_entry.get() == placeholder_text:
            customer_id_entry.delete(0, tk.END)
            customer_id_entry.config(fg='black')

    def set_placeholder(event):
        if customer_id_entry.get() == "":
            customer_id_entry.insert(0, placeholder_text)
            customer_id_entry.config(fg='grey')

    customer_id_entry.bind("<FocusIn>", clear_placeholder)
    customer_id_entry.bind("<FocusOut>", set_placeholder)

    # Radio Button Options
    def update_customer_entry_state():
        is_manual = customer_option.get() == "manual"
        state = "normal" if is_manual else "disabled"
        customer_id_entry.config(state=state)
        if not is_manual:
            customer_id_entry.delete(0, tk.END)
            customer_id_entry.insert(0, placeholder_text)
            customer_id_entry.config(fg='grey')

    radio_options = [
        ("Enter customer ID", "manual"),
        ("Search for an active customer from TG5", "active_one"),
        ("Search for all active customers from TG5", "active_all"),
        ("Search for a suspended customer from TG5", "suspended_one"),
        ("Search for all suspended customers from TG5", "suspended_all"),
    ]

    for i, (label, value) in enumerate(radio_options):
        rb = tk.Radiobutton(
            main_frame, text=label, variable=customer_option, value=value,
            bg="#f4f4f4", anchor="w", font=("Segoe UI", 9),
            command=update_customer_entry_state
        )
        rb.grid(row=2+i, column=0, columnspan=2, sticky="w", pady=2)

    """"# ========== Plan Dropdown ==========
    tk.Label(main_frame, text="\nSelect Plan", font=LABEL_FONT, bg="#f4f4f4").grid(row=7, column=0, sticky="w")
    plan_options = ["Standard", "Premium", "Family", "Student"]
    plan_dropdown = ttk.Combobox(main_frame, values=plan_options, width=37, state="readonly")
    plan_dropdown.set("Select Plan")
    plan_dropdown.grid(row=8, column=0, columnspan=2, pady=(0, 15), sticky="ew")"""
    plan_options = ["Standard", "Premium", "Family", "Student"]
    plan_dropdown = ttk.Combobox(main_frame, values=plan_options, width=37, state="readonly")

    # ========== Action Buttons ==========
    def handle_action(action_type):
        plan = plan_dropdown.get()
        option = customer_option.get()
        cid = customer_id_entry.get().strip()

        if plan == "Select Plan":
            messagebox.showwarning("Missing Input", "Please select a plan.")
            return

        if option == "manual":
            if cid == placeholder_text or not cid:
                messagebox.showwarning("Missing Input", "Please enter a valid Customer ID.")
                return
        else:
            cid = f"[{option} from TG5]"

        if action_type == "change":
            result = run_plan_change(cid, plan)
        else:
            result = run_plan_renew(cid, plan)

        messagebox.showinfo("Test Result", result)

    tk.Button(main_frame, text="Run Plan Change", font=BUTTON_FONT, bg="#2196f3", fg="white",
              command=lambda: handle_action("change"), width=20).grid(row=9, column=0, pady=10, sticky="ew")

    tk.Button(main_frame, text="Run Plan Renew", font=BUTTON_FONT, bg="#ff9800", fg="white",
              command=lambda: handle_action("renew"), width=20).grid(row=9, column=1, pady=10, sticky="ew")

    root.mainloop()


if __name__ == "__main__":
    start_ui()
