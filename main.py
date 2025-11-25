from typing import List
from src.classical_genetic_algorithm.classical_genetic_algorithm import CGA
from src.newton_method.newton_method import NewtonMethod


def main_1():
    def user_function(param: List[str]):
        return sum([float(p) for p in param])

    cga = CGA(user_function)
    cga.run()

def main_2():
    nm = NewtonMethod()
    nm.run()


if __name__ == '__main__':
    main_2()