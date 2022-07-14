# html = '<img class=" u-hidden-with-nojs" data-src="https://static.ah.nl/static/gall/img_83234_Gall_500.png" src=\'https://static.ah.nl/static/gall/img_83234_Gall_60.png\' data-'
#
#
# html = html.replace('<img class=" u-hidden-with-nojs" data-src="', '')
# image_end = html.find('" src=')
# image = html[:image_end]
# print(image)
matching2_discount = '<span class="u-sr-only">Van: &euro; 19.99 voor: &euro; 13.99</span>'
price_begin = matching2_discount.find('voor: &euro; ')
price = matching2_discount[price_begin+len('voor: &euro; '):]
price = price.replace('</span>', '')
print(price)