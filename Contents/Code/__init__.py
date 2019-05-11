# -*- coding: UTF-8 -*-
import re
import urllib2
import json
import ssl

def Start():
	Log('start my agent')
	pass

class AvgleAgent(Agent.Movies):
	name = 'Avgle.com'
	languages = [Locale.Language.English,  Locale.Language.Japanese]
	primary_provider = True
	accepts_from = ['com.plexapp.agents.localmedia']


	def search(self, results, media, lang, manual):
		Log('media.name:%s' % media.name)
		Log('lang:%s' % lang)
		Log('manual:%s' % manual)
		query = media.name.replace(' ', '-')
		url = 'https://api.avgle.com/v1/jav/%s/0?limit=10' % query
		Log('SEARCH URL:%s' % url)
		request = urllib2.Request(url)
		response = urllib2.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
		data = json.load(response, encoding="utf-8")
		Log('SEARCH DATA:%s' % data)
		if data['success']:
			videos = data['response']['videos']
			for idx in range(0, len(videos)):
				video = videos[idx]
				id = video['vid']
				name = video['title']
				name = name
				year = media.year
				score = 100 - (idx*5)
				new_result = dict(id=id, name=name, year='', score=score, lang=lang)
				results.Append(MetadataSearchResult(**new_result))

	def update(self, metadata, media, lang):
		Log('update metadata.id:%s' % metadata.id)
		vid = metadata.id
		url = 'https://api.avgle.com/v1/video/%s' % vid
		request = urllib2.Request(url)
		response = urllib2.urlopen(request, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
		data = json.load(response, encoding="utf-8")
		Log('UPDATE DATA:%s' % data)
		if data['success']:
			video = data['response']['video']
			name = video['title']
			name = name
			metadata.title = name
			metadata.tagline = video['keyword']
			str = name + '\n'
			str += 'Keyword : %s\n' % metadata.tagline
			str += video['embedded_url'] + '\n'
			str += video['preview_url'] + '\n'
			metadata.summary = str
			poster_url = video['preview_url']
			try:
				#for mode in ['left', 'right']:
				if Prefs['POSTER_SPLIT_PAGE_URL'] == '' or Prefs['POSTER_SPLIT_PAGE_URL'] is None: raise
				for mode in ['right']:
					tmp = '%s?mode=%s&url=%s' % (Prefs['POSTER_SPLIT_PAGE_URL'], mode, poster_url)
					poster = HTTP.Request( tmp )
					try: metadata.posters[tmp] = Proxy.Media(poster)
					except: pass
			except Exception as e:
				poster = HTTP.Request( poster_url )
				try: metadata.posters[poster_url] = Proxy.Media(poster)
				except: pass


