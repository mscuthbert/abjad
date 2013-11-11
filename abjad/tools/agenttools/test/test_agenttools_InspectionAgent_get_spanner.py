# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_agenttools_InspectionAgent_get_spanner_01():

    container = Container("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, container.select_leaves()[:-1])
    slur = Slur()
    attach(slur, container.select_leaves()[:-1])
    trill = spannertools.TrillSpanner()
    attach(trill, container)

    assert testtools.compare(
        container,
        r'''
        {
            c'8 [ ( \startTrillSpan
            d'8
            e'8 ] )
            f'8 \stopTrillSpan
        }
        '''
        )

    assert inspect(container).get_spanner() == trill

    string = 'inspect(container[0]).get_spanner()'
    assert pytest.raises(ExtraSpannerError, string)

    string = 'inspect(container[-1]).get_spanner()'
    assert pytest.raises(MissingSpannerError, string)