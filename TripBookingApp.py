import tkinter as tk
from tkinter import messagebox, ttk
import os
import json

class TripBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Rezerwacji Wycieczek")
        self.root.geometry("1000x800")

        # Dane użytkowników (logowanie)
        self.users = {"admin": "admin123", "user": "user123"}
        self.current_user = None

        # Dane wycieczek (przykładowe)
        self.trips = [
            {"name": "Paryż - Miasto Miłości", "price": 3000, "availability": 10, "details": "4 dni, 3 noce. Wycieczka z przewodnikiem."},
            {"name": "Wenecja - Romantyczne Kanały", "price": 2500, "availability": 5, "details": "3 dni, 2 noce. Rejs gondolą."},
            {"name": "Egipt - Piramidy i Plaże", "price": 4000, "availability": 8, "details": "7 dni, 6 nocy. All Inclusive."},
        ]
        self.bookings = []

        # Plik z historią rezerwacji
        self.history_file = "bookings.json"
        self.trips_file = "trips.json"

        self.load_data()

        # Rozpocznij od ekranu logowania
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Logowanie", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Label(self.root, text="Nazwa użytkownika:").pack(pady=5)
        self.username_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.username_var).pack(pady=5)

        tk.Label(self.root, text="Hasło:").pack(pady=5)
        self.password_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.password_var, show="*").pack(pady=5)

        tk.Button(self.root, text="Zaloguj", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if username in self.users and self.users[username] == password:
            self.current_user = username
            messagebox.showinfo("Sukces", "Zalogowano pomyślnie!")
            self.create_main_screen()
        else:
            messagebox.showerror("Błąd", "Nieprawidłowa nazwa użytkownika lub hasło.")

    def create_main_screen(self):
        self.clear_screen()

        # Nagłówek
        tk.Label(self.root, text=f"Witaj, {self.current_user}!", font=("Arial", 18, "bold")).pack(pady=10)

        # Przycisk wylogowania
        tk.Button(self.root, text="Wyloguj", command=self.logout).pack(pady=5)

        # Pole wyszukiwania i filtrowania
        self.create_widgets()

    def logout(self):
        self.current_user = None
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_widgets(self):
        # Pole wyszukiwania i filtrowania
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Szukaj wycieczki:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Szukaj", command=self.search_trip).pack(side=tk.LEFT, padx=5)

        tk.Label(search_frame, text="Cena od:").pack(side=tk.LEFT, padx=5)
        self.price_min_var = tk.IntVar(value=0)
        tk.Entry(search_frame, textvariable=self.price_min_var, width=10).pack(side=tk.LEFT)

        tk.Label(search_frame, text="Cena do:").pack(side=tk.LEFT, padx=5)
        self.price_max_var = tk.IntVar(value=10000)
        tk.Entry(search_frame, textvariable=self.price_max_var, width=10).pack(side=tk.LEFT)
        tk.Button(search_frame, text="Filtruj", command=self.filter_trips).pack(side=tk.LEFT, padx=5)

        # Lista wycieczek
        self.trip_tree = ttk.Treeview(self.root, columns=("name", "price", "availability"), show="headings")
        self.trip_tree.heading("name", text="Nazwa wycieczki")
        self.trip_tree.heading("price", text="Cena (PLN)")
        self.trip_tree.heading("availability", text="Dostępność (osoby)")
        self.trip_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.refresh_trip_list()

        # Przyciski administratora
        if self.current_user == "admin":
            admin_frame = tk.Frame(self.root)
            admin_frame.pack(pady=10)

            tk.Button(admin_frame, text="Dodaj wycieczkę", command=self.add_trip_window).pack(side=tk.LEFT, padx=5)
            tk.Button(admin_frame, text="Edytuj wycieczkę", command=self.edit_trip_window).pack(side=tk.LEFT, padx=5)

    def search_trip(self):
        query = self.search_var.get().lower()
        for item in self.trip_tree.get_children():
            self.trip_tree.delete(item)

        for trip in self.trips:
            if query in trip["name"].lower():
                self.trip_tree.insert("", tk.END, values=(trip["name"], trip["price"], trip["availability"]))

    def filter_trips(self):
        price_min = self.price_min_var.get()
        price_max = self.price_max_var.get()

        for item in self.trip_tree.get_children():
            self.trip_tree.delete(item)

        for trip in self.trips:
            if price_min <= trip["price"] <= price_max:
                self.trip_tree.insert("", tk.END, values=(trip["name"], trip["price"], trip["availability"]))

    def add_trip_window(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Dodaj nową wycieczkę")

        tk.Label(new_window, text="Nazwa wycieczki:").grid(row=0, column=0, padx=5, pady=5)
        name_var = tk.StringVar()
        tk.Entry(new_window, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(new_window, text="Cena (PLN):").grid(row=1, column=0, padx=5, pady=5)
        price_var = tk.IntVar()
        tk.Entry(new_window, textvariable=price_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(new_window, text="Dostępność:").grid(row=2, column=0, padx=5, pady=5)
        availability_var = tk.IntVar()
        tk.Entry(new_window, textvariable=availability_var).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(new_window, text="Szczegóły:").grid(row=3, column=0, padx=5, pady=5)
        details_var = tk.StringVar()
        tk.Entry(new_window, textvariable=details_var).grid(row=3, column=1, padx=5, pady=5)

        def add_trip():
            new_trip = {
                "name": name_var.get(),
                "price": price_var.get(),
                "availability": availability_var.get(),
                "details": details_var.get()
            }
            self.trips.append(new_trip)
            self.refresh_trip_list()
            self.save_data()
            new_window.destroy()

        tk.Button(new_window, text="Dodaj", command=add_trip).grid(row=4, column=0, columnspan=2, pady=10)

    def edit_trip_window(self):
        selected_item = self.trip_tree.selection()
        if not selected_item:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać wycieczkę do edycji!")
            return

        trip_index = self.trip_tree.index(selected_item[0])
        trip = self.trips[trip_index]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edytuj wycieczkę")

        tk.Label(edit_window, text="Nazwa wycieczki:").grid(row=0, column=0, padx=5, pady=5)
        name_var = tk.StringVar(value=trip["name"])
        tk.Entry(edit_window, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(edit_window, text="Cena (PLN):").grid(row=1, column=0, padx=5, pady=5)
        price_var = tk.IntVar(value=trip["price"])
        tk.Entry(edit_window, textvariable=price_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(edit_window, text="Dostępność:").grid(row=2, column=0, padx=5, pady=5)
        availability_var = tk.IntVar(value=trip["availability"])
        tk.Entry(edit_window, textvariable=availability_var).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(edit_window, text="Szczegóły:").grid(row=3, column=0, padx=5, pady=5)
        details_var = tk.StringVar(value=trip["details"])
        tk.Entry(edit_window, textvariable=details_var).grid(row=3, column=1, padx=5, pady=5)

        def save_changes():
            trip["name"] = name_var.get()
            trip["price"] = price_var.get()
            trip["availability"] = availability_var.get()
            trip["details"] = details_var.get()
            self.refresh_trip_list()
            self.save_data()
            edit_window.destroy()

        tk.Button(edit_window, text="Zapisz zmiany", command=save_changes).grid(row=4, column=0, columnspan=2, pady=10)

    def refresh_trip_list(self):
        for item in self.trip_tree.get_children():
            self.trip_tree.delete(item)

        for trip in self.trips:
            self.trip_tree.insert("", tk.END, values=(trip["name"], trip["price"], trip["availability"]))

    def save_data(self):
        # Zapisuje dane wycieczek i historii rezerwacji do plików JSON
        with open(self.trips_file, "w") as f:
            json.dump(self.trips, f, ensure_ascii=False, indent=4)

        with open(self.history_file, "w") as f:
            json.dump(self.bookings, f, ensure_ascii=False, indent=4)

    def load_data(self):
        # Ładuje dane wycieczek i historii rezerwacji z plików JSON (jeśli istnieją)
        if os.path.exists(self.trips_file):
            with open(self.trips_file, "r") as f:
                self.trips = json.load(f)

        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                self.bookings = json.load(f)


# Uruchomienie aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    app = TripBookingApp(root)
    root.mainloop()
