# PMA TCB Mock Dataset Generator
Create and update a certain model of mock time series datasets for PMA TCB efforts.

Used in tandem with business intelligence(BI) software such as Microsoft PowerBI.

## Requirements
- Python3
- Microsoft Excel or alternative
- BI Software for import
- A source data workbook

## Source data workbook
### What it is
This python package can only be used in tandem with a source data workbook file. However, due to sensitive personnel information contained in the file, the file itself is not included in this repository.

### How to obtain
You will have to obtain the workbook elsewhere, or otherwise create a new one from 'example.xlsx'.

### Workbook contents
- Every worksheet except for "readme", anything starting with the word "data", or ending with ".txt" are for modeling.
- Any worksheet containing the word "unjoined" is for mock data that is not yet joined with model tables in the workbook.
- All other worksheets starting with the word "data" can be imported into BI software or otherwise used for analysis.

## Usage
### I. Generate new mock dataset, broken down by personnel
1. The "data_by_person_unjoined" worksheet can be updated by running the "tcb_mock_dataset_generator.py" python script. It will generate an "output.csv".
2. Before you run the python script, make sure to create a file called "personnel.txt" and place it in the same directory with the Python script. The contents of "personnel.txt" should be a list of all personnel that are subject to TCB scoring and learning, AKA 'learners'. Currently, there is a worksheet called "personnel.txt", which filters out the list of learners from the "personnel" worksheet. You should use that as the text file's contents.
3. Run the following python script: create_new_personnel_dataset.py
4. The script will create a CSV called "output.csv". That CSV can then be saved as the new contents for the "data_by_person_unjoined" worksheet. For all intents and purposes, you can delete the current "data_by_person_unjoined" worksheet and replace with a new one.

### II. Check the data
1. Go to the "data" worksheet and check that all the contents of the "data_by_person_unjoined" worksheet appear. At the time of this writing, the "data" worksheet assumes that all of the data in the "data_by_person_unjoined" worksheet will be found in the range of A1 to TE1500 of that worksheet.

### III. Import or continue
1. If you need only need a tidy dataset or one broken down by skills rather than personnel, continue to the next step. Otherwise, continue with this step.
2. Save the file as is, or save the "data" worksheet as a new CSV file.
3. Import either saved CSV or the entire workbook itself into your BI software or use elsewhere for analysis.

### IV. Convert to a tidy dataset
1. If you only need a dataset broken down by skill, skip this step.
2. Save the contents of the "data" worksheet as a new CSV called "input.csv".
3. Run the following python script: personnel_to_tidy.py
4. The script will create a CSV called "output.csv". That CSV can then be saved as the new contents for the "data" worksheet. For all intents and purposes, you can delete the current "data" worksheet and replace with a new one.
5. Save the file as is, or save the "data" worksheet as a new CSV file.
6. Import either saved CSV or the entire workbook itself into your BI software or use elsewhere for analysis.

### V. Convert to a skills dataset
1. Save the contents of the "data" worksheet as a new CSV called "input.csv".
2. Run the following python script: personnel_to_skill.py
3. The script will create a CSV called "output.csv". That CSV can then be saved as the new contents for the "data_by_skill" worksheet. For all intents and purposes, you can delete the current "data_by_skill" worksheet and replace with a new one.
4. Save the file as is, or save the "data" worksheet as a new CSV file.
5. Import either saved CSV or the entire workbook itself into your BI software or use elsewhere for analysis.
