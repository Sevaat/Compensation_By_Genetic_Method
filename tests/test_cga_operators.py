from typing import Callable
import pytest
from src.classical_genetic_algorithm.model.population_initialization import Population
from src.classical_genetic_algorithm.options.operators import Operators


def test_operators_1(fixture_operators):
    """тест на успешную инициализацию"""
    operators = Operators(fixture_operators, sum)
    assert operators.population_initialization == Population.get_new_random_population
    assert isinstance(operators.target_function, Callable)


def test_operators_2(fixture_operators):
    """тест на неуспешную инициализацию (нет ключа в словаре)"""
    fixture_operators["parent_selection"] = 5
    with pytest.raises(KeyError):
        Operators(fixture_operators, sum)


def test_operators_3(fixture_operators):
    """тест на неуспешную инициализацию (неполнота данных)"""
    del fixture_operators["parent_selection"]
    with pytest.raises(KeyError):
        Operators(fixture_operators, sum)
