import  requests
import json

app_id = '38f2798f'
app_key = '5624c7925eac00132d52179385c02b29'
language = 'en'
word_id = 'Ace'
url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/'  + language + '/'  + word_id.lower()
urlFR = 'https://od-api.oxforddictionaries.com:443/api/v2/stats/frequency/word/'  + language + '/?corpus=nmc&lemma=' + word_id.lower()
r = requests.get(url, headers = {'app_id' : app_id, 'app_key' : app_key})

print("text \n" + r.text)
print("json \n" + json.dumps(r.json()))