from abjad import *


def test_MarkupCommand_args_01( ):
    mc = markuptools.MarkupCommand('draw-circle', ['#1', '#0.1', '##f'], None)
    assert mc.args == ('#1', '#0.1', '##f')
