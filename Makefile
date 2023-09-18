.PHONY: server client-upload

server:
	python3 -m src.server.main

client-upload:
	python3 -m src.client.main upload -H 127.0.0.1 -p 6000 -s $(p) -n $(n)