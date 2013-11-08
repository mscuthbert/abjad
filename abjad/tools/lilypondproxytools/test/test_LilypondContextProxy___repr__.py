# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondproxytools.LilyPondContextProxy \
	import LilyPondContextProxy


def test_LilypondContextProxy___repr___01():
    r'''LilyPond component proxy repr is evaluable.
    '''

    note = Note("c'4")
    setting(note).staff.tuplet_full_length = True

    context_proxy_1 = setting(note).staff
    context_proxy_2 = eval(repr(context_proxy_1))

    assert isinstance(context_proxy_1, LilyPondContextProxy)
    assert isinstance(context_proxy_2, LilyPondContextProxy)