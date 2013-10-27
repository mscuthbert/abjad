# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_Spanner___len___01():
    r'''Spanner length equals length of components.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[1])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8
                d'8
            }
            {
                e'8 [
                f'8 ]
            }
            {
                g'8
                a'8
            }
        }
        '''
        )

    assert len(beam) == 1
    assert len(beam.components) == 1
    assert len(beam.leaves) == 2


def test_spannertools_Spanner___len___02():
    r'''Spanner length equals length of components.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = spannertools.BeamSpanner()
    beam.attach(voice[:])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }
        '''
        )

    assert len(beam) == 3
    assert len(beam.components) == 3
    assert len(beam.leaves) == 6
