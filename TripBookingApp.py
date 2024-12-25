import tkinter as tk
from tkinter import messagebox

class VacationBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikacja Rezerwacji Wakacji")

        # Dostępne destynacje
        self.destinations = [
            "Hawaje",
            "Bali",
            "Santorini",
            "Malediwy",
            "Alaska",
            "Paryż",
            "Tokio",
            "Sydney",
        ]

        # Elementy interfejsu
        tk.Label(root, text="Rezerwacja Wakacji", font=("Helvetica", 16)).pack(pady=10)

        tk.Label(root, text="Imię i nazwisko:").pack(anchor="w", padx=20)
        self.name_entry = tk.Entry(root, width=40)
        self.name_entry.pack(padx=20, pady=5)

        tk.Label(root, text="E-mail:").pack(anchor="w", padx=20)
        self.email_entry = tk.Entry(root, width=40)
        self.email_entry.pack(padx=20, pady=5)

        tk.Label(root, text="Numer telefonu:").pack(anchor="w", padx=20)
        self.phone_entry = tk.Entry(root, width=40)
        self.phone_entry.pack(padx=20, pady=5)

        tk.Label(root, text="Wybierz destynację:").pack(anchor="w", padx=20)
        self.destination_var = tk.StringVar(value=self.destinations[0])
        self.destination_menu = tk.OptionMenu(root, self.destination_var, *self.destinations)
        self.destination_menu.pack(padx=20, pady=5)

        tk.Label(root, text="Daty podróży:").pack(anchor="w", padx=20)
        tk.Label(root, text="Data rozpoczęcia (RRRR-MM-DD):").pack(anchor="w", padx=40)
        self.start_date_entry = tk.Entry(root, width=20)
        self.start_date_entry.pack(padx=40, pady=5)

        tk.Label(root, text="Data zakończenia (RRRR-MM-DD):").pack(anchor="w", padx=40)
        self.end_date_entry = tk.Entry(root, width=20)
        self.end_date_entry.pack(padx=40, pady=5)

        tk.Label(root, text="Uwagi specjalne:").pack(anchor="w", padx=20)
        self.special_requests_text = tk.Text(root, width=50, height=5)
        self.special_requests_text.pack(padx=20, pady=5)

        tk.Button(root, text="Zarezerwuj wakacje", command=self.book_vacation).pack(pady=20)
        tk.Button(root, text="Pokaż wszystkie rezerwacje", command=self.show_bookings).pack(pady=10)

        # Lista rezerwacji
        self.bookings = []

    def book_vacation(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        destination = self.destination_var.get()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()
        special_requests = self.special_requests_text.get("1.0", tk.END).strip()

        if not name or not email or not phone or not start_date or not end_date:
            messagebox.showerror("Błąd", "Wszystkie pola oprócz 'Uwagi specjalne' są wymagane!")
            return

        if "@" not in email or "." not in email:
            messagebox.showerror("Błąd", "Niepoprawny format e-mail!")
            return

        if not phone.isdigit() or len(phone) < 10:
            messagebox.showerror("Błąd", "Niepoprawny numer telefonu! Powinien zawierać co najmniej 10 cyfr.")
            return

        booking = {
            "name": name,
            "email": email,
            "phone": phone,
            "destination": destination,
            "start_date": start_date,
            "end_date": end_date,
            "special_requests": special_requests if special_requests else "Brak"
        }
        self.bookings.append(booking)

        confirmation_message = (
            f"Szczegóły rezerwacji wakacji:\n"
            f"Imię i nazwisko: {name}\n"
            f"E-mail: {email}\n"
            f"Numer telefonu: {phone}\n"
            f"Destynacja: {destination}\n"
            f"Daty podróży: {start_date} do {end_date}\n"
            f"Uwagi specjalne: {special_requests if special_requests else 'Brak'}"
        )
        messagebox.showinfo("Rezerwacja potwierdzona", confirmation_message)
        self.clear_fields()

    def show_bookings(self):
        if not self.bookings:
            messagebox.showinfo("Brak rezerwacji", "Nie ma jeszcze żadnych rezerwacji.")
            return

        bookings_details = "\n\n".join([
            f"Imię i nazwisko: {b['name']}\n"
            f"E-mail: {b['email']}\n"
            f"Numer telefonu: {b['phone']}\n"
            f"Destynacja: {b['destination']}\n"
            f"Daty podróży: {b['start_date']} do {b['end_date']}\n"
            f"Uwagi specjalne: {b['special_requests']}"
            for b in self.bookings
        ])

        messagebox.showinfo("Wszystkie rezerwacje", bookings_details)

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.special_requests_text.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = VacationBookingApp(root)
    root.mainloop()
