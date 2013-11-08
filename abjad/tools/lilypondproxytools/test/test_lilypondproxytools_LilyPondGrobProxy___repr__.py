# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondproxytools.LilyPondGrobProxy import LilyPondGrobProxy


def test_lilypondproxytools_LilyPondGrobProxy___repr___01():
    r'''LilyPond grob proxy repr is evaluable.
    '''

    note = Note("c'4")
    override(note).note_head.color = 'red'

    grob_proxy_1 = override(note).note_head
    grob_proxy_2 = eval(repr(grob_proxy_1))

    assert isinstance(grob_proxy_1, LilyPondGrobProxy)
    assert isinstance(grob_proxy_2, LilyPondGrobProxy)