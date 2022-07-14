import requests
categories = ["Wijn"]#, "mousserende-wijn", "Whisky", "Mixen", "Likeuren", "Bier", "jenever-bitter-en-vieux", "Port-Sherry", "Cognac", "Cadeau"]

for category in categories:
    with requests.Session() as s:
        pagina = s.get('https://www.gall.nl/')
        s.close()
        rawdata = pagina.text.splitlines()
    #name_number = rawdata.index('<a href="/' + category.casefold() + '/?start=12" aria-label="pagina ..." class="pagination__item pagination__item--number" data-pagination-item=\'{"page": "..."}\' track-click-pagination-item>')
    name_number = rawdata.index('...')
    print(len(rawdata))
    print(rawdata[-1])
