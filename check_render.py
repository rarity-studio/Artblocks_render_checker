

## Render checker for static AB projects
## by aerotrader
## -- prints the number of incorrectly rendered image(s)


from PIL import Image
import os
import requests
import imagehash
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

#project prefix, max mint and target size for faster processing
prefix='37'
max=520
basewidth = 400

os.chdir('WORKING_DIRECTORY') # download destination for images
add='https://mainnet.oss.nodechef.com/'
add_live='https://api.artblocks.io/generator/'
# path to your chromedriver (https://sites.google.com/a/chromium.org/chromedriver/downloads)
driver = webdriver.Chrome(options=options, executable_path='PATH/TO/chromedriver')



for i in range(0,max):
    # get rendered image
    num=str(i)
    num_l=num.zfill(6)
    name=prefix+num_l+'.png'
    image_url=add+prefix+num_l+'.png'
    img_render = requests.get(image_url).content
    # save it
    with open(name, 'wb') as handler:
            handler.write(img_render)
    # resize it
    img = Image.open(name)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(name)

    # get live generated image
    image_url_live=add_live+prefix+num_l 
    name_live=prefix+'00'+num_l+'_live'+'.png'
    driver.get(image_url_live)
    base64_image = driver.execute_script("return document.querySelectorAll('canvas')[1].toDataURL('image/png').substring(21);")
    img_live = base64.b64decode(base64_image)
    # save it
    with open(name_live, 'wb') as f:
        f.write(img_live)

    # resize it
    img = Image.open(name_live)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(name_live)

    # compare images
    hash0 = imagehash.average_hash(Image.open(name))
    hash1 = imagehash.average_hash(Image.open(name_live))
    cutoff = 5 # edit for different sensitivity

    if hash0 - hash1 > cutoff:
        # if signif. differences
        print(i)
