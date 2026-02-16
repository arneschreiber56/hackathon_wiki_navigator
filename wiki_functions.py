import wikipedia
WIKI_INPUT = "Olympische Spiele"

def get_wiki_content(topic):
    """
    Retrieve the full content of a German Wikipedia article using the
    `wikipedia` Python module.

    The function attempts to load the page for the given topic and returns
    its full text content. If the topic is ambiguous (DisambiguationError),
    the function prints up to five suggested alternative pages. If the page
    does not exist (PageError), it prints an error message and up to five
    search suggestions.
    :param topic: str
        The title or search term of the Wikipedia article to retrieve.
    :return:
        str or None
        The full article content as a string if the page exists.
        Returns None if the topic is ambiguous or the page cannot be found.
    """
    wikipedia.set_lang("de")
    try:
        wiki_full = wikipedia.page(topic)
        return wiki_full.content
        # print(wiki_full.url)
    except wikipedia.DisambiguationError:
        wiki_search = wikipedia.search(topic, results=5)
        print("Achtung! DisambiguationError! Meintest Du:")
        print(wiki_search)
    except wikipedia.PageError:
        wiki_search = wikipedia.search(topic, results=5)
        print("Achtung! PageError!")
        if not wiki_search:
            print("Nichts gefunden: Versuche erneut!")
            #continue
        else:
            print(wiki_search)


    
get_wiki_content(WIKI_INPUT)



