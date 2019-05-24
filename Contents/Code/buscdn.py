import re
import datetime
import random
import urllib2

SEARCH_URL = 'https://www.buscdn.life/en/search/%s'

curID = "buscdn"

def search(query, results, media, lang):
    query = media.name.replace(' ', '-')
    Log('Search Query: %s' % str(SEARCH_URL % query))

    for movie in HTML.ElementFromURL(SEARCH_URL % query).xpath('//div[contains(@class,"card mb-3")]'):
        movieid = movie.xpath('.//h5[contains(@class,"title is-4 is-spaced")]/a')[0].text_content().strip()
        Log('Search Result: id: %s' % movieid)
        results.Append(MetadataSearchResult(id= curID + "|" + str(movieid), name=str(movieid), score=100,lang=lang))
        
    
    results.Sort('score', descending=True)
    Log(results)

def update(metadata, media, lang): 

    if curID != str(metadata.id).split("|")[0]:
        return

    query = str(metadata.id).split("|")[1]
    Log('Update Query: %s' % str(SEARCH_URL % metadata.id))
    try:
        movie = HTML.ElementFromURL(SEARCH_URL % query).xpath('//div[contains(@class,"card mb-3")]')[0]

        #post
        image = movie.xpath('.//img[contains(@class,"image")]')[0]
        thumbUrl = image.get('src')
        thumb = HTTP.Request(thumbUrl)
        posterUrl = image.get('src')
        metadata.posters[posterUrl] = Proxy.Preview(thumb)

        #name
        metadata.title = metadata.id
        metadata.movie.xpath('.//p[contains(@class,"level has-text-grey-dark")]')[0].text_content().strip()
    except: pass