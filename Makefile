.PHONY: all test clean

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
		
format:
	black ./
	
lint:
	pylint --load-plugins pylint_flask_sqlalchemy --disable=R,C app &&\
		pylint --load-plugins pylint_flask_sqlalchemy --disable=R,C test &&\
			pylint --load-plugins pylint_flask_sqlalchemy --disable=R,C run.py

test:
	python -m unittest discover -s test/ -p 'test_*.py'