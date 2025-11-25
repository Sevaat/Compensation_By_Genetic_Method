from typing import List
from src.classical_genetic_algorithm.classical_genetic_algorithm import CGA


def main():
    def user_function(param: List[str]):
        return sum([float(p) for p in param])

    cga = CGA(user_function)
    cga.run()


if __name__ == '__main__':
    main()