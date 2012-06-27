from abjad.cfg.cfg import ABJADPATH, EXPERIMENTALPATH, ROOTPATH
from abjad.tools import iotools
from experimental.developerscripttools.DirectoryScript import DirectoryScript
from experimental.developerscripttools.CleanScript import CleanScript
import argparse
import os


class AbjGrepScript(DirectoryScript):

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def alias(self):
        return 'grep'

    @property
    def long_description(self):
        return '''\
If no PATH flag is specified, the current directory will be searched.
    '''

    @property
    def scripting_group(self):
        return None

    @property
    def short_description(self):
        return 'grep PATTERN in PATH'

    @property
    def version(self):
        return 1.0

    ### PUBLIC METHODS ###

    def process_args(self, args):

        iotools.clear_terminal()
        if args.whole_words_only:
            whole_words_only = '-w'
        else:
            whole_words_only = ''
        command = r'grep {} -Irn {!r} {} | grep -v svn-base | grep -v svn\/ | grep -v docs'.format(
            whole_words_only, args.pattern, os.path.relpath(args.path))
        iotools.spawn_subprocess(command)

    def setup_argument_parser(self, parser):

        parser.add_argument('pattern',
            help='pattern to search for'
            )

        parser.add_argument('-W', '--whole-words-only',
            action='store_true',
            help='''match only whole words, similar to grep's "-w" flag''',
            )

        group = parser.add_mutually_exclusive_group()

        group.add_argument('-P', '--path',
            dest='path',
            help='grep PATH',
            type=self._validate_path,
            )

        group.add_argument('-E', '--experimental',
            action='store_const',
            const=EXPERIMENTALPATH,
            dest='path',
            help='grep Abjad experimental directory',
            )

        group.add_argument('-M', '--mainline',
            action='store_const',
            const=ABJADPATH,
            dest='path',
            help='grep Abjad mainline directory',
            )

        group.add_argument('-T', '--tools',
            action='store_const',
            const=os.path.join(ABJADPATH, 'tools'),
            dest='path',
            help='grep Abjad mainline tools directory',
            )

        group.add_argument('-R', '--root',
            action='store_const',
            const=ROOTPATH,
            dest='path',
            help='grep Abjad root directory',
            )

        parser.set_defaults(path=os.path.abspath(os.path.curdir))
