from typing import Any, Dict, List

from pydantic import BaseModel, Field, ValidationError


class Parameters(BaseModel):
    """
    Параметры классического генетического алгоритма
    """

    number_of_individuals: int = Field(gt=0, le=1000000)  # количество особей в популяции
    proportion_of_elite_individuals: float = Field(ge=0, le=1)  # доля элитных особей
    number_of_eras: int = Field(gt=0, le=1000000)  # количество эпох
    gene_sets: List[Any]  # данные хромосом
    mutation_probability: float = Field(ge=0, le=1)  # вероятность мутации
    change_counter: int = Field(gt=0, le=1000000)  # счётчик изменений лучшей особи
    number_of_results: int = Field(gt=0, le=1000000)  # количество выводимых результатов
    recombination_point_count: int = Field(gt=0, le=1000000)  # количество точек рекомбинации
    number_of_recurring_individuals: int = Field(
        ge=0, le=1000000
    )  # количество повторяющихся особей (0 - сколько угодно)

    def __init__(self, parameters: Dict[str, Any], **data: Any):
        for key in vars(self):
            if key not in parameters:
                raise ValidationError
        parameters["gene_sets"] = self._get_gene_sets(parameters["gene_sets"])
        parameters.update(data)
        super().__init__(**parameters)

    @staticmethod
    def _get_gene_sets(data_gene_sets: Dict[str, List[Any]]) -> List[Any]:
        """
        Распаковка данных генотипов особей
        :param data_gene_sets: пользовательские данные генотипов особей
        :return: распакованные данные особей
        """
        gene_sets = []
        try:
            for gs in data_gene_sets["simple_set"]:
                gene_sets.append(gs.split())
            for gs in data_gene_sets["step_set"]:
                gene_set = []
                start, end, step = gs["start"], gs["end"], gs["step"]
                while start <= end:
                    gene_set.append(str(start))
                    start += step
                gene_sets.append(gene_set)
        except Exception as e:
            print(e)
        return gene_sets
