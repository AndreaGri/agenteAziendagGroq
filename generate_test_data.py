from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_pdf(filename, title, content):
    if not os.path.exists('data'):
        os.makedirs('data')
    path = f"data/{filename}"
    c = canvas.Canvas(path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, title)
    c.setFont("Helvetica", 11)
    y = 720
    for line in content:
        if line == "---":
            y -= 10
            c.line(50, y, 500, y)
            y -= 20
        else:
            c.drawString(50, y, line)
            y -= 15
        if y < 50:
            c.showPage()
            y = 750
    c.save()
    print(f"[+] Creato: {path}")

# --- 5 CV INFORMATICI ---
cvs = [
    {
        "file": "cv_luca_web.pdf",
        "title": "CV: LUCA VERDI - Full Stack Developer",
        "content": ["Specialista Web Development", "Esperienza: 5 anni presso WebAgency Srl", "Tecnologie: React, Next.js, Node.js, Tailwind CSS", "Progetti: E-commerce scalabili e Dashboard interattive", "Seniority: Middle-Senior"]
    },
    {
        "file": "cv_sara_data.pdf",
        "title": "CV: SARA NERI - Database Administrator",
        "content": ["Esperta SQL e Big Data", "Esperienza: 10 anni in ambito Bancario", "Tecnologie: PostgreSQL, Oracle, PL/SQL, Tuning query complesse", "Progetti: Migrazione database da 50TB", "Seniority: Expert"]
    },
    {
        "file": "cv_marco_mobile.pdf",
        "title": "CV: MARCO ROSSI - Mobile App Developer",
        "content": ["Sviluppatore App Android e iOS", "Esperienza: 3 anni Freelance", "Tecnologie: Flutter, Dart, Firebase, Swift", "Progetti: App di food delivery e Social Network locale", "Seniority: Junior-Middle"]
    },
    {
        "file": "cv_elena_devops.pdf",
        "title": "CV: ELENA BIANCHI - DevOps Engineer",
        "content": ["Cloud Architect & Automation", "Esperienza: 7 anni in Multinazionale Tech", "Tecnologie: Docker, Kubernetes, AWS, Terraform, CI/CD Jenkins", "Progetti: Infrastruttura a microservizi resiliente", "Seniority: Senior"]
    },
    {
        "file": "cv_paolo_ai.pdf",
        "title": "CV: PAOLO BRUNI - AI Engineer",
        "content": ["Specialista Machine Learning", "Esperienza: 4 anni Centro Ricerca", "Tecnologie: Python, PyTorch, Scikit-learn, LangChain", "Progetti: Modelli predittivi per la sanità", "Seniority: Middle"]
    }
]

# --- 5 CORSI DI FORMAZIONE ---
courses = [
    {
        "file": "cert_giulia_nodejs.pdf",
        "title": "CERTIFICATO DI FORMAZIONE: GIULIA GIALDI",
        "content": ["Corso: Master in Node.js Backend Advanced", "Durata: 80 ore", "Argomenti: Microservizi, Pattern di design, WebSockets", "Data: Dicembre 2023"]
    },
    {
        "file": "cert_roberto_angular.pdf",
        "title": "CERTIFICATO DI FORMAZIONE: ROBERTO BLU",
        "content": ["Corso: Angular 17 Architecture", "Durata: 40 ore", "Argomenti: Signals, SSR, State Management con NgRx", "Data: Gennaio 2024"]
    },
    {
        "file": "cert_anna_sql.pdf",
        "title": "CERTIFICATO DI FORMAZIONE: ANNA ORO",
        "content": ["Corso: SQL for Data Science & Analytics", "Durata: 60 ore", "Argomenti: Query analitiche, Window Functions, ETL", "Data: Marzo 2023"]
    },
    {
        "file": "cert_fabio_cyber.pdf",
        "title": "CERTIFICATO DI FORMAZIONE: FABIO FERRO",
        "content": ["Corso: Cybersecurity Fundamentals", "Durata: 100 ore", "Argomenti: Pentesting, OWASP Top 10, Network Security", "Data: Febbraio 2024"]
    },
    {
        "file": "cert_marta_ux.pdf",
        "title": "CERTIFICATO DI FORMAZIONE: MARTA VIOLET",
        "content": ["Corso: UI/UX Design Professional", "Durata: 50 ore", "Argomenti: Figma, Prototipazione, User Research", "Data: Aprile 2023"]
    }
]

if __name__ == "__main__":
    for item in cvs:
        create_pdf(item["file"], item["title"], item["content"])
    for item in courses:
        create_pdf(item["file"], item["title"], item["content"])
    print("\n[!] Tutti i 10 file di test sono pronti nella cartella 'data/'")
