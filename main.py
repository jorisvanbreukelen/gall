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

        #matching2 = [k for k in rawdata[:3000] if '<strong class="price-v2 pdp-info_price" role="button" aria-label="&euro; ' in k]
        matching2 = [k for k in rawdata[:] if '<strong class="price-v2 pdp-info_price" role="button" aria-label="&euro; ' in k]
        matching2_discount = [k for k in rawdata[:] if '<span class="price-v2-value" content="' in k]
        if len(matching2) > 0:
            price = matching2[0].replace('<strong class="price-v2 pdp-info_price" role="button" aria-label="&euro; ', '')
            price = price.replace('">', '')
        elif len(matching2_discount) > 0:
            price = matching2_discount[0].replace('<span class="price-v2-value" content="', '')
            price = price.replace('" aria-hidden="true">', '')
            print('Price:')
            print(price)
            print(('https://www.gall.nl' + product))
        #     #price = matching2_discount[0].replace('<span class="u-sr-only">Van: &euro;', '')
        #     price_begin = matching2_discount[0].find('voor: &euro; ')
        #     price = matching2_discount[0][price_begin+len('voor: &euro; '):]

        #If I want to work out discount: <strong class="price-v2 pdp-info_price" role="button" aria-label="Van: &euro; 23.87 voor: &euro; 20.99">

        price = price.replace(' Per fles', '')
        price = price.replace(' Per pack', '')
        prices.append(float(price))

        #Moet nog ff gefixt worden
        matching3 = [k for k in rawdata[:] if '<img class="img" src="' in k]
        html = matching3[0].replace('<img class="img" src="', '')
        image_end = html.find('" srcset="')
        image = html[:image_end]
        images.append(image)

        # name_number = rawdata.index('<h1 class="pdp-info_name">')
        # name = rawdata[name_number + 1]
        # names.append(name)
        # print(names)

        matching4 = [k for k in rawdata[:] if '<h1 class="pdp-info_name">' in k]
        html = matching3[0].replace('<h1 class="pdp-info_name">', '')
        name_end = html.find('</h1>')
        name = html[:name_end]
        names.append(name)

        category_name = category.replace("-", " ")
        print(category_name)
        category_names.append(category_name)

        if('<td>Alcoholpercentage</td>' in rawdata):
            ap_number = rawdata.index('<td>Alcoholpercentage</td>')
            ap = rawdata[ap_number + 1].replace('<td>', '')
            ap = ap.replace(',','.')
            ap = float(ap.replace('%</td>', ''))
        else:
            ap = 'nog niet bekend'
        print(ap)
        aps.append(ap)

        if ('<td>Inhoud</td>' in rawdata):
            volume_number = rawdata.index('<td>Inhoud</td>')
            volume = rawdata[volume_number + 1].replace('<td>', '')
            volume = volume.replace(',', '.')
            volume = float(volume.replace(' Centiliter</td>', ' '))
            # if (' ml' in volume):
            #     volume = float(volume.replace(' ml</p>', ''))/10
            # elif(' l' in volume):
            #     volume = float(volume.replace(' l</p>', '')) * 100
            # elif (' cl' in volume):
            #     volume = float(volume.replace(' cl</p>', ''))
        else:
            volume = 'nog niet bekend'
        print(volume)
        volumes.append(volume)
        number += 1

process_workbook(names, prices, category_names, aps, volumes, products, images)






