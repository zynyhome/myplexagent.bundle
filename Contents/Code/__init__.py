import re
import datetime
import random
import urllib2

# URLS
SEARCH_URL = 'https://onejav.com/search/%s'

def Start():
    HTTP.CacheTime = CACHE_1MINUTE
    HTTP.SetHeader('User-agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)')

class OneJavAgent(Agent.Movies):
    name = 'onejav'
    languages = [Locale.Language.English,  Locale.Language.Japanese]
    primary_provider = True
    accepts_from = ['com.plexapp.agents.localmedia']
    
    def search(self, results, media, lang, manual):
        query = media.name.replace(' ', '-')
        Log('Search Query: %s' % str(SEARCH_URL % query))

        for movie in HTML.ElementFromURL(SEARCH_URL % query).xpath('//div[contains(@class,"card mb-3")]'):
            movieid = movie.xpath('.//h5[contains(@class,"title is-4 is-spaced")]/a')[0].text_content().strip()
            Log('Search Result: id: %s' % movieid)
            results.Append(MetadataSearchResult(id=str(movieid), name=str(movieid), score=100,lang=lang))
            
        
        results.Sort('score', descending=True)
        Log(results)

    def update(self, metadata, media, lang): 
        query = metadata.id
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