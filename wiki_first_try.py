import wikipedia
WIKI_INPUT = "Olympische Spiele"
wikipedia.set_lang("de")
try:
    wiki_full = wikipedia.page(WIKI_INPUT)
except wikipedia.DisambiguationError:
    wiki_search = wikipedia.search(WIKI_INPUT, results=5)
    print("Achtung! DisambiguationError! Meintest Du:")
    print(wiki_search)
except wikipedia.PageError:
    wiki_search = wikipedia.search(WIKI_INPUT, results=5)
    print("Achtung! PageError!")
    if not wiki_search:
        print("Nichts gefunden: Versuche erneut!")
        #continue
    else:
        print(wiki_search)

else:
    print(wiki_full.content)
    print(wiki_full.url)
    




