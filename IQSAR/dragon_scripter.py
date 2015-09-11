import os
#import module_locator
import time
import xml.etree.ElementTree as ET
import dragonss

class MolFilePath:
    '''helper function to make a custom .drs file for dragon 6 or more recent.'''
    def __init__(self,molfol,datapath,scriptpath):
        #my_path=module_locator.module_path()
        #tree=ET.parse(dss)
        root = ET.fromstring(dragonss.samp())
        self.root=root
        #self.root=tree.getroot()
        self.molfol=molfol
        self.datapath=datapath
        self.scriptpath=scriptpath
    def defaultoptions(self):
        self.root.find("OPTIONS/SaveOnlyData").set("value","false")
        self.root.find("OPTIONS/SaveLabelsOnSeparateFile").set("value","false")
        self.root.find("OPTIONS/SaveFormatBlock").set("value","%b - %n.txt")
        self.root.find("OPTIONS/SaveFormatSubBlock").set("value","%b-%s - %n - %m.txt")
        self.root.find("OPTIONS/SaveExcludeMisVal").set("value","false")
        self.root.find("OPTIONS/SaveExcludeAllMisVal").set("value","true")
        self.root.find("OPTIONS/SaveExcludeConst").set("value","true")
        self.root.find("OPTIONS/SaveExcludeNearConst").set("value","true")
        self.root.find("OPTIONS/SaveExcludeStdDev").set("value","false")
        self.root.find("OPTIONS/SaveStdDevThreshold").set("value","0.0001")
        self.root.find("OPTIONS/SaveExcludeCorrelated").set("value","true")
        self.root.find("OPTIONS/SaveCorrThreshold").set("value",".99")
        self.root.find("OPTIONS/SaveExclusionOptionsToVariables").set("value","false")
        self.root.find("OPTIONS/SaveExcludeMisMolecules").set("value","false")
        self.root.find("OPTIONS/SaveExcludeRejectedMolecules").set("value","false")
    def _getmols(self,folderaddress, m_ext="hin"):
        files=[]
        for file in os.listdir(folderaddress):
            if file.endswith("."+str(m_ext)):
                files.append(folderaddress+file)
            
        return sorted(files)

    def entermolfolder(self,molext="hin"):
        thist=self.root.find("MOLFILES/molInput")
        #self.root.remove()
        listofmols=self._getmols(self.molfol, m_ext=molext)
        #print listofmols
        
        for mol in listofmols:
            #print mol
            ET.SubElement(thist,"molFile").set('value',mol)               
#        for mol in thist:
        
            
            #print mol
                #print molfile.attrib
        
    def enterblocks(self,listofblocks):
        for b in listofblocks:
            for blk in self.root.iter("block"):
            #print blk.attrib
                blk.set('SelectAll',"true")
            #print blk.attrib

 #   def enterweights(weightslist)
 #       for e in root.iter("weight"):
 #           print e.attrib
    def _puttodaysdate(self):
    
        for trait in self.root.iter("DRAGON"):
            #print trait.attrib
            trait.set("generation_date",time.strftime("%Y/%m/%d"))
        #print trait.attrib
                
    def changesavefilepath(self):
        if type(self.datapath)==str:
            for savefile in self.root.iter("SaveFilePath"):
                savefile.set("value",self.datapath)
        else:
            raise TypeError("Save path must be a string")
    def write_defaultdrs(self,ext):
        self.defaultoptions()
        self.entermolfolder(molext=ext)
        self.enterblocks(range(1,30))
        self._puttodaysdate()
        self.changesavefilepath()
        tree=ET.ElementTree(element=self.root)
        tree.write(self.scriptpath)
        
