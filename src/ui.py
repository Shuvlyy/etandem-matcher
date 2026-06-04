import os
from tkinter import filedialog, messagebox

import customtkinter as ctk

from exporter import export_results_to_excel
from matcher import Matcher
from student import load_students

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("E-Tandem Matcher")
        self.geometry("500x420")

        self.path_inter = None
        self.path_local = None

        # main title
        self.title_lbl = ctk.CTkLabel(
            self, text="E-Tandem Matcher", font=ctk.CTkFont(size=20, weight="bold")
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
        self.slider_lbl = ctk.CTkLabel(self, text="Matches per student: 3")
        self.slider_lbl.pack(pady=(20, 0))

        self.slider = ctk.CTkSlider(
            self, from_=1, to=5, number_of_steps=4, command=self.update_slider
        )
        self.slider.set(3)
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

    def load_inter(self):
        path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx *.xls")])
        if path:
            self.path_inter = path
            self.lbl_inter.configure(text=os.path.basename(path), text_color="white")

    def load_local(self):
        path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx *.xls")])
        if path:
            self.path_local = path
            self.lbl_local.configure(text=os.path.basename(path), text_color="white")

    def update_slider(self, val):
        self.slider_lbl.configure(text=f"Matches per student: {int(val)}")

    def run_matcher(self):
        # basic checks
        if not self.path_inter or not self.path_local:
            messagebox.showerror("Error", "Please select both Excel files first.")
            return

        # ask where to save
        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            initialfile="match_results.xlsx",
            title="Save results as...",
            filetypes=[("Excel files", "*.xlsx")],
        )

        if not save_path:
            return

        self.btn_run.configure(text="Processing...", state="disabled")
        self.update()

        try:
            internationals = load_students(self.path_inter, is_international=True)
            locals_students = load_students(self.path_local, is_international=False)

            matcher = Matcher(internationals, locals_students)
            top_n = int(self.slider.get())
            results_df = matcher.get_top_matches(top_n=top_n)

            export_results_to_excel(results_df, save_path)

            messagebox.showinfo(
                "Success", f"File saved to:\n{os.path.basename(save_path)}"
            )

        except Exception as e:
            messagebox.showerror(":(", f"Something went wrong:\n{e}")

        finally:
            self.btn_run.configure(text="Compute Matches", state="normal")
