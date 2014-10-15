from eulexistdb.manager import Manager
from eulexistdb.models import XmlModel
from eulxml.xmlmap.teimap import Tei, TeiDiv, TEI_NAMESPACE
from eulxml import xmlmap

class Pages(XmlModel, TeiDiv):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    pages = Manager('//tei:div')
    doc_id = xmlmap.StringField('tei:TEI/@xml:id')

class Documents(XmlModel, Tei):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    docs = Manager('//tei:TEI')
    ids = xmlmap.StringListField('//tei:div/@xml:id')
    author = xmlmap.StringField('(//tei:author/tei:name/tei:choice/tei:reg | //tei:titleStmt/tei:author/@n)[1]')
    collection = xmlmap.StringField("tei:teiHeader/tei:profileDesc/tei:creation/tei:rs[@type='collection']")