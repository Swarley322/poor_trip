RUN (do not use)
================
.. code-block:: text

    $ python3 -m venv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ flask db upgrade
    $ python city_list.py    
    $ export FLASK_APP=webapp && export FLASK_ENV=development && flask run
    $ python get_hotels.py

Docker RUN
==========
.. code-block:: text
    
    $ docker-compose up
