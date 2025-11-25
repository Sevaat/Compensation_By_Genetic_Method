import copy
from typing import List

import pytest


@pytest.fixture
def fixture_parameters():
    parameters = {
        "number_of_individuals": 100,
        "proportion_of_elite_individuals": 0.2,
        "number_of_eras": 100,
        "mutation_probability": 0.02,
        "change_counter": 10,
        "number_of_results": 5,
        "recombination_point_count": 1,
        "number_of_recurring_individuals": 0,
        "gene_sets": {
            "simple_set": [
                "0 1 2 3 4"
            ],
            "step_set": [
                {"start": 5, "end": 9, "step": 1}
            ]
        }
    }
    return parameters


@pytest.fixture
def fixture_operators():
    operators = {
        "parent_selection": "standard",
        "stops": "epochs",
        "purpose": "minimum",
        "recombination": "point",
        "population_initialization": "random",
        "mutation": "inversion_one_bit",
        "replacement": "elite"
    }
    return operators
