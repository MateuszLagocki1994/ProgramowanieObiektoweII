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

    def update_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for trip in self.trips:
            self.tree.insert("", tk.END, values=(trip["id"], trip["name"], trip["price"], trip["spots"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = ReservationSystem(root)
    root.geometry("600x400")
    root.mainloop()
