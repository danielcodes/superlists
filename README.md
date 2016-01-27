# Superlists

This is my second Django tutorial as I dive into Test-Driven-Development. 
The tutorial comes from the Test Driven Development with Python by Harry Percival, see it [here](http://chimera.labs.oreilly.com/books/1234000000754/index.html).

Compared to my first tutorial, Tango with Django, this Superlists app is a lot more simpler (though not less complex), as it's main focus is on creating a test suite for the app rather than creating a flashy application.

.. picture here

## To run locally
* Create a directory beforehand, call it lists and ```cd``` into it

  ``` mkdir lists && cd lists``` 

* Now, inside ```lists/``` create a directory called database,

  ``` mkdir database ```

* Finally, inside ```lists/``` you can clone down the repo,

  ``` git clone https://github.com/danielcodes/superlists.git ```

The database folder is kept outside the source code during deployment, so we setup the same way during development.

Before starting up the server, you need to create a virtualenv and install the dependencies,

* In ```list/```, run ``` virtualenv --python=/usr/bin/python3 lists ```, activate it ``` source lists/bin/activate ```
* Install dependencies, ``` pip install -r superlists/requirements.txt ```

Now that we have Django,
Run ``` python manage.py migrate ``` to create the database
and start the server with ``` python manage.py runserver ```. Go to ``` http://localhost:8000/ ``` :)
