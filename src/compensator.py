import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Dict, Any, List, Union

from src.classical_genetic_algorithm.options.parameters import Parameters
from src.newton_method.models.branch import Branch
from src.newton_method.models.node import Node
from src.newton_method.newton_method import NewtonMethod


class Compensator:
    nodes: List[Node]
    branches: List[Branch]
    parameters: Parameters
    installations: List[Dict[str, Any]]
    load_schedule: List[Union[int, float]]

    def __init__(self):
        data = self._load_data_nm()
        self.nodes = [Node(node) for node in data["nodes"]]
        for branch in data["branches"]:
            for node in self.nodes:
                if not isinstance(branch["start"], Node):
                    if branch["start"] == node.name:
                        branch["start"] = node
                if not isinstance(branch["end"], Node):
                    if branch["end"] == node.name:
                        branch["end"] = node
        self.branches = [Branch(branch) for branch in data["branches"]]
        self.parameters = Parameters(data["parameters"])

        self.installations = self._load_data_installations()

        self.load_schedule = self._load_data_load_schedule()


    @staticmethod
    def _load_data_nm() -> Dict[str, Any]:
        """
        Читать JSON файл с данными по узлам, ветвям и параметрам метода Ньютона
        :return:
        """
        filepath = str(Path(__file__).resolve().parent.parent.parent / "data")
        os.makedirs(filepath, exist_ok=True)
        filepath = f"{filepath}/data_nm.json"
        data = {}
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
            print("Файл успешно загружен (данные узлов)")
        except FileNotFoundError as e:
            print(f"Файл не найден (данные узлов): {e}")
        except json.JSONDecodeError as e:
            print(f"Ошибка в формате JSON (данные узлов): {e}")
        except Exception as e:
            print(f"Произошла ошибка (данные узлов): {e}")
        return data

    @staticmethod
    def _load_data_installations() -> List[Dict]:
        """
        Читать JSON файл с данными установок компенсирующих
        :return:
        """
        filepath = str(Path(__file__).resolve().parent.parent.parent / "data")
        os.makedirs(filepath, exist_ok=True)
        filepath = f"{filepath}/data_installations.json"
        data = []
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
            print("Файл успешно загружен (данные установок)")
        except FileNotFoundError as e:
            print(f"Файл не найден (данные установок): {e}")
        except json.JSONDecodeError as e:
            print(f"Ошибка в формате JSON (данные установок): {e}")
        except Exception as e:
            print(f"Произошла ошибка (данные установок): {e}")
        return data

    @staticmethod
    def _load_data_load_schedule() -> List[Union[int, float]]:
        """
        Читать JSON файл с данными графика электрических нагрузок в % от максимальных нагрузок
        :return:
        """
        filepath = str(Path(__file__).resolve().parent.parent.parent / "data")
        os.makedirs(filepath, exist_ok=True)
        filepath = f"{filepath}/data_load_schedule.json"
        data = []
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
            print("Файл успешно загружен (данные графика нагрузок)")
        except FileNotFoundError as e:
            print(f"Файл не найден (данные графика нагрузок): {e}")
        except json.JSONDecodeError as e:
            print(f"Ошибка в формате JSON (данные графика нагрузок): {e}")
        except Exception as e:
            print(f"Произошла ошибка (данные графика нагрузок): {e}")
        return data

    def _corrector(self, genotype: List[str]) -> List[Node]:
        """
        Корректировать максимальную реактивную мощность узлов по генотипу особи
        :param genotype: генотип особи из ГА
        :return: скорректированные по реактивной мощности узлы
        """
        corrected_nodes = deepcopy(self.nodes)
        i = 0
        for node in corrected_nodes:
            if node.type_node =="ИП":
                continue
            elif node.type_node =="ИПО":
                installation = self.installations[int(genotype[i])]
                adjustment = installation["Реактивная мощность, квар"] * int(genotype[i+1]) / 1000
                node.imaginary_power = node.imaginary_power + adjustment
                i += 1
            else:
                installation = self.installations[int(genotype[i])]
                adjustment = installation["Реактивная мощность, квар"] * int(genotype[i + 1]) / 1000
                node.imaginary_power = node.imaginary_power - adjustment
                i += 1
        return corrected_nodes

    def run(self, genotype: List[str]):
        corrected_nodes = self._corrector(genotype)
        nm = NewtonMethod(corrected_nodes, self.branches, self.parameters)
        nm.run()
