import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class WydatkiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Wydatkometr 2.0 - Analiza Boxplot")
        self.df = pd.DataFrame(columns=["Data", "Kategoria", "Kwota"])

        # Ramka górna - przyciski
        top_frame = ttk.Frame(root)
        top_frame.pack(pady=10)

        ttk.Button(top_frame, text="📂 Wczytaj CSV", command=self.load_data).grid(row=0, column=0, padx=5)
        ttk.Button(top_frame, text="💾 Zapisz CSV", command=self.save_data).grid(row=0, column=1, padx=5)
        ttk.Button(top_frame, text="📊 Generuj Boxplot", command=self.generate_plot).grid(row=0, column=2, padx=5)

        # Tabela danych
        self.tree = ttk.Treeview(root, columns=("Data", "Kategoria", "Kwota"), show='headings', height=8)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')
        self.tree.pack(pady=5)

        # Formularz dodawania danych
        form_frame = ttk.LabelFrame(root, text="➕ Dodaj wydatek")
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Data (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=2)
        self.entry_date = ttk.Entry(form_frame)
        self.entry_date.grid(row=0, column=1, padx=5)

        ttk.Label(form_frame, text="Kategoria:").grid(row=1, column=0, padx=5, pady=2)
        self.entry_category = ttk.Entry(form_frame)
        self.entry_category.grid(row=1, column=1, padx=5)

        ttk.Label(form_frame, text="Kwota:").grid(row=2, column=0, padx=5, pady=2)
        self.entry_amount = ttk.Entry(form_frame)
        self.entry_amount.grid(row=2, column=1, padx=5)

        ttk.Button(form_frame, text="Dodaj", command=self.add_record).grid(row=3, column=0, columnspan=2, pady=5)

        # Dropdown do boxplota
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(root, textvariable=self.category_var, state="readonly")
        self.category_menu.pack(pady=5)

        # Canvas na wykres
        self.canvas = None

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df = pd.read_csv(file_path)
            self.refresh_table()
            self.update_categories()

    def save_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv")
        if file_path:
            self.df.to_csv(file_path, index=False)
            messagebox.showinfo("Zapisano", "Dane zapisane pomyślnie!")

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for _, row in self.df.iterrows():
            self.tree.insert("", tk.END, values=list(row))

    def update_categories(self):
        categories = self.df["Kategoria"].unique().tolist()
        self.category_menu["values"] = categories
        if categories:
            self.category_menu.set(categories[0])

    def add_record(self):
        date = self.entry_date.get()
        category = self.entry_category.get()
        amount = self.entry_amount.get()
        try:
            amount = float(amount)
            new_row = pd.DataFrame([[date, category, amount]], columns=["Data", "Kategoria", "Kwota"])
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            self.refresh_table()
            self.update_categories()
            self.entry_date.delete(0, tk.END)
            self.entry_category.delete(0, tk.END)
            self.entry_amount.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Błąd", "Podaj poprawną kwotę!")

    def generate_plot(self):
        if self.df.empty:
            return

        selected_category = self.category_var.get()
        if selected_category not in self.df["Kategoria"].unique():
            return

        filtered = self.df[self.df["Kategoria"] == selected_category]

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.boxplot(filtered["Kwota"])
        ax.set_title(f"Boxplot - {selected_category}")
        ax.set_ylabel("Kwota [PLN]")

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

# Start aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    app = WydatkiApp(root)
    root.mainloop()