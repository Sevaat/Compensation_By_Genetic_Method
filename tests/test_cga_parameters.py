from copy import deepcopy
import pytest
from pydantic import ValidationError

from src.classical_genetic_algorithm.options.parameters import Parameters


def test_parameters_1(fixture_parameters):
    """Тест на корректную инициализацию"""
    parameters = Parameters(fixture_parameters)
    assert parameters.number_of_individuals == 100
    assert parameters.proportion_of_elite_individuals == 0.2
    assert parameters.number_of_eras == 100
    assert parameters.gene_sets == [["0", "1", "2", "3", "4"], ["5", "6", "7", "8", "9"]]
    assert parameters.mutation_probability == 0.02
    assert parameters.change_counter == 10
    assert parameters.number_of_results == 5
    assert parameters.recombination_point_count == 1
    assert parameters.number_of_recurring_individuals == 0


def test_parameters_2(fixture_parameters):
    """Тест на некорректную инициализацию (значения выходят за диапазон)"""
    for key in fixture_parameters.keys():
        if key == "gene_sets":
            continue
        parameters = deepcopy(fixture_parameters)
        parameters[key] = 10000000
        with pytest.raises(ValidationError):
            Parameters(parameters)
        parameters[key] = -1
        with pytest.raises(ValidationError):
            Parameters(parameters)


def test_parameters_3(fixture_parameters):
    """Тест на некорректную инициализацию (неполнота данных)"""
    del fixture_parameters["number_of_individuals"]
    with pytest.raises(ValidationError):
        Parameters(fixture_parameters)
