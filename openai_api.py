import json

# Ermöglicht das Laden von Umgebungsvariablen aus einer .env-Datei
from dotenv import load_dotenv

# Importiert die OpenAI-Klasse, um API-Anfragen zu senden
from openai import OpenAI

# Lädt die Datei "openai_key.env", die den API-Key enthält
load_dotenv("openai_key.env")

# Zugriff auf Umgebungsvariablen
import os
api_key = os.getenv("OPENAI_API_KEY")

# Erstellt den OpenAI-Client mit dem API-Key
client = OpenAI(api_key=api_key)


def summarize(text):
    """
    Erstellt eine einfache Zusammenfassung eines Wikipedia-Artikels.

    Ablauf:
    1. Der Text wird auf 5000 Zeichen begrenzt (Token-Limit Schutz).
    2. Dem Modell wird gesagt, WIE es zusammenfassen soll (System-Nachricht).
    3. Der Text wird als User-Nachricht gesendet.
    4. Die Antwort wird aus response.choices extrahiert.
    5. Falls ein Fehler auftritt (z. B. Internetproblem), wird eine Fehlermeldung zurückgegeben.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",  # schnelles, günstiges Modell
            messages=[
                {
                    "role": "system",
                    "content": "Fasse den Text in 5 einfachen Sätzen zusammen, ohne Fachbegriffe zu benutzen."
                },
                {
                    "role": "user",
                    "content": text[:5000]  # Begrenzung gegen zu große Anfragen
                }
            ]
        )

        # Hier holen wir den eigentlichen Text aus der API-Antwort
        return response.choices[0].message.content

    except Exception as e:
        # Falls die API nicht erreichbar ist oder ein Fehler auftritt
        return f"Entschuldigung, die KI ist aktuell nicht verfügbar. Fehler: {e}"


def quiz_from_summary(summary: str, num_questions: int = 3):
    """
    Erstellt ein Quiz im JSON-Format.
    Rückgabe: Liste von Fragen (Python-Objekte)
    """

    # Nur 2–3 Fragen erlauben
    num_questions = 2 if num_questions < 2 else (3 if num_questions > 3 else num_questions)

    prompt = f"""
Erstelle genau {num_questions} Multiple-Choice-Fragen basierend auf der Summary.

Antworte ausschließlich im gültigen JSON-Format:

[
  {{
    "question": "Frage hier",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": "A"
  }}
]

Regeln:
- Sprache: Deutsch
- correct darf nur A, B, C oder D sein
- Keine zusätzliche Erklärung außerhalb des JSON
- Nur auf die Summary beziehen

SUMMARY:
{summary[:2000]}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {
                    "role": "system",
                    "content": "Du antwortest nur im gültigen JSON-Format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        quiz_text = response.choices[0].message.content.strip()

        # JSON-Text in Python-Liste umwandeln
        return json.loads(quiz_text)

    except Exception as e:
        print(f"Quiz konnte nicht erstellt werden: {e}")
        return None
