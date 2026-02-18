import wikipedia

WIKI_INPUT = "Olympische Spiele"
wikipedia.set_lang("de")

def is_wiki_content_found(topic):
    """
    Prüft, ob zu einem gegebenen Wikipedia-Thema eine gültige Seite
    existiert.
    Die Funktion versucht die entsprechende Wikipedia-Seite zu laden.
    Bei Erfolg wird das vollständige Wiki-Objekt zurückgegeben.
    Bei Mehrdeutigkeiten (DisambiguationError) werden bis zu 5 alternative
    Seitentitel zurückgegeben.
    Bei nicht existierenden Seiten (PageError) werden bis zu 5 Suchvorschläge
    zurückgegeben.
    :param topic: str
        Der Titel oder Suchbegriff des Wiki-Artikels.
    :return:
        tupel: (Wiki-Objekt, None) bei Erfolg,
                (None, Liste[strings]) bei Mehrdeutigkeit oder fehlender Seite
    """
    try:
        wiki_full = wikipedia.page(topic)
        return wiki_full, None
    except wikipedia.DisambiguationError as e:
        return None, e.options[:5]
    except wikipedia.PageError:
        wiki_search = wikipedia.search(topic, results=5)
        return None, wiki_search


"""def get_content_for_wiki_suggest(topic):
    wiki_search, wiki_suggest = wikipedia.search(
        topic, results=5, suggestion=True)
    wiki_search = wikipedia.search(wiki_suggest, results=5)
    if is_wiki_content_found(wiki_suggest)[0]:
        wiki_full = wikipedia.page(wiki_search[0])
        return wiki_full, wiki_search
    else:
        return None, wiki_search"""


def get_wiki_content(topic):
    """
    Ruft den vollständigen Textinhalt eines Wikipedia-Artikels ab.
    Die Funktion nutzt "is_wiki_content_found()" um zu prüfen, ob eine
    gültige Seite existiert. Falls ja, wird der gesamte Artikelinhalt
    zurückgegeben. Falls nicht, werden alternative Vorschläge oder
    Suchergebnisse zurückgegeben, die dem Nutzer helfen können, den richtigen
    Artikel zu finden.
    :param topic: str
        Der Titel oder Suchbegriff des Wiki-Artikels.
    :return:
        tuple:
            (content, None) bei Erfolg,
            (None, Liste[strings]) bei Mehrdeutigkeit oder fehlender Seite
    """
    wiki_full, wiki_search = is_wiki_content_found(topic)
    if wiki_full:
        return wiki_full.content, None
    else:
        return None, wiki_search




    """if is_wiki_content_found(topic)[0]:
        wiki_full = wikipedia.page(topic)
        return wiki_full.content, None
    elif is_wiki_content_found(topic)[1] == "DisambiguationError":
        wiki_full, wiki_search = get_content_for_wiki_suggest(topic)
        if wiki_full is None:
            return None, wiki_search
        else:
            return wiki_full.content, wiki_search
    elif is_wiki_content_found(topic)[1] == "PageError":
        wiki_full, wiki_search = get_content_for_wiki_suggest(
            topic)
        if wiki_full is None:
            return None, wiki_search
        else:
            return wiki_full.content, wiki_search"""



def get_wiki_url(topic):
    """
    Ruft die URL eines Wikipedia-Artikels ab.
    Die Funktion nutzt "is_wiki_content_found()" um zu prüfen, ob eine
    gültige Seite existiert. Falls ja, wird die URL des Artikels
    zurückgegeben. Falls nicht, werden alternative Vorschläge oder
    Suchergebnisse zurückgegeben, die dem Nutzer helfen können, den richtigen
    Artikel zu finden.
    :param topic: str
        Der Titel oder Suchbegriff des Wiki-Artikels.
    :return:
        tuple:
            (url, None) bei Erfolg,
            (None, Liste[strings]) bei Mehrdeutigkeit oder fehlender Seite
    """
    wiki_full, wiki_search = is_wiki_content_found(topic)
    if wiki_full:
        return wiki_full.url, None
    else:
        return None, wiki_search
    """if is_wiki_content_found(topic)[0]:
        wiki_full = wikipedia.page(topic)
        return wiki_full.url, None
    elif is_wiki_content_found(topic)[1] == "DisambiguationError":
        wiki_full, wiki_search = get_content_for_wiki_suggest(topic)
        if wiki_full is None:
            return None, wiki_search
        else:
            return wiki_full.url, wiki_search
    elif is_wiki_content_found(topic)[1] == "PageError":
        wiki_full, wiki_search = get_content_for_wiki_suggest(topic)
        if wiki_full is None:
            return None, wiki_search
        else:
            return wiki_full.url, wiki_search"""

name = ""
wiki_full, wiki_search = get_wiki_url(name)
print(wiki_full)
print(wiki_search)












valid_articles = [
    "Berlin",
    "Angela Merkel",
    "Quantenmechanik",
    "Photosynthese",
    "Python (Programmiersprache)",
    "Bundesverfassungsgericht",
    "Mount Everest",
    "Albert Einstein",
    "Internet",
    "Bodensee",
]

ambiguous_terms = [
    "Java",
    "Jaguar",
    "Mercury",
    "Apple",
    "Saturn",
    "Phoenix",
    "Amazon",
    "Matrix",
    "Titanic",
    "Washington",
    "Bank",
    "Schloss",
    "Leiter",
    "Stern",
    "Kiefer",
]

misspelled_terms = [
    "Angella Merkel",
    "Alber Einstein",
    "Quantenmechnaik",
    "Photosynthse",
    "Berln",
    "Bundesverfasungsgericht",
    "Internett",
    "Goethee",
    "Shakespear",
    "Berlinn",
]

non_existing_terms = [
    "asdfghjkl",
    "QWERTZUIOP123",
    "Xyztkrplmn",
    "Hausbaumflugzeugkatze",
    "Unendlichkeitsquadrant",
    "BlaBlaArtikelTest",
    "NichtExistierendeEnzyklopädie",
    "SuperMegaUltraTheorieXYZ",
    "FantasiePlanet987654",
    "KeinWikipediaEintragHier",
]

unicode_terms = [
    "Gödel",
    "São Paulo",
    "Łódź",
    "François Hollande",
    "München",
    "Zürich",
    "Kraków",
    "北京",
    "東京",
    "Αθήνα",
]

numeric_special_terms = [
    "2024",
    "1990",
    "9/11",
    "World War II",
    "Formel 1",
    "3D-Druck",
    "COVID-19",
    "G8",
    "Area 51",
    "§ 823 BGB",
]

edge_case_terms = [
    "",
    " ",
    "   Berlin   ",
    None,
    True,
    12345,
    ".",
    "-",
    "(",
    "[]",
]
