import bs4 as bs, requests, webbrowser, json, wikipedia
from urllib.request import urlopen

def search(term = "", engine = "google"):
    reqUrl = ""
    if engine == 'yandex':
        #make change for yandex searches "https://www.yandex.com/search/?text=biggest+naval+ships+ever+built&lr=103356"
        mainUrl = "https://www.yandex.com/search/?text="
        reqUrl = mainUrl + term.replace(" ", "+").replace(",", "%2C")
    elif engine == "yahoo":
        #make change for yahoo searches "https://search.yahoo.com/search?p="
        mainUrl = "https://search.yahoo.com/search?p="
        reqUrl = mainUrl + term.replace(" ", "+").replace(",", "%2C")
    elif engine == "baidu":
        #for Baidu(basically chinese google) "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=hello%20kitty"
        mainUrl = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd="
        # reqUrl = mainUrl + term.replace(" ", "%20")
        reqUrl = mainUrl + term
    elif engine == "instagram":
        mainUrl = "https://www.instagram.com/explore/search/keyword/?q="
        reqUrl = mainUrl + term
    elif engine == "spotify":
        mainUrl = "https://open.spotify.com/search/"
        reqUrl = mainUrl + term.replace(",", "%2C")
    elif engine == "youtube":
        # https://www.youtube.com/results?search_query=pepperoni+bread
        mainUrl = "https://www.youtube.com/results?search_query="
        reqUrl = mainUrl + term.replace(" ", "+").replace(",", "%2C")
    elif engine == "amazon":
        # https://www.amazon.com/s?k=kentucky%2C+usa&crid=18JBHEP4G6V2U&sprefix=kentucky%2C+usa%2Caps%2C129&ref=nb_sb_noss
        mainUrl = "https://www.amazon.com/s?k="
        reqUrl = mainUrl + term.replace(" ", "+").replace(",", "%2C")
    else: 
        mainUrl = "https://www." + engine + ".com/search?q="
        if term:
            reqUrl = mainUrl + term.replace(" ", "+").replace(",", "%2C")
    
    soup = None
    try:
        soup = bs.BeautifulSoup(requests.get(reqUrl).content, 'html.parser')
    except Exception as e:
        return ("Unable to return results, due to: " + str(e) + " Error")

    webbrowser.open(reqUrl)
    return reqUrl, soup

def ddgSrch(term = ""):
    reqUrl = ""
    if term:#uses duckduckgo's Instant Answer API(https://duckduckgo.com/api)
        reqUrl = "https://api.duckduckgo.com/?q=" + term.replace(" ", "+").replace(",", "%2C") + "&format=json&pretty=1"
    
    # try:
    #     soup = bs.BeautifulSoup(requests.get(reqUrl).content, 'html.parser')
    # except Exception:
    #     print(Exception)

    try:
        response = urlopen(reqUrl)
        data_json = json.loads(response.read())
    except Exception as e:
        return ("Unable to return results, due to: " + str(e) + " Error")

    abstract = None
    abstractSource = None

    if data_json['Abstract']:
        abstract = data_json['Abstract']
        abstractSource = data_json['AbstractSource']
    
    # webbrowser.open(reqUrl)
    return abstract, abstractSource#, reqUrl

def dictDef(term = "", meaning_index = 0, definition_index = 0):
    ''' (word, part of speech, definition, info source, total number of meanings) '''
    # Free Dictionary API - https://dictionaryapi.dev/
    baseUrl = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    # reqUrl = baseUrl + term
    reqUrl = baseUrl + term.replace(" ", "+")
    # print(reqUrl)

    try:
        response = urlopen(reqUrl)
        data_json = json.loads(response.read())
    except Exception as e:
        # return "Unable to return results, due to: " + str(e) + " Error"
        return None

    if meaning_index <= len(data_json[0]['meanings']):
        if definition_index <= len(data_json[0]['meanings'][meaning_index]['definitions']):
            return data_json[0]['word'], data_json[0]['meanings'][meaning_index]['partOfSpeech'], data_json[0]['meanings'][meaning_index]['definitions'][definition_index]['definition'], data_json[0]['sourceUrls'][0], len(data_json[0]['meanings']), len(data_json[0]['meanings'][meaning_index]['definitions']), reqUrl
        
        else:
            return None

    else:
        # print(reqUrl, data_json)
        # print(data_json[0], len(data_json[0]['meanings']))
        # print(data_json[0]['meanings'])
        return None

def wikiSearch(term = ""): # https://pypi.org/project/wikipedia/
    summ = wikipedia.summary(term)
    site = wikipedia.page(term).url

    # sea = wikipedia.search(term)
    # print(sea)

    return summ, site

if __name__ == "__main__":
    # print(search("what is the capitol of Brazil")[0])
    # print("test, ", ddgSrch(term = "paris, texas")[1])
    # print("From DuckDuckGo:\n Result: %s \nSource: %s." % ddgSrch(term = input("> ")))
    # print(ddgSrch("McDonald's"))
    # print('Using Free Dictionary API:\n"%s" is a %s, meaning:\n"%s"' % dictDef("swallow"))
    # print(dictDef("swallow"))
    # print(dictDef("sleight"))
    print(dictDef("cornucopia"))
    # print(dictDef("cornucopia", definition_index = 1))
    # print(wikiSearch("Wikipedia"))
    # print(wikiSearch("McDonald's"))
    # print(wikiSearch(input("> ")))

    # "https://libgen.li/index.php?req=The+Anthropology+of+Religion%2C+Magic%2C+and+Witchcraft.++Rebecca+L.+Stein+and+Philip+L.+Stein%2C+Fourth+Edition+&columns%5B%5D=t&columns%5B%5D=a&columns%5B%5D=s&columns%5B%5D=y&columns%5B%5D=p&columns%5B%5D=i&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=s&objects%5B%5D=a&objects%5B%5D=p&objects%5B%5D=w&topics%5B%5D=l&topics%5B%5D=c&topics%5B%5D=f&topics%5B%5D=a&topics%5B%5D=m&topics%5B%5D=r&topics%5B%5D=s&res=25&filesuns=all"