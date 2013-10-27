from abjad import *


def test_tuplettools_Tuplet_toggle_prolation_01():
    '''Change augmentation to diminution.
    '''

    tuplet = Tuplet((4, 3), "c'8 d'8 e'8")

    assert testtools.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 4/3 {
            c'8
            d'8
            e'8
        }
        '''
        )

    tuplet.toggle_prolation()

    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'4
            d'4
            e'4
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_tuplettools_Tuplet_toggle_prolation_02():
    '''Change diminution to augmentation.
    '''

    tuplet = Tuplet((2, 3), "c'8 d'8 e'8")

    assert testtools.compare(
        tuplet,
        r'''
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        '''
        )

    tuplet.toggle_prolation()

    assert testtools.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 4/3 {
            c'16
            d'16
            e'16
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()
