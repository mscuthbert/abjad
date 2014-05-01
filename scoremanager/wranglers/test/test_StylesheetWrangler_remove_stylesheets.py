# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_remove_stylesheets_01():

    path = os.path.join(
        score_manager._configuration.abjad_stylesheets_directory_path,
        'clean-letter-14.ily',
        )
    backup_path = path + '.backup'

    assert os.path.exists(path)
    assert not os.path.exists(backup_path)
    shutil.copyfile(path, backup_path)
    assert os.path.exists(backup_path)

    input_ = 'y rm clean-letter-14.ily remove q'
    score_manager._run(pending_user_input=input_)
    assert not os.path.exists(path)
    assert os.path.exists(backup_path)
    shutil.move(backup_path, path)
    manager = scoremanager.managers.FileManager(
        path=path,
        session=score_manager._session,
        )
    manager.add_to_repository(prompt=False)

    assert os.path.exists(path)
    assert not os.path.exists(backup_path)