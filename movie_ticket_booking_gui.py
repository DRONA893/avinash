import os
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

# -------------------- Configuration --------------------
APP_TITLE = "CINEMAX | Movie Ticket Booking"
FILE = "bookings.txt"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MovieBookingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(fg_color="#0b1020")
        self.bookings = []

        self._setup_styles()
        self._build_layout()
        self.refresh_bookings()

    def _setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(
            "Treeview",
            background="#141c30",
            foreground="#f1f5f9",
            fieldbackground="#141c30",
            rowheight=34,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background="#202b45",
            foreground="#dbeafe",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padding=(10, 10),
        )
        style.map(
            "Treeview",
            background=[("selected", "#1d4ed8")],
            foreground=[("selected", "#ffffff")],
        )

    def _build_layout(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="#111a2e", corner_radius=0, height=86)
        header.pack(fill="x")
        header.pack_propagate(False)

        brand = ctk.CTkFrame(header, fg_color="transparent")
        brand.pack(side="left", padx=28, pady=15)
        ctk.CTkLabel(
            brand, text="CINEMAX", font=ctk.CTkFont("Segoe UI", 25, "bold"),
            text_color="#60a5fa"
        ).pack(anchor="w")
        ctk.CTkLabel(
            brand, text="MOVIE TICKET BOOKING SYSTEM",
            font=ctk.CTkFont("Segoe UI", 10, "bold"), text_color="#94a3b8"
        ).pack(anchor="w")

        ctk.CTkLabel(
            header, text="BOOK • MANAGE • ENJOY",
            font=ctk.CTkFont("Segoe UI", 11, "bold"), text_color="#cbd5e1"
        ).pack(side="right", padx=30)

        # Main content
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=22, pady=20)

        # Stats cards
        stats = ctk.CTkFrame(body, fg_color="transparent")
        stats.pack(fill="x", pady=(0, 18))
        self.stat_booking = self._stat_card(stats, "TOTAL BOOKINGS", "0", "#60a5fa")
        self.stat_tickets = self._stat_card(stats, "TICKETS SOLD", "0", "#34d399")
        self.stat_movies = self._stat_card(stats, "MOVIE TITLES", "0", "#fbbf24")

        # Work area
        content = ctk.CTkFrame(body, fg_color="transparent")
        content.pack(fill="both", expand=True)
        content.grid_columnconfigure(0, weight=0, minsize=280)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        # Left booking panel
        panel = ctk.CTkFrame(content, fg_color="#111a2e", corner_radius=16, width=280)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        panel.grid_propagate(False)

        ctk.CTkLabel(
            panel, text="Manage Booking", font=ctk.CTkFont("Segoe UI", 19, "bold"),
            text_color="#f8fafc"
        ).pack(anchor="w", padx=20, pady=(22, 4))
        ctk.CTkLabel(
            panel, text="Enter the customer details below.",
            font=ctk.CTkFont("Segoe UI", 11), text_color="#94a3b8"
        ).pack(anchor="w", padx=20, pady=(0, 18))

        self.name_entry = self._field(panel, "CUSTOMER NAME", "e.g. Rahul Kumar")
        self.movie_entry = self._field(panel, "MOVIE NAME", "e.g. Interstellar")
        self.tickets_entry = self._field(panel, "NUMBER OF TICKETS", "e.g. 2")

        ctk.CTkButton(
            panel, text="＋  Book Tickets", height=42, corner_radius=10,
            fg_color="#2563eb", hover_color="#1d4ed8",
            font=ctk.CTkFont("Segoe UI", 13, "bold"), command=self.book_ticket
        ).pack(fill="x", padx=20, pady=(18, 9))

        ctk.CTkButton(
            panel, text="✕  Cancel Selected Booking", height=38, corner_radius=10,
            fg_color="#7f1d1d", hover_color="#991b1b",
            font=ctk.CTkFont("Segoe UI", 12, "bold"), command=self.cancel_selected
        ).pack(fill="x", padx=20, pady=(0, 9))

        ctk.CTkButton(
            panel, text="Clear Form", height=34, corner_radius=10,
            fg_color="#25324a", hover_color="#334155",
            font=ctk.CTkFont("Segoe UI", 11), command=self.clear_form
        ).pack(fill="x", padx=20, pady=(0, 20))

        # Right records panel
        records = ctk.CTkFrame(content, fg_color="#111a2e", corner_radius=16)
        records.grid(row=0, column=1, sticky="nsew")
        records.grid_columnconfigure(0, weight=1)
        records.grid_rowconfigure(2, weight=1)

        top = ctk.CTkFrame(records, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        ctk.CTkLabel(
            top, text="Booking Records", font=ctk.CTkFont("Segoe UI", 19, "bold"),
            text_color="#f8fafc"
        ).pack(side="left")

        searchrow = ctk.CTkFrame(records, fg_color="transparent")
        searchrow.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))
        searchrow.grid_columnconfigure(0, weight=1)
        self.search_entry = ctk.CTkEntry(
            searchrow, placeholder_text="Search customer or movie...",
            height=38, corner_radius=9, border_color="#334155",
            fg_color="#0b1020", text_color="#f8fafc"
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.search_entry.bind("<KeyRelease>", lambda _event: self.populate_table())
        ctk.CTkButton(
            searchrow, text="Refresh", width=90, height=38,
            fg_color="#25324a", hover_color="#334155", command=self.refresh_bookings
        ).grid(row=0, column=1)

        table_frame = ctk.CTkFrame(records, fg_color="#141c30", corner_radius=10)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        columns = ("name", "movie", "tickets")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        self.table.heading("name", text="CUSTOMER")
        self.table.heading("movie", text="MOVIE")
        self.table.heading("tickets", text="TICKETS")
        self.table.column("name", width=160, anchor="w")
        self.table.column("movie", width=180, anchor="w")
        self.table.column("tickets", width=80, anchor="center")
        self.table.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.bind("<Double-1>", self.fill_form_from_selection)

        footer = ctk.CTkLabel(
            self, text="CINEMAX  •  Local booking records saved automatically",
            font=ctk.CTkFont("Segoe UI", 10), text_color="#64748b"
        )
        footer.pack(pady=(0, 10))

    def _stat_card(self, parent, title, value, accent):
        card = ctk.CTkFrame(parent, fg_color="#111a2e", corner_radius=14, height=86)
        card.pack(side="left", fill="x", expand=True, padx=(0, 12))
        card.pack_propagate(False)
        ctk.CTkLabel(
            card, text=title, font=ctk.CTkFont("Segoe UI", 10, "bold"),
            text_color="#94a3b8"
        ).pack(anchor="w", padx=17, pady=(13, 1))
        label = ctk.CTkLabel(
            card, text=value, font=ctk.CTkFont("Segoe UI", 24, "bold"),
            text_color=accent
        )
        label.pack(anchor="w", padx=17)
        return label

    def _field(self, parent, label, placeholder):
        ctk.CTkLabel(
            parent, text=label, font=ctk.CTkFont("Segoe UI", 10, "bold"),
            text_color="#cbd5e1"
        ).pack(anchor="w", padx=20, pady=(0, 6))
        entry = ctk.CTkEntry(
            parent, placeholder_text=placeholder, height=39, corner_radius=9,
            border_color="#334155", fg_color="#0b1020", text_color="#f8fafc"
        )
        entry.pack(fill="x", padx=20, pady=(0, 14))
        return entry

    def read_bookings(self):
        records = []
        if not os.path.exists(FILE):
            return records

        try:
            with open(FILE, "r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):
                    line = line.rstrip("\n")
                    if not line:
                        continue
                    parts = line.split(",")
                    if len(parts) != 3:
                        # Ignore malformed lines rather than crashing the app.
                        continue
                    name, movie, tickets = (part.strip() for part in parts)
                    try:
                        tickets_num = int(tickets)
                    except ValueError:
                        continue
                    records.append({"name": name, "movie": movie, "tickets": tickets_num})
        except OSError as exc:
            messagebox.showerror("File Error", f"Could not read {FILE}:\n{exc}")
        return records

    def write_bookings(self, records):
        try:
            with open(FILE, "w", encoding="utf-8") as file:
                for record in records:
                    # Commas would break this simple text-file format.
                    file.write(
                        f'{record["name"].replace(",", " ")} ,'
                        f'{record["movie"].replace(",", " ")} ,'
                        f'{record["tickets"]}\n'
                    )
            return True
        except OSError as exc:
            messagebox.showerror("File Error", f"Could not save {FILE}:\n{exc}")
            return False

    def book_ticket(self):
        name = self.name_entry.get().strip()
        movie = self.movie_entry.get().strip()
        tickets_text = self.tickets_entry.get().strip()

        if not name or not movie or not tickets_text:
            messagebox.showwarning("Missing Details", "Please fill in all three fields.")
            return
        if "," in name or "," in movie:
            messagebox.showwarning("Invalid Character", "Please do not use commas in names or movie titles.")
            return
        try:
            tickets = int(tickets_text)
            if tickets <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Quantity", "Enter a whole number of tickets greater than zero.")
            return

        # Keep the same comma-separated bookings.txt format as the original program.
        try:
            with open(FILE, "a", encoding="utf-8") as file:
                file.write(f"{name},{movie},{tickets}\n")
        except OSError as exc:
            messagebox.showerror("File Error", f"Could not save booking:\n{exc}")
            return

        messagebox.showinfo("Booking Confirmed", f"Tickets booked successfully!\n\nCustomer: {name}\nMovie: {movie}\nTickets: {tickets}")
        self.clear_form()
        self.refresh_bookings()

    def refresh_bookings(self):
        self.bookings = self.read_bookings()
        self.populate_table()
        total_tickets = sum(record["tickets"] for record in self.bookings)
        movie_titles = {record["movie"].strip().lower() for record in self.bookings}
        self.stat_booking.configure(text=str(len(self.bookings)))
        self.stat_tickets.configure(text=str(total_tickets))
        self.stat_movies.configure(text=str(len(movie_titles)))

    def populate_table(self):
        query = self.search_entry.get().strip().lower() if hasattr(self, "search_entry") else ""
        for item in self.table.get_children():
            self.table.delete(item)

        for index, record in enumerate(self.bookings):
            if query and query not in record["name"].lower() and query not in record["movie"].lower():
                continue
            self.table.insert(
                "", "end", iid=str(index),
                values=(record["name"], record["movie"], record["tickets"])
            )

    def cancel_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Select Booking", "Select a booking from the table first.")
            return

        index = int(selected[0])
        if index >= len(self.bookings):
            self.refresh_bookings()
            return
        record = self.bookings[index]
        confirm = messagebox.askyesno(
            "Confirm Cancellation",
            f'Cancel this booking?\n\nCustomer: {record["name"]}\nMovie: {record["movie"]}\nTickets: {record["tickets"]}'
        )
        if not confirm:
            return

        remaining = self.bookings.copy()
        remaining.pop(index)
        if self.write_bookings(remaining):
            messagebox.showinfo("Cancelled", "Booking cancelled successfully.")
            self.refresh_bookings()

    def fill_form_from_selection(self, _event=None):
        selected = self.table.selection()
        if not selected:
            return
        record = self.bookings[int(selected[0])]
        self.clear_form()
        self.name_entry.insert(0, record["name"])
        self.movie_entry.insert(0, record["movie"])
        self.tickets_entry.insert(0, str(record["tickets"]))

    def clear_form(self):
        for entry in (self.name_entry, self.movie_entry, self.tickets_entry):
            entry.delete(0, "end")


if __name__ == "__main__":
    app = MovieBookingApp()
    app.mainloop()
