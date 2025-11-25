from abc import ABC
from typing import List

from src.classical_genetic_algorithm.options.parameters import Parameters


class GrayCodeConverter(ABC):
    @staticmethod
    def __get_maximum_discharge(parameters: Parameters) -> List[int]:
        """
        Определение наибольших разрядов параметров особи в бинарной кодировке
        :param parameters: параметры ГА
        :return: список значений наибольших разрядов
        """
        maximum_discharge = []
        for gene_set in parameters.gene_sets:
            value = len(gene_set) - 1
            discharge = bin(value)[2:]
            maximum_discharge.append(len(discharge))
        return maximum_discharge

    @staticmethod
    def convert_to_code(genotype: List[int], parameters: Parameters) -> str:
        """
        Преобразование списка значений параметров особи в код Грея с определенной разрядностью
        :param genotype: генотип особи (через индексы)
        :param parameters: параметры ГА
        :return: код Грея особи
        """
        gray_code = ""
        for i, gene in enumerate(genotype):
            gray_number = gene ^ (gene >> 1)
            gray_binary = bin(gray_number)[2:]
            maximum_discharge = GrayCodeConverter.__get_maximum_discharge(parameters)
            gray_binary = gray_binary.zfill(maximum_discharge[i])
            gray_code += gray_binary
        return gray_code

    @staticmethod
    def convert_from_code(code: str, parameters: Parameters) -> List[int]:
        """
        Преобразование кода Грея с определенной разрядностью в список значений параметров особи
        :param parameters: параметры ГА
        :param code: код Грея особи
        :return: генотип особи (через индексы)
        """
        genotype = []
        j = 0
        maximum_discharge = GrayCodeConverter.__get_maximum_discharge(parameters)
        for md in maximum_discharge:
            part = code[j : j + md]
            binary = part[0]
            for i in range(1, len(part)):
                if part[i] == "1":
                    if binary[i - 1] == "0":
                        binary += "1"
                    else:
                        binary += "0"
                else:
                    binary += binary[i - 1]
            genotype.append(int(binary, 2))
            j += md
        return genotype
