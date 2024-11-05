|actions| |codecov| |pypi| |womm|

.. |actions| image:: https://github.com/wimglenn/oyaml/actions/workflows/tests.yml/badge.svg
.. _actions: https://github.com/wimglenn/oyaml/actions/workflows/tests.yml

.. |codecov| image:: https://codecov.io/gh/wimglenn/oyaml/branch/master/graph/badge.svg
.. _codecov: https://codecov.io/gh/wimglenn/oyaml

.. |pypi| image:: https://img.shields.io/pypi/v/oyaml.svg
.. _pypi: https://pypi.org/project/oyaml

.. |womm| image:: https://cdn.rawgit.com/nikku/works-on-my-machine/v0.2.0/badge.svg
.. _womm: https://github.com/nikku/works-on-my-machine


oyaml
=====

oyaml is a drop-in replacement for `PyYAML <http://pyyaml.org/wiki/PyYAML>`_ which preserves dict ordering.  Both Python 2 and Python 3 are supported. Just ``pip install oyaml``, and import as shown below:

.. code-block:: python

   import oyaml as yaml

You'll no longer be annoyed by screwed-up mappings when dumping/loading.
