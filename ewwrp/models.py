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
    author = xmlmap.StringField('(//tei:author/tei:name/tei:choice/tei:reg | //tei:titleStmt/tei:author/@n)[1]')
    collection = xmlmap.StringField("tei:teiHeader/tei:profileDesc/tei:creation/tei:rs[@type='collection']")
    
class Essays(XmlModel, Tei):
    ROOT_NAMESPACES = {'tei': TEI_NAMESPACE}
    objects = Manager("//tei:div[@type='critical essay']")
    collection = xmlmap.StringField("//tei:rs[@type='collection']")