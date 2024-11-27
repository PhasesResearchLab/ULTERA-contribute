import os
import csv
import textwrap
import datetime

def update_readme():
    csv_dir = '.github/excel2csv'
    readme_path = 'README.md'

    if not os.path.exists(csv_dir):
        print(f"Directory {csv_dir} does not exist.")
        return

    files = []
    names = []
    emails = []
    comments = []
    line_counts = []

    for filename in os.listdir(csv_dir):
        if filename.endswith('.csv'):
            with open(os.path.join(csv_dir, filename), 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                current_name = ''
                current_email = ''
                current_comment = ''
                line_count = 0
                for i, row in enumerate(csvreader):
                    if i == 0:
                        current_name = row[1].strip()  # Extract Name
                    elif i == 1:
                        current_email = row[1].strip()  # Extract Email
                    elif i == 4:
                        current_comment = row[1].strip()  # Extract Comment
                    # Count lines starting from line 8
                    if i >= 7:
                        line_count += 1
                # Append the extracted data for the current file to the lists
                files.append(filename)
                names.append(current_name)
                emails.append(current_email)
                comments.append(current_comment)
                line_counts.append(line_count)

    readme = ''
    
    if files: 
        # Writes README.md preamble
        readme += textwrap.dedent(f'''
        ## This Dataset Contributions

        **Name:** {' / '.join(set(names))}
        <br>
        **Email:** {' / '.join(set(emails))}
        ''')

        for i, comment in enumerate(comments):
            readme += textwrap.dedent(f'''
            ```
            File: {files[i]}
            Datapoints: {line_counts[i]}
            Comment: {comment}
            ```
            ''')

        readme += textwrap.dedent(f'''
        **Last time updated:** {datetime.datetime.now().strftime("%m-%d-%Y %I:%M%p").lower()}
        ''')

    readme += textwrap.dedent('''
    ## The ULTERA Database
    This template repository was developed for contributing to the [**ULTERA Database**](https://ultera.org) carried under the [**DOE ARPA-E ULTIMATE program**](https://arpa-e.energy.gov/?q=arpa-e-programs/ultimate) that aims to develop a new generation of materials for turbine blades in gas turbines and related applications. 

    The main scope of this dataset is collecting data on compositionally complex alloys (CCAs), also known as high entropy alloys (HEAs) and multi-principle-element alloys (MPEAs), with extra attention given to (1) high-temperature (refractory) mechanical data, (2) phases present under different processing conditions. Although low-entropy alloys (incl. binaries) are typically not presented to the end-user (or counted in statistics), some are present and used in ML efforts; thus **all high-quality alloy data contributions are welcome!**

    For further information, please visit the [ULTERA-contribute](https://github.com/PhasesResearchLab/ULTERA-contribute/) repository.
    ''')

    with open(readme_path, 'w') as readme_file:
        readme_file.write(readme)

    print(f"README.md has been updated with the latest contributions.")

if __name__ == '__main__':
    update_readme()