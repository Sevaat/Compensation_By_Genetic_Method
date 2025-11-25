import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

from src.classical_genetic_algorithm.model.individual import Individual
from src.classical_genetic_algorithm.options.operators import Operators
from src.classical_genetic_algorithm.options.parameters import Parameters


class CGA:
    def __init__(self, users_function: Callable):
        self._operators, self._parameters = CGA._get_operators_and_parameters(users_function)

    @property
    def operators(self) -> Operators:
        return self._operators

    @property
    def parameters(self) -> Parameters:
        return self._parameters

    @staticmethod
    def _load_data() -> Dict[str, Any]:
        """
        Читать JSON файл
        :return:
        """
        filepath = str(Path(__file__).resolve().parent.parent.parent / "data")
        os.makedirs(filepath, exist_ok=True)
        filepath = f"{filepath}/data_cga.json"
        data = {}
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
            print("Файл успешно загружен")
        except FileNotFoundError as e:
            print(f"Файл не найден: {e}")
        except json.JSONDecodeError as e:
            print(f"Ошибка в формате JSON: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        return data

    @staticmethod
    def _save_data(population: List[Individual], parameters: Parameters) -> None:
        """
        Запись в JSON файл
        :return:
        """
        filepath = str(Path(__file__).resolve().parent.parent.parent / "result")
        os.makedirs(filepath, exist_ok=True)
        filepath = f"{filepath}/result_cga_{datetime.now().strftime("%d.%m.%Y_%H-%M-%S")}.json"
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump([ind.to_dict(parameters) for ind in population], file)
            print("Запись результатов прошла успешно")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    @staticmethod
    def _get_operators_and_parameters(users_function: Callable) -> Tuple[Operators, Parameters]:
        """
        Получать операторы и параметры ГА
        :param users_function: пользовательская функция
        :return: операторы, параметры ГА
        """
        data = CGA._load_data()
        operators = Operators(data["operators"], users_function)
        parameters = Parameters(data["parameters"])
        return operators, parameters

    def run(self) -> None:
        """
        Оптимизировать задачи с использованием классического генетического алгоритма
        :return:
        """
        best_individual = None
        counter = None

        population = self.operators.population_initialization(self.parameters)
        population = self.operators.target_function(population, self.parameters)
        era = 0
        while True:
            parents = self.operators.parent_selection(population, self.operators.purpose)
            children = self.operators.recombination(population, parents, self.parameters)
            del parents
            mutants = self.operators.mutation(population, children, self.parameters)
            del children
            mutants = self.operators.target_function(mutants, self.parameters)
            population = self.operators.replacement(population, mutants, self.parameters, self.operators.purpose)
            del mutants
            data_stops = {
                "individuals": population,
                "best_individual": best_individual,
                "counter": counter,
                "parameters": self._parameters,
                "era": era,
            }
            if self.operators.stops[0](data_stops) or self.operators.stops[1](data_stops):
                print(f"Расчет окончен на эре: {era}")
                break
            else:
                era += 1
        self._save_data(population[: self.parameters.number_of_results], self.parameters)
