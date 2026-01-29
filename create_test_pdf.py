from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_pdf():
    if not os.path.exists('data'):
        os.makedirs('data')
    
    c = canvas.Canvas("data/test_cv.pdf", pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "DR. ALESSANDRO VERONESI")
    
    c.setFont("Helvetica", 12)
    lines = [
        "Senior Research Scientist | Laboratorio di Chimica Avanzata - Milano",
        "",
        "PROFILO PROFESSIONALE:",
        "Ricercatore con 12 anni di esperienza nella caratterizzazione dei materiali.",
        "Specializzato in tecniche spettroscopiche e automazione dei processi.",
        "",
        "ESPERIENZA:",
        "- Responsabile dell'unita' di Analisi Spettroscopica a Milano.",
        "- Sviluppo di protocolli innovativi per la Spettroscopia IR (Infrarosso).",
        "- Implementazione di algoritmi in Python per l'analisi dei dati.",
        "",
        "COMPETENZE TECNICHE:",
        "Spettroscopia IR, Spettrometria di Massa, NMR, Python, MATLAB, R.",
        "",
        "LINGUE:",
        "Italiano (Madrelingua), Inglese (C2)."
    ]
    
    y = 730
    for line in lines:
        y -= 20
        c.drawString(100, y, line)
    
    c.save()
    print("[+] PDF 'data/test_cv.pdf' creato con successo!")

if __name__ == "__main__":
    create_pdf()
