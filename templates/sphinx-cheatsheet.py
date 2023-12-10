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

        How to reference various things:

        - Modules: :mod:`datetime`
        - Functions: :func:`~time.time`
        - Toplevel variable: :data:`CONSTANT`
        - Class: :class:`datetime.datetime`
        - Method: :meth:`hello`
        - Class attributes: :attr:`datetime.datetime.year`
        - Exceptions: :exc:`RuntimeError`
        - Builtin constants: :obj:`True`, :obj:`False`, :obj:`None`
        - :meth:`custom link text like: Path.rglob('*')<pathlib.Path.rglob>`

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
