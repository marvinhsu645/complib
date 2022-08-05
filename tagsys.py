'''
this is the implementation of tags with
Block, Component, as well as 
Ports as PortBlock and PortComp.
'''

import copy
import sympy


class Block:
    '''
    a block is a "mutable" (or "taggable") object.
    from a tagged block, you can find a list of candidate
    components that can implement it.
    Usually a block doesn't have ports until you start
    considering the connections. otherwise the candidate ports
    will be too many.
    '''
    allow_redefine = True  # allow portblocks name to be redefined
    silent_macro_udef = False  # if macro undefined, stay silent
    # added to support macro expansion for Components

    @property
    def macro_dict(self):
        return Component.macro_dict

    def __init__(self, name, tag=None, parent=None, design=None):
        self._name = name
        self._attr_dict = {}
        self._parent_block = parent
        self._parent_design = design
        if tag in Component.all_comp:
            # special case: we could tag a block as a component!
            # This way, it remains the only candidate.
            # this is a component name! the component
            # becomes the only candidate, and the tag set is
            # the same as that of the component.
            self._candidates = {Component.all_comp[tag]}
            self._tagset = copy.copy(Component.all_comp[tag]._tagset)
        else:
            self._tagset = set()  # empty set
            self._candidates = set(Component.all_comp.keys())
            if tag is not None:
                self << tag
        # this is not the most efficient way to do it, but
        # at least I think it is according to definition.
        self._all_portblocks = []  # all portblocks of this block
        # @@@ may need to initialize parent block and design.
        # should come back and add the code

    def lookup_macro(self, macrotag):
        if self.silent_macro_udef:
            # if not found, just return None
            return self.macro_dict.get(macrotag)
        else:
            # let the dict [ ] mechanism raise exception if key not
            # found in dict
            return self.macro_dict[macrotag]

    def __lshift__(self, tag):
        '''
        we use the << syntax for tagging self with RHS.
        however, if any of the candidate components
        in the current configuration cannot accept this
        tag, then it is no longer a candidate.
        it returns self so the tagging can be cascaded.
        Q: what happens if a tag is already in the _tagset?
        A: a more sophisticated model needs to handle
           multiplicity like a counting semaphore.
        '''
        # added macro preprocessing
        if tag[0] == '#':
            # macro, expand it
            for t in self.lookup_macro(tag[1:]):
                self << t
            return

        if tag[0] == '^':
            # exclusion, not yet implemented; future work
            raise ValueError('^ tag not implemented')

        if tag[:3] == '../':
            # go up to the containing block, create if not exist
            self.parent_block << tag[3:]
            return

        if tag[:2] == ':/':
            # go up to the containing design (which is
            # taggable)
            self.parent_design << tag[2:]
            return

        # note that here we pass attribute through, because
        # it is the candidate Component's job to determine if
        # its attribute is compatible with the @tag's.
        # end of macro preprocessing
        # now the regular tagging code

        for c in list(self.candidates):
            # the tag can include @attribute=value.
            # it's each component's responsibility to interpret
            # the attribute and check attribute compatibility.
            if not Component.all_comp[c].taggable(self._tagset, tag):
                # don't keep
                self._candidates.remove(c)
        # 2022/4/10 fixed bug -- need to add tagset.
        # if tag is attribute, save separately
        if tag[0] == '@':
            key, val = tag[1:].split('=')
            self._attr_dict[key] = val
            # @@@ maybe if the key has already been defined, we
            # then append val to the dict's value's list?
            # for now we just overwrite if key already defined.
        else:
            # regular attributes to tagset.
            self._tagset.update({tag})
        return self

    def __str__(self):
        return self._name

    def __repr__(self):
        return __class__.__name__+f'({repr(name)})'

    def __hash__(self):
        return hash((self._name, id(self)))

    @property
    def candidates(self):
        '''
        returns the list of candidate components for this tagged
        block.
        '''
        return self._candidates

    @property
    def parent_block(self):
        '''
        returns this block's parent block.
        '''
        return self._parent_block

    @property
    def parent_design(self):
        '''
        returns the design that contains this block
        '''
        return self._parent_design

    @property
    def all_cand_cmp_ports(self):
        '''
        this returns the list of block's candidate
        components' PortComps. 
        Right now this is an inefficient implementation because
        it reconstructs a new one each time, but it could be
        cached and reconstructed only if the candidates changed.
        '''

        return [p for c in list(self.candidates)
                for p in c.all_portcomps]

    @property
    def all_portblocks(self):
        return self._all_portblocks

    def add_portblock(self, name=None, tagset=None):
        '''
        called to add a new portblock to this block.
        name can be empty (though we should still make a unique
        internal name for it... I haven't done so).
        this block is the container. make sure the name does not
        conflict with any name here.
        '''
        p = PortBlock(self, name, tagset)
        if name:
            if not self.allow_redefine and name in self.__dict__:
                raise NameError(f"port name '{name}' redefined")
            self.__dict__[name] = p
        # in either case, put it in list
        self._all_portblocks.append(p)
        return p


