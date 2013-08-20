# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.pitchtools.NamedInterval import NamedInterval


class NamedHarmonicInterval(NamedInterval):
    '''Abjad model harmonic diatonic interval:

    ::

        >>> pitchtools.NamedHarmonicInterval('M9')
        NamedHarmonicInterval('M9')

    Harmonic diatonic intervals are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools.pitchtools.is_harmonic_diatonic_interval_abbreviation \
            import harmonic_diatonic_interval_abbreviation_regex
        if len(args) == 1 and isinstance(args[0], NamedInterval):
            _quality_string = args[0].quality_string
            _number = abs(args[0].number)
        elif len(args) == 1 and isinstance(args[0], str):
            match = \
                harmonic_diatonic_interval_abbreviation_regex.match(args[0])
            if match is None:
                message = '"%s" does not have the form of an hdi abbreviation.'
                raise ValueError(message % args[0])
            quality_abbreviation, number_string = match.groups()
            _quality_string = \
                NamedInterval._quality_abbreviation_to_quality_string[
                    quality_abbreviation]
            _number = int(number_string)
        elif len(args) == 2:
            _quality_string = args[0]
            _number = abs(args[1])
        self._quality_string = _quality_string
        self._number = _number

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)(self)

    # TODO: remove?
    __deepcopy__ = __copy__

    def __ge__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError
        if self.number == arg.number:
            return self.semitones >= arg.semitones
        return self.number >= arg.number

    def __gt__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError
        if self.number == arg.number:
            return self.semitones > arg.semitones
        return self.number > arg.number

    def __le__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError
        if self.number == arg.number:
            return self.semitones <= arg.semitones
        return self.number <= arg.number

    def __lt__(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError
        if self.number == arg.number:
            return self.semitones < arg.semitones
        return self.number < arg.number

    def __repr__(self):
        return "%s('%s')" % (self._class_name, str(self))

    def __str__(self):
        return '%s%s' % (self._quality_abbreviation, self.number)

    ### PUBLIC METHODS ###

    @classmethod
    def from_pitch_carriers(cls, pitch_carrier_1, pitch_carrier_2):
        '''Calculate harmonic diatonic interval from `pitch_carrier_1` to
        `pitch_carrier_2`:

        ::

            >>> pitchtools.NamedHarmonicInterval.from_pitch_carriers(
            ...     pitchtools.NamedPitch(-2), 
            ...     pitchtools.NamedPitch(12),
            ...     )
            NamedHarmonicInterval('M9')

        Return harmonic diatonic interval.
        '''
        from abjad.tools import pitchtools
        # get melodic diatonic interval
        mdi = pitchtools.NamedMelodicInterval.from_pitch_carriers(
            pitch_carrier_1, pitch_carrier_2)
        # return harmonic diatonic interval
        return mdi.harmonic_diatonic_interval

    ### PUBLIC PROPERTIES ###

    @property
    def harmonic_diatonic_interval_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedHarmonicIntervalClass(self)

    @property
    def melodic_diatonic_interval_ascending(self):
        from abjad.tools.pitchtools.NamedMelodicInterval \
            import NamedMelodicInterval
        return NamedMelodicInterval(self.quality_string, self.number)

    @property
    def melodic_diatonic_interval_descending(self):
        return -self.melodic_diatonic_interval_ascending

    # TODO: this can be abstracted higher up the inheritence hierarchy
    @property
    def semitones(self):
        result = 0
        interval_class_number_to_semitones = {
            1: 0,  2: 1,  3: 3, 4: 5, 5: 7, 6: 8, 7: 10, 8:0}
        try:
            interval_class_number = abs(
                self.harmonic_diatonic_interval_class.number)
        except AttributeError:
            interval_class_number = self.number
        result += interval_class_number_to_semitones[interval_class_number]
        result += (abs(self.number) - 1) / 7 * 12
        quality_string_to_semitones = {
            'perfect': 0, 
            'major': 1, 
            'minor': 0, 
            'augmented': 1, 
            'diminished': -1,
            }
        result += quality_string_to_semitones[self.quality_string]
        if self.number < 0:
            result *= -1
        return result

    @property
    def staff_spaces(self):
        if self.quality_string == 'perfect' and self.number == 1:
            return 0
        return abs(NamedInterval.staff_spaces.fget(self))
