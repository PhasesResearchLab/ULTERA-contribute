#%%
import pandas as pd
import sys
import json

def convert(datasheet:str):
    '''This function converts an PyQAlloy-compliant Excel datasheet into a CSV file for the purpose of
    tracking changes in the data collection and curation, while preserving the original template/datasheet
    file along with its style and formatting. The CSV file is named after the original datasheet file, with
    the extension changed to .csv. The metadata is stored in the first few lines of the CSV file, and the
    data is stored in the rest of the file.

    Args:
        datasheet: Path to PyQAlloy-compliant Excel datasheet file.
    '''

    #Import metadata
    print('Reading the metadata.')
    metaDF = pd.read_excel(datasheet,
                           usecols="A:F",
                           nrows=4)
    meta = metaDF.to_json(orient="split")
    metaParsed = json.loads(meta, strict=False)['data']

    # Format metadata into a dictionary
    metaData = {
        'Name': metaParsed[0][1],
        'Email': metaParsed[1][1],
        'Direct Fetched': metaParsed[2][1],
        'Hand Fetched': metaParsed[3][1],
        'Comment': metaParsed[0][5]
    }

    # Logging progress into a CSV table
    dataFileName = datasheet.replace('.xls', '').replace('.xlsx', '')

    # Import data
    print('\nImporting data.')
    df2 = pd.read_excel(datasheet,
                        usecols="A:N",
                        nrows=20000,
                        skiprows=8)
    result = df2.to_json(orient="records")
    parsed = json.loads(result, strict=False)
    print('Imported '+str(parsed.__len__())+' datapoints.\n')

    with open(dataFileName+'.csv', 'w+') as outFile:
        for line, val in metaData.items():
            outFile.write(line+':,'+str(val)+'\n')
        outFile.write('\n')
        outFile.write(df2.to_csv(index=False))

if __name__ == '__main__':
    convert(sys.argv[1])



