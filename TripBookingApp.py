import tkinter as tk
from tkinter import messagebox, ttk
import os
import json


class TripBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Rezerwacji Wycieczek")
        self.root.geometry("900x700")

        # Dane wycieczek (przykładowe)
        self.trips = [
            {"name": "Paryż - Miasto Miłości", "price": 3000, "availability": 10, "details": "4 dni, 3 noce. Wycieczka z przewodnikiem."},
            {"name": "Wenecja - Romantyczne Kanały", "price": 2500, "availability": 5, "details": "3 dni, 2 noce. Rejs gondolą."},
            {"name": "Egipt - Piramidy i Plaże", "price": 4000, "availability": 8, "details": "7 dni, 6 nocy. All Inclusive."},
        ]
        self.bookings = []

        # Plik z historią rezerwacji
        self.history_file = "bookings.json"
        self.load_bookings()

        # Interfejs użytkownika
        self.create_widgets()

    def create_widgets(self):
        # Nagłówek
        tk.Label(self.root, text="System Rezerwacji Wycieczek", font=("Arial", 18, "bold")).pack(pady=10)

        # Pole wyszukiwania
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Szukaj wycieczki:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Szukaj", command=self.search_trip).pack(side=tk.LEFT)

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

        # Szczegóły wycieczki
        tk.Button(self.root, text="Szczegóły wycieczki", command=self.show_trip_details).pack(pady=5)

        # Historia rezerwacji
        tk.Label(self.root, text="Historia Rezerwacji:", font=("Arial", 14)).pack(pady=10)
        self.booking_listbox = tk.Listbox(self.root, height=10)
        self.booking_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Podsumowanie finansowe
        tk.Button(self.root, text="Podsumowanie finansowe", command=self.show_financial_summary).pack(pady=5)

    def search_trip(self):
        query = self.search_var.get().lower()
        for item in self.trip_tree.get_children():
            self.trip_tree.delete(item)

        for trip in self.trips:
            if query in trip["name"].lower():
                self.trip_tree.insert("", tk.END, values=(trip["name"], trip["price"], trip["availability"]))

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
        self.save_bookings()

        messagebox.showinfo("Sukces", "Rezerwacja zakończona pomyślnie!")

    def show_trip_details(self):
        selected_item = self.trip_tree.selection()
        if not selected_item:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać wycieczkę!")
            return

        trip_index = self.trip_tree.index(selected_item[0])
        trip = self.trips[trip_index]
        details = f"Nazwa: {trip['name']}\nCena: {trip['price']} PLN\nDostępność: {trip['availability']} osoby/osób\nSzczegóły: {trip['details']}"
        messagebox.showinfo("Szczegóły wycieczki", details)

    def show_financial_summary(self):
        total = 0
        for booking in self.bookings:
            price = int(booking.split("-")[-1].strip().split()[0])
            total += price

        messagebox.showinfo("Podsumowanie finansowe", f"Łączna wartość rezerwacji: {total} PLN")

    def save_bookings(self):
        with open(self.history_file, "w") as file:
            json.dump(self.bookings, file)

    def load_bookings(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as file:
                self.bookings = json.load(file)


if __name__ == "__main__":
    root = tk.Tk()
    app = TripBookingApp(root)
    root.mainloop()
