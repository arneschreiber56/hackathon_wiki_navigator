import textwrap  # Zum Formatieren von Text auf eine bestimmte Breite
from colorama import init, Fore, Style  # Für farbige Terminal-Ausgabe
import openai_api  # Eigene Datei, die die OpenAI API ansteuert
import wiki_functions  # Eigene Datei, um Wikipedia-Artikel abzurufen
import warnings

# Hiermit sagen wir Python: "Bitte ignoriere alle Warnungen an User"
warnings.filterwarnings("ignore", category=UserWarning, module="wikipedia")

# Hier kommt dann dein restlicher Code, z.B.:
import wikipedia
# ...# Colorama initialisieren (wichtig für Windows, damit Farben korrekt angezeigt werden)
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


def run_quiz(quiz_data):
    """
    Führt ein Quiz aus, das als JSON-Liste vorliegt.
    """

    if not quiz_data:
        print(Fore.RED + "Quiz konnte nicht geladen werden.")
        return

    print(Fore.CYAN + "\n" + "=" * TERMINAL_WIDTH)
    print(Style.BRIGHT + Fore.CYAN + "QUIZ".center(TERMINAL_WIDTH))
    print(Fore.CYAN + "=" * TERMINAL_WIDTH + "\n")

    score = 0
    letters = ["A", "B", "C", "D"]

    """
    Durchläuft jede Frage im Quiz.
    enumerate(..., 1) sorgt dafür, dass die Fragennummer bei 1 beginnt.
    """

    for i, question in enumerate(quiz_data, 1):
        print(Fore.YELLOW + f"Frage {i}: {question['question']}")

        for index, option in enumerate(question["options"]):
            print(Fore.WHITE + f"{letters[index]}) {option}")

        while True:
            user_answer = input(Fore.GREEN + "Deine Antwort (A/B/C/D): ").strip().upper()
            if user_answer in letters:
                break
            print(Fore.RED + "Bitte A, B, C oder D eingeben.")

        if user_answer == question["correct"]:
            print(Fore.GREEN + "✅ Richtig!\n")
            score += 1
        else:
            correct_letter = question["correct"]
            correct_index = letters.index(correct_letter)
            correct_text = question["options"][correct_index]
            print(Fore.RED + f"❌ Falsch! Richtig wäre: {correct_letter}) {correct_text}\n")

    percent = round((score / len(quiz_data)) * 100)

    print(Fore.CYAN + "=" * TERMINAL_WIDTH)
    print(Style.BRIGHT + Fore.CYAN + "ERGEBNIS".center(TERMINAL_WIDTH))
    print(Fore.CYAN + "=" * TERMINAL_WIDTH)
    print(Fore.WHITE + f"Du hast {score}/{len(quiz_data)} richtig ({percent}%).")

    input("\nEnter drücken für Menü...")


def handle_search():
    """
    Fragt den Nutzer nach einem Thema, ruft den Wikipedia-Artikel ab,
    erstellt eine Zusammenfassung mit OpenAI und zeigt die URL an.
    """
    # Hier müssen Leerstring abfangen
    topic = input(Fore.GREEN + "\nGebe ein Thema ein: ")
    if not topic:
        print(Fore.RED + "Bitte drücken Sie nicht nur Enter!")
        return
    print(Fore.BLUE + f"\nWikipedia sucht nach '{topic}'...\n")

    # Holt den Status, den Text und die URL des Artikels
    article_text, search_lst = wiki_functions.get_wiki_content(topic)
    article_url = wiki_functions.get_wiki_url(topic)
    if article_text:
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
        print(Fore.BLUE + article_url[0])
        print()

        # --- QUIZ (optional) ---
        make_quiz = input(Fore.YELLOW + "Möchtest du ein kurzes Quiz? (j/n): ").strip().lower()
        if make_quiz == "j":
            quiz_data = openai_api.quiz_from_summary(summary, num_questions=3)
            run_quiz(quiz_data)

    elif not search_lst:
        print(Fore.RED + "Keine Einträge gefunden, bitte versuchen Sie eine andere Eingabe!")

    else:
        # Fehlerfall: Kein eindeutiger Artikel gefunden
        print(Fore.RED + "Kein eindeutiger Artikel gefunden. Suchergebnisse: " + ", ".join(map(str, search_lst)))



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
