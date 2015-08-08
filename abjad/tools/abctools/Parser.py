# -*- encoding: utf-8 -*-
import abc
import logging
import os
import pickle
import ply
from abjad.tools.abctools.AbjadObject import AbjadObject


class Parser(AbjadObject):
    r'''Abstract base class for Abjad parsers.

    Rules objects for lexing and parsing must be defined by overriding the
    abstract properties `lexer_rules_object` and `parser_rules_object`.

    For most parsers these properties should simply return `self`.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_debug',
        '_lexer',
        '_logger',
        '_parser',
        )

    ### INITIALIZER ###

    def __init__(self, debug=False):

        self._debug = bool(debug)
        self._lexer = None
        self._parser = None

        if self.debug:
            logging.basicConfig(
                level=logging.DEBUG,
                filename=self.logger_path,
                filemode='w',
                format='%(filename)10s:%(lineno)8d:%(message)s'
                )
            self._logger = logging.getLogger()
        else:
            self._logger = logging.getLogger()
            self._logger.addHandler(logging.NullHandler())

        self._lexer = ply.lex.lex(
            debug=self.debug,
            debuglog=self.logger,
            object=self.lexer_rules_object
            )

        if not os.path.exists(self.pickle_path):
            directory_path, _ = os.path.split(self.pickle_path)
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            string = pickle.dumps(None)
            with open(self.pickle_path, 'wb') as file_pointer:
                file_pointer.write(string)

        self._parser = ply.yacc.yacc(
            debug=self.debug,
            debuglog=self.logger,
            module=self.parser_rules_object,
            outputdir=self.output_path,
            picklefile=self.pickle_path,
            )

    ### SPECIAL METHODS ###

    def __call__(self, input_string):
        r'''Parse `input_string` and return result.
        '''

        if hasattr(self, '_setup'):
            self._setup()

        if self.debug:
            result = self.parser.parse_debug(
                input_string,
                lexer=self.lexer,
                debug=self.logger)
        else:
            result = self.parser.parse(
                input_string,
                lexer=self.lexer)

        if hasattr(self, '_cleanup'):
            result = self._cleanup(result)

        return result

    ### PUBLIC PROPERTIES ###

    @property
    def debug(self):
        r'''True if the parser runs in debugging mode.
        '''
        return self._debug

    @property
    def lexer(self):
        r'''The parser's PLY Lexer instance.
        '''
        return self._lexer

    @abc.abstractproperty
    def lexer_rules_object(self):
        r'''The object containing the parser's lexical rule definitions.
        '''
        raise NotImplementedError

    @property
    def logger(self):
        r'''The parser's Logger instance.
        '''
        return self._logger

    @property
    def logger_path(self):
        r'''The output path for the parser's logfile.
        '''
        import sys
        file_name = 'parselog_{}_{}.txt'.format(
            type(self).__name__,
            '-'.join(str(x) for x in sys.version_info),
            )
        return os.path.join(self.output_path, file_name)

    @property
    def output_path(self):
        r'''The output path for files associated with the parser.
        '''
        from abjad import abjad_configuration
        abjad_configuration_directory = \
            abjad_configuration.abjad_configuration_directory
        output_path = os.path.join(
            abjad_configuration_directory,
            'parsers',
            )
        if not os.path.isdir(output_path):
            os.makedirs(output_path)
        return output_path

    @property
    def parser(self):
        r'''The parser's PLY LRParser instance.
        '''
        return self._parser

    @abc.abstractproperty
    def parser_rules_object(self):
        r'''The object containing the parser's syntactical rule definitions.
        '''
        raise NotImplementedError

    @property
    def pickle_path(self):
        r'''The output path for the parser's pickled parsing tables.
        '''
        import sys
        file_name = 'parse_tables_{}_{}.pkl'.format(
            type(self).__name__,
            '-'.join(str(x) for x in sys.version_info),
            )
        return os.path.join(self.output_path, file_name)

    ### PUBLIC METHODS ###

    def tokenize(self, input_string):
        r'''Tokenize `input string` and print results.
        '''
        self.lexer.input(input_string)
        for token in self.lexer:
            print(token)