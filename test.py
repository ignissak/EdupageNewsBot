import requests
import json
import bs4 as bs

session = requests.session()

request_url = "https://gamtt.edupage.org/login/index.php"

csrf_response = session.get(request_url).content.decode()

# we parse the token from the html
csrf_token = csrf_response.split(
    "name=\"csrfauth\" value=\"")[1].split("\"")[0]

# now everything is the same as in the first approach, we just add the csrf token
parameters = {
    "username": 'JakubBordas',
    "password": 'PGT6R2KPMN',
    "csrfauth": csrf_token
}
request_url = "https://gamtt.edupage.org/login/edubarLogin.php"

response = session.post(request_url, parameters)

js_json = response.content.decode().split("$j(document).ready(function() {")[1] \
    .split(");")[0] \
    .replace("\t", "") \
    .split("userhome(")[1] \
    .replace("\n", "") \
    .replace("\r", "")
data = json.loads(js_json)
idd = 0

for item in data.get("items"):
    if item.get("typ") == "news":
        idd = item.get("ineid")
        break

request_url = "https://gamtt.edupage.org/news"
response = session.post(request_url).content.decode()

#print(response)

soup = bs.BeautifulSoup(response, 'lxml')
# news_DFHtml_1-[ID]
supa = soup.find('div', attrs={'id': "news_DFHtml_1-" + idd})
print(supa)
print(supa.get("erte-text-inner"))