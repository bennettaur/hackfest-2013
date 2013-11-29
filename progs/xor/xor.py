import requests
import time
from HTMLParser import HTMLParser
import re
from threading import Thread
import base64

class Worker(Thread):

    def __init__(self, id, base_url, key, decoded_msg):
        self.id = id
        self.key = key
        self.msg = decoded_msg
        self.base_url = base_url
        super(Worker, self).__init__()

    def run(self):

        new_key = (self.key[self.id:self.id+10] * ((len(self.msg)/len(self.key)) + 1))[:len(self.msg)]
        xored = base64.b64encode(''.join(chr(ord(a) ^ ord(b)) for a,b in zip(new_key, self.msg)))
        #xored = ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(self.key, self.msg))
        self.send(xored)


    def send(self, answer):
        r = requests.get(self.base_url + answer)
        if "Wrong answer or too slow!" not in r.text:
            with open('output{}.txt'.format(self.id), 'w') as out:
                out.write("Trying answer:\n")
                out.write(answer + '\n')
                out.write(r.text)


class MyParser(HTMLParser):

    def __init__(self, base_url):
        HTMLParser.__init__(self)
        self.found_xor = base_url
        self.found_message = False
        self.base_url = base_url
        self.msg_count = 0
        self.xor_count = 0
        self.msg = ''
        self.xor = ''
        self.data = ''

    # def handle_starttag(self, tag, attrs):
    #     if (u'class', u'message') in attrs:
    #         if self.found_xor:
    #             self.found_message = True
    #         else:
    #             self.found_xor = True

    def handle_endtag(self, tag):
        if self.found_message and tag == 'div':
            self.found_message = False

    def handle_data(self, data):
        if self.found_message:
            self.msg = data.strip()
            self.found_message = False
            i = 0
            while i+10 < len(self.xor):
                print "starting thread " + str(i)
                t = Worker(i, self.base_url, self.xor, self.msg)
                t.start()
                i += 1

        elif self.found_xor:
            self.xor += data.strip()
            self.found_xor = False

        if "----- BEGIN XOR KEY -----" in data:
            self.found_xor = True
        elif "----- BEGIN CRYPTED MESSAGE -----" in data:
            self.found_message = True

    def send(self, hash):
        r = requests.get(self.base_url + hash)
        with open('output.txt', 'w') as out:
            out.write(r.text)

parser = MyParser('http://prog.ctf.hf/decryptor/')

start = time.time()
r = requests.get(parser.base_url)

#reg = re.search('----- BEGIN CRYPTED MESSAGE -----\s+(.+)\s+----- BEGIN CRYPTED MESSAGE -----', r.text)
#print reg
parser.feed(r.text)

#print "XOR key: \n" + parser.xor
#print "msg: \n" + parser.msg
finish = time.time()


print "########### Parsing Finished in {}##################".format(finish-start)