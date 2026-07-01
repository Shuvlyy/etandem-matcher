import os
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox, ttk

import customtkinter as ctk

import app_info
from exporter import export_results_to_excel
from matcher import Matcher
from student import load_students

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class ResultsViewer(ctk.CTkToplevel):
    def __init__(self, master, df):
        super().__init__(master)

        self.title("Match Results")
        self.geometry("1280x720")
        self.df = df

        # force the window to the front
        self.after(10, self.lift)

        self.title_lbl = ctk.CTkLabel(
            self, text="Generated Matches", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_lbl.pack(pady=10)

        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        # frame for the table and scrollbar
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # treeview creation
        columns = list(df.columns)
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        scrollbar = ttk.Scrollbar(
            self.table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", expand=True, fill="both")

        for col in columns:
            self.tree.heading(col, text=col)
            width = 300 if col == "Common Interests" else 150
            self.tree.column(col, width=width, anchor="center")

        for _, row in df.iterrows():
            self.tree.insert("", tk.END, values=list(row))

        self.btn_export = ctk.CTkButton(
            self,
            text="Export to Excel",
            command=self.export_data,
            fg_color="#27AE60",
            hover_color="#2ECC67",
        )
        self.btn_export.pack(pady=15)

    def export_data(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            initialfile="match_results.xlsx",
            title="Save results as...",
            filetypes=[("Excel files", "*.xlsx")],
        )

        if not save_path:
            return

        try:
            export_results_to_excel(self.df, save_path)
            messagebox.showinfo(
                "Success", f"File saved to:\n{os.path.basename(save_path)}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(app_info.APP_NAME)
        self.geometry("500x420")

        self.path_inter = None
        self.path_local = None

        # main title
        self.title_lbl = ctk.CTkLabel(
            self, text=app_info.APP_NAME, font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_lbl.pack(pady=20)

        # international students excel file select
        self.btn_inter = ctk.CTkButton(
            self, text="Select International students Excel", command=self.load_inter
        )
        self.btn_inter.pack(pady=10)
        self.lbl_inter = ctk.CTkLabel(self, text="No file selected", text_color="gray")
        self.lbl_inter.pack()

        # local students excel file select
        self.btn_local = ctk.CTkButton(
            self, text="Select Local students Excel", command=self.load_local
        )
        self.btn_local.pack(pady=10)
        self.lbl_local = ctk.CTkLabel(self, text="No file selected", text_color="gray")
        self.lbl_local.pack()

        # matches slider
        self.slider_lbl = ctk.CTkLabel(self, text="Matches per student: 1")
        self.slider_lbl.pack(pady=(20, 0))

        self.slider = ctk.CTkSlider(
            self, from_=1, to=5, number_of_steps=4, command=self.update_slider
        )
        self.slider.set(1)
        self.slider.pack(pady=10)

        # run button
        self.btn_run = ctk.CTkButton(
            self,
            text="Generate Matches",
            command=self.run_matcher,
            fg_color="#27AE60",
            hover_color="#2ECC71",
        )
        self.btn_run.pack(pady=20)

        # help button
        self.btn_help = ctk.CTkButton(
            self,
            text="?",
            width=30,
            height=30,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.open_guide,
        )
        self.btn_help.place(relx=0.95, rely=0.95, anchor="se")

        self.version_lbl = ctk.CTkLabel(
            self,
            text=f"v{app_info.APP_VERSION}, {app_info.APP_COPYRIGHT}",
            text_color="gray",
            font=("Arial", 10),
        )
        self.version_lbl.place(relx=0.02, rely=0.99, anchor="sw")

    def load_inter(self):
        path = filedialog.askopenfilename(
            filetypes=[("Excel", "*.xlsx *.xls"), ("CSV Files", "*.csv")]
        )
        if path:
            self.path_inter = path
            self.lbl_inter.configure(text=os.path.basename(path), text_color="white")

    def load_local(self):
        path = filedialog.askopenfilename(
            filetypes=[("Excel", "*.xlsx *.xls"), ("CSV Files", "*.csv")]
        )
        if path:
            self.path_local = path
            self.lbl_local.configure(text=os.path.basename(path), text_color="white")

    def update_slider(self, val):
        self.slider_lbl.configure(text=f"Matches per student: {int(val)}")

    def open_guide(self):
        try:
            webbrowser.open(
                "https://github.com/Shuvlyy/etandem-matcher/blob/master/README.md"
            )
        except Exception as e:
            messagebox.showerror(":(", f"Something went wrong: {str(e)}")

    def run_matcher(self):
        # basic checks
        if not self.path_inter or not self.path_local:
            messagebox.showerror("Error", "Please select both Excel files first.")
            return

        self.btn_run.configure(text="Processing...", state="disabled")
        self.update()

        try:
            inter_students = load_students(self.path_inter, is_international=True)
            local_students = load_students(self.path_local, is_international=False)

            matcher = Matcher(inter_students, local_students)
            top_n = int(self.slider.get())
            results_df = matcher.get_top_matches(top_n=top_n)

            ResultsViewer(self, results_df)

        except Exception as e:
            messagebox.showerror(":(", f"Something went wrong:\n{e}")

        finally:
            self.btn_run.configure(text="Compute Matches", state="normal")
