statspost.py
================

.. image:: https://discord.com/api/guilds/920190307595874304/embed.png
   :target: https://discord.gg/vfXHwS3nmQ
   :alt: Discord server invite
.. image:: https://img.shields.io/pypi/v/statspost.py.svg
   :target: https://pypi.python.org/pypi/statspost.py
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/statspost.py.svg
   :target: https://pypi.python.org/pypi/statspost.py
   :alt: PyPI supported Python versions

A python pakage to post the stats to some known botlists.

Key Features
--------------

- Modern Pythonic API using ``async`` and ``await``.
- Proper rate limit handling.
- Optimised in both speed and memory.

Installing
------------

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
---------------

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


Links
------

- `Documentation <https://statspostpy.readthedocs.io/en/latest/>`_
- `Official Support Discord Server <https://discord.gg/vfXHwS3nmQ>`_
