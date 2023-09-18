.PHONY: server client-upload

server:
	python3 -m src.start-server

client-upload:
	python3 -m src.upload upload -H 127.0.0.1 -p 6000 -s $(p) -n $(n)