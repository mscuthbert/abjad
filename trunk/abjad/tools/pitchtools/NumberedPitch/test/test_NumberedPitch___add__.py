# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitch___add___01():
    r'''Add numbered chromatic pitch to numbered chromatic pitch.
    '''

    pitch_1 = pitchtools.NumberedPitch(12)
    pitch_2 = pitchtools.NumberedPitch(13)

    assert pitch_1 + pitch_2 == pitchtools.NumberedPitch(25)


def test_NumberedPitch___add___02():
    r'''Add number to numbered chromatic pitch.
    '''

    pitch_1 = pitchtools.NumberedPitch(12)

    assert pitch_1 + 13 == pitchtools.NumberedPitch(25)
