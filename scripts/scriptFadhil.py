#python
import sys

import requests

import random


########### USAGE MANUAL ###################

#### USE AS python trial.py {imagefilename} {cloudmersive apikey} {twinword apikey}

#### USAGE LIMITS

## Cloudmersive @ 1500/month, twinword @ 100/month, use sparringly #####


############################################

    
    
def main():
    a,b = fadhilProcess(sys.argv[1], sys.argv[2], sys.argv[3])
    print(a)
    print(b)
    #pass


def fadhilProcess(lokasi, apiCM, apiTW):
    base_url = 'https://api.cloudmersive.com/image/recognize/describe'
    api_key = apiCM

    header = {'Apikey': api_key}

    files = {'imageFile': open(lokasi,'rb')}


    r = requests.post(base_url, files=files, headers=header)
    #print(r.json())

    ###################################################

    hasil = r.json()['BestOutcome']['Description']

    url2 = 'https://twinword-emotion-analysis-v1.p.rapidapi.com/analyze/'

    header2 = {
        'x-rapidapi-host': "twinword-emotion-analysis-v1.p.rapidapi.com",
        'x-rapidapi-key': apiTW
        }

    querystring = {'text': hasil}

    r2 = requests.get(url2, headers=header2, params=querystring)

    #print(r2.json())
    hasil2 = r2.json()['emotions_detected'][0]

    url3 = 'https://quote-garden.herokuapp.com/quotes/search/' + hasil2

    r3 = requests.get(url3)

    ### added randomizer for quotes ###
    upperlimit = r3.json()['count']
    randChoice = random.randrange(0,upperlimit)

    text = r3.json()['results'][randChoice]['quoteText']
    author = r3.json()['results'][randChoice]['quoteAuthor']
    return (text, author)


if __name__ == "__main__":
    main()