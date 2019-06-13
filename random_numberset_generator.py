"""Random numberset generator

Reads and writes dataset files. Creates mock datasets.

Usage:
    Creating a new dataset
    1. Set CONFIG values.
    2. Run `python random_numberset_generator.py`
    3. Utilize CSV file output.
"""
import calendar
import csv
from copy import copy
from datetime import date
from random import randint, random as random_0_to_1, choice as random_choice
from typing import Callable, List, Dict, Any, Union

# Edit these values as needed, then simply run this module.
COMPOSITE_ID_FIELDS: List[str] = ['Date', 'Person', 'Scorer']
SKILL_FIELD_REPEATS: List[str] = \
    ['relevancy', 'priority', 'score', 'notes', 'current_capacity',
     'targeted_capacity']
SKILLS: List[str] = \
    ['A1', 'A2', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'C1', 'C2', 'C3',
     'C4', 'C5', 'C6', 'C7', 'D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2',
     'F3', 'F4', 'F5', 'F6', 'F7', 'G1', 'G2', 'H1', 'H2', 'H3', 'I1', 'I2',
     'J1', 'J2', 'K1', 'K2', 'L1', 'L2', 'L3', 'M1', 'M2', 'M3', 'M4', 'M5',
     'N1', 'N2', 'O1', 'O2', 'P1', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7',
     'Q8', 'Q9', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'S1', 'S2', 'S3', 'T1',
     'T2', 'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8', 'U9', 'V1', 'W1',
     'X1', 'X2', 'X3']
SCORER_TYPES: List[str] = ['self', 'PI', 'DM', 'ODK', 'SO']
NUM_SCORERS: int = len(SCORER_TYPES)
FIRST_VAL_IDX: int = \
    len(COMPOSITE_ID_FIELDS) + SKILL_FIELD_REPEATS.index('score') + 1
SCORE_MIN: int = 1
SCORE_MAX: int = 5
START_DATE = date(2019, 9, 1)
RAND_SCORE_FUNC: Callable = lambda: randint(a=SCORE_MIN, b=SCORE_MAX)
HEADER: List[str] = \
    [x for x in COMPOSITE_ID_FIELDS] + \
    ['{}_{}'.format(skill, field_type)
     for skill in SKILLS
     for field_type in SKILL_FIELD_REPEATS]
SKILL_FIELD_FUNCS: Dict[str, Callable] = {
    'Date': lambda: START_DATE,
    'notes': lambda: 'This is a miscellaneous note.',
    'current_capacity': lambda: '',
    'targeted_capacity': lambda: '',
    'relevancy': RAND_SCORE_FUNC,
    'priority': RAND_SCORE_FUNC,
    'score': RAND_SCORE_FUNC
}
CONFIG: Dict[str, Any] = {
    'min': SCORE_MIN,
    'max': SCORE_MAX,
    'num_cols': len(HEADER),
    'input_file_path': './input.csv',
    'input_personnel_list_path': './personnel.txt',
    'output_file_path': './output.csv',
    'mutation_min_increment': 0,
    'mutation_max_increment': 1,
    'mutation_pct_chance': 0.25,
    # 'start_date': datetime.strptime('2019-09-01', '%Y-%m-%d')
    'start_date': START_DATE,
    'note_field_suffix': '_notes',
    'progression_timeseries_months_step': 3,
    'progression_timeseries_iters': 3,  # 1yr=baseline + 3 additional quarters
    'include_header': True,
    'special_field_funcs': SKILL_FIELD_FUNCS,
}


def get_field_funcs(
    header: List[str] = HEADER,
) -> Dict[int, Callable]:
    """Get mapping of fields and funcs to call on them when generating data.

    Args:
        header (list): Header of output file containing fields

    Returns:
         dict: Mapping of indexes to funcs
    """
    field_funcs: Dict[int, Callable] = {}
    skill_field_types: List[str] = SKILL_FIELD_FUNCS.keys()
    for idx, field in enumerate(header):
        if field in skill_field_types:
            field_funcs[idx] = SKILL_FIELD_FUNCS[field]
        elif not any(field.endswith(x) for x in skill_field_types):
            field_funcs[idx] = lambda: ''
        else:
            for field_type in skill_field_types:
                if field.endswith(field_type):
                    field_funcs[idx] = SKILL_FIELD_FUNCS[field_type]
                    break

    return field_funcs


def get_personnel_list(
    personnel_file: str = CONFIG['input_personnel_list_path'],
) -> List[str]:
    """Get Personnel list

    Args:
        personnel_file (str): Path to '\n' delimited text file containing
        list of personnel.

    Returns:
        int: Number of rows
    """
    with open(personnel_file, 'r') as f:
        lines: List[str] = f.readlines()
    personnel_list: List[str] = [x.replace('\n', '') for x in lines]
    
    return personnel_list


def get_num_rows(
    personnel_list: List[str] = get_personnel_list(), 
) -> int:
    """Get number of rows for each iteration timeslice of mock dataset

    Args:
        personnel_list (list): Personnel list

    Returns:
        int: Number of rows
    """
    return len(personnel_list) * NUM_SCORERS


def generate_baseline_values(
    n_cols: int = CONFIG['num_cols'],
    n_rows: int = get_num_rows(),
    field_funcs_by_index: Dict[int, Callable] = get_field_funcs(),
) -> List[List[Any]]:
    """Create a dataset of random numbers.

    Args:
        n_cols (int): Number of dataset columns
        n_rows (int): Number of dataset rows
        field_funcs_by_index (dict): Indices of "special fields", that
        is, fields to run the "special_field_func" rather than using randint,
        and corresponding functions to run to generate a value that is used in
        substitution.

    Returns:
        list: Two-dimensional array as dataset
    """
    two_dim_array: List[List[Any]] = []

    for i in range(n_rows):
        row: List = []
        for j in range(n_cols):
            special_operation: Callable = field_funcs_by_index[j]
            val: Union[Any, int] = special_operation()
            row.append(val)
        two_dim_array.append(row)

    return two_dim_array


