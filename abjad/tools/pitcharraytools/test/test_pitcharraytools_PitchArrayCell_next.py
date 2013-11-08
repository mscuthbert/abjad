# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import pitcharraytools
from abjad.tools.pitcharraytools import PitchArrayCell
import pytest


def test_pitcharraytools_PitchArrayCell_next_01():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    assert array[0][1].next is array[0][3]


def test_pitcharraytools_PitchArrayCell_next_02():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])

    '''
    [] [      ] []
    [      ] [] []
    '''

    assert pytest.raises(IndexError, 'array[0][-1].next')


def test_pitcharraytools_PitchArrayCell_next_03():

    cell = PitchArrayCell([pitchtools.NamedPitch(1)])

    assert pytest.raises(IndexError, 'cell.next')