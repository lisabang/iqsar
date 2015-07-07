import os
import pandas as pd
class qdbrep(object):
    
    def __init__(self, dir):
        self.dir=dir
    def _getsub(self):
        return [name for name in os.listdir(self.dir)
            if os.path.isdir(os.path.join(self.dir, name))]
    def get_descriptors(self):
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

    def get_yvals(self):
        if "properties" in self._getsub():
            propfolder=self.dir+"properties/"
            for root, dirs, files in os.walk(propfolder):
                if not dirs:
                    pass
                else:
                    return pd.read_table(propfolder+str(dirs[0])+"/values", index_col=0)
                
        else:
            raise IOError("No properties folder present in this particular QSAR-DB!")
            
