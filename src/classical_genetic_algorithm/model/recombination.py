import random
from abc import ABC
from typing import List, Tuple

from src.classical_genetic_algorithm.model.individual import Individual
from src.classical_genetic_algorithm.options.parameters import Parameters
from src.classical_genetic_algorithm.utils.duplicate_check import DuplicateCheck


class Recombination(ABC):
    @staticmethod
    def point_crossing(
        population: List[Individual], parents: List[Tuple[Individual, Individual]], parameters: Parameters
    ) -> List[Individual]:
        """
        Точечное скрещивание (случайная точка (точки) для обмена частью генотипа особей)
        :param parameters: параметры ГА
        :param population: список особей популяции
        :param parents: список родителей
        :return: список детей
        """
        children: List[Individual] = []
        for par_par in parents:
            points = Recombination.get_points(len(par_par[0].code), parameters)
            children_1 = ""
            children_2 = ""
            for i in range(len(points) - 1):
                children_1 += par_par[i % 2].code[points[i] : points[i + 1]]
                children_2 += par_par[(i + 1) % 2].code[points[i] : points[i + 1]]
            children += Recombination.child_addition(population + children, children_1, children_2, parameters)
        return children

    @staticmethod
    def segmental_crossing(
        population: List[Individual], parents: List[Tuple[Individual, Individual]], parameters: Parameters
    ) -> List[Individual]:
        """
        Сегментное скрещивание (случайная точка (точки) для обмена частью генотипа особей с вероятностью 20%)
        :param parameters: параметры ГА
        :param population: список особей популяции
        :param parents: список родителей
        :return: список детей
        """
        children: List[Individual] = []
        for par_par in parents:
            points = Recombination.get_points(len(par_par[0].code), parameters)
            children_1 = ""
            children_2 = ""
            s = True
            for i in range(0, len(points) - 1):
                if s:
                    children_1 += par_par[0].code[points[i] : points[i + 1]]
                    children_2 += par_par[1].code[points[i] : points[i + 1]]
                else:
                    children_1 += par_par[1].code[points[i] : points[i + 1]]
                    children_2 += par_par[0].code[points[i] : points[i + 1]]
                if random.randint(0, 100) < 20:
                    s = not s
            children += Recombination.child_addition(population + children, children_1, children_2, parameters)
        return children

    @staticmethod
    def even_crossing(
        population: List[Individual], parents: List[Tuple[Individual, Individual]], parameters: Parameters
    ) -> List[Individual]:
        """
        Равномерное скрещивание (выбор каждого детского признака от родителей с вероятностью 50%)
        :param parameters: параметры ГА
        :param population: список особей популяции
        :param parents: список родителей
        :return: список детей
        """
        children: List[Individual] = []
        for par_par in parents:
            points = Recombination.get_points(len(par_par[0].code), parameters)
            children_1 = ""
            children_2 = ""
            for i in range(0, len(points) - 1):
                p = random.choices(list(par_par), weights=[50, 50], k=1)
                children_1 += p[0].code[points[i] : points[i + 1]]
                p = random.choices(list(par_par), weights=[50, 50], k=1)
                children_2 += p[0].code[points[i] : points[i + 1]]
            children += Recombination.child_addition(population + children, children_1, children_2, parameters)
        return children

    @staticmethod
    def get_points(length: int, parameters: Parameters) -> List[int]:
        """
        Получение точек для рекомбинации
        :param parameters: параметры ГА
        :param length: длина закодированной последовательности признаков
        :return: список точек для рекомбинации
        """
        points = [random.randint(1, length - 2) for i in range(parameters.recombination_point_count)]
        points.append(0)
        points.append(length)
        points = sorted(points)
        return points

    @staticmethod
    def child_addition(
        population: List[Individual], children_1: str, children_2: str, parameters: Parameters
    ) -> List[Individual]:
        """
        Проверка на дубликаты и добавление новых особей в список детей
        :param parameters: параметры ГА
        :param population: список особей популяции
        :param children_1: ребенок 1
        :param children_2: ребенок 2
        :return: список детей с возможными добавлениями
        """
        added_children: List[Individual] = []
        ch_1 = Individual.new_individual_by_code(children_1, parameters)
        if ch_1 is not None:
            if DuplicateCheck.individual_addition(population, ch_1, parameters):
                added_children.append(ch_1)

        ch_2 = Individual.new_individual_by_code(children_2, parameters)
        if ch_2 is not None:
            if DuplicateCheck.individual_addition(population, ch_2, parameters):
                added_children.append(ch_2)

        return added_children
