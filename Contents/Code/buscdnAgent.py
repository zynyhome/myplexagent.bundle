import urllib2
import ssl
from lxml import html



SEARCH_URL = 'https://www.buscdn.life/en/search/%s'
curID = "buscdn"

def getElementFromUrl(url):
    return html.fromstring(request(url))

def request(url):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 
    #url="https://www.buscdn.life"
    Log('Search Query: %s' % url)
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
        
    	#Log(urllib2.urlopen(request,context=ctx).read())

        for movie in getElementFromUrl(url).xpath('//a[contains(@class,"movie-box")]'):
            Log('Search Result: %s' % movie)
            movieid = movie.get("href").replace('/',"_")
            results.Append(MetadataSearchResult(id= curID + "|" + str(movieid), name=str(movieid), score=100,lang=lang))
            
        results.Sort('score', descending=True)
        Log(results)
    except Exception as e: Log(e)


def update(metadata, media, lang): 
    if curID != str(metadata.id).split("|")[0]:
        return

    query = str(metadata.id).split("|")[1].replace('_','/')
    Log('Update Query: %s' % str(query))
    try:
        movie = getElementFromUrl(query).xpath('//div[@class="container"]')[0]
        Log('Find Moive: %s' % elementToString(movie))
        #post
        image = movie.xpath('.//a[contains(@class,"bigImage")]')[0]
        thumbUrl = image.get('href')
        thumb = request(thumbUrl)
        posterUrl = image.get('href')
        metadata.posters[posterUrl] = Proxy.Preview(thumb)

        #name
        metadata.title = metadata.id
        #metadata.movie.xpath('.//p[contains(@class,"level has-text-grey-dark")]')[0].text_content().strip()
    except Exception as e: Log(e)