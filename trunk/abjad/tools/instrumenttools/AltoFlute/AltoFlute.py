# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Flute import Flute


class AltoFlute(Flute):
    r'''Abjad model of the alto flute:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.AltoFlute()(staff)
        AltoFlute()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Alto flute }
            \set Staff.shortInstrumentName = \markup { Alt. fl. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The alto flute targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Flute.__init__(self, **kwargs)
        self._default_instrument_name = 'alto flute'
        self._default_short_instrument_name = 'alt. fl.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("g")
        self._default_pitch_range = pitchtools.PitchRange(-5, 31)
