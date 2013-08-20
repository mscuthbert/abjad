# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class InversionIndicator(AbjadObject):
    '''Indicator of the inversion of tertian chords: 5, 63, 64 and
    also 7, 65, 43, 42, etc. Also root position, first, second, third
    inversions, etc.

    Value object that can not be changed once initialized.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, arg=0):
        if isinstance(arg, (int, long)):
            number = arg
        elif isinstance(arg, str):
            number = self._inversion_name_to_inversion_number[arg]
        else:
            raise ValueError('can not initialize inversion indicator.')
        self._number = number

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.number == arg.number:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '{}({})'.format(self._class_name, self.name)

    ### PRIVATE PROPERTIES ###

    _inversion_name_to_inversion_number = {
        'root': 0, 
        'root position': 0,
        'first': 1, 
        'second': 2, 
        'third': 3, 
        'fourth': 4,
    }

    _inversion_number_to_inversion_name = {
        0: 'root position',
        1: 'first', 
        2: 'second', 
        3: 'third', 
        4: 'fourth',
    }

    _seventh_chord_inversion_to_figured_bass_string = {
        0: '7', 
        1: '6/5', 
        2: '4/3', 
        3: '4/2',
    }

    _triadic_inversion_to_figured_bass_string = {
        0: '', 
        1: '6', 
        2: '6/4',
    }

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        return self._inversion_number_to_inversion_name[self.number]

    @property
    def number(self):
        return self._number

    @property
    def title(self):
        name = self._inversion_number_to_inversion_name[self.number]
        if name == 'root position':
            return 'RootPosition'
        return '{}Inversion'.format(name.title())

    ### PUBLIC METHODS ###

    def extent_to_figured_bass_string(self, extent):
        if extent == 5:
            return self._triadic_inversion_to_figured_bass_string[self.number]
        elif extent == 7:
            return self._seventh_chord_inversion_to_figured_bass_string[
                self.number]
        else:
            raise NotImplementedError
