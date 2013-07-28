# TODO: Write tests #
def analyze_incomplete_tonal_function(expr, key_signature):
    '''.. versionadded:: 2.0

    Analyze tonal function of `expr` according to `key_signature`:

    ::

        >>> chord = Chord("<c' e'>4")
        >>> key_signature = contexttools.KeySignatureMark('g', 'major')
        >>> tonalanalysistools.analyze_incomplete_tonal_function(chord, key_signature)
        IVMajorTriadInRootPosition

    Return tonal function.
    '''
    from abjad.tools import tonalanalysistools

    if isinstance(expr, tonalanalysistools.ChordClass):
        chord_class = expr
    else:
        chord_class = tonalanalysistools.analyze_incomplete_chord(expr)
    root = chord_class.root
    scale = tonalanalysistools.Scale(key_signature)
    scale_degree = scale.named_chromatic_pitch_class_to_scale_degree(root)
    quality = chord_class.quality_indicator.quality_string
    extent = chord_class.extent
    inversion = chord_class.inversion
    tonal_function = tonalanalysistools.TonalFunction(scale_degree, quality, extent, inversion)

    return tonal_function
