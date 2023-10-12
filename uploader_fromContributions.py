#%%
import pandas as pd
import sys
import json
from pymatgen.core import Composition
from pymatgen.core.periodic_table import get_el_sp
import time
from datetime import datetime
from pymongo import MongoClient
from zoneinfo import ZoneInfo
import DataTools.compositionVector as cd2cv
import fire
from pprint import pprint

def upload(target:str = '',
           datasheet:str = '',
           purge:bool = False,
           purgeByField:bool = False,
           forceDataReplacement:bool = False,
           isDatabase:bool = False
           ):

    if target=='':
        raise Exception('You must specify a target collection to upload to.')

    if datasheet=='' and not purge and not purgeByField:
        raise Exception('You must specify a datasheet to upload or use a purge command.')

    print('Starting the upload process!\nLoading credentials...')

    cred = json.load(open('credentials.json'), strict=False)
    if cred['name']=='test':
        raise Exception('You are using test credentials. Aborting!')

    print('Loaded credentials for: '+cred['name'])

    # Connect to the MongoDB using the credentails
    client_string = f"mongodb+srv://{cred['name']}:{cred['dbKey']}@testcluster.g3kud.mongodb.net/ULTREA_materials?retryWrites=true&w=majority"
    database_name = 'ULTREA_materials'

    client = MongoClient(client_string)
    collection = client[database_name][target]
    print('Connected to the database.')
    print(f'Working under {database_name} -> {target}')

    if purge==True:
        print('Warning. All data from your collection will be removed in 5s.\nPress Ctrl+C to abort.')
        time.sleep(5)
        collection.delete_many({})
        print('Collection purged.')
        return

    if purgeByField==True:
        print('You are attempting to remove all datapoints in your database that match certain field or its value.\nUse "." to specify subfields. E.g., meta.comment or material.system\nLeave the field value empty to match any datapoint for which the field exists.')
        field = input('Field Name:')
        value = input('Field Value:')
        if value=='':
            value = {"$exists" : "true"}
        print('Warning. Specified data will be removed in 3s.\nPress Ctrl+C to abort.')
        time.sleep(3)
        collection.delete_many({field : value})
        print('Specified data removed.')
        return

    if forceDataReplacement==True:
        print('You are attempting to force replacement of all data uploaded from template (or templates) with this name:')
        print(f'Warning. All of old data from\n{datasheet}\nwill be removed in 5s and new upload will proceed.\nPress Ctrl+C to abort.')
        time.sleep(5)
        collection.delete_many({'meta.dataSheetName': datasheet})
        print(f'OLD data from {datasheet} has been removed. Proceeding to NEW.')

    #Import metadata
    print('Reading the metadata.')
    metaDF = pd.read_excel(datasheet, usecols="A:F", nrows=4)
    meta = metaDF.to_json(orient="split")
    metaParsed = json.loads(meta, strict=False)['data']

    # get timestamp
    dateString = datetime.now().strftime('%Y-%d-%b-%H-%M')

    # Format metadata into a dictionary
    metaData = {
        'source': 'LIT',
        'name': metaParsed[0][1],
        'email': metaParsed[1][1],
        'directFetch': metaParsed[2][1],
        'handFetch': metaParsed[3][1],
        'comment': metaParsed[0][5],
        'timeStamp': datetime.now(ZoneInfo('America/New_York')),
        'dataSheetName': datasheet
    }

    if isDatabase:
        metaData.update({'parentDatabase': target})
        metaData.update({'handFetch': False})

    print('Data credited to: '+metaParsed[0][1])
    print('Contact email: '+metaParsed[1][1])
    pprint(metaData)

    # Logging progress into a CSV table
    dataFileName = datasheet.replace('.xls', '').replace('.xlsx', '')
    logger = open(dataFileName+'_REPORT_'+dateString+'.csv', "w")
    logger.write('Composition, Result\n')

    # Import data
    print('\nImporting data.')
    df2 = pd.read_excel(datasheet, usecols="A:N", nrows=5000, skiprows=8)
    result = df2.to_json(orient="records")
    parsed = json.loads(result, strict=False)
    print('Imported '+str(parsed.__len__())+' datapoints.\n')

    # Convert metadata and data into database datapoints and upload
    for datapoint in parsed:
        comp = datapoint['Composition'].replace(' ','')
        print('Processing: '+comp)
        try:
            uploadEntry = datapoint2entry(metaData, datapoint)
            collection.insert_one(uploadEntry)
            logger.write(comp+',Success!\n')
            print('Succesfully uploaded the datapoint!\n')
        except ValueError as e:
            exceptionMessage = str(e)
            print(exceptionMessage)
            logger.write(comp + ',Fail!,<-------,'+exceptionMessage+'\n')
            print('Upload failed!\n')
            pass
    logger.close()


