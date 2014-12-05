import copy
from pandas import *
def desc(sumzdf,kt,et,r2t,q2t):
    """filters out descriptors of a sumtable.  filters out kurtosis higher than 2nd arg, etnropy less than 3rd arg, r2 lower than 4th arg, and q2 lower than 5th arg"""
    s=copy.deepcopy(sumzdf)
    s["kurtosis"]=s["kurtosis"].where(s["kurtosis"]<kt)
    s["entropy"]=s["entropy"].where(s["entropy"]>et)
    s["r2"]=s["r2"].where(s["r2"]>r2t)
    s["q2"]=s["q2"].where(s["q2"]>q2t)
    return s.dropna(subset=["kurtosis", "entropy", "r2", "q2"])
