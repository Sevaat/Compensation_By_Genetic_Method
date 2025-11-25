from abc import ABC
from typing import List

from src.classical_genetic_algorithm.model.individual import Individual, IndividualFactory
from src.classical_genetic_algorithm.options.parameters import Parameters
from src.classical_genetic_algorithm.utils.duplicate_check import DuplicateCheck


class Population(ABC):
    @staticmethod
    def get_new_random_population(parameters: Parameters) -> List[Individual]:
        """
        Создание новой случайной популяции без повторений
        :param parameters: параметры ГА
        :return: список особей
        """
        population: List[Individual] = []
        while len(population) < parameters.number_of_individuals:
            individual = IndividualFactory.new_random_individual(parameters)
            if DuplicateCheck.individual_addition(population, individual, parameters):
                population.append(individual)
        return population
