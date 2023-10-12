import re

# Return a float or a float based on int or string
def propertyValueUnify(val):
    if isinstance(val, float):
        return val
    elif isinstance(val, int):
        return float(val)
    elif isinstance(val, str):
        try:
            return float(val)
        except:
            if bool(re.search("\d+-\d+", val)):
                return float(eval(val.replace('-','+')))/2
            else:
                print('Could not parse: '+val)
                return None


propertyExceptionToUpper = []

# The values below are incorporated into the aggregation framework already
propertyExceptionPairs = {'creeprate': 'creep rate',
                          'CreepRate': 'creep rate',
                          'CreepRate - feature1': 'creep rate feature 1',
                          'CreepRate - feature2': 'creep rate feature 2',
                          'Hardness': 'hardness',
                          'hardness ': 'hardness',
                          'Hardness ': 'hardness',
                          'B/G ratio': 'B/G ratio',
                          'B/G': 'B/G ratio',
                          'd parameter(surface e/unstable stacking fault e )': 'd parameter',
                          'young modulus': 'youngs modulus',
                          'Tm': 'melting temperature',
                          'UTS': 'ultimate tensile strength',
                          'compressive fracture strain': 'compressive ductility',
                          'tensile fracture strain': 'tensile ductility',
                          'compressive yield strength': 'compressive yield stress',
                          'tensile yield strength': 'tensile yield stress'}

# As well as pairs below:
# Tensile Ductility - tensile ductility
# Compressive Ductility - compressive ductility

propertyApprovedNames = ['creep rate',
                         'hardness',
                         'd parameter',
                         'tensile ductility',
                         'compressive ductility',
                         'tensile yield stress',
                         'compressive yield stress',
                         'fracture toughness',
                         'ultimate tensile strength',
                         'ultimate compressive strength',
                         'youngs modulus',
                         'density',
                         'B/G ratio',
                         'CTE',
                         'VEC',
                         'bulk modulus',
                         'shear modulus',
                         'mixing enthalpy',
                         'mixing entropy',
                         'melting temperature']

def propertyNameUnify(propertyName: str):
    if propertyName in propertyApprovedNames:
        return propertyName
    elif propertyName in propertyExceptionPairs:
        return propertyExceptionPairs[propertyName]
    elif propertyName is None or propertyName.isspace():
        return None
    elif propertyName in propertyExceptionToUpper:
        return propertyName.upper()
    elif propertyName.isupper():
        return propertyName
    elif propertyName.endswith(' '):
        return propertyName[:-1].lower()
    elif propertyName.startswith(' '):
        return propertyName[1:].lower()
    else:
        return propertyName.lower()

propertySourceApprovedNames = ['GAN', 'EM', 'ML', 'DFT', 'EXP', 'VAL', 'CALC']

def propertySourceUnifier(propertySource: str):
    if propertySource in propertySourceApprovedNames:
        return propertySource
    elif propertySource.replace(' ','') in propertySourceApprovedNames:
        return propertySource.replace(' ','')
    else:
        return propertySource.lower()
