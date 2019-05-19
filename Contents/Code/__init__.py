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
    
    def search(self, results, media, lang):
        title = media.name
        if media.primary_metadata is not None:
            title = media.primary_metadata.title
  
        query = String.URLEncode(String.StripDiacritics(title))
        Log('Search Query: %s' % str(SEARCH_URL % query))

        for movie in HTML.ElementFromURL(SEARCH_URL % query).xpath('//div[contains(@class,"card mb-3")]'):
            name = movie.xpath('.//img[contains(@class,"level has-text-grey-dark")]')
            id = movie.xpath('.//img[contains(@class,"title is-4 is-spaced")]/a')
            score = 100 - (idx*5)
            new_result = dict(id=id, name=name, year='', score=score)
            results.Append(MetadataSearchResult(**new_result))


    def update(self, metadata, media, lang): 
        for movie in HTML.ElementFromURL(SEARCH_URL % query).xpath('//div[contains(@class,"card mb-3")]'):
            image = movie.xpath('.//img[contains(@class,"image")]')
            thumbUrl = image.get('src')
            thumb = HTTP.Request(thumbUrl)
            
            posterUrl = image.get('src')
            metadata.posters[posterUrl] = Proxy.Preview(thumb)