class PortBlock:
    '''
    a PortBlock is a Port on a Block, and such a Port is modeled
    as a special kind of Block in that it can also be tagged,
    but it maintains a reference to its containing block, and
    it also gets its candidates from the container's candidates
    rather than all components.
    End user probably should not call his constructor directly,
    but should call add_portblock() on the container block.
    '''

    def __init__(self, blk, name=None, tagset=None,
                 parent_portblock=None):
        '''
        the constructor is called with the portblock's name, the
        reference to the container block (blk).
        The name could be None, but if not None, then it should
        be unique in the container's space and addressable by
        the container.name
        We don't support initial tagging.
        '''
        self._blk = blk    # link to container
        self._name = name  # port name
        self._parent_portblock = parent_portblock
        self._candidates = copy.copy(blk.all_cand_cmp_ports)
        self._attr_dict = {}
        if tagset:
            # special case: if tagset is just a portcomp of the
            # same component, then copy all of its tags, and
            # make  it the only candidate.
            d = {p.name: p for p in self._candidates}
            if len(tagset) == 1 and len(blk._candidates) == 1 and \
                    (n := [*tagset][0]) in d:
                # make this the only candidate
                self._candidates = [p := d[n]]
                # copy the tagset from that port
                self._tagset = p._tagset
                # @@@ copy the component's attributes as well?
                return
            else:
                self._tagset = copy.copy(tagset)
        else:
            self._tagset = set()  # empty set
        for t in tagset:
            self << t

        # this is not the most efficient way to do it, but
        # at least I think it is according to definition.

    def __lshift__(self, tag):
        '''
        we use the << syntax for tagging self with RHS.
        This is like the block's tagging method, except the
        candidate "components" are not the global dict of
        components but the component's portcomp dict.
        Otherwise, if any of the portcomp
        in the current configuration cannot accept this
        tag, then it is no longer a candidate.
        it returns self so the tagging can be cascaded.
        Q: what happens if a tag is already in the _tagset?
           Do we ignore it? or is the sequence at work here?
        '''
        # added macro preprocessing
        if tag[0] == '#':
            # macro, expand it
            for t in self.lookup_macro(tag[1:]):
                self << t
            return

        if tag[0] == '^':
            # exclusion, not yet implemented; future work
            raise ValueError('^ tag not implemented')

        if tag[:3] == '../':
            # go up to the containing portblock, create if not exist
            self.parent_portblock << tag[3:]
            return

        if tag[:2] == ':/':
            # go up to the containing block (which is
            # taggable)
            self.block << tag[2:]
            return

        # Q: do we allow '::/' to signify design? or ':/:/'?

        # end of macro preprocessing
        # now the regular tagging code

        for p in list(self._candidates):
            if not p.taggable(self._tagset, tag):
                # don't keep
                self._candidates.remove(p)

        if tag[0] == '@':
            # attribute, parse it
            key, expr = tag[1:].split('=', 1)
            self._attr_dict[key] = value
        else:
            self._tagset.update({tag})
        return self

    def taggable(self, curr_tags, newtag):
        '''
        5/27/2022 - unclear if this method makes sense?
        probably should delete it.

        checks if a portblock that is already tagged with
        curr_tags can still be tagged with the newtag
        and still contain this component as a candidate.
        A subclass can override this method if it needs
        a stricter rule, such as mutual exclusion
        '''
        raise('should not call PortBlock.taggable')
        if not (curr_tags <= self._tagset):
            return False
        # bug fix 2022/04/10 parenthesization
        return (curr_tags | {newtag}) <= self._tagset

    @property
    def name(self):
        return self._name

    @property
    def block(self):
        return self._blk

    @property
    def parent_portblock(self):
        '''
        get this portblock's parent (containing port).
        maybe create one on demand if one does not exist?
        '''
        if self._parent_portblock is None:
            self._parent_portblock = self.block.add_portblock()
        return self._parent_portblock

    @property
    def tagset(self):
        return self._tagset

    @property
    def candidates(self):
        return self._candidates

    @property
    def candidate(self):
        '''
        this is a special case when we have just one candidate
        such as the case with implementation portblock
        '''
        if len(self._candidates) != 1:
            raise ValueError(f'portblock {self._name} candidates'
                             f'{list(map(str, self._candidates))} not singleton')
        return [*(self._candidates)][0]

    def __str__(self):
        return f'{self._blk._name}.{self._name}'

    __repr__ = __str__

    def __hash__(self):
        return hash((self._name, id(self)))


