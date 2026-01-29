from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_mongodb_cv():
    if not os.path.exists('data'):
        os.makedirs('data')
    
    c = canvas.Canvas("data/cv_stefano_mongodb.pdf", pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "CV: STEFANO DE LUCA - NoSQL Solution Architect")
    
    c.setFont("Helvetica", 11)
    lines = [
        "Specialista Database NoSQL e Scalabilità Orizzontale",
        "Esperienza: 8 anni nel settore High-Traffic Web",
        "---",
        "COMPETENZE CORE:",
        "- MongoDB (Sharding, Replication, Aggregation Framework)",
        "- Modellazione dati a documenti (Document Data Modeling)",
        "- Database: Redis, Cassandra, Elasticsearch",
        "- Linguaggi: JavaScript (Node.js), Python, Go",
        "---",
        "ESPERIENZA LAVORATIVA:",
        "Lead Database Engineer presso CloudStream S.p.A (2018 - Presente)",
        "- Gestione di cluster MongoDB su larga scala (oltre 100 nodi).",
        "- Ottimizzazione delle performance di scrittura per sistemi di log in tempo reale.",
        "- Migrazione di legacy database SQL verso architetture MongoDB Atlas.",
        "",
        "Database Administrator presso DataLogic (2015 - 2018)",
        "- Manutenzione database MongoDB e PostgreSQL.",
        "---",
        "CERTIFICAZIONI:",
        "- MongoDB Certified DBA Associate",
        "- MongoDB Certified Developer Associate"
    ]
    
    y = 720
    for line in lines:
        if line == "---":
            y -= 10
            c.line(50, y, 500, y)
            y -= 20
        else:
            c.drawString(50, y, line)
            y -= 15
    
    c.save()
    print("[+] PDF 'data/cv_stefano_mongodb.pdf' creato con successo!")

if __name__ == "__main__":
    create_mongodb_cv()
