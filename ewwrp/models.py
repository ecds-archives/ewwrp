from eulexistdb.manager import Manager
from eulexistdb.models import XmlModel
from eulxml.xmlmap.teimap import Tei, TeiDiv, TEI_NAMESPACE
from eulxml import xmlmap

class Pages(XmlModel, Tei, TeiDiv):
    ''' Specify a page in the document '''
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    pages = Manager('//tei:div')

class Docs(XmlModel, Tei):
    ''' Attributes of the entire document '''
    ROOT_NAMESPACES = {'tei': TEI_NAMESPACE}
    objects = Manager("//tei:TEI")
    id = xmlmap.StringField('@xml:id')
    divs = xmlmap.NodeListField('//tei:div', TeiDiv)
    
    # These are important attributes of each document
    author = xmlmap.StringField('(//tei:author/tei:name/tei:choice/tei:reg | //tei:titleStmt/tei:author/@n)[1]')
    collection = xmlmap.StringField("tei:teiHeader/tei:profileDesc/tei:creation/tei:rs[@type='collection']")
    language = xmlmap.StringField("tei:teiHeader/tei:profileDesc/tei:creation/tei:rs[@type='language']")
    ethnicity = xmlmap.StringField("tei:teiHeader/tei:profileDesc/tei:creation/tei:rs[@type='ethnicity']")
    form = xmlmap.StringField("tei:teiHeader/tei:profileDesc/tei:creation/tei:rs[@type='form']")
    genre = xmlmap.StringField("tei:teiHeader/tei:profileDesc/tei:creation/tei:rs[@type='genre']")
    geography = xmlmap.StringField("tei:teiHeader/tei:profileDesc/tei:creation/tei:rs[@type='geography']")
    date = xmlmap.StringField("tei:teiHeader/tei:profileDesc/tei:creation/tei:date")
    
    # Backwords compatibility with tei:list/tei:item
    keywords = xmlmap.StringListField("tei:teiHeader/tei:profileDesc/tei:textClass/tei:keywords/tei:list/tei:item | tei:teiHeader/tei:profileDesc/tei:textClass/tei:keywords/tei:term")