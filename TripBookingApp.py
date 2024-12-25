import tkinter as tk
from tkinter import messagebox, ttk


class TripBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Rezerwacji Wycieczek")
        self.root.geometry("800x600")

        # Dane wycieczek (przykładowe)
        self.trips = [
            {"name": "Paryż - Miasto Miłości", "price": 3000, "availability": 10},
            {"name": "Wenecja - Romantyczne Kanały", "price": 2500, "availability": 5},
            {"name": "Egipt - Piramidy i Plaże", "price": 4000, "availability": 8},
        ]
        self.bookings = []

        # Interfejs użytkownika
        self.create_widgets()

    def create_widgets(self):
        # Nagłówek
        tk.Label(self.root, text="System Rezerwacji Wycieczek", font=("Arial", 18, "bold")).pack(pady=10)

        # Lista dostępnych wycieczek
        self.trip_tree = ttk.Treeview(self.root, columns=("name", "price", "availability"), show="headings")
        self.trip_tree.heading("name", text="Nazwa wycieczki")
        self.trip_tree.heading("price", text="Cena (PLN)")
        self.trip_tree.heading("availability", text="Dostępność (osoby)")
        self.trip_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        for trip in self.trips:
            self.trip_tree.insert("", tk.END, values=(trip["name"], trip["price"], trip["availability"]))

        # Pole wyboru liczby osób
        tk.Label(self.root, text="Liczba osób:").pack(pady=5)
        self.num_people_var = tk.IntVar(value=1)
        self.num_people_spinbox = tk.Spinbox(self.root, from_=1, to=10, textvariable=self.num_people_var, width=5)
        self.num_people_spinbox.pack()

        # Przycisk rezerwacji
        self.book_button = tk.Button(self.root, text="Zarezerwuj", command=self.book_trip)
        self.book_button.pack(pady=10)

        # Historia rezerwacji
        tk.Label(self.root, text="Historia Rezerwacji:", font=("Arial", 14)).pack(pady=10)
        self.booking_listbox = tk.Listbox(self.root, height=10)
        self.booking_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def book_trip(self):
        selected_item = self.trip_tree.selection()
        if not selected_item:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać wycieczkę!")
            return

        trip_index = self.trip_tree.index(selected_item[0])
        trip = self.trips[trip_index]
        num_people = self.num_people_var.get()

        if num_people > trip["availability"]:
            messagebox.showerror("Błąd", f"Niewystarczająca dostępność! Pozostało miejsc: {trip['availability']}.")
            return

        trip["availability"] -= num_people
        self.trip_tree.item(selected_item, values=(trip["name"], trip["price"], trip["availability"]))

        booking_info = f"{trip['name']} - {num_people} osoby/osób - {trip['price'] * num_people} PLN"
        self.bookings.append(booking_info)
        self.booking_listbox.insert(tk.END, booking_info)

        messagebox.showinfo("Sukces", "Rezerwacja zakończona pomyślnie!")


if __name__ == "__main__":
    root = tk.Tk()
    app = TripBookingApp(root)
    root.mainloop()
