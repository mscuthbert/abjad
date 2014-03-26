# -*- encoding: utf-8 -*-
import abc
import inspect
import os
from abjad.tools import stringtools
from abjad.tools.abctools.ContextManager import ContextManager


class ScoreManagerObject(object):
    r'''Score manager object.
    '''

    ### CLASS VARIABLES ###

    __meta__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, session=None):
        from scoremanager import core
        from scoremanager import iotools
        self._backtrack = iotools.Backtrack(self)
        self._configuration = core.ScoreManagerConfiguration()
        self._session = session or core.Session()
        self._io_manager = iotools.IOManager(self._session)
        self._transcript = self._session.transcript

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when types are the same. Otherwise false.

        Returns boolean.
        '''
        return type(self) is type(expr)

    def __ne__(self, expr):
        r'''Is true when types are not the same. Otherwise false.

        Returns boolean.
        '''
        return not self == expr

    def __repr__(self):
        r'''Gets interpreter representation of score manager object.

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

    ### PRIVATE PROPERTIES ###

    @property
    def _space_delimited_lowercase_class_name(self):
        return stringtools.string_to_space_delimited_lowercase(
            type(self).__name__)

    @property
    def _spaced_class_name(self):
        return stringtools.string_to_space_delimited_lowercase(
            type(self).__name__)

    @property
    def _where(self):
        if self._session.is_tracking_source_code:
            return inspect.stack()[1]

    ### PRIVATE METHODS ###

    def _exit_io_method(self, source=None):
        result = False
        if self._session.is_complete:
            result = True
        elif self._session.is_backtracking_to_score_manager:
            result = True
        elif (self._session.is_backtracking_locally and 
            self._session.backtrack_stack):
            result = True
        elif (self._session.is_backtracking_locally and 
            not self._session.backtrack_stack):
            self._session._is_backtracking_locally = False
            result = True
        elif self._session.is_backtracking_to_score:
            result = True
        elif self._session.is_autonavigating_within_score:
            result = True
        return result

    def _exit_io_method_inside(self):
        if self._session.is_complete:
            return True
        elif self._session.is_backtracking_to_score_manager:
            return True
        elif self._session.is_backtracking_locally:
            self._session._is_backtracking_locally = False
            return True
        else:
            return False