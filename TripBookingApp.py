import tkinter as tk
from tkinter import ttk, messagebox

class ReservationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("System Rezerwacji Wycieczek")

        # Przechowywanie danych o wycieczkach i rezerwacjach
        self.trips = [
            {"id": 1, "name": "Góry", "price": 1200, "spots": 10},
            {"id": 2, "name": "Morze", "price": 800, "spots": 15},
            {"id": 3, "name": "Mazury", "price": 1000, "spots": 8}
        ]
        self.reservations = []

        # Interfejs aplikacji
        self.create_widgets()

    def create_widgets(self):
        # Nagłówek
        header = tk.Label(self.root, text="System Rezerwacji Wycieczek", font=("Arial", 18, "bold"))
        header.pack(pady=10)

        # Lista wycieczek
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Price", "Spots"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Nazwa")
        self.tree.heading("Price", text="Cena (zł)")
        self.tree.heading("Spots", text="Wolne miejsca")

        for trip in self.trips:
            self.tree.insert("", tk.END, values=(trip["id"], trip["name"], trip["price"], trip["spots"]))

        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Sekcja rezerwacji
        reservation_frame = tk.Frame(self.root)
        reservation_frame.pack(pady=10)

        tk.Label(reservation_frame, text="ID Wycieczki:").grid(row=0, column=0, padx=5, pady=5)
        self.trip_id_entry = ttk.Entry(reservation_frame)
        self.trip_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(reservation_frame, text="Imię i nazwisko:").grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(reservation_frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(reservation_frame, text="Liczba miejsc:").grid(row=2, column=0, padx=5, pady=5)
        self.spots_entry = ttk.Entry(reservation_frame)
        self.spots_entry.grid(row=2, column=1, padx=5, pady=5)

        reserve_button = ttk.Button(reservation_frame, text="Zarezerwuj", command=self.reserve_trip)
        reserve_button.grid(row=3, columnspan=2, pady=10)

        # Sekcja zarządzania wycieczkami
        manage_frame = tk.Frame(self.root)
        manage_frame.pack(pady=10)

        tk.Label(manage_frame, text="Nazwa wycieczki:").grid(row=0, column=0, padx=5, pady=5)
        self.new_trip_name = ttk.Entry(manage_frame)
        self.new_trip_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(manage_frame, text="Cena (zł):").grid(row=1, column=0, padx=5, pady=5)
        self.new_trip_price = ttk.Entry(manage_frame)
        self.new_trip_price.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(manage_frame, text="Liczba miejsc:").grid(row=2, column=0, padx=5, pady=5)
        self.new_trip_spots = ttk.Entry(manage_frame)
        self.new_trip_spots.grid(row=2, column=1, padx=5, pady=5)

        add_trip_button = ttk.Button(manage_frame, text="Dodaj wycieczkę", command=self.add_trip)
        add_trip_button.grid(row=3, columnspan=2, pady=10)

        # Sekcja rezerwacji
        view_reservations_button = ttk.Button(self.root, text="Pokaż rezerwacje", command=self.view_reservations)
        view_reservations_button.pack(pady=10)

        # Eksport danych
        export_button = ttk.Button(self.root, text="Eksportuj rezerwacje", command=self.export_reservations)
        export_button.pack(pady=10)

        # Usuwanie rezerwacji
        delete_reservation_button = ttk.Button(self.root, text="Usuń rezerwację", command=self.delete_reservation)
        delete_reservation_button.pack(pady=10)

        # Modyfikowanie wycieczek
        modify_trip_button = ttk.Button(self.root, text="Modyfikuj wycieczkę", command=self.modify_trip)
        modify_trip_button.pack(pady=10)

        # Statystyki wycieczek
        stats_button = ttk.Button(self.root, text="Pokaż statystyki", command=self.show_statistics)
        stats_button.pack(pady=10)

    def reserve_trip(self):
        try:
            trip_id = int(self.trip_id_entry.get())
            name = self.name_entry.get().strip()
            spots = int(self.spots_entry.get())

            if not name:
                raise ValueError("Imię i nazwisko nie może być puste.")

            trip = next((t for t in self.trips if t["id"] == trip_id), None)
            if not trip:
                raise ValueError("Wycieczka o podanym ID nie istnieje.")

            if spots <= 0 or spots > trip["spots"]:
                raise ValueError(f"Nieprawidłowa liczba miejsc. Dostępnych miejsc: {trip['spots']}.")

            # Aktualizacja danych
            trip["spots"] -= spots
            self.reservations.append({"trip_id": trip_id, "name": name, "spots": spots})

            # Odświeżenie tabeli
            self.update_tree()

            messagebox.showinfo("Sukces", f"Rezerwacja dla {name} zakończona powodzeniem!")

            # Czyszczenie pól
            self.trip_id_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.spots_entry.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Błąd", str(e))

    def add_trip(self):
        try:
            name = self.new_trip_name.get().strip()
            price = float(self.new_trip_price.get())
            spots = int(self.new_trip_spots.get())

            if not name:
                raise ValueError("Nazwa wycieczki nie może być pusta.")

            if price <= 0 or spots <= 0:
                raise ValueError("Cena i liczba miejsc muszą być dodatnie.")

            new_trip = {
                "id": max(t["id"] for t in self.trips) + 1,
                "name": name,
                "price": price,
                "spots": spots
            }

            self.trips.append(new_trip)
            self.update_tree()

            messagebox.showinfo("Sukces", "Wycieczka dodana pomyślnie!")

            # Czyszczenie pól
            self.new_trip_name.delete(0, tk.END)
            self.new_trip_price.delete(0, tk.END)
            self.new_trip_spots.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Błąd", str(e))

    def delete_reservation(self):
        try:
            name = self.name_entry.get().strip()

            if not name:
                raise ValueError("Podaj imię i nazwisko, aby usunąć rezerwację.")

            reservation = next((r for r in self.reservations if r["name"] == name), None)

            if not reservation:
                raise ValueError("Rezerwacja dla podanego imienia nie istnieje.")

            trip = next(t for t in self.trips if t["id"] == reservation["trip_id"])
            trip["spots"] += reservation["spots"]

            self.reservations.remove(reservation)
            self.update_tree()

            messagebox.showinfo("Sukces", "Rezerwacja została usunięta.")
        except ValueError as e:
            messagebox.showerror("Błąd", str(e))

    def modify_trip(self):
        try:
            trip_id = int(self.trip_id_entry.get())
            name = self.new_trip_name.get().strip()
            price = float(self.new_trip_price.get())
            spots = int(self.new_trip_spots.get())

            trip = next((t for t in self.trips if t["id"] == trip_id), None)
            if not trip:
                raise ValueError("Wycieczka o podanym ID nie istnieje.")

            if not name:
                raise ValueError("Nazwa wycieczki nie może być pusta.")

            if price <= 0 or spots < 0:
                raise ValueError("Cena i liczba miejsc muszą być prawidłowe.")

            trip["name"] = name
            trip["price"] = price
            trip["spots"] = spots

            self.update_tree()

            messagebox.showinfo("Sukces", "Wycieczka została zmodyfikowana.")
        except ValueError as e:
            messagebox.showerror("Błąd", str(e))

    def show_statistics(self):
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Statystyki Wycieczek")

        total_trips = len(self.trips)
        total_reservations = len(self.reservations)
        total_spots = sum(trip["spots"] for trip in self.trips)

        tk.Label(stats_window, text=f"Łączna liczba wycieczek: {total_trips}").pack(pady=10)
        tk.Label(stats_window, text=f"Łączna liczba rezerwacji: {total_reservations}").pack(pady=10)
        tk.Label(stats_window, text=f"Łączna liczba dostępnych miejsc: {total_spots}").pack(pady=10)

    def update_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for trip in self.trips:
            self.tree.insert("", tk.END, values=(trip["id"], trip["name"], trip["price"], trip["spots"]))

    def view_reservations(self):
        reservations_window = tk.Toplevel(self.root)
        reservations_window.title("Lista Rezerwacji")

        tree = ttk.Treeview(reservations_window, columns=("TripID", "Name", "Spots"), show="headings")
        tree.heading("TripID", text="ID Wycieczki")
        tree.heading("Name", text="Imię i nazwisko")
        tree.heading("Spots", text="Liczba miejsc")

        for res in self.reservations:
            tree.insert("", tk.END, values=(res["trip_id"], res["name"], res["spots"]))

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def export_reservations(self):
        try:
            with open("reservations.csv", "w", encoding="utf-8") as file:
                file.write("TripID,Name,Spots\n")
                for res in self.reservations:
                    file.write(f"{res['trip_id']},{res['name']},{res['spots']}\n")

            messagebox.showinfo("Sukces", "Rezerwacje zostały wyeksportowane do pliku reservations.csv")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił problem podczas eksportu: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReservationSystem(root)
    root.geometry("600x700")
    root.mainloop()
