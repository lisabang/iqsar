#if isinstance(rendered, unicode):
#    rendered = rendered.encode('UTF-8')

import xml.etree.ElementTree as ET
def xmltoinchi(xmlfile):
    if xmlfile.endswith(".xml"):
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        
        inchilist=[]
        for child in root:
            for ele in child:
                st= unicode(ele.text)
                st=st.encode('UTF-8')
                if st.startswith("InChI="):
                    inchilist.append(st)
        return inchilist
    #kocinchilist.append(child[5].text)
    else:
        raise TypeError("Input file must be of type XML!")
def xmltocas(xmlfile):
    if xmlfile.endswith(".xml"):
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        
        inchilist=[]
        for child in root:
            for ele in child:
                st= unicode(ele.text)
                #print ele.tag
                st=ele.tag
                if st.endswith("Cas"):
                    cas=ele.text
                    inchilist.append(cas)
        return inchilist
    #kocinchilist.append(child[5].text)
    else:
        raise TypeError("Input file must be of type XML!")
