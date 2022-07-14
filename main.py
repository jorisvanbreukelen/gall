import requests
from export_to_excel import process_workbook

with requests.Session() as s:
    pagina = s.get('https://www.gall.nl/')
    s.close()

categories = ["Wijn", "mousserende-wijn", "Whisky", "Mixen", "Likeuren", "Bier", "jenever-bitter-en-vieux", "Port-Sherry", "Cognac", "Cadeau"]
names = []
prices = []
category_names = []
aps = []
volumes = []
products = []
images = []
number = 0

for category in categories:
    pagina = s.get('https://www.gall.nl/'+category)
    print(category)
    s.close()
    rawdata = pagina.text.splitlines()

    matching = [k for k in rawdata if "ptile-v2_link" in k]
    i = 0
    for product in matching:
        product = product[:product.rfind(".html")+5]
        print(product)
        #product = product.replace('" track-click-product class="product-tile__container-link" itemprop="url" tabindex="-1">', '')
        product = product.replace('<a class="ptile-v2_link" href="', '')
        print(product)
        matching[i] = product
        i += 1
    print(matching)

    for product in matching:
        pagina = s.get('https://www.gall.nl' + product)
        s.close()
        rawdata = pagina.text.splitlines()

        products.append(product)

        matching2 = [k for k in rawdata[:1500] if '<span class="u-sr-only"> &euro; ' in k]
        matching2_discount = [k for k in rawdata[:1500] if '<span class="u-sr-only">Van: &euro;' in k]

        if len(matching2) > 0:
            price = matching2[0].replace('<span class="u-sr-only"> &euro; ', '')
        elif len(matching2_discount) > 0:
            #price = matching2_discount[0].replace('<span class="u-sr-only">Van: &euro;', '')
            price_begin = matching2_discount[0].find('voor: &euro; ')
            price = matching2_discount[0][price_begin+len('voor: &euro; '):]
        price = price.replace('</span>', '')
        print(price)
        prices.append(float(price))

        matching3 = [k for k in rawdata[:1500] if '<img class=" u-hidden-with-nojs" data-src=' in k]
        html = matching3[0].replace('<img class=" u-hidden-with-nojs" data-src="', '')
        image_end = html.find('" src=')
        image = html[:image_end]
        print(image)
        images.append(image)

        name_number = rawdata.index('<h1 class="h1--bordered product-info__title">')
        name = rawdata[name_number + 1]
        names.append(name)

        category_name = category.replace("-", " ")
        print(category_name)
        category_names.append(category_name)

        if('<h3 class="h6">Alcoholpercentage</h3>' in rawdata):
            ap_number = rawdata.index('<h3 class="h6">Alcoholpercentage</h3>')
            ap = rawdata[ap_number + 1].replace('<p>', '')
            ap = ap.replace(',','.')
            ap = float(ap.replace('%</p>', ''))
        else:
            ap = 'nog niet bekend'
        print(ap)
        aps.append(ap)

        if ('<h3 class="h6">Inhoud</h3>' in rawdata):
            volume_number = rawdata.index('<h3 class="h6">Inhoud</h3>')
            volume = rawdata[volume_number + 1].replace('<p>', '')
            volume = volume.replace(',', '.')
            if (' ml' in volume):
                volume = float(volume.replace(' ml</p>', ''))/10
            elif(' l' in volume):
                volume = float(volume.replace(' l</p>', '')) * 100
            elif (' cl' in volume):
                volume = float(volume.replace(' cl</p>', ''))
        else:
            volume = 'nog niet bekend'
        print(volume)
        volumes.append(volume)
        number += 1

process_workbook(names, prices, category_names, aps, volumes, products, images)






