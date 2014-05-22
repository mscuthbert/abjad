# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DistributionFileWrangler_go_home_01():

    input_ = 'red~example~score d h q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score Manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution files',
        'Score Manager - scores',
        ]
    assert score_manager._transcript.titles == titles


def test_DistributionFileWrangler_go_home_02():

    input_ = 'd h q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score Manager - scores',
        'Score Manager - distribution files',
        'Score Manager - scores',
        ]
    assert score_manager._transcript.titles == titles