def add_composite_key_padding(
    value_set: List[List[Any]],
    width: int = len(COMPOSITE_ID_FIELDS)
) -> List[List[Any]]:
    """Add composite key field padding to a value set

    Args:
        value_set (list): Wide set of values only
        width (int): How much padding (num fields) to add?

    Returns:
        list: Dataset with composite key field padding and values
    """
    combined: List[List[Any]] = []
    default_val = ''
    padding = [default_val] * width
    for row in value_set:
        new_row = padding + row
        combined.append(new_row)

    return combined


def seed_column(
    dataset: List[List[Any]],
    column_index: int,
    value: Any
) -> List[List[Any]]:
    """Seed a column in given dataset with given value

    Args:
        dataset (list): Dataset to seed
        column_index (int): Index for column to seed
        value (Any): Value to seed into column

    Returns:
        list: New, seeded dataset
    """
    result: List[List[Any]] = []

    for row in dataset:
        new_row: List[Any] = copy(row)
        new_row[column_index]: Any = value
        result.append(new_row)
    
    return result


def save_csv(
    array: List[List[Any]],
    path: str = CONFIG['output_file_path']
):
    """Creates a CSV str from 2d array.

    Args:
        array (list): 2d array
        path (str): Path to save output file

    Side effects:
        - Saves CSV file
    """
    with open(path, 'w+') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(array)


def add_months(
    sourcedate: date,
    months: int
) -> date:
    """From given date and months to add, get new date

    Args:
        sourcedate (date): Source date
        months (int): Months to add

    Returns:
        date: New date
    """
    month: int = sourcedate.month - 1 + months
    year: int = sourcedate.year + month // 12
    month: int = month % 12 + 1
    day: int = min(sourcedate.day, calendar.monthrange(year, month)[1])

    return date(year, month, day)


def random_mutation(
    input_value: int,
    min_increment: int = CONFIG['mutation_min_increment'],
    max_increment: int = CONFIG['mutation_max_increment'],
    value_celing: int = CONFIG['max'],
    pct_chance: float = CONFIG['mutation_pct_chance'],
) -> int:
    """Takes an integer and 

    Args:
        input_value (int): Input value to be mutated
        min_increment (int): Minium possible value to increment if incremented
        max_increment (int): Maximum possible value to increment if incremented
        value_celing (int): Maximum output value; cannot be exceeded even if 
        incrementation randomizer procs.
        pct_chance (float): Percent chance to randomly proc mutation.

    Returns:
        int: Mutated value
    """
    new_val: int = None
    mutation_procced: bool = \
        input_value < value_celing \
        and random_0_to_1() <= pct_chance

    if mutation_procced:
        incrementors: List[int] = \
            [x for x in range(min_increment, max_increment + 1)]
        incremented: List[int] = [x + input_value for x in incrementors]
        value_pool: List[int] = [x for x in incremented if x <= value_celing]
        new_val: int = random_choice(value_pool)
    
    return new_val if mutation_procced else input_value


def generate_timeseries(
        baseline: List[List[Any]],
        timeseries_months_step: int,
        timeseries_iters: int,
        start_date: date,
        date_index: int,
        mutation_func: Callable,
) -> List[List[Any]]:
    """Generate mock time series progression dataset, given a baseline

    Generate mock time series progression dataset from an initial non time
    series dataset.

    Args:
        baseline (list): Dataset containing initial values
        timeseries_months_step (int): How many months of time pass in each
        iteration?
        timeseries_iters (int): How many iterations of time pass?
        start_date (datetime): What is the start date?
        date_index (int): Column index for dates
        mutation_func (func): A function which performs the mutation

    Returns:
        list: Two dimensional array as mock progression dataset
    """
    timeseries: List[List[Any]] = []
    mutation_field_indices: List[int] = \
        [idx for idx, fld in enumerate(HEADER) if fld.endswith('score')]

    for i in range(timeseries_iters):
        timeslice_dataset: List[List[Any]] = []
        new_date: date = add_months(
            sourcedate=start_date,
            months=timeseries_months_step * (i + 1),)
        for row in baseline:
            new_row = []
            for idx, val in enumerate(row):
                if idx in mutation_field_indices:
                    new_val: Any = mutation_func(val)
                    new_row.append(new_val)
                else:
                    new_row.append(val)
            new_row[date_index] = new_date

            timeslice_dataset.append(new_row)
        timeseries += timeslice_dataset

    return timeseries


def run(config: Dict = CONFIG):
    """Run the module.

    Args:
        config (dict): Dictionary containing configuration options.
    """
    baseline: List[List[Any]] = generate_baseline_values(
        n_cols=config['num_cols'],
        n_rows=get_num_rows(),)
    timeseries: List[List[Any]] = generate_timeseries(
        baseline=baseline,
        mutation_func=random_mutation,
        timeseries_months_step=config['progression_timeseries_months_step'],
        timeseries_iters=config['progression_timeseries_iters'],
        start_date=config['start_date'],
        date_index=COMPOSITE_ID_FIELDS.index('Date'),)
    data: List[List[Any]] = baseline + timeseries
    dataset: List[List[Any]] = \
        [HEADER] + data if config['include_header'] else data
    save_csv(
        array=dataset,
        path=config['output_file_path'])


if __name__ == '__main__':
    run(CONFIG)
