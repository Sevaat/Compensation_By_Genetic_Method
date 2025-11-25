from abc import ABC
from typing import Callable, List

from src.classical_genetic_algorithm.model.individual import Individual
from src.classical_genetic_algorithm.options.parameters import Parameters


class TargetFunction(ABC):
    function: Callable

    @staticmethod
    def get_result_user_defined_function(individuals: List[Individual], parameters: Parameters) -> List[Individual]:
        """
        Пользовательская целевая функция
        :param parameters: параметры ГА
        :param individuals: список особей
        :return: список особей без некорректных (значение хромосомы выходит за допустимые границы)
        """
        new_individuals = []
        for ind in individuals:
            if ind.overstepping(parameters):
                individual_parameters = ind.transcript_individual(parameters)
                try:
                    ind.rank = TargetFunction.function(individual_parameters)
                except Exception as e:
                    print(f"Ошибка: {e}")
                    print("Введена некорректная функция или функция принимает некорректные аргументы.")
                    print("Проверьте правильность введенной информации и повторите попытку.")
                new_individuals.append(ind)
        return new_individuals