#%% Modify composition string from the template into a unified
# representation of (1) IUPAC standardized formula, (2) pymatgen dictionary
# composition object, (3) anonymized formula, (4) reduced formula, (5) chemical system,
# and (6) number of components

def percentileFormula(cd: dict):
    order = sorted(cd.keys(), key=lambda s: get_el_sp(s).iupac_ordering)
    return ' '.join([f'{el}{round(100*cd[el], 1):g}' for el in order])

def relationalFormula(cd: dict):
    order = sorted(cd.keys(), key=lambda s: get_el_sp(s).iupac_ordering)
    lowest = min([v for v in cd.values() if v>0.005])
    return ' '.join([f'{el}{round(cd[el]/lowest, 2):g}' for el in order])

def compStr2compList(s: str):
    try:
        compObj = Composition(s).reduced_composition
        if not compObj.valid:
            print("Composition invalid")
        return [compObj.iupac_formula,
                dict(compObj.fractional_composition.as_dict()),
                percentileFormula(dict(compObj.fractional_composition.as_dict())),
                relationalFormula(dict(compObj.fractional_composition.as_dict())),
                compObj.anonymized_formula,
                compObj.reduced_formula,
                compObj.chemical_system,
                compObj.chemical_system.split('-'),
                compObj.__len__()]
    except Exception as e:
        print(e)
        raise ValueError("Warning! Can't parse composition!: "+s)
        #return ['', [], '', '', '', 0]

#%% Unifies phase names in the database
# If composition -> keep as is
# if all uppercase (e.g. BCC, FCC) -> keep as is
# otherwise -> make all lowercase

def phaseNameUnifier(s):
    exceptionToUpper = ['b0', 'b1', 'b2', 'a0', 'a1', 'a2']
    replaceDict = {'bulkmetallic\nglass' : 'amorphous', 'bcc' : 'BCC', 'fcc' : 'FCC', 'LAVES' : 'laves'}

    try:
        isComp = Composition(s).valid
    except Exception as e:
        isComp = False

    if s in exceptionToUpper:
        return s.upper()
    elif s in replaceDict:
        return replaceDict[s]
    elif isComp:
        return s
    elif s.isupper():
        return s
    else:
        return s.lower()

#%% Transforms the structure string into a list of
# individual phases, interpreting (1) multiple phases
# of the same type, (2) composition-defined phases, and
# (3) named phases. Processes them in a unified way.

def structStr2list(s: str):
    ls = []

    s = s.replace(' ','')
    tempLs = list(s.split('+'))
    for phase in tempLs:
        if phase[0].isdigit():
            for i in range(int(phase[0])):
                ls.append(phaseNameUnifier(phase[1:]))
        else:
            ls.append(phaseNameUnifier(phase))
    ls.sort()
    if ls.__len__()>0:
        return [ls, ls.__len__()]
    else:
        return []

#%% Process name unifier

def processNameUnifier(s: str):
    exceptions = []

    if s in exceptions:
        return s
    elif s.isupper():
        return s
    else:
        return s.lower()

