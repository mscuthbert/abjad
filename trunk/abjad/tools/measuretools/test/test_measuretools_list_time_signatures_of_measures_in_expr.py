from abjad import *


def test_measuretools_list_time_signatures_of_measures_in_expr_01():
    '''Extract ordered list of time signature pairs from components. 
    '''

    t = Staff([Measure((2, 8), "c'8 d'8"),
        Measure((3, 8), "c'8 d'8 e'8"),
        Measure((4, 8), "c'8 d'8 e'8 f'8")])

    r'''
    \new Staff {
            \time 2/8
            c'8
            d'8
            \time 3/8
            c'8
            d'8
            e'8
            \time 4/8
            c'8
            d'8
            e'8
            f'8
    }
    '''

    time_signature_list = measuretools.list_time_signatures_of_measures_in_expr(t[:])
    assert time_signature_list == [(2, 8), (3, 8), (4, 8)]


def test_measuretools_list_time_signatures_of_measures_in_expr_02():
    '''Extract ordered list of time signature pairs from components.
    '''

    t = Staff("c'8 d'8 e'8 f'8")

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    time_signature_list = measuretools.list_time_signatures_of_measures_in_expr(t[:])
    assert time_signature_list == []
