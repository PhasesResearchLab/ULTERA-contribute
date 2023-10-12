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
from typing import List

print('Running!')

# Process name unifier

def processNameUnifier(s: str):
    exceptions = []

    if s in exceptions:
        return s
    elif s.isupper():
        return s
    else:
        return s.lower()
    
# Processes processing string into a unified-form process list

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
    
# Unifies phase names in the database
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
    
# Transforms the structure string into a list of
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
    
# Modify composition string from the template into a unified
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

# Convert data into ULTERA Database datapoint
def datapoint2entry(dataP, printOuts=True):
    entry = {'error': {'bool': False, 'errMessage': ''}, 
             'material' : {}, 
             'property' : {}, 
             'reference' : {}}

    # composition
    try:
        compList = compStr2compList(dataP['Composition'])
    except Exception as e:
        print(str(e))
        raise ValueError("Could not parse the composition! Required for upload. Aborting upload!")
    
    # material
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

# Convert a pair of metadata and data into ULTERA Database datapoint
def datapoint2entryFail(dataP, printOuts=True):
    entry = {'error': {}, 'material' : {}, 'property' : {}, 'reference' : {}}

    entry['error'].update({'bool': True, 'errMessage': 'Could not parse the composition!'})

    entry['material'].update({'rawFormula': dataP['Composition']})

    if 'Name' in dataP:
        if dataP['Name'] is not None:
            entry['property'].update({
                'name' : dataP['Name'],
                'value': float(dataP['Value [SI]'])})
    else:
            entry['property'].update({
                'name' : '',
                'value': ''})
    
    return entry
            

# function to generate 2d array of [[raw formula],[percentile formula],[property name],[property value]]
# for the materials in dataset

def arrayGenerator(parsedData):
    prop_values = []
    prop_names = []
    raw_formulas = []
    percentile_formulas = []
    err_messages = []
    validations = []
    dataset = []
    markers = []

    for datapoint in parsedData:
        try:
            dataset.append(datapoint2entry(datapoint))
        except Exception as e:
            print(str(e))
            dataset.append(datapoint2entryFail(datapoint))
            print("Could not parse the composition! Required for upload. Aborting upload!")

    def adjustLen(strArray: List[str]) -> List[str]:
        max_str_length = max([len(f) for f in strArray])
        formulas = [f'{formula:=<{max_str_length}}' for formula in strArray]
        # adjFormulas = [formula.replace('=', '&nbsp;') for formula in formulas]
        # return adjFormulas
        return formulas

    for data in dataset:
        if data['error']['bool'] is True:
            raw_formulas.append(data['material']['rawFormula'])
            percentile_formulas.append('')
            prop_names.append('')
            prop_values.append('')
            err_messages.append(data['error']['errMessage'])
        else:
            err_messages.append('')
            if 'material' in data:
                raw_formulas.append(data['material']['rawFormula'])
                percentile_formulas.append(data['material']['percentileFormula'])
            else:
                raw_formulas.append('')
                percentile_formulas.append('')

            if 'property' in data:
                prop_names.append(data['property']['name'])
                prop_values.append(data['property']['value'])
            else:
                prop_names.append('')
                prop_values.append(0)
    
    raw_formulas = adjustLen(raw_formulas)
    percentile_formulas = adjustLen(percentile_formulas)

    property_condition = 'UTS'
    value_condition = 6e8

    for prop, value, err_message in zip(prop_names, prop_values, err_messages):
        if err_message:
            validations.append(err_message)
            markers.append('🔴')
        else:
            if prop == '' and value == 0:
                validations.append('No property data!')
                markers.append('🟠')
            elif value >= value_condition and prop == property_condition:
                validations.append(f"High {property_condition} value is {value}")
                markers.append('🟠')
            else:
                validations.append('')
                markers.append('🟢')

    return [
        f'- {marker}  {raw_formula} | {percentile_formula} | {prop_name} | {validation} \n'
        for marker, raw_formula, percentile_formula, prop_name, validation 
        in zip(markers, raw_formulas, percentile_formulas, prop_names, validations)
    ]

if __name__ == '__main__':
    datasheet = 'template_v4_DatasetExample.xlsx'
    isDatabase = False

    # get timestamp
    dateString = datetime.now().strftime('%Y-%d-%b-%H-%M')

    ### Logging progress into Markdown file
    MdLogger = open('PyQAlloyReport'+dateString+'.md', "w")
    MdLogger.write('\n# PyQAlloyReport '+dateString+'\n\n')
    MdLogger.write('**Legend:** \n\n🟢 Successful Upload / 🟠 Abnormal Upload / 🔴 Failed Upload\n\n')
    MdLogger.write('## Raw Formula  |  Percentile Formula  |  Property  |  Comment \n')

    # Import data
    print('\nImporting data.')
    df2 = pd.read_excel(datasheet, usecols="A:N", nrows=5000, skiprows=8)
    result = df2.to_json(orient="records")
    parsed = json.loads(result, strict=False)
    print('Imported '+str(parsed.__len__())+' datapoints.\n')

    ## Convert data into database datapoints and upload
    results = arrayGenerator(parsed)
    for result in results:
        MdLogger.write(result)

