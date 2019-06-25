"""Convert tidy data format to data by skill"""
from datetime import date
from typing import Dict, Any, List, Union

from config import NO_SCORER_SKILL_FIELDS
from utils import save_csv


HEADER: List[str] = \
    ['Skill', 'Date', 'Person', 'Current Capacity', 'Targeted Capacity']
VALUE_FIELDS: List[str] = ['Current Capacity', 'Targeted Capacity']
SKILL_FIELD_MAPPING: Dict[str, str] = {
    'current_capacity': 'Current Capacity',
    'targeted_capacity': 'Targeted Capacity',
}
CONFIG: Dict[str, Any] = {
    'output_file_path': './output.csv',
    'include_scorer_skills': False
}


def transform(
    source: List[List[Any]],
    include_scorer_skills: bool = False
) -> List[List[Any]]:
    """Transform dataset from tidy to PMA TCB specific skill dataset

    Args:
        source (list): Source dataset
        include_scorer_skills (bool): Include PMA TCB specific skills which
        represent skills which are given by a specific person who is scoring
        a learner personnel's skill capacity?

    TODOs:
        - Implement inclusion of scorer skills as variable export dataset.

    Returns:
        list: Transformed dataset
    """
    transformed: List[List[Any]] = []
    source_header: List[str] = source[0]

    # Sort source
    source_data_sorted = sorted(source[1:], key=lambda x: (
        x[source_header.index('Skill')],
        x[source_header.index('Date')],
        x[source_header.index('Person')],))

    # Transform
    header: List[str] = HEADER
    current_entry: List[Any] = []
    for row in source_data_sorted:
        # avoid repeats
        last_entry_composite_key: List[Any] = \
            None if transformed == [] else \
            [transformed[-1][header.index('Skill')],
             transformed[-1][header.index('Date')],
             transformed[-1][header.index('Person')]]
        this_entry_composite_key: List[Any] = \
            [row[source_header.index('Skill')],
             row[source_header.index('Date')],
             row[source_header.index('Person')]]
        if last_entry_composite_key == this_entry_composite_key:
            continue

        if not current_entry:
            current_entry: List[Any] = [None for _ in range(len(header))]
            current_entry[header.index('Skill')]: str \
                = row[source_header.index('Skill')]
            current_entry[header.index('Date')]: date \
                = row[source_header.index('Date')]
            current_entry[header.index('Person')]: str \
                = row[source_header.index('Person')]

        skill_field: str = row[source_header.index('SkillField')]
        if skill_field not in NO_SCORER_SKILL_FIELDS:
            if not include_scorer_skills:
                continue
            pass  # edit from here in future if these fields needed

        target_value_field: str = SKILL_FIELD_MAPPING[skill_field]
        current_entry[header.index(target_value_field)]: Union[int, str] = \
            row[source_header.index('Value')] if \
            row[source_header.index('Value')] is not None \
            else ''  # substitution for 'None' for disambiguation

        values: List[Union[int, str]] = \
            [current_entry[header.index(x)] for x in VALUE_FIELDS]
        if None in values:
            continue
        else:
            transformed.append(current_entry)
            current_entry = []

    # Sort result
    transformed = sorted(transformed, key=lambda x: (
        x[HEADER.index('Skill')],
        x[HEADER.index('Date')],
        x[HEADER.index('Person')]))

    return [header] + transformed


def run(
    dataset: List[List[Any]] = None,
    config: Dict = CONFIG,
):
    """Run the module.

    Args:
        config (dict): Dictionary containing configuration options.
        dataset (list): Source dataset to transform and save
    """
    transformed: List[List[Any]] = transform(
        source=dataset,
        include_scorer_skills=config['include_scorer_skills'],)
    save_csv(
        array=transformed,
        path=config['output_file_path'])
    print('Saved to: ' + config['output_file_path'])


if __name__ == '__main__':
    run()
