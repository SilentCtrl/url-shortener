# WEBSITE

This project was done via flask. It still requires a bit of cleanup, but the basic functionalities are still there.

INSTALLATION REQUIREMENTS:

You need to install MySQL- you need to install the correct compatible distribution with homebrew:
```
brew install mysql
```

Then you need to have the python package requirements installed. This is in requirements.txt

In order to deploy the application, you need to do that following:
```
mysql.server start
export FLASK_APP=short
flask run
```

And don't forget to do the following to stop running the code:
```
mysql.server stop
```

You should then have this running on http://127.0.0.1:5000/

The shortener application is on http://127.0.0.1:5000/s/

In order to use a shortened url, type http://127.0.0.1:5000/s/<shortened_url>