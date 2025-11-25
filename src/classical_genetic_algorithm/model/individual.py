import random
from typing import Any, Dict, List, Self, Union

from src.classical_genetic_algorithm.options.parameters import Parameters
from src.classical_genetic_algorithm.utils.gray_code_converter import GrayCodeConverter


class Individual:
    code: str
    rank: Union[int, float]

    def __init__(self) -> None:
        self.code = ""  # код Грея особи
        self.rank = 0  # значение функции приспособленности

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Individual):
            return self.code == other.code
        else:
            return False

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Individual):
            return self.code != other.code
        else:
            return False

    def __str__(self) -> str:
        return str(self.code)

    def __repr__(self) -> str:
        return str(self.code)

    def to_dict(self, parameters: Parameters) -> Dict[str, Any]:
        """
        Вывод особи в виде словаря
        :param parameters: параметры ГА
        :return: словарь описания особи
        """
        return {"code": self.code, "rank": self.rank, "genotype": self.transcript_individual(parameters)}

    def transcript_individual(self, parameters: Parameters) -> List[str]:
        """
        Перевод кода особи в список параметров
        :param parameters: параметры ГА
        :return: список параметров
        """
        genotype = GrayCodeConverter.convert_from_code(self.code, parameters)
        genotype_str = [parameters.gene_sets[i][p] for i, p in enumerate(genotype)]
        return genotype_str

    def overstepping(self, parameters: Parameters) -> bool:
        """
        Проверка допустимости параметров особи (нахождение в допустимых пределах)
        :param parameters: параметры ГА
        :return: True - если в допустимых пределах, False - иначе
        """
        genotype = GrayCodeConverter.convert_from_code(self.code, parameters)
        flag = True
        for i, gene in enumerate(genotype):
            if gene >= len(parameters.gene_sets[i]):
                flag = False
                break
        return flag

    @classmethod
    def new_individual_by_code(cls, code: str, parameters: Parameters) -> Union[Self, None]:
        """
        Создание особи по коду Грея
        :param code: код Грея особи
        :param parameters: параметры ГА
        :return: особь
        """
        individual = cls()
        individual.code = code
        if individual.overstepping(parameters):
            return individual
        else:
            return None


class IndividualFactory:
    @staticmethod
    def new_random_individual(parameters: Parameters) -> Individual:
        """
        Фабрика для производства случайных особей
        :param parameters: параметры ГА
        :return: случайная особь
        """
        individual = Individual()
        new_genotype = []
        for gene_set in parameters.gene_sets:
            individual_chromosome = random.randint(0, len(gene_set) - 1)
            new_genotype.append(individual_chromosome)
        individual.code = GrayCodeConverter.convert_to_code(new_genotype, parameters)
        return individual
