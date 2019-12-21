#python
import sys

import requests


########### USAGE MANUAL ###################

#### USE AS python trial.py {imagefilename} {cloudmersive apikey} {twinword apikey}

#### USAGE LIMITS

## Cloudmersive @ 1500/month, twinword @ 100/month, use sparringly #####


############################################


base_url = 'https://api.cloudmersive.com/image/recognize/describe'
api_key = sys.argv[2]

header = {'Apikey': api_key}

files = {'imageFile': open(sys.argv[1],'rb')}


r = requests.post(base_url, files=files, headers=header)
print(r.json())

###################################################

hasil = r.json()['BestOutcome']['Description']

url2 = 'https://twinword-emotion-analysis-v1.p.rapidapi.com/analyze/'

header2 = {
    'x-rapidapi-host': "twinword-emotion-analysis-v1.p.rapidapi.com",
    'x-rapidapi-key': sys.argv[3] 
    }

querystring = {'text': hasil}

r2 = requests.get(url2, headers=header2, params=querystring)

print(r2.json())
hasil2 = r2.json()['emotions_detected'][0]

url3 = 'https://quote-garden.herokuapp.com/quotes/search/' + hasil2

r3 = requests.get(url3)

### added randomizer for quotes ###
upperlimit = r3.json()['count']
randChoice = random.randrange(0,upperlimit)

print(r3.json()['results'][randChoice]['quoteText'])
