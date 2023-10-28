# separate script to validate property data

from pprint import pprint
from pathlib import Path
from ruamel.yaml import YAML
from typing import List

path = Path('/workspaces/ULTERA-contribute/DataTools/propertyValidations.yaml')
yaml = YAML(typ='safe')
propValidations = yaml.load(path)

def propValidator(parsedDataset):
    prop_values = []
    prop_names = []
    raw_formulas = []
    percentile_formulas = []
    err_messages = []
    validations = []
    markers = []

    def adjustLen(strArray: List[str]) -> List[str]:
        max_str_length = max([len(f) for f in strArray])
        return [f'{formula:=<{max_str_length}}'.replace('=',' ') for formula in strArray]
        # return formulas

    for data in parsedDataset:
        err_messages.append(data['error'])
        raw_formulas.append(data['material']['rawFormula'])
        percentile_formulas.append(data['material']['percentileFormula'])

        if data['error'] or 'property' not in data:
            prop_names.append('')
            prop_values.append('')
        else:
            prop_names.append(data['property']['name'])
            prop_values.append(data['property']['value'])

    pprint(prop_names)

    raw_formulas = adjustLen(raw_formulas)
    percentile_formulas = adjustLen(percentile_formulas)

    conditionList = propValidations['propertyConditions']
    nameList = []
    abbrevList = []
    maxErrorList = []
    minErrorList = []
    maxWarningList = []
    minWarningList = []
    for propDict in conditionList:
        nameList.append(propDict['name'])
        abbrevList.append(propDict['abbrevs'])
        maxErrorList.append(propDict['maxError'])
        minErrorList.append(propDict['minError'])
        maxWarningList.append(propDict['maxWarning'])
        minWarningList.append(propDict['minWarning'])

    pprint(nameList)
    pprint(abbrevList)

    propValidationList = [nameList, abbrevList, maxErrorList, minErrorList,
                            maxWarningList, minWarningList]

    for prop, value, err_message in zip(prop_names, prop_values, err_messages):
        if err_message:
            validations.append(err_message)
            markers.append('🔴')
        elif prop == '' or value == '':
            validations.append('No property data!')
            markers.append('🟠')
        else:
            for name in nameList:
                nameIndex = nameList.index(name)
                if (prop == name):
                    propIndex = nameIndex
                    break
                elif (abbrevList[nameIndex] is not None):
                    if ((prop == abbrevList[nameIndex][0]) or (prop == abbrevList[nameIndex][1])):
                        propIndex = nameIndex
                        break
                else:
                    propIndex = None
                    
            if propIndex is not None:
                boundList = []
                for field in propValidationList:
                    fieldIndex = propValidationList.index(field)
                    # skip over name and abbrevs fields
                    if fieldIndex < 1:
                        continue
                    else:
                        boundList.append(propValidationList[fieldIndex][propIndex])
                        print(boundList)
        
                # maxError check
                if (boundList[2] is not None and value > boundList[2]):
                    validations.append(f"Unreasonably high {prop} value of {value}")
                    markers.append('🔴')
                # minError check
                elif (boundList[3] is not None and value < boundList[3]):
                    validations.append(f"Unreasonably low {prop} value of {value}")
                    markers.append('🔴')
                # maxWarning check
                elif (boundList[4] is not None and value > boundList[4]):
                    validations.append(f"High {prop} value of {value}")
                    markers.append('🟠')
                # minWarningCheck
                elif (boundList[5] is not None and value < boundList[5]):
                    validations.append(f"Low {prop} value of {value}")
                    markers.append('🟠')
                else:
                    validations.append('')
                    markers.append('🟢')

            else:
                validations.append('Uncommon property!')
                # use green or orange ?
                markers.append('🟠')

    return [
        f'| {marker} | {raw_formula} | {percentile_formula} | {prop_name} | {validation} |\n'
        for marker, raw_formula, percentile_formula, prop_name, validation
        in zip(markers, raw_formulas, percentile_formulas, prop_names, validations)
    ]

