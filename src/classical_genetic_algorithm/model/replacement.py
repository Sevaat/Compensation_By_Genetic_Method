from abc import ABC
from typing import Callable, List

from src.classical_genetic_algorithm.model.individual import Individual
from src.classical_genetic_algorithm.options.parameters import Parameters


class Replacement(ABC):
    @staticmethod
    def elite(
        individuals_1: List[Individual], individuals_2: List[Individual], parameters: Parameters, sorter: Callable
    ) -> List[Individual]:
        """
        Замена популяции через элитизм (неизменным остаётся % лучших особей)
        :param sorter: сортировщик по убыванию или возрастанию
        :param parameters: параметры ГА
        :param individuals_1: список особей в начальной популяции
        :param individuals_2: список новых особей-мутантов
        :return: список элитных особей и лучших особей-мутантов в количестве не превышающем макс. значения популяции
        """
        n_elite = int(parameters.proportion_of_elite_individuals * parameters.number_of_individuals)
        if len(individuals_1) - n_elite > len(individuals_2):
            n_elite = len(individuals_1) - n_elite
        new_individuals: List[Individual] = individuals_1[:n_elite]
        new_individuals += individuals_2
        new_individuals = sorter(new_individuals)
        return new_individuals[: parameters.number_of_individuals]

    @staticmethod
    def simple_cut(
        individuals_1: List[Individual], individuals_2: List[Individual], parameters: Parameters, sorter: Callable
    ) -> List[Individual]:
        """
        Замена популяции через отсечения лучших особей
        :param individuals_1: список особей в начальной популяции
        :param individuals_2: список новых особей-мутантов
        :param sorter: сортировщик по убыванию или возрастанию
        :param parameters: параметры ГА
        :return: список лучших особей и особей-мутантов в количестве не превышающем максимального значения популяции
        """
        new_individuals: List[Individual] = individuals_1 + individuals_2
        new_individuals = sorter(new_individuals)
        return new_individuals[: parameters.number_of_individuals]
