# -*- encoding: utf-8 -*-


def set_default_accidental_spelling(spelling='mixed'):
    '''Set default accidental spelling to sharps:

    ::

        >>> pitchtools.set_default_accidental_spelling('sharps')

    ::

        >>> [Note(13, (1, 4)), Note(15, (1, 4))]
        [Note("cs''4"), Note("ds''4")]

    Set default accidental spelling to flats:

    ::

        >>> pitchtools.set_default_accidental_spelling('flats')

    ::

        >>> [Note(13, (1, 4)), Note(15, (1, 4))]
        [Note("df''4"), Note("ef''4")]

    Set default accidental spelling to mixed:

    ::

        >>> pitchtools.set_default_accidental_spelling()

    ::

        >>> [Note(13, (1, 4)), Note(15, (1, 4))]
        [Note("cs''4"), Note("ef''4")]

    Mixed is system default.

    Mixed test case must appear last here for doc tests to check correctly.

    Return none.
    '''
    from abjad import abjad_configuration

    if spelling not in ('mixed', 'sharps', 'flats'):
        raise ValueError

    abjad_configuration['accidental_spelling'] = spelling
