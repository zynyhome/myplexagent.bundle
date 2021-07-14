import urllib2
import json
import ssl
from lxml import html



SEARCH_URL = 'https://www.javbus.com/search/%s'
PIC_BASE_URL = 'https://www.javbus.com/'
curID = "javbus"

def getElementFromUrl(url):
    return html.fromstring(request(url))

def request(url):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,}
    request = urllib2.Request(url,headers=headers)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return urllib2.urlopen(request,context=ctx).read()

def elementToString(ele):
    html.tostring(ele, encoding='unicode')

def search(query, results, media, lang):
    try:
        url=str(SEARCH_URL % query)
        for movie in getElementFromUrl(url).xpath('//a[contains(@class,"movie-box")]'):
            img = PIC_BASE_URL + movie.xpath('.//img')[0].get("src")
            results.Append(MetadataSearchResult(id=curID + "|" + str(query), thumb=img , name=query, score=100,lang=lang))

        results.Sort('score', descending=True)
    except Exception as e: pass


def update(metadata, media, lang):
    if curID != str(metadata.id).split("|")[0]:
        return
    try:
        url=str(SEARCH_URL % str(metadata.id).split("|")[1])
        link = getElementFromUrl(url).xpath('//a[contains(@class,"movie-box")]')[0]
        movie = getElementFromUrl(link.get("href")).xpath('//div[@class="container"]')[0]
        #post
        #  the horizon form which are not suiable for plex
        #  let use the thumb instead

        thumb = PIC_BASE_URL + link.xpath('.//img')[0].get("src")
        metadata.posters[thumb] = Proxy.Preview(thumb)

        #art
        bigImage = PIC_BASE_URL+ movie.xpath('.//a[contains(@class,"bigImage")]')[0].get('href')
        metadata.art[bigImage] = Proxy.Preview(bigImage)


        #name
        if movie.xpath('.//h3'):
            metadata.title = movie.xpath('.//h3')[0].text_content().strip()

        #actors
        metadata.roles.clear()
        for actor in  movie.xpath('.//div[@id="star-div"]'):
            elementToString(actor)
            # TODO read actor info in another page
            img = actor.xpath('.//img')[0]
            role = metadata.roles.new()
            role.name = img.get("title")
            # role.photo = img.get("src")

        # TODO Genres.
        # if len(movie.xpath('genre')) > 0:
        #     metadata.genres.clear()
        #     for genre in [g.get('genre') for g in movie.xpath('genre')]:
        #     metadata.genres.add(genre)

    except Exception as e: Log(e)