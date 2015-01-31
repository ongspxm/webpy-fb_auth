import web
import json
import time
import urllib
import urlparse

FB_APP_SECRET = '<App Secret>'
FB_APP_ID = '<App ID>'

urls = [
    '/', 'Index',
    '/li', 'Login',
    '/lo', 'Logout'
]
app = web.application(urls, globals())

def getURL():
    return web.ctx.home + web.ctx.fullpath

class Index:
    def GET(self):
        html = "<a href='/li'>FB Login</a>"

        uid = web.cookies().get('fb_uid')
        uname = web.cookies().get('fb_uname')

        if uid:
            html = "<img src='https://graph.facebook.com/"+uid+"/picture' /><br /><h4>"+uname+"</h4><a href='/lo'>Logout</a>"

        return '''
<html>
<body>
    <h1>Hi!!!</h1>
    '''+html+'''
</body>
</html>
        '''

class Login:
    def GET(self):
        i = web.input(code = None)
        args = dict(client_id=FB_APP_ID, redirect_uri=getURL())

        ### Authentication stage
        if not i.code:
            web.seeother('http://www.facebook.com/dialog/oauth?' + urllib.urlencode(args))
            return

        ### Access token stage
        args['code'] = i.code
        args['client_secret'] = FB_APP_SECRET
        req = 'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(args)
        res = urlparse.parse_qs(urllib.urlopen(req).read())
        tkn = res['access_token'][-1]

        ### Retrieving profile information
        req =  'https://graph.facebook.com/me?' + urllib.urlencode(dict(access_token=tkn))
        res = json.load(urllib.urlopen(req))

        t = time.time() + 7*86400
        web.setcookie('fb_uid', res['id'], t)
        web.setcookie('fb_uname', res['name'], t)

        web.seeother('/')

class Logout:
    def GET(self):
        web.setcookie('fb_uid', '', time.time() - 86400)
        web.setcookie('fb_uname', '', time.time() - 86400)
        web.seeother('/')

if __name__=='__main__':
    app.run()
