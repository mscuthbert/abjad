# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_BaritoneSaxophone_sounding_pitch_of_written_middle_c_01():

    baritone_saxophone = instrumenttools.BaritoneSaxophone()

    assert baritone_saxophone.sounding_pitch_of_written_middle_c == 'ef,'