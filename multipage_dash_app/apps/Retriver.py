import urllib2
import ssl
import json

class Retriver:
    def __init__(self, server_base_url):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE
        self.server_base_url = server_base_url

    def geturl_as_raw( self, url ):
        contents = urllib2.urlopen(self.server_base_url+url, context=self.ctx).read()
        return contents

    def geturl_as_dict( self, url ):
        response = urllib2.urlopen(self.server_base_url+url, context=self.ctx)
        data = json.load( response )
        return data
