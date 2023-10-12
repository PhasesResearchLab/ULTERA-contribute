version = 1
sourceDataDate = 'Feb 14th 2022'
sourceDataCount = 2149

elementOrder = ['Ni', 'Co', 'Cr', 'Fe', 'Al', 'Ti', 'Mo', 'Zr', 'Nb', 'V', 'W', 'Ta', 'Hf', 'Cu', 'Mn', 'Si', 'B',
                'Re', 'Ru', 'Sn', 'Zn', 'Mg', 'Li', 'Y', 'Ca', 'Pd', 'Sc', 'Ir', 'Be', 'Nd', 'U', 'Er', 'Dy', 'Gd',
                'Sm', 'Pr', 'Ce', 'La', 'Ag', 'Ga', 'Bi', 'Pu', 'Th', 'Pb', 'Au', 'Pt', 'Os', 'Yb', 'Ho', 'Ba', 'In',
                'Cd', 'Sr', 'C', 'O', 'N', 'S']

common = elementOrder[:20]
metallic = elementOrder[:-4]
all = elementOrder[:]

def compDict2Vec(compDict):
    outVec = []
    dictElements = set(compDict)

    for coverage in [common, metallic, all]:
        if dictElements.issubset(coverage):
            vecCover = coverage
            break
        else:
            vecCover = None

    if vecCover is not None:
        for el in vecCover:
            if el in dictElements:
                outVec.append(float(round(compDict[el], 4)))
            else:
                outVec.append(float(0))
    else:
        elementsNotInAll = list(dictElements.difference(set(all)))
        print(f'Composition vector could not be computed due to missing definition for {elementsNotInAll}')
        return None

    return outVec

def printMetadata():
    print(f'Composition Vector Version {version}\n'
          f'Created from ULTERA Database on {sourceDataDate} based on {sourceDataCount} unique HEAs '
          '(alloy-processing-structure combinations)\n')
    print('Elements are in the reverse order of the least loss of data caused by the element removal given previous\n'
          'removal of all less impactful elements; except in the case of C, O, N, S, which are removed first and \n'
          'placed at the last 4 positions.')

