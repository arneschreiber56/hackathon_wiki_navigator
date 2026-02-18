import textwrap  # Zum Formatieren von Text auf eine bestimmte Breite
from colorama import init, Fore, Style  # Für farbige Terminal-Ausgabe
import openai_api  # Eigene Datei, die die OpenAI API ansteuert
import wiki_functions  # Eigene Datei, um Wikipedia-Artikel abzurufen

# Colorama initialisieren (wichtig für Windows, damit Farben korrekt angezeigt werden)
init(autoreset=True)

# Definieren, wie breit die Ausgabe im Terminal maximal sein soll
TERMINAL_WIDTH = 80


def show_welcome():
    """Zeigt die Startnachricht im Terminal mit Farben und Linien"""
    print(Fore.CYAN + "=" * TERMINAL_WIDTH)
    print(Style.BRIGHT + Fore.CYAN + "Willkommen beim Wikipedia-Wissensnavigator".center(TERMINAL_WIDTH))
    print(Fore.CYAN + "=" * TERMINAL_WIDTH)


def show_menu():
    """Zeigt das Hauptmenü mit Auswahlmöglichkeiten"""
    print(Fore.YELLOW + "\nBitte wähle eine Option:")
    print(Fore.YELLOW + "1. Artikel suchen")
    print(Fore.YELLOW + "2. Ende des Programms")


def run_quiz(quiz_text: str):
    """
    Führt das Quiz interaktiv im Terminal aus.

    Ablauf:
    1. Trennt die richtigen Antworten (Answer:) vom sichtbaren Text.
    2. Zeigt dem Nutzer nur die Fragen + Antwortmöglichkeiten.
    3. Fragt die Antworten einzeln ab.
    4. Vergleicht mit den richtigen Lösungen.
    5. Berechnet Score und Prozentzahl.
    """

    # Falls OpenAI einen Fehler zurückgegeben hat
    if quiz_text.startswith("Quiz konnte nicht erstellt werden"):
        print(Fore.RED + quiz_text)
        return

    # Text in einzelne Zeilen zerlegen
    lines = quiz_text.splitlines()

    correct_answers = []  # Speichert richtige Antworten (A/B/C/D)
    visible_lines = []    # Speichert nur die sichtbaren Quiz-Zeilen

    # Jede Zeile analysieren
    for line in lines:
        stripped = line.strip()

        # Wenn es eine Lösungszeile ist → merken, aber nicht anzeigen
        if stripped.startswith("Answer:"):
            correct_answers.append(stripped.replace("Answer:", "").strip().upper())
        else:
            visible_lines.append(line)

    # Falls keine Antworten erkannt wurden (Formatfehler)
    if not correct_answers:
        print(Fore.RED + "\nKonnte die Antworten nicht lesen (Format stimmt nicht).")
        return

    # Überschrift anzeigen
    print(Fore.CYAN + "\n" + "=" * TERMINAL_WIDTH)
    print(Style.BRIGHT + Fore.CYAN + "QUIZ".center(TERMINAL_WIDTH))
    print(Fore.CYAN + "=" * TERMINAL_WIDTH + "\n")

    # Quiz ohne Lösungen anzeigen
    print(Fore.WHITE + "\n".join(visible_lines))
    print(Fore.YELLOW + "\nBitte beantworte die Fragen (A/B/C/D).")

    score = 0
    total = len(correct_answers)
    valid = ["A", "B", "C", "D"]

    # Jede Frage einzeln abfragen
    for i in range(total):
        while True:
            user_answer = input(Fore.GREEN + f"Deine Antwort für F{i+1}: ").strip().upper()

            # Prüfen, ob Eingabe gültig ist
            if user_answer in valid:
                break

            print(Fore.RED + "Bitte nur A, B, C oder D eingeben.")

        # Antwort vergleichen
        if user_answer == correct_answers[i]:
            score += 1

    # Prozentwert berechnen
    percent = round((score / total) * 100)

    # Ergebnis anzeigen
    print(Fore.CYAN + "\n" + "=" * TERMINAL_WIDTH)
    print(Style.BRIGHT + Fore.CYAN + "ERGEBNIS".center(TERMINAL_WIDTH))
    print(Fore.CYAN + "=" * TERMINAL_WIDTH)

    print(Fore.WHITE + f"Richtig: {score}/{total} ({percent}%)")

    # Feedback je nach Leistung
    if percent >= 80:
        print(Fore.GREEN + "✅ Sehr gut! Das sieht nach gutem Verständnis aus.")
    elif percent >= 50:
        print(Fore.YELLOW + "👍 Ganz okay! Du hast einiges verstanden.")
    else:
        print(Fore.RED + "💡 Vielleicht nochmal kurz die Zusammenfassung lesen.")

    input("\nPress Enter to return to menu...")


def handle_search():
    """
    Fragt den Nutzer nach einem Thema, ruft den Wikipedia-Artikel ab,
    erstellt eine Zusammenfassung mit OpenAI und zeigt die URL an.
    """
    topic = input(Fore.GREEN + "\nGebe ein Thema ein: ")
    print(Fore.BLUE + f"\nWikipedia sucht nach '{topic}'...\n")

    # Holt den Status, den Text und die URL des Artikels
    error_marker, article_text, article_url = wiki_functions.get_wiki_url(topic)

    if error_marker == "Full_content_ok" and article_text:
        print(Fore.MAGENTA + "Zusammenfassung des Artikels...\n")

        # Die KI fasst den Text zusammen
        summary = openai_api.summarize(article_text)

        # Ausgabe der Zusammenfassung mit Linien und Überschrift
        print(Fore.CYAN + "=" * TERMINAL_WIDTH)
        print(Style.BRIGHT + Fore.CYAN + "ZUSAMMENFASSUNG".center(TERMINAL_WIDTH))
        print(Fore.CYAN + "=" * TERMINAL_WIDTH)

        # Text formatieren, damit er auf TERMINAL_WIDTH passt
        formatted_summary = textwrap.fill(summary, width=TERMINAL_WIDTH)
        print(Fore.WHITE + formatted_summary)

        print(Fore.CYAN + "=" * TERMINAL_WIDTH)

        # Link zum vollständigen Wikipedia-Artikel anzeigen
        print(Fore.YELLOW + "\nDen kompletten Artikel findest du hier:")
        print(Fore.BLUE + article_url)
        print()

        #Babar
        # --- QUIZ (optional) ---
        make_quiz = input(Fore.YELLOW + "Möchtest du ein kurzes Quiz? (j/n): ").strip().lower()
        if make_quiz == "j":
            quiz_text = openai_api.quiz_from_summary(summary, num_questions=3)
            run_quiz(quiz_text)



    else:
        # Fehlerfall: Kein eindeutiger Artikel gefunden
        print(Fore.RED + "Kein eindeutiger Artikel gefunden. Suchergebnisse: " + str(article_url))



def main():
    """Hauptfunktion: Zeigt das Menü und reagiert auf Nutzereingaben"""
    show_welcome()

    while True:
        show_menu()
        choice = input(Fore.GREEN + "Deine Wahl: ")

        if choice == "1":
            handle_search()  # Suche starten

        elif choice == "2":
            print(Fore.CYAN + "\nAuf Wiedersehen!")
            break  # Programm beenden

        else:
            # Ungültige Eingabe
            print(Fore.RED + "\nUngültige Eingabe. Bitte wähle 1 oder 2.")


# Startpunkt des Programms
if __name__ == "__main__":
    main()
