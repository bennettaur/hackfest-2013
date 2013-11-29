import requests
import hashlib
from HTMLParser import HTMLParser
import time
import binascii
import base64

class MyParser(HTMLParser):

    def __init__(self, base_url):
        HTMLParser.__init__(self)
        self.found_message = False
        self.base_url = base_url
        self.hasher = hashlib.sha512()
        self.count = 0
        self.data = ''

    def handle_starttag(self, tag, attrs):
        #print attrs
        if (u'class', u'message') in attrs:
            self.found_message = True

    def handle_endtag(self, tag):
        if self.found_message and tag == 'div':
            self.found_message = False

    def handle_data(self, data):
        if self.found_message:
            self.count +=1
            if self.count == 2:
                self.raw_data = data[2:]
                self.data = self.raw_data
                #self.data = base64.b64encode(self.raw_data).strip()
                # length = len(self.raw_data)
                # segment = 57
                # for x in xrange(0, len(self.raw_data), segment):
                #     end = x+segment
                #     if end < length:
                #         self.data += binascii.b2a_base64(self.raw_data[x:end]).strip()
                #     else:
                #         self.data += binascii.b2a_base64(self.raw_data[x:]).strip()
                # if len(self.data) != 8192:
                #     print "Error with the hash to parse. Length was: {}".format(len(data))
                #     with open('hash', 'w') as hashfile:
                #         hashfile.write(data)
                self.hasher.update(self.data)
                self.send(self.hasher.hexdigest())
                # print "To hash:"
                # print data[2:]
                # print "len: ", len(data[2:])

    def send(self, hash):
        r = requests.get(self.base_url + hash)
        with open('output.txt', 'w') as out:
            out.write(r.text)

parser = MyParser('http://prog.ctf.hf/reloaded/')

start = time.time()
r = requests.get(parser.base_url)

parser.feed(r.text)

finish = time.time()
with open("first_req.txt", 'w') as first:
    first.write(r.text)

with open('hash', 'w') as hashfile:
    hashfile.write(parser.data)
#print r.text
print "########### Parsing Finished in {}##################".format(finish-start)