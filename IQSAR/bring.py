def data(n):
    """another way to import files into pandas without specifying .txt or .csv.  IQSAR.bring.data(DIRECT_PATH_TO_YOUR_DIRECTORY_HERE)"""
    import pandas as pd

    if n.endswith(".csv"):
       importedfile=pd.read_csv(n, index_col=0)
       print("csv file imported")
    elif n.endswith(".txt"):
       importedfile=pd.read_table(n, index_col=0)
       print("text file imported")
    else:
       importedfile="None"
       print("File extension is not csv or txt!")
    
    return importedfile
