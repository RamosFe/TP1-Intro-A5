.PHONY: server client-upload

server:
	python3 -m src.server.main

client-upload:
	python3 -m src.client.main upload -v -H 127.0.0.1 -p 6000 -s $(p) -n $(n)

client-download:
	python3 -m src.client.main download -v -H 127.0.0.1 -p 6000 -d $(p) -n $(n)