# Restaurant Delivery System - Admin GUI
# Author: Hoai Nam
# This GUI allows an admin to register drivers, deactivate drivers,
# view overdue delivery tickets, and update ticket status.

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import mysql.connector
from db_config import DB_CONFIG


def get_db_connection():
    """Create and return a MySQL database connection."""
    return mysql.connector.connect(**DB_CONFIG)


def test_connection():
    """Test database connection when the program starts."""
    try:
        conn = get_db_connection()
        print("Connected to MySQL successfully!")
        conn.close()
    except Exception as e:
        print("Connection failed:", e)


class AdminGUI:
    """Main Admin GUI for the Restaurant Delivery System."""

    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Delivery System")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.entries = {}
        self.ticket_table = None

        self.show_dashboard()

    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def header(self):
        """Display common page header."""
        tk.Label(
            self.root,
            text="Restaurant Delivery System",
            font=("Arial", 24, "bold"),
            bg="#d9e6ff",
            pady=15
        ).pack(fill="x")

    def show_dashboard(self):
        """Display admin dashboard."""
        self.clear_window()
        self.header()

        tk.Label(
            self.root,
            text="Admin Dashboard",
            font=("Arial", 22, "bold")
        ).pack(pady=45)

        tk.Button(
            self.root,
            text="Register New Driver",
            width=25,
            height=2,
            command=self.show_register_driver
        ).pack(pady=12)

        tk.Button(
            self.root,
            text="Deactivate Driver",
            width=25,
            height=2,
            command=self.deactivate_driver
        ).pack(pady=12)

        tk.Button(
            self.root,
            text="View Overdue Tickets",
            width=25,
            height=2,
            command=self.show_overdue_tickets
        ).pack(pady=12)

    def show_register_driver(self):
        """Display driver registration form."""
        self.clear_window()
        self.header()

        tk.Label(
            self.root,
            text="Register New Driver",
            font=("Arial", 22, "bold")
        ).pack(pady=30)

        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        labels = [
            "Driver Name",
            "Phone Number",
            "Email",
            "License Number",
            "Vehicle Type"
        ]

        self.entries = {}

        for row, label in enumerate(labels):
            tk.Label(
                form_frame,
                text=label + ":",
                font=("Arial", 12),
                width=18,
                anchor="e"
            ).grid(row=row, column=0, padx=10, pady=10)

            entry = tk.Entry(form_frame, width=35, font=("Arial", 12))
            entry.grid(row=row, column=1, padx=10, pady=10)
            self.entries[label] = entry

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=25)

        tk.Button(
            button_frame,
            text="Submit",
            width=15,
            height=2,
            bg="#d5e8d4",
            command=self.register_driver
        ).grid(row=0, column=0, padx=15)

        tk.Button(
            button_frame,
            text="Cancel",
            width=15,
            height=2,
            bg="#f8cecc",
            command=self.show_dashboard
        ).grid(row=0, column=1, padx=15)

    def register_driver(self):
        """Insert a new driver into User and Driver tables."""
        name = self.entries["Driver Name"].get().strip()
        phone = self.entries["Phone Number"].get().strip()
        email = self.entries["Email"].get().strip()
        license_number = self.entries["License Number"].get().strip()
        vehicle_type = self.entries["Vehicle Type"].get().strip()

        if not name or not phone or not email or not license_number or not vehicle_type:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO User
                (full_name, email, phone, password_hash, account_status)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (name, email, phone, "default123", "Active")
            )

            new_user_id = cursor.lastrowid

            cursor.execute(
                """
                INSERT INTO Driver
                (driver_id, license_number, vehicle_type, availability_status)
                VALUES (%s, %s, %s, %s)
                """,
                (new_user_id, license_number, vehicle_type, "Available")
            )

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                f"Driver profile created successfully.\nNew Driver ID: {new_user_id}"
            )

            for entry in self.entries.values():
                entry.delete(0, tk.END)

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))

    def deactivate_driver(self):
        """Deactivate a driver by ID."""
        driver_id = simpledialog.askstring(
            "Deactivate Driver",
            "Enter Driver ID:"
        )

        if not driver_id:
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE Driver
                SET availability_status = 'Inactive'
                WHERE driver_id = %s
                """,
                (driver_id,)
            )

            cursor.execute(
                """
                UPDATE User
                SET account_status = 'Inactive'
                WHERE user_id = %s
                """,
                (driver_id,)
            )

            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning(
                    "Not Found",
                    f"No driver found with ID {driver_id}."
                )
            else:
                messagebox.showinfo(
                    "Success",
                    f"Driver {driver_id} has been deactivated."
                )

            cursor.close()
            conn.close()

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))

    def show_overdue_tickets(self):
        """Display overdue tickets screen."""
        self.clear_window()
        self.header()

        tk.Label(
            self.root,
            text="Overdue Delivery Tickets",
            font=("Arial", 22, "bold")
        ).pack(pady=25)

        columns = (
            "Ticket ID",
            "Order ID",
            "Status",
            "Time Open",
            "Max Time",
            "Note"
        )

        self.ticket_table = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings",
            height=8
        )

        for col in columns:
            self.ticket_table.heading(col, text=col)
            self.ticket_table.column(col, width=115, anchor="center")

        self.ticket_table.pack(pady=15)

        self.load_overdue_tickets()

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Close Ticket",
            width=15,
            height=2,
            bg="#d5e8d4",
            command=self.close_selected_ticket
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="Escalate Ticket",
            width=15,
            height=2,
            bg="#fff2cc",
            command=self.escalate_selected_ticket
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            button_frame,
            text="Back",
            width=15,
            height=2,
            bg="#f8cecc",
            command=self.show_dashboard
        ).grid(row=0, column=2, padx=10)

    def load_overdue_tickets(self):
        """Load overdue tickets from MySQL."""
        for row in self.ticket_table.get_children():
            self.ticket_table.delete(row)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    ticket_id,
                    order_id,
                    ticket_status,
                    TIMESTAMPDIFF(MINUTE, open_time, NOW()) AS time_open,
                    max_delivery_time,
                    IFNULL(admin_note, '')
                FROM DeliveryTicket
                WHERE ticket_status = 'Overdue'
                   OR (
                       ticket_status = 'Open'
                       AND TIMESTAMPDIFF(MINUTE, open_time, NOW()) > max_delivery_time
                   )
                """
            )

            rows = cursor.fetchall()

            for row in rows:
                self.ticket_table.insert("", tk.END, values=row)

            cursor.close()
            conn.close()

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))

    def get_selected_ticket_id(self):
        """Get ticket ID from selected table row."""
        selected_item = self.ticket_table.selection()

        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a ticket first.")
            return None

        values = self.ticket_table.item(selected_item[0], "values")
        return values[0]

    def close_selected_ticket(self):
        """Close selected ticket."""
        ticket_id = self.get_selected_ticket_id()

        if not ticket_id:
            return

        note = simpledialog.askstring("Close Ticket", "Enter admin note:")

        if note is None:
            note = ""

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE DeliveryTicket
                SET ticket_status = 'Closed',
                    close_time = NOW(),
                    admin_note = %s
                WHERE ticket_id = %s
                """,
                (note, ticket_id)
            )

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Ticket closed successfully.")
            self.load_overdue_tickets()

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))

    def escalate_selected_ticket(self):
        """Escalate selected ticket."""
        ticket_id = self.get_selected_ticket_id()

        if not ticket_id:
            return

        note = simpledialog.askstring("Escalate Ticket", "Enter escalation note:")

        if note is None:
            note = ""

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE DeliveryTicket
                SET ticket_status = 'Escalated',
                    admin_note = %s
                WHERE ticket_id = %s
                """,
                (note, ticket_id)
            )

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Ticket escalated successfully.")
            self.load_overdue_tickets()

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))


if __name__ == "__main__":
    test_connection()
    root = tk.Tk()
    app = AdminGUI(root)
    root.mainloop()
