from typing import Any, Callable, Dict, Tuple

from pydantic import BaseModel, ValidationError

from src.classical_genetic_algorithm.model.mutation import Mutation
from src.classical_genetic_algorithm.model.parent_selection import Selection
from src.classical_genetic_algorithm.model.population_initialization import Population
from src.classical_genetic_algorithm.model.recombination import Recombination
from src.classical_genetic_algorithm.model.replacement import Replacement
from src.classical_genetic_algorithm.model.stops import Stops
from src.classical_genetic_algorithm.model.target_function import TargetFunction
from src.classical_genetic_algorithm.utils.purpose import Purpose


class Operators(BaseModel):
    """
    Операторы классического генетического алгоритма
    """

    parent_selection: Callable  # тип выбора родителей
    stops: Tuple[Callable, Callable]  # условия останова
    purpose: Callable  # цель оптимизации (min, max)
    recombination: Callable  # тип рекомбинации
    target_function: Callable  # целевая функция
    population_initialization: Callable  # способ инициализации новой популяции
    mutation: Callable  # тип мутации
    replacement: Callable  # тип замены популяции

    def __init__(self, operations: Dict[str, Any], user_function: Callable, **data: Any):
        for key in vars(self):
            if key not in operations and key != "target_function":
                raise ValidationError
        operations["parent_selection"] = self._get_parent_selection(operations["parent_selection"])
        operations["stops"] = self._get_stops(operations["stops"])
        operations["purpose"] = self._get_purpose(operations["purpose"])
        operations["recombination"] = self._get_recombination(operations["recombination"])
        operations["population_initialization"] = self._get_population_initialization(
            operations["population_initialization"]
        )
        operations["mutation"] = self._get_mutation(operations["mutation"])
        operations["replacement"] = self._get_replacement(operations["replacement"])
        TargetFunction.function = user_function
        operations["target_function"] = self._target_function = TargetFunction.get_result_user_defined_function
        operations.update(data)
        super().__init__(**operations)

    @staticmethod
    def _get_parent_selection(value: str) -> Callable:
        """
        Выбор родителей для рекомбинации
        :param value: пользовательский выбор оператора
        :return: функция выбранного оператора
        """
        ps_dict = {
            "standard": Selection.standard_selection,
            "stochastic_universal_sampling": Selection.stochastic_universal_sampling,
        }
        if value in ps_dict.keys():
            return ps_dict[value]
        else:
            raise KeyError

    @staticmethod
    def _get_stops(value: str) -> Tuple[Callable, Callable]:
        """
        Оператор останова
        :param value: пользовательский выбор оператора
        :return: функция выбранного оператора
        """
        s_dict = {"epochs": Stops.stopping_by_the_number_of_eras, "immutability": Stops.stopping_for_the_best}
        if value in s_dict.keys():
            return s_dict[value], Stops.stop_for_homogeneity
        else:
            raise KeyError

    @staticmethod
    def _get_purpose(value: str) -> Callable:
        """
        Направление оптимизации
        :param value: пользовательский выбор оператора
        :return: функция выбранного оператора
        """
        p_dict = {"minimum": Purpose.sort_by_more, "maximum": Purpose.sort_by_less}
        if value in p_dict.keys():
            return p_dict[value]
        else:
            raise KeyError

    @staticmethod
    def _get_recombination(value: str) -> Callable:
        """
        Вид рекомбинации параметров особи
        :param value: пользовательский выбор оператора
        :return: функция выбранного оператора
        """
        r_dict = {
            "point": Recombination.point_crossing,
            "segmented": Recombination.segmental_crossing,
            "uniform": Recombination.even_crossing,
        }
        if value in r_dict.keys():
            return r_dict[value]
        else:
            raise KeyError

    @staticmethod
    def _get_population_initialization(value: str) -> Callable:
        """
        Инициализация начальной популяции
        :param value: пользовательский выбор оператора
        :return: функция выбранного оператора
        """
        pi_dict = {"random": Population.get_new_random_population}
        if value in pi_dict.keys():
            return pi_dict[value]
        else:
            raise KeyError

    @staticmethod
    def _get_mutation(value: str) -> Callable:
        """
        Тип мутации особи
        :param value: пользовательский выбор оператора
        :return: функция выбранного оператора
        """
        m_dict = {
            "inversion_one_bit": Mutation.inversion_one_bit,
            "inversion_group_bits": Mutation.inversion_group_bits,
            "swap": Mutation.swap,
            "reverse": Mutation.reverse,
            "shuffle": Mutation.shuffle,
        }
        if value in m_dict.keys():
            return m_dict[value]
        else:
            raise KeyError

    @staticmethod
    def _get_replacement(value: str) -> Callable:
        """
        Тип отбора лучших особей
        :param value: пользовательский выбор оператора
        :return: функция выбранного оператора
        """
        r_dict = {"elite": Replacement.elite, "easy_cut": Replacement.simple_cut}
        if value in r_dict.keys():
            return r_dict[value]
        else:
            raise KeyError