#%% Processes processing string into a unified-form process list

def processStr2list(s):
    ls = []
    s = s.replace(' ','')
    tempLs = list(s.split('+'))
    for process in tempLs:
        if process[0].isdigit():
            for i in range(int(process[0])):
                ls.append(processNameUnifier(process[1:]))
        else:
            ls.append(processNameUnifier(process))
    if ls.__len__()>0:
        return [ls, ls.__len__()]
    else:
        return []


#%% Convert a pair of metadata and data into ULTERA Database datapoint
def datapoint2entry(metaD, dataP, printOuts=True):
    # metadata
    entry = {'meta' : metaD, 'material' : {}, 'property' : {}, 'reference' : {}}

    # composition
    try:
        compList = compStr2compList(dataP['Composition'])
    except Exception as e:
        print(str(e))
        raise ValueError("Could not parse the composition! Required for upload. Aborting upload!")

    entry['material'].update({
            'rawFormula': dataP['Composition'],
            'formula': compList[0],
            'compositionDictionary' : compList[1],
            'percentileFormula': compList[2],
            'relationalFormula': compList[3],
            'compositionVector': cd2cv.compDict2Vec(compList[1]),
            'anonymizedFormula' : compList[4],
            'reducedFormula' : compList[5],
            'system' : compList[6],
            'elements' : compList[7],
            'nComponents' : compList[8]})

    # structure
    if 'Structure' in dataP:
        if dataP['Structure'] is not None:
            structList = structStr2list(dataP['Structure'])
            entry['material'].update({
                'structure': structList[0],
                'nPhases': structList[1]})
        else:
            if printOuts:
                print('No structure data!')

    # processing
    if 'Processing' in dataP:
        if dataP['Processing'] is not None:
            processingList = processStr2list(dataP['Processing'])
            entry['material'].update({
                    'processes' : processingList[0],
                    'nProcessSteps' : processingList[1]})
        else:
            if printOuts:
                print('No process data!')

    # comment
    if 'Material Comment' in dataP:
        if dataP['Material Comment'] is not None:
            entry['material'].update({
                    'comment' : dataP['Material Comment']})

    if 'Temperature [K]' in dataP:
        # If there is temperature reported, regardless of property report, note the temperature of material
        if dataP['Temperature [K]'] is not None:
            entry['material'].update({
                'observationTemperature': float(dataP['Temperature [K]'])})

    if 'Name' in dataP:
        # Requires: Name and Value
        if dataP['Name'] is not None:
            entry['property'].update({
                'name' : dataP['Name'],
                'value': float(dataP['Value [SI]'])})

            # If property has a name, go through all of property parameters and value
            if 'Source' in dataP:
                if dataP['Source'] is not None:
                    entry['property'].update({
                        'source': dataP['Source']})
            if 'Property Parameters' in dataP:
                if dataP['Property Parameters'] is not None:
                    entry['property'].update({
                        'parameters': dataP['Property Parameters']})
            if 'Temperature [K]' in dataP:
                if dataP['Temperature [K]'] is not None:
                    entry['property'].update({
                        'temperature': float(dataP['Temperature [K]'])})
            if 'Unit [SI]' in dataP:
                if dataP['Unit [SI]'] is not None:
                    entry['property'].update({
                        'unitName': dataP['Unit [SI]']})
        else:
            del entry['property']
            if printOuts:
                print('No property data or error occurred!')

    if 'DOI' in dataP:
        # Requires DOI
        if 'DOI' in dataP:
            if dataP['DOI'] is not None:
                entry['reference'].update({
                        'doi' : dataP['DOI']})
                if 'Pointer' in dataP:
                    if dataP['Pointer'] is not None:
                        entry['reference'].update({
                            'pointer': dataP['Pointer']})
            else:
                del entry['reference']
                if printOuts:
                    print('No reference data!')

    return entry


if __name__ == "__main__":
    fire.Fire(upload)
