# -*- encoding: utf-8 -*-
from abjad import *


def test_DecrescendoSpanner___init___01():
    r'''Init empty decrescendo spanner.
    '''

    decrescendo = DecrescendoSpanner()
    assert isinstance(decrescendo, DecrescendoSpanner)


def test_DecrescendoSpanner___init___02():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    decrescendo = DecrescendoSpanner()
    attach(decrescendo, staff[:4])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 \>
            d'8
            e'8
            f'8 \!
            g'2
        }
        '''
        )