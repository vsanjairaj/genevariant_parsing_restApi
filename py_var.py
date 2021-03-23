import requests 
import json
import pandas as pd
from pprint import pprint
import sys


def merge_url(var):
    url = 'http://rest.ensembl.org/vep/human/hgvs/'
    new_url = url + var
    return new_url

def req_new_url(new_url):
    object1 = requests.get(new_url,headers={ "Content-Type" : "application/json"})
    if not object1.ok:
        #object1.raise_for_status() 
        return -2
    try: 
        object2 = object1.json()
    except json.JSONDecodeError:
        return -1
    return object2

def txt_to_list(filepath):
    with open(filepath) as f:
        variants = []
        for line in f:
            stripped_line = line.strip()
            variants.append(stripped_line)
    return variants 
        
def get_tsv(file_name):
    list_of_variants = txt_to_list(file_name)
    error_api = [] #To store variants which return error #Print the error API variants at the end
    rows = []
    #df = pd.DataFrame() #New DataFrame
    for var in list_of_variants:  #Loop running through individual variants
        url = merge_url(var) #Creates API url for each variants
        obj = req_new_url(url)  #Object which stores JSON object for individual Campaign IDs
        if type(obj) == int :
            pass
            error_api.append(var)           
        else :
            for key in obj:
                temp = []
                temp_conseq = []
                temp.append(var)
                temp.append(key['assembly_name'])
                temp.append(key['seq_region_name'])
                temp.append(key['start'])
                temp.append(key['end'])
                temp.append(key['most_severe_consequence'])
                temp.append(key['strand'])
                for key_2 in key['transcript_consequences']:                    
                    temp_conseq.append(key_2['gene_symbol'])
                temp_conseq_set = set(temp_conseq)
                temp_conseq = list(temp_conseq_set)
                temp.append(temp_conseq)
                rows.append(temp)
    df = pd.DataFrame(rows,columns=['input_variant','assembly_name','seq_region_name','start','end','most_severe_consequence','strand','transcript_consequences'])
    print(df)        
    
    
if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")
    get_tsv(sys.argv[1])
    