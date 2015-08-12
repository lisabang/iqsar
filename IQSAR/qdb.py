import os
import pandas as pd
import xml.etree.ElementTree as ET
import urllib

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
    def getcas(self,xmlfile):
        
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


    def getmol(self,folderpath):
        '''This command automatically downloads .mol files from the NIST websites to folderpath (must be written as string, i.e. /absolute/path/to/folder/).  for this to work, the original QSAR-DB must have  inchi files. this relies on the getinchi() method of this class.  This may not work if the inchi is ambiguous and there is more than one NIST mol entry.  Check the folder and the print output to check.'''
        nisturl="http://webbook.nist.gov/cgi/cbook.cgi?InChIFile="
        inchilist=self.getinchis()
        if type(folderpath)==str:

            for inchi in inchilist:
                #print nisturl+inchi
                urllib.urlretrieve(nisturl+inchi, folderpath+str(inchilist.index(inchi))+".mol")
                if inchilist.index(inchi)==len(inchilist):
                    print "saved "+str(folderpath)+"1~"+str(inchilist.index(inchi))+".mol"
        else:
            raise TypeError("Type of folderpath must be a string!")
