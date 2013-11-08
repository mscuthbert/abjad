# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_ClefMark_middle_c_position_01():

    assert marktools.ClefMark('treble').middle_c_position == -6
    assert marktools.ClefMark('alto').middle_c_position == 0
    assert marktools.ClefMark('tenor').middle_c_position == 2
    assert marktools.ClefMark('bass').middle_c_position == 6
    assert marktools.ClefMark('treble^8').middle_c_position == -13
    assert marktools.ClefMark('alto^15').middle_c_position == -13
    assert marktools.ClefMark('tenor_8').middle_c_position == 9
    assert marktools.ClefMark('bass_15').middle_c_position == 19