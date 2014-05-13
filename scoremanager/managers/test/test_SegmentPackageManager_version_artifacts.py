# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageManager_version_artifacts_01():
    
    versions_directory = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'segments',
        'segment_01',
        'versions',
        )
    file_names = (
        'definition_0002.py',
        'output_0002.ly',
        'output_0002.pdf',
        )
    paths = []
    for file_name in file_names:
        path = os.path.join(versions_directory, file_name)
        paths.append(path)

    with systemtools.FilesystemState(remove=paths):
        input_ = 'red~example~score g segment~01 ver y q'
        score_manager._run(pending_input=input_)
        assert all(os.path.isfile(_) for _ in paths)