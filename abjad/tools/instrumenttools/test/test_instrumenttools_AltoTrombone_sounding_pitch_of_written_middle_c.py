# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_AltoTrombone_sounding_pitch_of_written_middle_c_01():

    trombone = instrumenttools.AltoTrombone()

    assert trombone.sounding_pitch_of_written_middle_c == "c'"