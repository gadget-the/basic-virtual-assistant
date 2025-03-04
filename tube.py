import bs4 as bs, requests, webbrowser#, json
from requests_html import HTMLSession
# from urllib.request import urlopen
import threading

def tube(term = "fireball pitball", resSlot = 0):
    #https://www.youtube.com/results?search_query=fireball+pitbull
    url = "https://www.youtube.com/results?search_query="
    url += term.replace(" ", "+")

    try:
        session = HTMLSession()
        response = session.get(url)
        response.html.render(sleep=1, keep_page = True, scrolldown = 2, timeout=30)
    except Exception as e:
        print(e)
        return ("Unable to get video, due to: " + str(e) + " Error")

    res = []

    for lnk in response.html.find('a#video-title'):
        res.append(next(iter(lnk.absolute_links)))

    tRes = res[resSlot]

    webbrowser.open(tRes)
    return tRes, url#, res

def lyric(term = "fireball pitball lyrics"):
    if not any([x in term for x in ["lyric", "lyrics", "words"]]):
        term += " lyrics"
    #"https://www.google.com/search?q=" + "pitbull+fireball+lyrics"
    url = "https://www.google.com/search?q="
    url += term.replace(" ", "+")
    res = ""
    # print(term, url)

    try:
        soup = bs.BeautifulSoup(requests.get(url).content, 'html.parser')
        span = soup.find_all("div", attrs={'class': 'BNeawe tAd8D AP7Wnd'})[2] # div class="BNeawe tAd8D AP7Wnd"
        res = span.text

    except Exception as e:
        return ("Unable to get lyrics, due to: " + str(e) + " Error")

    return res, url#, span, soup

if __name__ == "__main__":
    # print(tube("verbatim mother mother"))
    # print(tube("fireball pitbull"))
    # print(tube(input("> ")))

    # print(lyric(input("> ")))
    # print(lyric("pitbull fireball")[0])
    # print(lyric("verbatim mother mother"))
    # print(lyric("verbatim mother mother")[0])

    # "Unable to get lyrics, due to: list index out of range Error" - doesn't work because google doesn't actually display the lyrics in the search results;need to find a better way of getting the lyrics
    # print(lyric("trouble by taylor swift?"))

    # print(tube("abc 123 jackson5"))

    music = threading.Thread(target=tube, args=("fireball pitbull",))
    music.start()
    print(music.is_alive)