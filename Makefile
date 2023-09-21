.PHONY: server client-upload

server:
	python3 -m src.start-server

upload:
	python3 -m src.upload -v -H 127.0.0.1 -p 6000 -s $(p) -n $(n)

download:
	python3 -m src.download -v -H 127.0.0.1 -p 6000 -d $(p) -n $(n)