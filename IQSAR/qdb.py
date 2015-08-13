import os
import pandas as pd
import xml.etree.ElementTree as ET
import urllib
import copy
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
    def getcompounds(self):
        if "compounds" in self._getsub():
            xmlfile=self.dir+"compounds/compounds.xml"
            
            if xmlfile.endswith(".xml"):
                tree = ET.parse(xmlfile)
                root = tree.getroot()
                childs=[]
                for child in root:
                    tindex=[ele.tag for ele in child]
                    for n,i in enumerate(tindex):
                        junk,notjunk=i.split("}")
                        tindex[n]=notjunk
                    childinfo=pd.Series([ele.text for ele in child], index=tindex)#, index=pdin)
                    childs.append(childinfo)
                mas=pd.concat(childs, axis=1)
                mas2=mas.T
                return mas2.set_index(keys="Id", drop=True)

            else:
                raise TypeError("Input file must be of type XML!")
    def getmol(self,folderpath):
        '''This command automatically downloads .mol files from the NIST websites to folderpath (must be written as string, i.e. /absolute/path/to/folder/).  for this to work, the original QSAR-DB must have  inchi files. this relies on the getinchi() method of this class.  This may not work if the inchi is ambiguous and there is more than one NIST mol entry.  Check the folder and the print output to check.'''
        nisturl="http://webbook.nist.gov/cgi/cbook.cgi?InChIFile="
        inchiseries=self.getcompounds()["InChI"]
        import math

        if type(folderpath)==str:
            for i in inchiseries.index:
                if type(inchiseries[i])==float:
                    print str(i)+".mol not downloaded"
                else:
                    urllib.urlretrieve(nisturl+inchiseries[i], folderpath+str(i)+".mol")
                
          #  for inchi in inchilist:
          #      #print nisturl+inchi
          #      urllib.urlretrieve(nisturl+inchi, folderpath+str(inchilist.index(inchi))+".mol")
          #      print "saved "+str(folderpath)+"1~"+str(inchilist.index(inchi))+".mol"
        else:
            raise TypeError("Type of folderpath must be a string!")
