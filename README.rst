RUN
===
.. code-block:: text

    $ python3 -m venv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ python3 create_db.py
    $ python3 city_list.py    
    $ export FLASK_APP=webapp && export FLASK_ENV=development && flask run
    $ python3 get_hotels.py

Docker RUN
===
.. code-block:: text

    $ docker build -t [name]:[tag]
    $ docker run --name [name] -p 5000:5000 [image_name]:[image_tag]
    
