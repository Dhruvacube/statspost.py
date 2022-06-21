.. statspost documentation master file, created by
   sphinx-quickstart on Mon May 23 22:43:39 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to statspost's documentation!
=====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


A modern, easy to use, feature-rich, and async ready API wrapper for statspost written in Python.


Key Features
-------------

- Modern Pythonic API using ``async`` and ``await``.
- Proper rate limit handling.
- Optimised in both speed and memory.

Installing
----------

**Python 3.8 or higher is required**

To install the library, you can just run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U statspost.py

    # Windows
    py -3 -m pip install -U statspost.py

To speedup the api wrapper you should run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U "statspost.py[speed]"

    # Windows
    py -3 -m pip install -U statspost.py[speed]


To install the development version, do the following:

.. code:: sh

    $ git clone https://github.com/Dhruvacube/statspost.py
    $ cd statspost.py
    $ python3 -m pip install -U .[speed]


Quick Example
--------------

.. code:: py

      from statspost import StatsPost
      import asyncio
      import sys
      
      #defining run function
      run = asyncio.get_event_loop().run_until_complete

      # setting up the statpost client handler
      a=StatsPost(bot_id=935242576343224352,servers=80) 
      a.add_botlist('topgg','topgg_token')

      # setting up the windows loop policy according to the operating system
      if sys.platform.startswith(('win32', 'cygwin')):
          asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

      # Post stats, and return the data
      print(run(a.post_stats(return_post_data=True)))


You can find more examples in the `examples directory <https://github.com/Dhruvacube/statspost.py/tree/master/examples>`_.

Links
------

- `Official Support Discord Server <https://discord.gg/vfXHwS3nmQ>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

.. toctree::
  :maxdepth: 2

  autoapi/index.rst

