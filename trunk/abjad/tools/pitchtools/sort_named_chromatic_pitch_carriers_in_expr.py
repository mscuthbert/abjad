# -*- encoding: utf-8 -*-


def sort_named_chromatic_pitch_carriers_in_expr(pitch_carriers):
    '''List named chromatic pitch carriers in `expr` sorted by 
    numbered chromatic pitch-class:

    ::

        >>> notes = notetools.make_notes([9, 11, 12, 14, 16], (1, 4))

    ::

        >>> pitchtools.sort_named_chromatic_pitch_carriers_in_expr(notes)
        [Note("c''4"), Note("d''4"), Note("e''4"), Note("a'4"), Note("b'4")]

    The elements in `pitch_carriers` are not changed in any way.

    Return list.
    '''
    from abjad.tools import pitchtools

    result = list(pitch_carriers[:])
    tmp = pitchtools.list_named_chromatic_pitches_in_expr
    result.sort(key=lambda x: abs(tmp(x)[0].numbered_chromatic_pitch_class))

    return result
