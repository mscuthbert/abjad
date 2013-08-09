# -*- encoding: utf-8 -*-


def offset_happens_before_timespan_stops(timespan=None, offset=None, hold=False):
    r'''Make time relation indicating that `offset` happens before `timespan` stops:

    ::

        >>> z(timerelationtools.offset_happens_before_timespan_stops())
        timerelationtools.OffsetTimespanTimeRelation(
            timerelationtools.CompoundInequality([
                timerelationtools.SimpleInequality('offset < timespan.stop')
                ],
                logical_operator='and'
                )
            )

    Return time relation or boolean.
    '''
    from abjad.tools import timerelationtools

    time_relation = timerelationtools.OffsetTimespanTimeRelation(
        timerelationtools.CompoundInequality([
            'offset < timespan.stop',
            ]),
        timespan=timespan,
        offset=offset)

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
