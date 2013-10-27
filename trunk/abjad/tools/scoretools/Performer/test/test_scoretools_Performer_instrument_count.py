# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Performer_instrument_count_01():

    performer = scoretools.Performer('Flutist')
    assert performer.instrument_count == 0

    performer.instruments.append(instrumenttools.Flute())
    assert performer.instrument_count == 1

    performer.instruments.append(instrumenttools.Piccolo())
    assert performer.instrument_count == 2
