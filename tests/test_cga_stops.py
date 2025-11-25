from src.classical_genetic_algorithm.model.individual import Individual
from src.classical_genetic_algorithm.model.stops import Stops
from src.classical_genetic_algorithm.options.parameters import Parameters


def test_stopping_for_the_best(fixture_parameters):
    """Тест на останов по повторениям лучшей особи"""
    parameters = Parameters(fixture_parameters)
    population = [
        Individual().new_individual_by_code("000000", parameters),
        Individual().new_individual_by_code("000001", parameters),
        Individual().new_individual_by_code("000010", parameters),
        Individual().new_individual_by_code("000011", parameters)
    ]

    stops_dict = {
        'individuals': population,
        'best_individual': None,
        'counter': 2,
        'parameters': parameters,
        'era': 0
    }

    i = 0
    while True:
        if Stops.stopping_for_the_best(stops_dict):
            break
        i += 1

    assert i == 10


def test_stopping_by_the_number_of_eras(fixture_parameters):
    """Тест на останов по количеству эпох"""
    parameters = Parameters(fixture_parameters)

    stops_dict = {
        'parameters': parameters,
        'era': 50
    }

    i = 0
    while True:
        if Stops.stopping_by_the_number_of_eras(stops_dict):
            break
        i += 1

    assert i == 50
