from abjad.tools.lilypondfiletools._AttributedBlock import _AttributedBlock


class LayoutBlock(_AttributedBlock):
    r'''.. versionadded:: 2.0

    Abjad model of LilyPond input file layout block::

        abjad> layout_block = lilypondfiletools.LayoutBlock()

    ::

        abjad> layout_block
        LayoutBlock()

    ::

        abjad> layout_block.indent = 0
        abjad> layout_block.ragged_right = True

    ::

        abjad> f(layout_block)
        \layout {
            indent = #0
            ragged-right = ##t
        }

    Return layout block.
    '''

    def __init__(self):
        _AttributedBlock.__init__(self)
        self._escaped_name = r'\layout'
        self._contexts = []

    # PRIVATE ATTRIUBTES #

    @property
    def _formatted_context_specifications(self):
        result = []
        for context_specification in self.contexts:
            result.append(r'\context {')
            for x in context_specification:
                result.append('\t' + str(x))
            result.append('}')
        return result

    ### PUBLIC ATTRIBUTES ###

    @property
    def contexts(self):
        return self._contexts
