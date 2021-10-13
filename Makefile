install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
		
format:
	black ./
	
lint run:
	touch __init__.py
	pylint --load-plugins pylint_flask_sqlalchemy, pylint_flask --disable=R,C /app
	
lint app:
	pylint --load-plugins pylint_flask_sqlalchemy, pylint_flask --disable=R,C run.py
test:
	python -m pytest -vv --cov=main test_main.py