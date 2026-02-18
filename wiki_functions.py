import wikipedia

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
        # setzen auto_suggest auf False um fehlerhafte Suggestions bei
        # der Erstsuche nach Content durch diese Funktion zu vermeiden
        # und behalten die Kontrolle
        wiki_full = wikipedia.page(topic, auto_suggest=False)
        return wiki_full, None
    except wikipedia.DisambiguationError as e:
        return None, e.options[:5]
    except wikipedia.PageError:
        wiki_search = wikipedia.search(topic, results=5)
        return None, wiki_search


def get_wiki_content(topic):
    """
    Ruft den vollständigen Objektinhalt eines Wikipedia-Artikels ab.
    Die Funktion nutzt "is_wiki_content_found()" um zu prüfen, ob eine
    gültige Seite existiert. Falls ja, wird der gesamte Artikelinhalt
    zurückgegeben. Falls nicht, wird zuerst eine Contentsuche durch
    einen von Wikipedia vorgeschlagenen Alternativbegriff durchgeführt.
    Ist diese erfolgreich, dann wird der Artikelinhalt für diesen Begriff
    ausgegeben. Wenn nicht, werden alternative Vorschläge oder
    Suchergebnisse vom neuen Begriff zurückgegeben, die dem Nutzer
    helfen können, den richtigen Artikel zu finden.
    :param topic: str
        Der Titel oder Suchbegriff des Wiki-Artikels.
    :return:
        tuple:
            (content, None) bei Erfolg,
            (None, Liste[strings]) bei Mehrdeutigkeit oder fehlender Seite
    """
    for i in range(2):
        wiki_full, wiki_search = is_wiki_content_found(topic)
        if not wiki_full:
            if wikipedia.suggest(topic):
                topic = wikipedia.suggest(topic)
                topic = topic.title()
                continue
            else:
                return None, wiki_search
        if wiki_full:
            return wiki_full.content, None
    return None, wiki_search


def get_wiki_url(topic):
    """
    Ruft den vollständigen Objektinhalt eines Wikipedia-Artikels ab.
    Die Funktion nutzt "is_wiki_content_found()" um zu prüfen, ob eine
    gültige Seite existiert. Falls ja, wird die URL des Artikels
    zurückgegeben. Falls nicht, wird zuerst eine Contentsuche durch einen
    von Wikipedia vorgeschlagenen Alternativbegriff durchgeführt.
    Ist diese erfolgreich, dann wird die URL für diesen Begriff
    ausgegeben. Wenn nicht, werden alternative Vorschläge oder
    Suchergebnisse vom neuen Begriff zurückgegeben, die dem Nutzer
    helfen können, den richtigen Artikel zu finden.
    :param topic: str
        Der Titel oder Suchbegriff des Wiki-Artikels.
    :return:
        tuple:
            (url, None) bei Erfolg,
            (None, Liste[strings]) bei Mehrdeutigkeit oder fehlender Seite
    """
    """wiki_full, wiki_search = is_wiki_content_found(topic)
    if wiki_full:
        return wiki_full.url, None
    else:
        return None, wiki_search"""
    for i in range(2):
        wiki_full, wiki_search = is_wiki_content_found(topic)
        if not wiki_full:
            if wikipedia.suggest(topic):
                topic = wikipedia.suggest(topic)
                topic = topic.title()
                continue
            else:
                return None, wiki_search
        if wiki_full:
            return wiki_full.url, None
    return None, wiki_search

