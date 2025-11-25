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

import pytest


@pytest.fixture
def test_data():
    return {
        "nodes": [
            {
                "name": "1",
                "type_node": "ИП",
                "real_power": 0,
                "imaginary_power": 0,
                "real_voltage": 115,
                "imaginary_voltage": 0
            },
            {
                "name": "2",
                "type_node": "ИПО",
                "real_power": 28.8675,
                "imaginary_power": 17.3205,
                "real_voltage": 110,
                "imaginary_voltage": 0
            },
            {
                "name": "3",
                "type_node": "НАГР",
                "real_power": 46.188,
                "imaginary_power": 23.094,
                "real_voltage": 110,
                "imaginary_voltage": 0
            }
        ],
        "branches": [
            {
                "start": "1",
                "end": "2",
                "real_resistance": 10,
                "imaginary_resistance": 20,
                "real_conductivity": 0,
                "imaginary_conductivity": 0
            },
            {
                "start": "1",
                "end": "3",
                "real_resistance": 15,
                "imaginary_resistance": 30,
                "real_conductivity": 0,
                "imaginary_conductivity": 0
            },
            {
                "start": "2",
                "end": "3",
                "real_resistance": 10,
                "imaginary_resistance": 25,
                "real_conductivity": 0,
                "imaginary_conductivity": 0
            }
        ],
        "parameters": {
            "nominal_voltage": 110,
            "accuracy": 0.001,
            "iterations": 100
        }
    }

