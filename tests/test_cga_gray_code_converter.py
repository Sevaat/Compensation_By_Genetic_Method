from src.classical_genetic_algorithm.options.parameters import Parameters
from src.classical_genetic_algorithm.utils.gray_code_converter import GrayCodeConverter

def test_convert_to_code(fixture_parameters):
    """Перевод значений в код Грея"""
    parameters = Parameters(fixture_parameters)
    # gene_sets = [[0 1 2 3 4], [5 6 7 8 9]]: количество знаков для первого набора - 3, для второго набора - 3

    code = GrayCodeConverter.convert_to_code([0, 0], parameters)
    assert code == '000000'
    code = GrayCodeConverter.convert_to_code([4, 4], parameters)
    assert code == '110110'
    code = GrayCodeConverter.convert_to_code([2, 3], parameters)
    assert code == '011010'

def test_convert_from_code(fixture_parameters):
    """Перевод значений из кода Грея"""
    parameters = Parameters(fixture_parameters)
    # gene_sets = [[0 1 2 3 4], [5 6 7 8 9]]: количество знаков для первого набора - 3, для второго набора - 3

    code = GrayCodeConverter.convert_from_code('000000', parameters)
    assert code == [0, 0]
    code = GrayCodeConverter.convert_from_code('110110', parameters)
    assert code == [4, 4]
    code = GrayCodeConverter.convert_from_code('011010', parameters)
    assert code == [2, 3]

