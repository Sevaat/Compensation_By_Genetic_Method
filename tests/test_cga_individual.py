from src.classical_genetic_algorithm.model.individual import Individual, IndividualFactory
from src.classical_genetic_algorithm.options.parameters import Parameters


def test_individual(fixture_parameters):
    """Создание особи"""
    parameters = Parameters(fixture_parameters)
    # gene_sets = [[0 1 2 3 4], [5 6 7 8 9]]: количество знаков для первого набора - 3, для второго набора - 3

    individual = Individual()
    assert individual.code == ""
    assert individual.rank == 0

    individual = Individual().new_individual_by_code("000000", parameters)
    assert individual.code == "000000"
    assert individual.rank == 0

    individual = IndividualFactory.new_random_individual(parameters)
    assert isinstance(individual, Individual)


def test_transcript_individual(fixture_parameters):
    """Перевод кода Грея в набор параметров"""
    parameters = Parameters(fixture_parameters)
    # gene_sets = [[0 1 2 3 4], [5 6 7 8 9]]: количество знаков для первого набора - 3, для второго набора - 3

    individual = Individual().new_individual_by_code("000000", parameters)
    genotype = Individual.transcript_individual(individual, parameters)
    assert genotype == ["0", "5"]

    individual = Individual().new_individual_by_code("110110", parameters)
    genotype = Individual.transcript_individual(individual, parameters)
    assert genotype == ["4", "9"]


def test_overstepping(fixture_parameters):
    """Проверка на вхождение параметра особи в поисковое пространство"""
    parameters = Parameters(fixture_parameters)
    # gene_sets = [[0 1 2 3 4], [5 6 7 8 9]]: количество знаков для первого набора - 3, для второго набора - 3

    individual = Individual()
    individual.code = "000000"  # число 000 соответствует 0му значению
    assert Individual.overstepping(individual, parameters)

    individual = Individual()
    individual.code = "111000"  # число 111 соответствует 6му значению, а всего значений 5
    assert not Individual.overstepping(individual, parameters)

    individual.code = "000111"  # число 111 соответствует 6му значению, а всего значений 5
    assert not Individual.overstepping(individual, parameters)
