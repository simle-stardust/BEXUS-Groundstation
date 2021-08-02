run: install
	python3 main.py

stop:
	kill -9 $(ps aux | grep main.py | awk '{print $2}' | head -n1)

install:
	pip install -r requirements.txt