from typing import List, Any, Union

from src.classical_genetic_algorithm.model.individual import Individual
from src.classical_genetic_algorithm.options.operators import Operators
from src.classical_genetic_algorithm.options.parameters import Parameters


def test_target_function(fixture_parameters, fixture_operators):
    """Проверка работы пользовательской функции"""
    # пользовательская функция
    def adder(ind_params: List[Any]) -> Union[int, float]:
        return sum([float(ip) for ip in ind_params])

    operators = Operators(fixture_operators, adder)
    parameters = Parameters(fixture_parameters)

    population = [
        Individual().new_individual_by_code("000000", parameters), # [0, 5]
        Individual().new_individual_by_code("000001", parameters), # [0, 6]
        Individual().new_individual_by_code("000010", parameters), # [0, 8]
        Individual().new_individual_by_code("001011", parameters) # [1, 7]
    ]

    population = operators.target_function(population, parameters)
    assert population[0].rank == 5
    assert population[1].rank == 6
    assert population[2].rank == 8
    assert population[3].rank == 8