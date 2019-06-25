"""Convert tidy data format to data by skill"""
from typing import Any, List

from personnel_to_tidy import run as load
from tidy_to_skill import run as pipe


def run():
    """Run the module"""
    dataset: List[List[Any]] = load(save=False)
    pipe(dataset=dataset)


if __name__ == '__main__':
    run()
