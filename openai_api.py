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


def quiz_from_summary(summary: str, num_questions: int = 3) -> str:
    """
    Erstellt aus der Zusammenfassung ein Multiple-Choice-Quiz.

    Parameter:
    - summary: Die vorher erstellte Zusammenfassung
    - num_questions: Anzahl der Fragen (wird auf 2–3 begrenzt)

    Rückgabe:
    - Ein formatierter Text im festen Layout mit:
      F1:
      A)
      B)
      C)
      D)
      Answer: A
    """

    # Sicherstellen, dass es nur 2 oder 3 Fragen sind
    num_questions = 2 if num_questions < 2 else (3 if num_questions > 3 else num_questions)

    # Prompt, der exakt vorgibt, wie das Quiz aussehen soll
    prompt = f"""
Erstellen Sie aus dieser Zusammenfassung genau {num_questions} Multiple-Choice-Fragen.
Das Format muss exakt wie folgt aussehen:

F1: question text
A) option
B) option
C) option
D) option
Answer: A

Rules:
- Nutze ausschließlich A, B, C oder D für die Antwort
- Die Fragen dürfen sich NUR auf die Summary beziehen
- Sprache: Deutsch

SUMMARY:
{summary[:2000]}
""".strip()

    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {
                    "role": "system",
                    "content": "Sie erstellen kurze Quizze im exakt gewünschten Format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Das komplette Quiz wird als Text zurückgegeben
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Quiz konnte nicht erstellt werden. Fehler: {e}"
