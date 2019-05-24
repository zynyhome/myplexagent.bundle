import re
import urllib2
import json
import ssl


curID = "avgle"
def search(query, results, media, lang):
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
			score = 90 - (idx*5)
			new_result = dict(id= curID + "|" + str(id), name=name, year='', score=score, lang=lang)
			results.Append(MetadataSearchResult(**new_result))

def update(metadata, media, lang):

	if curID != str(metadata.id).split("|")[0]:
		return

	Log('update metadata.id:%s' % metadata.id)
	vid = str(metadata.id).split("|")[1]
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
		summary = name + '\n'
		summary += 'Keyword : %s\n' % metadata.tagline
		summary += video['embedded_url'] + '\n'
		summary += video['preview_url'] + '\n'
		metadata.summary = summary
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