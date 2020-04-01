RUN (do not use)
================
.. code-block:: text

    $ python3 -m venv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ python3 create_db.py
    $ python3 city_list.py    
    $ export FLASK_APP=webapp && export FLASK_ENV=development && flask run
    $ python3 get_hotels.py

Docker RUN
==========
.. code-block:: text
    
    # по расписанию парсит каждые 2 часа, можно поменять в файле /webapp/config.py
    $ docker-compose up
