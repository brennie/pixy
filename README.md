pixy
====

Requirements
------------

Pixy requires Python3.3 or higher.


Building
--------

To build the modules, run `make`.


Installing Dependencies
-----------------------

Using virtualenv is recommended to manage dependencies

    virtualenv -p /usr/bin/python3 .env
    source .env/bin/activate
    pip3 install -r requirements.txt

Compilation
-----------

Before pixy can be configured, you must compile the transforms module:

    make

Configuration
-------------

Before running the app it must be configured. The setup script will walk you
through database configuration:

    ./setup.py config
    ./setup.py db-create

The database timeout setting should be set to a value (in seconds) less than
your MySQL's value for `interactive_timeout` and `wait_timeout`.

Development Mode
----------------

To run the server in development mode (i.e. with debugging enabled):

    ./setup.py run-devel

Production Mode
---------------

To run the server in production mode:

    uwsgi --ini pixy.ini -d pixy.log

The uwsgi log will be written to `pixy.log`. If logging is not required, you
can specify `-d /dev/null` instead.
