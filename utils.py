"""Package utils."""
import csv

from typing import List, Any


def load_csv(path) -> List[List[str]]:
    """Load csv

    Args:
        path (str): Path to file to load

    Returns:
        list: 2d array representing file
    """
    with open(path, 'r') as f:
        dataset: List[List[str]] = [x for x in csv.reader(f)]

    return dataset


def save_csv(
    array: List[List[Any]],
    path: str
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
