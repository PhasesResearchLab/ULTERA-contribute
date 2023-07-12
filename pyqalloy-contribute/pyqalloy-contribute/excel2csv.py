# %%
import pandas as pd
import sys
import json
import os


def convert(datasheet: str):
    '''This function converts an PyQAlloy-compliant Excel datasheet into a CSV file for the purpose of
    tracking changes in the data collection and curation, while preserving the original template/datasheet
    file along with its style and formatting. The CSV file is named after the original datasheet file, with
    the extension changed to .csv. The metadata is stored in the first few lines of the CSV file, and the
    data is stored in the rest of the file.

    Args:
        datasheet: Path to PyQAlloy-compliant Excel datasheet file.
    '''

    # Import metadata
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
    dataFileName = datasheet.replace('.xlsx', '').replace('.xls', '')

    # Import data
    print('Importing data.')
    df2 = pd.read_excel(datasheet,
                        usecols="A:N",
                        nrows=20000,
                        skiprows=8)
    # Convert the dataset
    parsed = df2.to_json(orient="split")
    labels = json.loads(parsed, strict=False)['columns']
    data = json.loads(parsed, strict=False)['data']

    print('Imported ' + str(len(data)) + ' datapoints.')

    with open(dataFileName + '.csv', 'w+') as outFile:
        # Write the metadata
        for line, val in metaData.items():
            outFile.write(line + ':,' + str(val) + '\n')
        outFile.write('\n')
        # Write the data
        outFile.write(','.join(labels) + '\n')
        for line in data:
            outFile.write(','.join(str(val) for val in line) + '\n')

        print('Successfully converted ' + datasheet + ' to ' + dataFileName + '.csv\n')


def detectDatasheetsAndConvert(path: str):
    '''This function detects all PyQAlloy-compliant Excel datasheets in a directory and converts them into
    CSV files. It skips the empty template file (template_v4.xlsx).

    Args:
        path: Path to the directory containing PyQAlloy-compliant Excel datasheets.
    '''

    for file in os.listdir(path):
        if file.endswith('.xlsx'):
            if file not in ['template_v4.xlsx', 'template_v4_DatasetExample.xlsx']:
                print('Converting ' + file)
                convert(path + '/' + file)
            else:
                print('Skipping ' + file)


if __name__ == '__main__':
    detectDatasheetsAndConvert(sys.argv[1])
