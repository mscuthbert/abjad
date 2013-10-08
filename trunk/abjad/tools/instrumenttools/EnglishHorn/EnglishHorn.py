# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Oboe import Oboe


class EnglishHorn(Oboe):
    r'''Abjad model of the English horn:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.EnglishHorn()(staff)
        EnglishHorn()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { English horn }
            \set Staff.shortInstrumentName = \markup { Eng. hn. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The English horn targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Oboe.__init__(self, **kwargs)
        self._default_instrument_name = 'English horn'
        self._default_short_instrument_name = 'Eng. hn.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch('f')
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-8, 24)
