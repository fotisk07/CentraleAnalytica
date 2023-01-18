
"""
    Ce programme permet la recherche d'images
    sur internet en rapport à des mots et la création
    d'une mosaüqe avec ces images.
"""

import os
import shutil
from PIL import Image
import requests
from bs4 import BeautifulSoup


def fetch_image(query_list, keyword):
    """Cherche des images en lien avec les mots fournis
    et enregistre dans les assets une mosaïque de ces images

    Args:
        query_list (list): liste des mots lié à la recherche d'image
    """

    images = []
    # dowload images
    for i, query in enumerate(query_list):
        url = 'https://www.google.com/search?as_st=y&tbm=isch&as_q=' + query + ' ' + keyword + \
            '&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=active&tbs=iar:s,\
                ift:jpg#imgrc=nvtpkfVUedp65M'

        htmldata = requests.get(url, timeout=10).text
        soup = BeautifulSoup(htmldata, 'html.parser')

        item = soup.find_all('img')[2]

        url = item['src']
        file_name = 'image' + str(i) + '.jpg'
        images.append(file_name)
        res = requests.get(url, stream=True, timeout=10)

        if res.status_code == 200:
            with open(file_name, 'wb') as file:
                shutil.copyfileobj(res.raw, file)

        else:
            print('Image Couldn\'t be retrieved')

    # build mosaic

    new = Image.new("RGBA", (2000, 1500))

    for i in range(4):
        for j in range(3):
            img = Image.open(images[3*i+j])
            img = img.resize((500, 500))
            new.paste(img, (500*i, 500*j))
            os.remove(images[3*i+j])
    return new
