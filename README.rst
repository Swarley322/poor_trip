RUN (do not use)
================
.. code-block:: text

    $ python3 -m venv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ flask db upgrade   
    $ python import_cities.py
    $ python import_attractions.py
    $ python import_airports_id.py
    $ python get_hotels.py
    $ export FLASK_APP=webapp && export FLASK_ENV=development && flask run

Docker RUN
==========
.. code-block:: text
    
    $ docker-compose up
