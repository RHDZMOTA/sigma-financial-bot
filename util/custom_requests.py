import json
from google.appengine.api import urlfetch

urlfetch.set_default_fetch_deadline(45)


def get_request_json(url):
    r = urlfetch.fetch(url=url, method='GET', deadline=45)
    #string_resp = json.dumps(r.content)
    #print (type(r.content))
    #print str(r.content.encode('utf8', 'replace').decode('utf8'))
    return json.loads(r.content)#json.loads(json.dumps(r.content))


#def get_request_json(url):
#    import requests
#    r = requests.get(url=url).json()
#    return r

def get_request_content(url):
    r = urlfetch.fetch(url=url, method='GET', deadline=45)
    return r.content

