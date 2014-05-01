# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MakerModuleWrangler_view_views_module_01():

    input_ = 'k vmro q'
    score_manager._run(pending_user_input=input_)

    assert score_manager._session._attempted_to_open_file


def test_MakerModuleWrangler_view_views_module_02():

    input_ = 'blue~example~score k vmro q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents

    assert not score_manager._session._attempted_to_open_file
    assert 'No views module found.' in contents