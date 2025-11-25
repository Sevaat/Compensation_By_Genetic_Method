from abc import ABC
from typing import Any, Dict


class Stops(ABC):
    @staticmethod
    def stopping_for_the_best(data_stops: Dict[str, Any]) -> bool:
        """
        Проверка на неизменность лучшей особи на протяжении ряда эпох

        Ожидаемое содержание словаря:
        individuals: List[Individual], best_individual: Union[Individual, None], counter: int, parameters: Parameters

        :param data_stops: список отсорт. особей, лучшая особь, количество повт. лучшей особи, параметры ГА
        :return: вывод True, если на протяжении ряда эпох не было изменения лучшей особи
        """
        if data_stops["best_individual"] is None:
            data_stops["best_individual"] = data_stops["individuals"][0]
            data_stops["counter"] = data_stops["parameters"].change_counter
        elif data_stops["individuals"][0] == data_stops["best_individual"]:
            data_stops["counter"] -= 1
            return bool(data_stops["counter"] == 0)
        else:
            data_stops["counter"] = data_stops["parameters"].change_counter
            data_stops["best_individual"] = data_stops["individuals"][0]
        return False

    @staticmethod
    def stopping_by_the_number_of_eras(data_stops: Dict[str, Any]) -> bool:
        """
        Останов по количеству эпох

        Ожидаемое содержание словаря:
        era: int, parameters: Parameters

        :param data_stops: номер текущей эры, параметры ГА
        :return: вывод False
        """
        if data_stops["era"] == data_stops["parameters"].number_of_eras:
            return True
        else:
            data_stops["era"] += 1
        return False

    @staticmethod
    def stop_for_homogeneity(data_stops: Dict[str, Any]) -> bool:
        """
        Останов по однородности популяции

        Ожидаемое содержание словаря:
        individuals: List[Individual]

        :param data_stops: список отсортированных особей
        :return:
        """
        if data_stops["individuals"].count(data_stops["individuals"][0]) / len(data_stops["individuals"]) >= 0.95:
            return True
        return False
