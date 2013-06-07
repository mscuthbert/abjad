from abjad.tools.abctools import AbjadObject


class CodeBlock(AbjadObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_exceptions',
        '_displayed_lines',
        '_executed_lines',
        '_hide',
        '_processed_results',
        '_strip_prompt',
        )

    ### INITIALIZER ###

    def __init__(self,
        displayed_lines,
        allow_exceptions=False,
        executed_lines=None,
        hide=False,
        strip_prompt=False,
        ):
        self._allow_exception = bool(allow_exceptions)
        self._displayed_lines = tuple(displayed_lines)
        self._executed_lines = None
        if executed_lines is not None:
            self._executed_lines = tuple(executed_lines)
        self._hide = bool(hide)
        self._processed_results = []
        self._strip_prompt = bool(strip_prompt)

    ### SPECIAL METHODS ###

    def __call__(self, console):
        self.processed_results.extend(self.execute(console))

    ### PUBLIC METHODS ###

    def execute(self, console):
        from experimental.tools import newabjadbooktools

        results = []
        is_incomplete_statement = False
        result = '>>> '
        lines = self.executed_lines or self.displayed_lines

        for line in lines:

            result += line + '\n'
            first, sep, rest = line.partition('(')
            with contextlib.closing(StringIO.StringIO()) as stream:
                with iotools.RedirectedStreams(stream, stream):
                    output_method = first.strip()
                    if output_method in self.output_triggers:

                        if ',' in rest:
                            object_reference = rest.rpartition(',')[0].strip()
                        else:
                            object_reference = rest.rpartition(')')[0].strip()
                        if object_reference not in console.locals:
                            # Simulate a bad reference, 
                            # and cause a captured Exception.
                            console.push(line)
                        else:
                            # Otherwise, it's OK: just grab out of locals 
                            output_proxy = newabjadbooktools.OutputProxy(
                                copy.deepcopy(console.locals[object_reference]),
                                self.output_triggers[output_method],
                                )
                            results.append(result)
                            results.append(output_proxy)
                        is_incomplete_statement = False
                    else:
                        is_incomplete_statement = console.push(line)
                    output = stream.getvalue()
                    if output:
                        result += output
                if not is_complete_statement:
                    result += '>>> '
                else:
                    result += '... '

        # Simulate a final carriage return to break any incomplete indents
        with contextlib.closing(StringIO.StringIO()) as stream:
            with iotools.RedirectedStreams(stream, stream):
                console.push('')
                output = stream.getvalue()
                if output:
                    result += output
        while result.endswith('\n>>> '):
            result = result[:-5]
         
        results.append(result)

        if self.executed_lines:
            results = ['\n'.join(self.displayed_results)]

        if self.hide:
            for x in reversed(results):
                if isinstance(x, str):
                    results.remove(x)

        if self.strip_prompt:
            for i, x in enumerate(results):
                if instance(x, str):
                    lines = x.splitlines()
                    for j, line in enumerate(lines):
                        if line.startswith(('>>> ', '... ')):
                            lines[j] = line[4:]
                    results[i] = '\n'.join(lines) 

        return results

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def allow_exceptions(self):
        return self._allow_exceptions

    @property
    def displayed_oines(self):
        return self._displayed_lines

    @property
    def executed_lines(self):
        return self._executed_lines

    @property
    def hide(self):
        return self._hide

    @property
    def output_triggers(self):
        return {
            'iotools.graph': 'graphviz',
            'iotools.play': 'midi',
            'iotools.plot': 'gnuplot',
            'iotools.show': 'lilypond',
            'play': 'midi',
            'show': 'lilypond',
        }

    @property
    def processed_results(self):
        return self._processed_results

    @property
    def strip_prompt(self):
        return self._strip_prompt


