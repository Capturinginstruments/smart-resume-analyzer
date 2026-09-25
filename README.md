# ✨ SMART RESUME ANALYZER

A modern, premium minimalist web application for resume intelligence and automated scoring, built as a **B.Tech CSE Python Mini-Project**.

---

## 🚀 Key Features

1. **Multi-Format Resume Support**: Extract text from **PDF** (`PyPDF2`), **DOCX** (`python-docx`), and **Images** (`Pillow` & `pytesseract`).
2. **Deterministic Python Analysis**:
   - Contact Info Extraction (Email, Phone, LinkedIn, GitHub via Regular Expressions `re`).
   - Section Detection (Contact, Education, Skills, Projects, Experience, Certifications).
   - Skill Matching against common technical stacks.
   - Action Verb frequency counting.
   - Career Field classification (Software Engineering, Web Dev, Data Science, etc.).
3. **Transparent 7-Subscore Calculation (Out of 100)**:
   - Structure (20 pts)
   - Skills (20 pts)
   - Experience / Projects (20 pts)
   - Action Words (10 pts)
   - Contact Info (10 pts)
   - Keywords (10 pts)
   - Formatting & Word Count (10 pts)
4. **SQLite Persistence**: Stores past resume evaluations for viewing under the **History** tab.
5. **Downloadable Analysis Summary**: Generates a clean text/HTML report file.
6. **Clean Minimalist Design**: Premium UI with CSS progress bars, circular score badges, drag-and-drop file upload, and responsive cards.

---

## 🛠 Tech Stack

- **Backend**: Python 3.13, Django 5.x, SQLite 3
- **Libraries**: `PyPDF2`, `python-docx`, `Pillow`, `pytesseract`, `re`
- **Frontend**: HTML5, CSS3 (Vanilla CSS, zero heavy frameworks), JavaScript (Vanilla JS for file drag-and-drop)

---

## 🧩 OOP Architecture (Viva Explanation)

The application adheres to clean Object-Oriented Programming principles:

```
                  ResumeExtractor (Base Class)
                   /       |       \
       PDFExtractor   DOCXExtractor   ImageExtractor
```

- **Inheritance & Polymorphism**: Base class `ResumeExtractor` defines `extract_text(file_path)`. Subclasses `PDFExtractor`, `DOCXExtractor`, and `ImageExtractor` provide specific implementations for their respective file formats.
- **Data Container**: `Resume` object encapsulates raw text, clean text, metadata, and word counts.
- **Domain Services**:
  - `ResumeAnalyzer`: Parses regex patterns, sections, skills, and career fields.
  - `ResumeScorer`: Executes separate scoring functions (`calculate_structure_score()`, `calculate_skill_score()`, etc.).

---
## 💻 How to Run on your device
## 🚀 Live Demo

👉 [Open Smart Resume Analyzer](https://smart-resume-analyzer-yx9h.onrender.com)
## 💻 How to Run the Project Locally

### 1. Activate Virtual Environment
```powershell
.\venv\Scripts\activate
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Run Database Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 4. Start the Django Development Server
```powershell
python manage.py runserver
```

Open your browser and navigate to:
`http://127.0.0.1:8000/`

---

## 📚 Python Concepts Used (For Mini-Project Viva)

- **Python Basics**: Strings, lists, dictionaries, conditionals, functions.
- **File Handling**: Reading binary files, processing uploaded document streams.
- **Modules & Packages**: `os`, `re`, `PyPDF2`, `docx`, `Pillow`, `pytesseract`.
- **Exception Handling**: `try...except...finally` blocks for file parsing safety and invalid upload handling.
- **Object-Oriented Programming (OOP)**: Inheritance, polymorphism, encapsulation.
- **Regular Expressions (`re`)**: Pattern matching for emails, phone numbers, and section headers.
- **Django Framework**: MVC architecture (Models, Views, Templates, Forms, Routing).
- **Database Management**: SQLite relational database integration with Django ORM.
