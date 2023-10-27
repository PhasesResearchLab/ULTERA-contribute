# separate script to validate property data

# import yaml
# with open('propertyBounds.yaml') as pb:
#     propConditions = yaml.safe_load(pb)

from pprint import pprint
from pathlib import Path
from ruamel.yaml import YAML
from typing import List

path = Path('/workspaces/ULTERA-contribute/DataTools/propertyValidations.yaml')
yaml = YAML(typ='safe')
propValidations = yaml.load(path)
# pprint(propValidations)

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
    # pprint(parsedDataset)

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

    # pprint(nameList)
    # pprint(abbrevList)

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
            for nameIndex in range(len(nameList)):
                # pprint(nameList[nameIndex])
                if (prop == nameList[nameIndex]):
                    propIndex = nameIndex
                elif abbrevList[nameIndex] is not None:
                    if (prop == abbrevList[nameIndex][0]
                    or prop == abbrevList[nameIndex][1]):
                        propIndex = nameIndex
                else:
                    propIndex = None
                    # validations.append('Uncommon property!')
                    #  # use green or orange ?
                    # markers.append('🟠')
            
            # pprint(propIndex)
                    
            if propIndex is not None:
                boundList = []
                for fieldIndex in range(len(propValidationList)):
                    # skip over name and abbrevs fields
                    if fieldIndex < 1:
                        continue
                    else:
                        boundList.append(propValidationList[fieldIndex][propIndex])
                        # pprint(boundList)
        
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





            # for propDict in conditionList:
            #     # test = f"Testing: {propDict} "
            #     # print(test)
            #     if propDict['abbrevs'] is None:
            #         abbrevList = [' ', ' ']
            #     else:
            #         abbrevList = propDict['abbrevs']
                
                # print(abbrevList)
                # print(abbrevList[0])
                # print(abbrevList[1])

                # if prop == abbrevList[0] or prop == abbrevList[1] or prop == propDict['name']:
                #     if propDict['maxError'] is not None and value > propDict['maxError']:
                #         validations.append(f"Unreasonably high {prop} value of {value}")
                #         markers.append('🔴')
                #     elif propDict['minError'] is not None and value < propDict['minError']:
                #         validations.append(f"Unreasonably low {prop} value of {value}")
                #         markers.append('🔴')
                #     elif propDict['maxWarning'] is not None and value > propDict['maxWarning']: 
                #         validations.append(f"High {prop} value of {value}")
                #         markers.append('🟠')
                #     elif propDict['minWarning'] is not None and value < propDict['minWarning']:
                #         validations.append(f"Low {prop} value of {value}")
                #         markers.append('🟠')
                #     else:
                #         validations.append('')
                #         markers.append('🟢')
                # else:
                #     validations.append('Uncommon property!')
                #     # use green or orange ?
                #     markers.append('🟠')

    return [
        f'| {marker} | {raw_formula} | {percentile_formula} | {prop_name} | {validation} |\n'
        for marker, raw_formula, percentile_formula, prop_name, validation
        in zip(markers, raw_formulas, percentile_formulas, prop_names, validations)
    ]



    # create yaml file for properties, abbrevs, and upper lower bounds
    # ^ similar to adam example sent in email
    # ^ error different from warning
    # ^ ex: can't have compressive ducility > 100%, so error
    #       compressive ductility warning would be around > 85%
    # ^^^ so need to consider physical limitations like this for each property
    # create at least 3-4 property distributions in mongodb
    # ^ use these for bounds in yaml file
    # if no abbrev or bound, use null or none in place



                # if propDict['maxError'] is not None and value > propDict['maxError']:
                #     validations.append(f"Unreasonably high {prop} value of {value}")
                #     markers.append('🔴')
                # elif propDict['minError'] is not None and value < propDict['minError']:
                #     validations.append(f"Unreasonably low {prop} value of {value}")
                #     markers.append('🔴')
                # elif propDict['maxWarning'] is not None and value > propDict['maxWarning']: 
                #     validations.append(f"High {prop} value of {value}")
                #     markers.append('🟠')
                # elif propDict['minWarning'] is not None and value < propDict['minWarning']:
                #     validations.append(f"Low {prop} value of {value}")
                #     markers.append('🟠')
                # else:
                #     validations.append('')
                #     markers.append('🟢')