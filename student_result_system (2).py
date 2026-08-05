"""
Student Result System
----------------------
A simple desktop GUI app built with Tkinter that lets you:
- Add / update student records (Name, Roll No, Class, Marks)
- View all records in a result table
- Automatically shows Pass/Fail for each student
- Shows totals: Total Students, Passed, Failed

Run with:  python student_result_system.py
(Tkinter ships with standard Python on Windows/Mac. On Linux you may need:
 sudo apt-get install python3-tk )
"""

import tkinter as tk
from tkinter import ttk, messagebox

PASS_MARK = 40  # marks >= this value counts as "Pass"

# ---------- Colors (matching the reference design) ----------
PURPLE_DARK = "#F504A5"
PURPLE_HEADER = "#01837A"
PURPLE_LIGHT = "#F3EEFB"
PURPLE_ACCENT = "#B809F8"
WHITE = "#FFFFFF"
GREEN = "#1E8E3E"
RED = "#D93025"
TEXT_DARK = "#2B2B2B"


class StudentResultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result System")
        self.root.geometry("420x680")
        self.root.configure(bg=PURPLE_LIGHT)
        self.root.resizable(False, False)

        # In-memory storage: roll_no -> {name, class, marks}
        self.students = {}

        self._build_header()
        self._build_form()
        self._build_table_section()
        self._build_summary()

        self.refresh_table()

    # ---------------------------------------------------------
    def _build_header(self):
        header = tk.Frame(self.root, bg=PURPLE_HEADER, height=60)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🎓  Student Result System",
            bg=PURPLE_HEADER,
            fg=WHITE,
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=15)

    # ---------------------------------------------------------
    def _build_form(self):
        form_card = tk.Frame(self.root, bg=WHITE, bd=0, highlightbackground="#DDD",
                              highlightthickness=1)
        form_card.pack(fill="x", padx=15, pady=15)

        pad = {"padx": 15, "pady": (10, 0)}

        tk.Label(form_card, text="Enter Name:", bg=WHITE, fg=TEXT_DARK,
                 font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", **pad)
        self.name_var = tk.StringVar()
        tk.Entry(form_card, textvariable=self.name_var, font=("Segoe UI", 10),
                 relief="solid", bd=1).grid(row=0, column=1, sticky="ew", padx=(0, 15), pady=(10, 0))

        tk.Label(form_card, text="Enter Roll No:", bg=WHITE, fg=TEXT_DARK,
                 font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", **pad)
        self.roll_var = tk.StringVar()
        tk.Entry(form_card, textvariable=self.roll_var, font=("Segoe UI", 10),
                 relief="solid", bd=1).grid(row=1, column=1, sticky="ew", padx=(0, 15), pady=(10, 0))

        tk.Label(form_card, text="Class:", bg=WHITE, fg=TEXT_DARK,
                 font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", **pad)
        self.class_var = tk.StringVar()
        tk.Entry(form_card, textvariable=self.class_var, font=("Segoe UI", 10),
                 relief="solid", bd=1).grid(row=2, column=1, sticky="ew", padx=(0, 15), pady=(10, 0))

        tk.Label(form_card, text="Marks:", bg=WHITE, fg=TEXT_DARK,
                 font=("Segoe UI", 10)).grid(row=3, column=0, sticky="w", **pad)
        self.marks_var = tk.StringVar()
        tk.Entry(form_card, textvariable=self.marks_var, font=("Segoe UI", 10),
                 relief="solid", bd=1).grid(row=3, column=1, sticky="ew", padx=(0, 15), pady=(10, 0))

        form_card.grid_columnconfigure(1, weight=1)

        btn = tk.Button(
            form_card, text="Add / Update", bg=PURPLE_ACCENT, fg=WHITE,
            font=("Segoe UI", 10, "bold"), relief="flat", bd=0,
            activebackground=PURPLE_DARK, activeforeground=WHITE,
            cursor="hand2", command=self.add_or_update_student,
        )
        btn.grid(row=4, column=0, columnspan=2, sticky="ew", padx=15, pady=15, ipady=6)

    # ---------------------------------------------------------
    def _build_table_section(self):
        tk.Label(self.root, text="Result List", bg=PURPLE_LIGHT, fg=PURPLE_DARK,
                 font=("Segoe UI", 12, "bold")).pack(pady=(0, 8))

        table_frame = tk.Frame(self.root, bg=WHITE)
        table_frame.pack(fill="both", expand=True, padx=15)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background=PURPLE_ACCENT, foreground=WHITE,
                         font=("Segoe UI", 9, "bold"), relief="flat")
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 9),
                         background=WHITE, fieldbackground=WHITE)
        style.map("Treeview", background=[("selected", "#E4D9F7")])

        columns = ("name", "roll", "marks", "result")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        self.tree.heading("name", text="Name")
        self.tree.heading("roll", text="Roll No.")
        self.tree.heading("marks", text="Marks")
        self.tree.heading("result", text="Result")

        self.tree.column("name", width=110, anchor="center")
        self.tree.column("roll", width=70, anchor="center")
        self.tree.column("marks", width=70, anchor="center")
        self.tree.column("result", width=70, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.tree.tag_configure("pass", foreground=GREEN)
        self.tree.tag_configure("fail", foreground=RED)

        self.tree.bind("<Double-1>", self.load_selected_into_form)

        # Delete button
        del_btn = tk.Button(
            self.root, text="Delete Selected", bg="#EDEDED", fg=TEXT_DARK,
            font=("Segoe UI", 9), relief="flat", cursor="hand2",
            command=self.delete_selected,
        )
        del_btn.pack(pady=8)

    # ---------------------------------------------------------
    def _build_summary(self):
        summary_card = tk.Frame(self.root, bg=PURPLE_LIGHT, highlightbackground="#DDD",
                                 highlightthickness=1)
        summary_card.pack(fill="x", padx=15, pady=(0, 15))

        self.total_label = tk.Label(summary_card, text="Total Students: 0",
                                     bg=PURPLE_LIGHT, fg=TEXT_DARK, font=("Segoe UI", 10, "bold"))
        self.total_label.pack(pady=(10, 2))

        self.passed_label = tk.Label(summary_card, text="Passed: 0",
                                      bg=PURPLE_LIGHT, fg=GREEN, font=("Segoe UI", 10, "bold"))
        self.passed_label.pack(pady=2)

        self.failed_label = tk.Label(summary_card, text="Failed: 0",
                                      bg=PURPLE_LIGHT, fg=RED, font=("Segoe UI", 10, "bold"))
        self.failed_label.pack(pady=(2, 10))

    # ---------------------------------------------------------
    def add_or_update_student(self):
        name = self.name_var.get().strip()
        roll = self.roll_var.get().strip()
        cls = self.class_var.get().strip()
        marks = self.marks_var.get().strip()

        if not name or not roll or not cls or not marks:
            messagebox.showwarning("Missing Data", "Please fill in all fields.")
            return

        try:
            marks_val = float(marks)
        except ValueError:
            messagebox.showwarning("Invalid Marks", "Marks must be a number.")
            return

        self.students[roll] = {"name": name, "class": cls, "marks": marks_val}

        self.name_var.set("")
        self.roll_var.set("")
        self.class_var.set("")
        self.marks_var.set("")

        self.refresh_table()

    def load_selected_into_form(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        name, roll, marks, _ = values
        record = self.students.get(roll)
        if record:
            self.name_var.set(name)
            self.roll_var.set(roll)
            self.class_var.set(record["class"])
            self.marks_var.set(str(record["marks"]))

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Select a row to delete.")
            return
        values = self.tree.item(selected[0], "values")
        roll = values[1]
        if roll in self.students:
            del self.students[roll]
        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        passed = 0
        failed = 0

        # Sort by roll number for stable display
        for roll, data in sorted(self.students.items(), key=lambda x: x[0]):
            result = "Pass" if data["marks"] >= PASS_MARK else "Fail"
            tag = "pass" if result == "Pass" else "fail"
            if result == "Pass":
                passed += 1
            else:
                failed += 1
            self.tree.insert("", "end", values=(data["name"], roll, data["marks"], result), tags=(tag,))

        total = len(self.students)
        self.total_label.config(text=f"Total Students: {total}")
        self.passed_label.config(text=f"Passed: {passed}")
        self.failed_label.config(text=f"Failed: {failed}")


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentResultApp(root)
    root.mainloop()