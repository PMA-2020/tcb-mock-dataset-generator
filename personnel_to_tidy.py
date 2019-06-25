"""Personnel dataset to tidy dataset"""
from copy import copy
from datetime import date, datetime
from typing import Dict, Any, List, Union

from config import SKILL_DATA_FIELDS, NO_SCORER_SKILL_FIELDS
from utils import save_csv, load_csv


HEADER: List[str] = \
    ['Date', 'Person', 'Scorer', 'Skill', 'SkillField', 'Value']
CONFIG: Dict[str, Any] = {
    'input_file_path': './input.csv',
    'output_file_path': './output.csv',
    'input_date_format': '%m/%d/%y',
}


def format_loaded_csv(
    source: List[List[str]],
) -> List[List[Union[str, int, date]]]:
    """Format a loaded CSV 2d array of raw strings into proper data types

    Args:
        source (list): 2d array of strings from a previously loaded CSV

    Returns:
        list: 2d array with strings formatted to correct data types
    """
    source_header: List[str] = source[0]

    # format dates
    date_formatted: List[List[Union[str, date]]] = [source_header, ]
    date_field_indices: List[int] = [source_header.index('Date'), ]
    for row in source[1:]:
        new_row: List[Union[str, date]] = copy(row)
        for idx in date_field_indices:
            date_format: str = CONFIG['input_date_format']
            new_row[idx]: date = \
                datetime.strptime(new_row[idx], date_format).date()
        date_formatted.append(new_row)

    # format integers
    all_formatted: List[List[Union[str, int, date]]] = [source_header, ]
    integer_field_indices: List[int] = [
        source_header.index(x)
        for x in SKILL_DATA_FIELDS
        if not x.endswith('notes')]
    for row in date_formatted[1:]:
        new_row: List[Union[str, int, date]] = copy(row)
        for idx in integer_field_indices:
            new_row[idx]: int = int(new_row[idx]) if new_row[idx] else None
        all_formatted.append(new_row)

    return all_formatted


def tidy_up(
    source: List[List[Any]]
) -> List[List[Any]]:
    """Convert specialized wide personnel dataset to tidy dataset

    Args:
        source (list): Source wide dataset

    Returns:
        list: Tidied up dataset
    """
    source_header: List[str] = source[0]

    # sort
    source_data_sorted: List[List[Any]] = sorted(source[1:], key=lambda x: (
        x[source_header.index('Date')],
        x[source_header.index('Person')]))
    source_sorted: List[List[Any]] = [source_header] + source_data_sorted

    # tidy up
    tidy_header: List[str] = HEADER
    tidy_dataset: List[List[Any]] = [tidy_header, ]
    for row in source_sorted[1:]:
        no_scorer_skills: List[str] = copy(NO_SCORER_SKILL_FIELDS)
        for idx, field in enumerate(SKILL_DATA_FIELDS):
            new_row: List[Any] = [None for _ in range(len(tidy_header))]
            skill_name: str = field.split('_')[0]
            skill_field: str = field.replace(skill_name + '_', '')

            new_row[tidy_header.index('Date')]: date \
                = row[source_header.index('Date')]
            new_row[tidy_header.index('Person')]: str \
                = row[source_header.index('Person')]
            new_row[tidy_header.index('Scorer')]: str \
                = row[source_header.index('Scorer')]
            new_row[tidy_header.index('Skill')]: str \
                = skill_name
            new_row[tidy_header.index('SkillField')]: str \
                = skill_field
            new_row[tidy_header.index('Value')]: str \
                = row[source_header.index(field)]

            if skill_field in no_scorer_skills:
                new_row[tidy_header.index('Scorer')] = None
                no_scorer_skills.remove(skill_field)

            tidy_dataset.append(new_row)

    return tidy_dataset


def run(
    config: Dict = CONFIG,
    save: bool = True
) -> List[List[Any]]:
    """Run the module.

    Args:
        config (dict): Dictionary containing configuration options.
        save (bool): Save CSV output? If not, returns dataset.

    Returns:
        list: Resulting dataset, if not save CSV output.
    """
    source: List[List[str]] = \
        load_csv(config['input_file_path'])
    source_formatted: List[List[Union[str, int, date]]] = \
        format_loaded_csv(source)
    dataset: List[List[Any]] = tidy_up(source_formatted)

    if save:
        save_csv(
            array=dataset,
            path=config['output_file_path'])
        print('Saved to: ' + config['output_file_path'])
    else:
        return dataset


if __name__ == '__main__':
    run(CONFIG)
