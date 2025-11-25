from src.classical_genetic_algorithm.model.individual import Individual
from src.classical_genetic_algorithm.options.parameters import Parameters
from src.classical_genetic_algorithm.utils.duplicate_check import DuplicateCheck


def test_duplicate_check(fixture_parameters):
    """Проверка на повторения"""
    parameters = Parameters(fixture_parameters)

    population = [
        Individual().new_individual_by_code("000000", parameters),
        Individual().new_individual_by_code("000001", parameters),
        Individual().new_individual_by_code("000010", parameters),
        Individual().new_individual_by_code("000011", parameters)
    ]

    parameters.number_of_recurring_individuals = 0  # можно сколько угодно дубликатов
    individual = Individual().new_individual_by_code("000000", parameters)
    assert DuplicateCheck.individual_addition(population, individual, parameters)

    parameters.number_of_recurring_individuals = 1  # возможен только один дубликат
    individual = Individual().new_individual_by_code("000000", parameters)
    assert not DuplicateCheck.individual_addition(population, individual, parameters)
