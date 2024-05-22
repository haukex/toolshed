from typing import NamedTuple

#: This is just an example constant.
CONSTANT = True

class Bar:
    """This is an example class.

    It has an attribute :attr:`foo`.

    .. note:: This is how to make a note

    .. py:attribute:: foo
        :type: str

        I'm not sure why Sphix isn't autodetecting the type of the attribute.
    """
    def __init__(self, foo :str):
        self.foo :str = foo

class Foo(NamedTuple):
    #: This will document the following element
    bar :str
    def hello(self, blah :int) -> int:
        """Just a test.

        Verbatim blocks are indented and introduced by a double colon. ::

            This is a verbatim block. It can also be introduced with just a
            double colon in a paragraph by itself, which will be removed. If
            the double colon is preceded by non-whitespace, it becomes a
            single colon.

        How to reference various things, as per
        https://www.sphinx-doc.org/en/master/usage/domains/python.html#cross-referencing-python-objects

        - Modules: :mod:`datetime`
        - Functions: :func:`~time.time`
        - Toplevel variable: :data:`CONSTANT` or :const:`CONSTANT`
        - Class: :class:`datetime.datetime`
        - Method: :meth:`hello`
        - Class attributes: :attr:`datetime.datetime.year`
        - Exceptions: :exc:`RuntimeError`
        - Builtin constants: :obj:`True`, :obj:`False`, :obj:`None`
        - :meth:`custom link text like: Path.rglob('*')<pathlib.Path.rglob>`
        - TODO: None of the above seem to work for enum members?

        .. warning:: This is how to make a warning.
            https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-warning

        :param blah: Something
            (I'm not sure why Sphinx isn't autodetecting the type, but if I needed to I could write ``:param int blah:``.)
        :return: Other thing
        :raises ValueError: If it feels like it

        :seealso: https://www.sphinx-doc.org/en/master/usage/domains/python.html

        .. seealso::

            https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-seealso
                Longer-form "see also" rendered as box
        """
        return blah
