# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageManager_go_back_01():

    input_ = 'red~example~score b q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Score manager - example scores',
        ]
    assert score_manager._transcript.titles == titles