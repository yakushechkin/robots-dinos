install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
		
format:
	black ./
	
lint:
	pylint --load-plugins pylint_flask_sqlalchemy --disable=R,C app

test:
	python -m pytest -vv --cov=main test_main.py