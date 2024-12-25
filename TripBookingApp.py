import tkinter as tk
from tkinter import messagebox
import csv

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
        tk.Button(root, text="Usuń wszystkie rezerwacje", command=self.clear_bookings).pack(pady=10)
        tk.Button(root, text="Eksportuj rezerwacje do pliku", command=self.export_bookings).pack(pady=10)
        tk.Button(root, text="Filtruj rezerwacje", command=self.filter_bookings).pack(pady=10)
        tk.Button(root, text="Edytuj rezerwację", command=self.edit_booking).pack(pady=10)
        tk.Button(root, text="Szukaj rezerwacji po nazwisku", command=self.search_booking).pack(pady=10)
        tk.Button(root, text="Statystyki destynacji", command=self.show_statistics).pack(pady=10)

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

    def clear_bookings(self):
        if not self.bookings:
            messagebox.showinfo("Brak rezerwacji", "Nie ma żadnych rezerwacji do usunięcia.")
            return

        self.bookings.clear()
        messagebox.showinfo("Sukces", "Wszystkie rezerwacje zostały usunięte.")

    def export_bookings(self):
        if not self.bookings:
            messagebox.showinfo("Brak rezerwacji", "Nie ma żadnych rezerwacji do eksportu.")
            return

        with open("rezerwacje.csv", "w", newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "email", "phone", "destination", "start_date", "end_date", "special_requests"])
            writer.writeheader()
            writer.writerows(self.bookings)

        messagebox.showinfo("Sukces", "Rezerwacje zostały wyeksportowane do pliku 'rezerwacje.csv'.")

    def filter_bookings(self):
        filter_window = tk.Toplevel(self.root)
        filter_window.title("Filtruj rezerwacje")

        tk.Label(filter_window, text="Filtruj rezerwacje według daty:").pack(pady=10)

        tk.Label(filter_window, text="Od daty (RRRR-MM-DD):").pack(anchor="w", padx=20)
        start_date_filter = tk.Entry(filter_window, width=20)
        start_date_filter.pack(padx=20, pady=5)

        tk.Label(filter_window, text="Do daty (RRRR-MM-DD):").pack(anchor="w", padx=20)
        end_date_filter = tk.Entry(filter_window, width=20)
        end_date_filter.pack(padx=20, pady=5)

        def apply_filter():
            start_date = start_date_filter.get().strip()
            end_date = end_date_filter.get().strip()

            if not start_date or not end_date:
                messagebox.showerror("Błąd", "Obie daty są wymagane do filtrowania.")
                return

            filtered_bookings = [
                b for b in self.bookings
                if start_date <= b["start_date"] <= end_date
            ]

            if not filtered_bookings:
                messagebox.showinfo("Brak wyników", "Nie znaleziono żadnych rezerwacji w podanym zakresie dat.")
                return

            filtered_details = "\n\n".join([
                f"Imię i nazwisko: {b['name']}\n"
                f"E-mail: {b['email']}\n"
                f"Numer telefonu: {b['phone']}\n"
                f"Destynacja: {b['destination']}\n"
                f"Daty podróży: {b['start_date']} do {b['end_date']}\n"
                f"Uwagi specjalne: {b['special_requests']}"
                for b in filtered_bookings
            ])

            messagebox.showinfo("Wyniki filtrowania", filtered_details)

        tk.Button(filter_window, text="Zastosuj filtr", command=apply_filter).pack(pady=10)

    def edit_booking(self):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edytuj rezerwację")

        tk.Label(edit_window, text="Wprowadź nazwisko do edycji:").pack(pady=10)
        search_name_entry = tk.Entry(edit_window, width=40)
        search_name_entry.pack(padx=20, pady=5)

        def search_for_edit():
            search_name = search_name_entry.get().strip()
            matching_bookings = [b for b in self.bookings if b["name"] == search_name]

            if not matching_bookings:
                messagebox.showinfo("Brak wyników", "Nie znaleziono rezerwacji o podanym nazwisku.")
                return

            b = matching_bookings[0]  # Assuming first match for simplicity
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, b['name'])

            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, b['email'])

            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, b['phone'])

            self.start_date_entry.delete(0, tk.END)
            self.start_date_entry.insert(0, b['start_date'])

            self.end_date_entry.delete(0, tk.END)
            self.end_date_entry.insert(0, b['end_date'])

            self.special_requests_text.delete("1.0", tk.END)
            self.special_requests_text.insert("1.0", b['special_requests'])

            self.bookings.remove(b)
            messagebox.showinfo("Informacja", "Możesz edytować szczegóły i ponownie zapisać rezerwację.")

        tk.Button(edit_window, text="Wyszukaj", command=search_for_edit).pack(pady=10)

    def search_booking(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Szukaj rezerwacji")

        tk.Label(search_window, text="Wprowadź nazwisko do wyszukiwania:").pack(pady=10)
        search_name_entry = tk.Entry(search_window, width=40)
        search_name_entry.pack(padx=20, pady=5)

        def perform_search():
            search_name = search_name_entry.get().strip()
            matching_bookings = [
                b for b in self.bookings if search_name.lower() in b["name"].lower()
            ]

            if not matching_bookings:
                messagebox.showinfo("Brak wyników", "Nie znaleziono rezerwacji o podanym nazwisku.")
                return

            search_results = "\n\n".join([
                f"Imię i nazwisko: {b['name']}\n"
                f"E-mail: {b['email']}\n"
                f"Numer telefonu: {b['phone']}\n"
                f"Destynacja: {b['destination']}\n"
                f"Daty podróży: {b['start_date']} do {b['end_date']}\n"
                f"Uwagi specjalne: {b['special_requests']}"
                for b in matching_bookings
            ])

            messagebox.showinfo("Wyniki wyszukiwania", search_results)

        tk.Button(search_window, text="Szukaj", command=perform_search).pack(pady=10)

    def show_statistics(self):
        if not self.bookings:
            messagebox.showinfo("Brak danych", "Nie ma żadnych rezerwacji do analizy.")
            return

        destination_counts = {}
        for b in self.bookings:
            destination = b["destination"]
            destination_counts[destination] = destination_counts.get(destination, 0) + 1

        stats_message = "\n".join([f"{dest}: {count} rezerwacji" for dest, count in destination_counts.items()])

        messagebox.showinfo("Statystyki destynacji", stats_message)

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
