# 🎓 Student Result System

A simple app to manage student records — add/update students, view results in a table, and automatically calculate Pass/Fail status with summary totals.

This repo has **two versions**:

| File | Type | Where it runs |
|---|---|---|
| `index.html` | Web app (HTML/CSS/JS) | Any browser — can be hosted live via GitHub Pages |
| `student_result_system.py` | Desktop app (Python + Tkinter) | Runs locally on your computer |

## ✨ Features

- Add / update student records (Name, Roll No, Class, Marks)
- View all records in a result table
- Automatic Pass/Fail based on a passing mark of 40
- Live summary: Total Students, Passed, Failed
- Click a row to select it, then delete it

## 🌐 Live Demo (Web Version)

This project is hosted using **GitHub Pages**.
👉 Live link: `https://your-username.github.io/student-result-system/`

*(Replace `your-username` with your actual GitHub username after deploying — see steps below.)*

## 🚀 How to Deploy the Web Version (GitHub Pages)

1. Create a new GitHub repository and upload `index.html` to it.
2. Go to **Settings → Pages**.
3. Under "Source", select the `main` branch and `/ (root)` folder → **Save**.
4. Wait 1–2 minutes — your live URL will appear at the top of the Pages settings.

## 🖥️ How to Run the Desktop Version (Python)

```bash
python student_result_system.py
```

Tkinter ships with standard Python on Windows/Mac.
On Linux, you may need to install it first:

```bash
sudo apt-get install python3-tk
```

## 🎨 Design

Both versions share the same color palette:

| Element | Color |
|---|---|
| Header | `#01837A` |
| Accent / Buttons | `#B809F8` |
| Background | `#F3EEFB` |
| Pass | `#1E8E3E` |
| Fail | `#D93025` |

## 📄 License

Free to use and modify.
