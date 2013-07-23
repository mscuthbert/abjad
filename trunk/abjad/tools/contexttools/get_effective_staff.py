from abjad.tools import componenttools


def get_effective_staff(component):
    '''.. versionadded:: 2.0

    Get effective staff of `component`:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> staff.name = 'First Staff'

    ::

        >>> f(staff)
        \context Staff = "First Staff" {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> for note in staff:
        ...     print note, contexttools.get_effective_staff(note)
        ...
        c'8 Staff-"First Staff"{4}
        d'8 Staff-"First Staff"{4}
        e'8 Staff-"First Staff"{4}
        f'8 Staff-"First Staff"{4}

    Return staff or none.
    '''
    from abjad.tools import contexttools
    from abjad.tools import stafftools

    staff_change_mark = component.get_effective_context_mark(
        contexttools.StaffChangeMark)

    if staff_change_mark is not None:
        return staff_change_mark.staff

    return component.select_parentage().get_first(stafftools.Staff)
