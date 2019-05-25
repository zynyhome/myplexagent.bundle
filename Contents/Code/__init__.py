import avgleAgent
import onejavAgent
import buscdnAgent
import re
import ssl
from SSLEXTRA import sslOptions




# URLS
def Start():
    HTTP.CacheTime = CACHE_1MINUTE
    HTTP.Headers['User-Agent'] = 'Plex Media Server/%s' % Platform.ServerVersion
    HTTP.Headers['Cookie'] = 'cok=1'

class OneJavAgent(Agent.Movies):
    name = 'onejav'
    languages = [Locale.Language.English,  Locale.Language.Japanese]
    primary_provider = True
    accepts_from = ['com.plexapp.agents.localmedia']
    
    
    def search(self, results, media, lang, manual):
        Log('media.name :%s' % media.name)
        file_name = media.name.replace(' ', '-')

        code_match_pattern1 = '[a-zA-Z]{2,5}[-_][0-9]{3,5}'
        code_match_pattern2 = '([a-zA-Z]{2,5})([0-9]{3,5})'
        re_rules1 = re.compile(code_match_pattern1, flags=re.IGNORECASE)
        re_rules2 = re.compile(code_match_pattern2, flags=re.IGNORECASE)
    
        file_code1 = re_rules1.findall(file_name)
        file_code2 = re_rules2.findall(file_name)
        if file_code1:
            query = file_code1[0].upper()
        elif file_code2:
            query = file_code2[0][0].upper() + '-' + file_code2[0][1]
        else:
            query = file_name

            
        Log('query keyword :%s' % query)
        buscdnAgent.search(query,results,media,lang)
        onejavAgent.search(query,results,media,lang)
        avgleAgent.search(query,results,media,lang)

    def update(self, metadata, media, lang): 
        onejavAgent.update(metadata,media,lang)
        avgleAgent.update(metadata,media,lang)
        buscdnAgent.update(metadata,media,lang)