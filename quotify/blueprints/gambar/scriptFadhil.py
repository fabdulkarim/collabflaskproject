#python
import sys, os

import requests

import random

from PIL import Image

########### USAGE MANUAL ###################

#### USE AS python trial.py {imagefilename} {cloudmersive apikey} {twinword apikey}

#### USAGE LIMITS

## Cloudmersive @ 1500/month, twinword @ 100/month, use sparringly #####


############################################

    
    
def main():
    checkResize(sys.argv[1])
    #a,b = fadhilProcess(sys.argv[1], sys.argv[2], sys.argv[3])
    #print(a)
    #print(b)
    #pass


def fadhilProcess(lokasi, apiCM, apiTW):
    base_url = 'https://api.cloudmersive.com/image/recognize/describe'
    api_key = apiCM

    checkResize(lokasi)

    header = {'Apikey': api_key}

    files = {'imageFile': open(lokasi,'rb')}


    r = requests.post(base_url, files=files, headers=header)
    #print(r.json())

    if r.status_code is not 200:
        print(r.status_code, r.text)
    ###################################################

    hasil = r.json()['BestOutcome']['Description']

    url2 = 'https://twinword-emotion-analysis-v1.p.rapidapi.com/analyze/'

    header2 = {
        'x-rapidapi-host': "twinword-emotion-analysis-v1.p.rapidapi.com",
        'x-rapidapi-key': apiTW
        }

    querystring = {'text': hasil}

    r2 = requests.get(url2, headers=header2, params=querystring)

    if r2.status_code is not 200:
        print(r2.status_code, r2.text)
    #print(r2.json())
    #hasil2 =
    sav = r2.json() 
    all_emo = list(sav['emotion_scores'].keys())
    high = 0
    hasil2 = None
    for i in all_emo:
        if sav['emotion_scores'][i] > high:
            high = sav['emotion_scores'][i]
            hasil2 = i

    url3 = 'https://quote-garden.herokuapp.com/quotes/search/' + hasil2

    r3 = requests.get(url3)

    if r3.status_code is not 200:
        print(r3.status_code, r3.text)
    ### added randomizer for quotes ###
    upperlimit = r3.json()['count']
    randChoice = random.randrange(0,upperlimit)

    text = r3.json()['results'][randChoice]['quoteText']
    author = r3.json()['results'][randChoice]['quoteAuthor']
    return (text, author)


def checkResize(lokasi):
    #print(os.stat(lokasi).st_size)
    #img = Image.open(lokasi)
    #img.save(lokasi,optimize=True, quality=75)
    #print(os.stat(lokasi).st_size)
    img = Image.open(lokasi)
    width, height = img.size
    fl_sz = int(os.stat(lokasi).st_size)
    while (fl_sz > 5000000) or (width > 1000) or (height > 1000):
        #print(os.stat(lokasi).st_size)
        img = Image.open(lokasi)
        if (width > 1000) or (height > 1000):
            img = img.resize(size=(round(width*0.8), round(height*0.8)))
        img.save(lokasi,optimize=True, quality=80)
        width, height = img.size
        fl_sz = int(os.stat(lokasi).st_size)
        


if __name__ == "__main__":
    main()