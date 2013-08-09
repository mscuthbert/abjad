# -*- encoding: utf-8 -*-


def chromatic_pitch_class_name_to_diatonic_pitch_class_name(chromatic_pitch_class_name):
    '''Change `chromatic_pitch_class_name` to diatonic pitch-class name:

    ::

        >>> pitchtools.chromatic_pitch_class_name_to_diatonic_pitch_class_name('cs')
        'c'

    Return string.
    '''

    return chromatic_pitch_class_name[0]
