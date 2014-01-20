# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Measure_should_scale_contents_01():

    tuplet = Tuplet((2, 3), "c'8 d'8 e'8 f'8 g'8")
    measure = Measure((5, 12), [tuplet], should_scale_contents=False)

    assert systemtools.TestManager.compare(
        measure,
        r'''
        {
            \time 5/12
            \times 2/3 {
                c'8
                d'8
                e'8
                f'8
                g'8
            }
        }
        '''
        )
