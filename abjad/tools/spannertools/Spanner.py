# -*-encoding: utf-8 -*-
import abc
import copy
from abjad.tools import durationtools
from abjad.tools import lilypondproxytools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import timespantools
from abjad.tools.abctools import AbjadObject
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import setting
Selection = selectiontools.Selection


class Spanner(AbjadObject):
    '''Any type of notation object that stretches horizontally
    and encompasses some number of notes, rest, chords, tuplets,
    measures, voices or other Abjad components.

    Beams, slurs, hairpins, trills, glissandi and piano pedal brackets
    all stretch horizontally on the page to encompass multiple notes
    and all implement as Abjad spanners.
    That is, these spanner all have an obvious graphic reality with
    definite start-, stop- and midpoints.

    Abjad also implements a number of spanners of a different type,
    such as tempo and instrument spanners, which mark a group of notes,
    rests, chords or measues as carrying a certain tempo or being
    played by a certain instrument.

    The spanner class described here
    abstracts the functionality that all such spanners, both graphic
    and nongraphics, share.
    This shared functionality includes methods to add, remove, inspect
    and test components governed by the spanner, as well as basic
    formatting properties.
    The other spanner classes, such as beam and glissando, all inherit from
    this class and receive the functionality implemented here.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, components=None, overrides=None):
        overrides = overrides or {}
        self._components = []
        self._contiguity_constraint = 'logical voice'
        self._initialize_components(components)
        self._apply_overrides(overrides)

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        r'''True when spanner contains `expr`.
        Otherwise false.

        Returns boolean.
        '''
        for x in self._components:
            if x is expr:
                return True
        else:
            return False

    def __copy__(self, *args):
        r'''Copies spanner.

        Does not copy spanner components.

        Returns new spanner.
        '''
        new = type(self)(*self.__getnewargs__())
        if getattr(self, '_override', None) is not None:
            new._override = copy.copy(override(self))
        if getattr(self, '_set', None) is not None:
            new._set = copy.copy(setting(self))
        self._copy_keyword_args(new)
        return new

    def __getitem__(self, expr):
        r'''Gets item from spanner.

        Returns component.
        '''
        return self._components.__getitem__(expr)

    def __getnewargs__(self):
        r'''Gets new arguments.

        Returns empty tuple.
        '''
        return ()

    def __len__(self):
        r'''Length of spanner.

        Returns nonnegative integer.
        '''
        return self._components.__len__()

    def __lt__(self, expr):
        r'''True when spanner is less than `expr`.

        Trivial comparison to allow doctests to work.

        Returns boolean.
        '''
        if not isinstance(expr, Spanner):
            raise TypeError
        return repr(self) < repr(expr)

    def __repr__(self):
        r'''Interpreter representation of spanner.

        Returns string.
        '''
        return '{}({})'.format(type(self).__name__, self._compact_summary)

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_summary(self):
        len_self = len(self)
        if not len_self:
            return ''
        elif 0 < len_self <= 8:
            return ', '.join([x._compact_representation for x in self])
        else:
            left = ', '.join([x._compact_representation for x in self[:2]])
            right = ', '.join([x._compact_representation for x in self[-2:]])
            number_in_middle = len_self - 4
            middle = ', ... [%s] ..., ' % number_in_middle
            return left + middle + right

    @property
    def _duration_in_seconds(self):
        duration = durationtools.Duration(0)
        for leaf in self.leaves:
            duration += leaf._get_duration(in_seconds=True)
        return duration

    @property
    def _preprolated_duration(self):
        return sum([component._preprolated_duration for component in self])

    @property
    def _summary(self):
        if 0 < len(self):
            return ', '.join([str(x) for x in self])
        else:
            return ' '

    ### PRIVATE METHODS ###

    def _apply_overrides(self, overrides):
        exec('from abjad import *')
        for grob_attribute_string in overrides:
            grob_value_string = overrides[grob_attribute_string]
            statement = 'override(self).{} = {}'
            grob_attribute_string = grob_attribute_string.replace('__', '.', 1)
            grob_value_string = grob_value_string.replace('\t', '')
            strings = (grob_attribute_string, grob_value_string)
            statement = statement.format(*strings)
            exec(statement)

    def _block_all_components(self):
        r'''Not composer-safe.
        '''
        for component in self:
            self._block_component(component)

    def _block_component(self, component):
        r'''Not composer-safe.
        '''
        component._spanners.remove(self)

    def _copy(self, components):
        r'''Returns copy of spanner with `components`.
        `components` must be an iterable of components already
        contained in spanner.
        '''
        my_components = self._components[:]
        self._components = []
        result = copy.copy(self)
        self._components = my_components
        for component in components:
            assert component in self
        for component in components:
            result._components.append(component)
        result._unblock_all_components()
        return result

    @abc.abstractmethod
    def _copy_keyword_args(self, new):
        raise NotImplemented

    def _duration_offset_in_me(self, leaf):
        leaf_start_offset = leaf._get_timespan().start_offset
        self_start_offset = self.get_timespan().start_offset
        return leaf_start_offset - self_start_offset

    def _format_after_leaf(self, leaf):
        result = []
        if self._is_my_last_leaf(leaf):
            result.extend(getattr(self, '_reverts', []))
        return result

    def _format_before_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.extend(getattr(self, '_overrides', []))
        return result

    def _format_right_of_leaf(self, leaf):
        result = []
        return result

    def _fracture_left(self, i):
        left = self._copy(self[:i])
        right = self._copy(self[i:])
        self._block_all_components()
        return self, left, right

    def _fracture_right(self, i):
        left = self._copy(self[:i+1])
        right = self._copy(self[i+1:])
        self._block_all_components()
        return self, left, right

    def _fuse_by_reference(self, spanner):
        result = self._copy(self[:])
        result.extend(spanner.components)
        self._block_all_components()
        spanner._block_all_components()
        return [(self, spanner, result)]

    def _get_my_first_leaf(self):
        for leaf in iterate(self).by_class(scoretools.Leaf):
            return leaf

    def _get_my_last_leaf(self):
        for leaf in iterate(self).by_class(scoretools.Leaf, reverse=True):
            return leaf

    def _get_my_nth_leaf(self, n):
        from abjad.tools import scoretools
        if not isinstance(n, (int, long)):
            raise TypeError
        if 0 <= n:
            leaves = iterate(self).by_class(scoretools.Leaf)
            for leaf_index, leaf in enumerate(leaves):
                if leaf_index == n:
                    return leaf
        else:
            leaves = iterate(self).by_class(scoretools.Leaf, reverse=True)
            for leaf_index, leaf in enumerate(leaves):
                leaf_number = -leaf_index - 1
                if leaf_number == n:
                    return leaf
        raise IndexError

    def _initialize_components(self, components):
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import iterate
        if components:
            raise Exception('deprecated')
        if isinstance(components, scoretools.Component):
            components = [components]
        elif not components:
            components = []
        assert not any(
            isinstance(x, scoretools.Context)
            for x in components), repr(components)
        if self._contiguity_constraint == 'logical voice':
            leaves = list(iterate(components).by_class(scoretools.Leaf))
            assert Selection._all_are_contiguous_components_in_same_logical_voice(leaves)
        self.extend(components)

    def _insert(self, i, component):
        r'''Not composer-safe.
        '''
        component._spanners.add(self)
        self._components.insert(i, component)

    def _is_exterior_leaf(self, leaf):
        r'''True if leaf is first or last in spanner.
        True if next leaf or previous leaf is none.
        False otherwise.
        '''
        if self._is_my_first_leaf(leaf):
            return True
        elif self._is_my_last_leaf(leaf):
            return True
        elif not leaf._get_leaf(-1) and not leaf._get_leaf(1):
            return True
        else:
            return False

    def _is_my_first(self, leaf, component_classes):
        for component in iterate(self).by_class(component_classes):
            if component is leaf:
                return True
            else:
                return False

    def _is_my_first_leaf(self, leaf):
        try:
            first_leaf = self._get_my_nth_leaf(0)
            return leaf is first_leaf
        except IndexError:
            return False

    def _is_my_last(self, leaf, component_classes):
        for component in iterate(self).by_class(
            component_classes,
            reverse=True,
            ):
            if component is leaf:
                return True
            else:
                return False

    def _is_my_last_leaf(self, leaf):
        try:
            last_leaf = self._get_my_nth_leaf(-1)
            return leaf is last_leaf
        except IndexError:
            return False

    def _is_my_only(self, leaf, component_classes):
        i = None
        components = iterate(self).by_class(component_classes)
        for i, component in enumerate(components):
            if 0 < i:
                return False
        return i == 0

    def _is_my_only_leaf(self, leaf):
        return self._is_my_first_leaf(leaf) and self._is_my_last_leaf(leaf)

    def _make_storage_format_with_overrides(self):
        override_dictionary = override(self)._make_override_dictionary()
        lines = []
        line = '{}.{}('.format(
            self._tools_package_name,
            type(self).__name__,
            )
        lines.append(line)
        lines.append('\toverrides = {')
        for key, value in override_dictionary.iteritems():
            value = value.replace('\t', '')
            line = '\t\t{!r}: {!r},'.format(key, value)
            lines.append(line)
        lines.append('\t}')
        lines.append(')')
        result = '\n'.join(lines)
        return result

    def _remove(self, component):
        r'''Not composer-safe.
        '''
        self._sever_component(component)

    def _remove_component(self, component):
        r'''Not composer-safe.
        '''
        for i, x in enumerate(self._components):
            if x is component:
                self._components.pop(i)
                break
        else:
            message = 'component {!r} not in spanner components list.'
            raise ValueError(message.format(component))

    def _reverse_components(self):
        r'''Reverses order of spanner components.

        Not composer-safe because reversing the order of spanner components
        could scramble components of some other spanner.

        Call method only as part of a full component- and spanner-reversal
        routine.

        Spanner subclasses with mapping variables (like the 'durations' list
        attaching to durated complex beam spanners) should override this
        method to reverse mapping elements.
        '''
        self._components.reverse()

    def _sever_all_components(self):
        r'''Not composer-safe.
        '''
        for n in reversed(range(len(self))):
            component = self[n]
            self._sever_component(component)

    def _sever_component(self, component):
        r'''Not composer-safe.
        '''
        self._block_component(component)
        self._remove_component(component)

    def _unblock_all_components(self):
        r'''Not composer-safe.
        '''
        for component in self:
            self._unblock_component(component)

    def _unblock_component(self, component):
        r'''Not composer-safe.
        '''
        component._spanners.add(self)

    ### PUBLIC PROPERTIES ###

    @property
    def components(self):
        r'''Components in spanner.

        Returns tuple.
        '''
        return tuple(self._components[:])

    @property
    def leaves(self):
        r'''Leaves in spanner.

        Returns tuple.
        '''
        from abjad.tools import iterationtools
        result = []
        for component in self._components:
            # EXPERIMENTAL: expand to allow staff-level spanner eventually
            for node in \
                iterationtools.iterate_components_depth_first(component):
                if isinstance(node, scoretools.Leaf):
                    result.append(node)
        result = tuple(result)
        return result

    ### PUBLIC METHODS ###

    def append(self, component):
        r'''Appends `component` to spanner.

        Returns none.
        '''
        if self._contiguity_constraint == 'logical voice':
            components = self[-1:] + [component]
            assert Selection._all_are_contiguous_components_in_same_logical_voice(
                components), repr(components)
        component._spanners.add(self)
        self._components.append(component)

    def append_left(self, component):
        r'''Appends `component` to left of spanner.

        Returns none.
        '''
        components = [component] + self[:1]
        assert Selection._all_are_contiguous_components_in_same_logical_voice(
            components)
        component._spanners.add(self)
        self._components.insert(0, component)

    def _attach(self, components):
        r'''Attaches spanner to `components`.

        Spanner must be empty.

        Returns none.
        '''
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        assert not self, repr(self)
        if isinstance(components, scoretools.Component):
            self.append(components)
        elif isinstance(components, (list, tuple, selectiontools.Selection)):
            self.extend(components)
        else:
            raise TypeError(components)

    def detach(self):
        r'''Detaches spanner.

        Returns none.
        '''
        self._sever_all_components()

    def extend(self, components):
        r'''Extends spanner with `components`.

        Returns none.
        '''
        component_input = self[-1:]
        component_input.extend(components)
        if self._contiguity_constraint == 'logical voice':
            assert Selection._all_are_contiguous_components_in_same_logical_voice(
                component_input), repr(component_input)
        for component in components:
            self.append(component)

    def extend_left(self, components):
        r'''Extends left of spanner with `components`.

        Returns none.
        '''
        component_input = components + self[:1]
        assert Selection._all_are_contiguous_components_in_same_logical_voice(
            component_input)
        for component in reversed(components):
            self.append_left(component)

    def fracture(self, i, direction=None):
        r'''Fractures spanner at `direction` of component at index `i`.

        Valid values for `direction` are ``Left``, ``Right`` and ``None``.

        Set `direction=None` to fracture on both left and right sides.

        Returns tuple of original, left and right spanners.
        '''
        if i < 0:
            i = len(self) + i
        if direction == Left:
            return self._fracture_left(i)
        elif direction == Right:
            return self._fracture_right(i)
        elif direction is None:
            left = self._copy(self[:i])
            right = self._copy(self[i+1:])
            center = self._copy(self[i:i+1])
            self._block_all_components()
            return self, left, center, right
        else:
            message = 'direction {!r} must be Left, Right or None.'
            raise ValueError(message.format(direction))

    def fuse(self, spanner):
        r'''Fuses spanner with contiguous `spanner`.

        Returns list of left, right and new spanners.
        '''
        return self._fuse_by_reference(spanner)

    def get_duration(self, in_seconds=False):
        r'''Gets duration of spanner.

        Returns duration.
        '''
        return sum(
            component._get_duration(in_seconds=in_seconds)
            for component in self
            )

    def get_timespan(self, in_seconds=False):
        r'''Gets timespan of spanner.

        Returns timespan.
        '''
        if len(self):
            start_offset = \
                self[0]._get_timespan(in_seconds=in_seconds).start_offset
        else:
            start_offset = Duration(0)
        if len(self):
            stop_offset = \
                self[-1]._get_timespan(in_seconds=in_seconds).stop_offset
        else:
            stop_offset = Duration(0)
        return timespantools.Timespan(
            start_offset=start_offset, stop_offset=stop_offset)

    def index(self, component):
        r'''Returns index of `component` in spanner.

        Returns nonnegative integer.
        '''
        for i, x in enumerate(self._components):
            if x is component:
                return i
        else:
            raise IndexError

    def pop(self):
        r'''Pops rightmost component off of spanner.

        Returns component.
        '''
        component = self[-1]
        self._sever_component(component)
        return component

    def pop_left(self):
        r'''Pops leftmost component off of spanner.

        Returns component.
        '''
        component = self[0]
        self._sever_component(component)
        return component