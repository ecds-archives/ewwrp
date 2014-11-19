from eulexistdb import db
from localsettings import *

from xml.etree import ElementTree as ET

import nltk
import os

'''
    This is a quick project to get some interesting data about these
    documents and try out the nltk package.
'''

class TestExist:
    def __init__(self):
        # Configure DJANGO_SETTINGS_MODULE for ExistDB
        os.environ['DJANGO_SETTINGS_MODULE'] = 'localsettings.py'
        self.db = db.ExistDB(server_url=EXISTDB_SERVER_URL)
        
    def get_data(self, query):
        result = list()
        qresult = self.db.executeQuery(query)
        hits = self.db.getHits(qresult)
        for i in range(hits):
            result.append(str(self.db.retrieve(qresult,i)))
        return result
    
def main():
    # Get the text of the document
    """
    xquery = '''declare namespace tei='http://www.tei-c.org/ns/1.0';
        let $x := xmldb:xcollection("/db/ewwrp/")
        return $x/tei:TEI/tei:text'''
    xquery = '''declare namespace tei='http://www.tei-c.org/ns/1.0';
        let $x := doc('/db/ewwrp/Arrow.xml')
        return $x/tei:TEI/tei:text'''
    a = TestExist()
    res = a.get_data(xquery)
    data = []
    f = open('test.xml','w')
    f.write(res[0])
    f.close()
    for r in res:
        data.append(analyze(r))
    """
    
    data = []
    
    # Trying it out with a local file first
    f = open('test.xml','r')
    txt = f.read()
    f.close()
    
    data = data + [analyze(txt)[:10]]
    print data
    
def analyze(data):
    root = ET.fromstring(data)
    
    # Read in text
    text = ''
    for i in root.itertext():
        text = text + i.strip() + ' '
    
    # Actual text analysis
    tokens = nltk.word_tokenize(text)
    pt = nltk.pos_tag(tokens)
    pt = [word for (word, tag) in pt if tag == 'NOUN']
    return pt
    
if __name__ == "__main__":
    main()