class Component:
    '''
    a component is a provider of tags and imposes rules on tags.
    a component is not taggable. Actually, each component is
    more like a definition ("class"), in terms of the tags.
    the all_comp class attribute saves the list of all
    instances.
    '''
    # this is the component universe for candidates;
    # could be set for different search paths...
    all_comp = {}
    allow_redefine = True  # allow component name to be redefined
    # this is for the package allowed for attribute expressions
    global_dict = {}.update(sympy.__dict__)
    # this is for macro expansion
    macro_dict = {'DC3V': ['DC', 'power', '@voltage=3']}

    def __init__(self, name, tagset, portdict={}, attrdict={}):
        '''
        define a new component (type) called name
        and is characterized by the given tagset.
        it makes a copy, registers the name mapping
        to this new component. raises an exception
        if the name is redefined.
        portdict is the dict of portcomp name: tagset.
        This is just the most straightforward implementation,
        but each portcomp could actually be more restrictive.
        we use this dict to systematically construct PortComps
        and add to.
        attrdict is a set of mappings to expressions so that
        they can be looked up and checked during @attr kind of
        tagging.
        '''
        if (not self.allow_redefine) and (name in self.all_comp):
            raise(f'Component({repr(name)}) redefined')
        self.all_comp[name] = self
        self._name = name
        # preprocess the tagset for macros and attributes
        self._attr_dict = copy.copy(attrdict)
        self._tagset = set()
        for t in tagset:
            self.process_tag(t)
        self._all_portcomps = []
        for portname, porttags in portdict.items():
            if portname in self.__dict__:
                raise NameError(f"portname '{portname} conflict")
            p = PortComp(portname, porttags, self)
            self.__dict__[portname] = p
            self._all_portcomps.append(p)

    def process_tag(self, tag):
        '''
        This is to preprocess one tag at a time,
        somewhat like << for blocks but
        only to expand macros and set attributes, 
        but not to subset candidates.
        '''
        if tag[0] == '#':
            # look up in macro_dict
            for t in Component.macro_dict[tag[1:]]:
                self.process_tag(t)
            return
        if tag[0] == '@':
            # for now, allow only @attr=expr
            attr, expr = tag[1:].split('=', 1)
            self._attr_dict[attr] = eval(expr,
                                         globals=global_dict, locals=self.attr_dict)
            return
        # otherwise, just an ordinary tag
        self._tagset.add(tag)

    def add_portcomp(self, portcomp):
        '''
        this adds a new PortComp to this Component.
        the name had better be unique
        '''
        if portcomp.name in self.__dict__:
            raise NameError(f"portname '{portname} conflict")
        self.__dict__[portname] = p
        self._all_portcomps.append(p)

    @property
    def all_portcomps(self):
        return self._all_portcomps

    def __hash__(self):
        '''
        define the hash so components (as immutable objects) can
        be put into sets.
        '''
        return hash((self._name, id(self)))

    def compatible(self, key, expr_str):
        '''
        this method evaluates the expr_str in the context
        of this component's attr_dict.
        Example: user tags '@cost<20', and the
        component defines {'cost': 5, ..}
           (ignore units for now), 
        then eval(tag[1:]) returns true.
        another Example: user tags
        '@voltage.is_superset(Interval(0, 3))'
        component defines {'voltage': Interval(0, 2.5))}
        then it evaluates to false.
        '''
        from sympy import Interval
        return eval(expr_str, globals=self.global_dict,
                    locals=self._attr_dict)

    def taggable(self, curr_tags, newtag):
        '''
        checks if a block that is already tagged with
        curr_tags can still be tagged with the newtag
        and still contain this component as a candidate.
        A subclass can override this method if it needs
        a stricter rule, such as mutual exclusion
        '''
        # need to catch attribute before regular tag
        if newtag[0] == '@':
            # attribute, parse it
            key, expression = newtag[1:].split('=', 1)
            # see if the particular attribute (identified by
            # key) has compatible value with that from the tag.
            return self.compatible(key, expression)
        if not (curr_tags <= self._tagset):
            return False
        # bug fix 2022/04/10 parenthesization
        return (curr_tags | {newtag}) <= self._tagset

    def __str__(self):
        return self._name

    def __repr__(self):
        return __class__.__name__ +\
            f'({repr(self._name)}, {repr(self._tagset)}, '\
            f'{repr(self._attr_dict)})'


