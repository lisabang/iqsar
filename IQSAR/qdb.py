import os
import pandas as pd
import xml.etree.ElementTree as ET
'''Contains a qdbrep class.  Declare using IQSAR.qdb.qdbrep(/absolute/path/to/unzipped/qsar-db/folder/) and perform getdescs, getyvals, getinchis, getcas functions on that object.'''
class qdbrep(object):
    
    def __init__(self, dir):
        self.dir=dir
    def _getsub(self):
        return [name for name in os.listdir(self.dir)
            if os.path.isdir(os.path.join(self.dir, name))]
    def getdescs(self):
        if "descriptors" in self._getsub():
            descfolder=self.dir+"descriptors/"
            for root, dirs, files in os.walk(descfolder):
                if not dirs:
                    pass
                else:
                    dfs=[]
                    for directorynum in range(len(dirs)):
                        dfs.append(pd.read_table(descfolder+str(dirs[directorynum])+"/values", index_col=0))
                    return pd.concat(dfs, axis=1)
        
        else:
            raise IOError("No descriptors folder present in this particular QSAR-DB!")

    def getyvals(self):
        if "properties" in self._getsub():
            propfolder=self.dir+"properties/"
            for root, dirs, files in os.walk(propfolder):
                if not dirs:
                    pass
                else:
                    return pd.read_table(propfolder+str(dirs[0])+"/values", index_col=0)
                
        else:
            raise IOError("No properties folder present in this particular QSAR-DB!")
    def getinchis(self):
        if "compounds" in self._getsub():
            xmlfile=self.dir+"compounds/compounds.xml"
            
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
    def getcas(xmlfile):
        
        if "compounds" in self._getsub():
            xmlfile=self.dir+"compounds/compounds.xml"
            
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
        
            
