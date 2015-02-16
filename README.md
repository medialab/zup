zup
===

a simple interface from extracting texts from (almost) any url.

## installation
Clone the repository and its submodules

	clone --recursive https://github.com/medialab/zup.git zup

If --recursive options is not available, consider using these command to install submodules

	cd zup
	git submodule init
	git submodule update

Create and activate a dedicated virtualenv for zup. If you're not sure, please follow this [how-to](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

Install then the dependencies via pip packages:
	
	cd zup
	pip install -r requirements.txt

Some python package that zup requires, like lxml, needs some other libraries to be available. On unix environment, make sure the development packages of libxml2 and libxslt are installed.

	sudo apt-get install libxml2-dev libxslt1-dev python-dev

In case, you are using Ubuntu/Lubuntu 13.04 or Ubuntu 13.10 and having problem with "/usr/bin/ld: cannot find -lz", you may need also install zlib1g-dev package.
	
	sudo apt-get install zlib1g-dev
		
##Configuration
Once installation has been completed, there is one more step: configuration.

	cd zup
	cp local_settings.py.example local_settings.py

And modify these two lines according to your own virtualenv
	
	SECRET_KEY = 'your own generated secret key'
		
	PYTHON_INTERPRETER = '<your virtualenv path>/.virtualenvs/zup/bin/python'
	
	
##Run
Zup needs a light sqlite database

	cd zup
	python manage.py syncdb
	python manage.py test

Test your installation with

	python manage.py runserver