class PortComp:
    '''
    a PortComp is a Port on a Component, and it itself is
    also modeled as a special kind of Component in that it can
    have its own set of tags to be matched by PortBlocks when
    tagged, and it maintains a reference to its containing
    component.
    '''

    def __init__(self, portname, porttags, comp):
        '''
        the constructor takes a portname, set of porttags, and a
        link to the container Component.
        '''
        self._name = portname
        self._tagset = porttags
        self._comp = comp

    def taggable(self, curr_tags, newtag):
        '''
        checks if a portblock that is already tagged with
        curr_tags can still be tagged with the newtag
        and still contain this portcomop as a candidate.
        A subclass can override this method if it needs
        a stricter rule, such as mutual exclusion
        '''
        # need to catch attribute before regular tag
        if newtag[0] == '@':
            # attribute, parse it
            key, expression = newtag[1:].split('=', 1)
            # see if the particular attribute (identified by
            # key) has compatible value with that from the tag.
            return self.compatible(key, expression)
        if not (curr_tags <= self._tagset):
            return False
        return (curr_tags | {newtag}) <= self._tagset

    @property
    def name(self):
        return self._name

    def __str__(self):
        return f'{self._comp._name}.{self._name}'


def base_test():
    # define our "component library"
    Component('c1', {'A', 'B', 'C', 'D'})
    Component('c2', {'A', 'C', 'D', 'E', 'F'})
    Component('c3', {'B', 'E', 'F', 'G'})
    Component('c4', {'B', 'C', 'D', 'F', 'G'})
    Component('c5', {'C', 'F', 'G', 'H'})
    # tag a block
    b = Block('b')
    print(b.candidates)
    for t in ['C', 'D', 'G']:
        b << t
        print(f'tag {t} => {b.candidates}')


def sensor_test():
    from sympy import Interval
    c1 = Component(name='c1', tagset={'BM'},
                   portdict={'pwr': {'#DC3V'}, 'stat': {'I2C'}},
                   attrdict={'voltage': Interval(0, 3)})
    c2 = Component('c2', {'Acc'},
                   {'aout': {'Analog', 'Output'}})
    c3 = Component('c3', {'MCU', 'CPU', 'SPI', 'I2C'},
                   {'usart': {'SPI', 'SPI.Master', 'I2C', 'I2C.Master'}})
    c4 = Component('c4', {'MCU', 'CPU', 'SPI', 'I2C', 'ADC'},
                   {'usart': {'SPI', 'SPI.Master', 'I2C', 'I2C.Master'},
                   'ain': {'Analog', 'Input'}})
    c5 = Component('c5', {'ADC', 'SPI'},
                   {'ain': {'Analog', 'Input'},
                    'dout': {'SPI', 'SPI.Slave'}})
    c6 = Component('c6', {'Acc', 'ADC', 'SPI', 'I2C'},
                   {'spi': {'SPI', 'SPI.Slave'},
                    'i2c': {'I2C', 'I2C.Slave'}})
    for c in [c1, c2, c3, c4, c5, c6]:
        print(repr(c))
    b1 = Block('b1')
    b2 = Block('b2')
    b3 = Block('b3')
    b1 << 'Acc'
    b2 << 'ADC'
    b3 << 'MCU'
    print(f'{b1.candidates}')
    print(f'{b2.candidates}')
    print(f'{b3.candidates}')
    # now we consider just one candidate from each block
    # as with example, c4 to c6
    # need to create a new block with designated candidate block
    i6 = Block('i6', 'c6')  # Implementation block with c6 as the
    # only candidate
    i4 = Block('i4', 'c4')
    # find pairwise intersection of portcomps
    print(f"i6 all cand's comp_ports = {list(map(str,i6.all_cand_cmp_ports))}")
    print(f"i4 all cand's comp_ports = {list(map(str,i4.all_cand_cmp_ports))}")
    print('port intersections:')
    import itertools
    for r, s in itertools.product(
            i6.all_cand_cmp_ports, i4.all_cand_cmp_ports):
        intags = (r._tagset & s._tagset)
        if intags:
            # pairs with nonempty intersections
            print(f"intags = {intags}")
            r = i6.add_portblock(None, intags)
            s = i4.add_portblock(None, intags)
            print(f'r candidates={list(map(str,r.candidates))}')
            print(f's candidates={list(map(str,s.candidates))}')


def macro_test():
    # @@@ 5/29/2022 work in progress, not yet done
    from sympy import Interval
    c1 = Component(name='MCP73832T', tagset={'charger', 'Li-ion'},
                   portdict={'pwr': {'#DC3V'}, 'stat': {'I2C'}},
                   attrdict={'input_voltage': Interval(3.75, 6),
                             'input_current': 500})  # mA


if __name__ == '__main__':
    # base_test()
    # now testing ports, assume allowing redefining
    sensor_test()
