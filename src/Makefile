.PHONY: server client-upload

server_sr:
	python3 -m start_server -r -v -H 127.0.0.1 -p 6000 -s "./lib/server_files/"

server_sw:
	python3 -m start_server -v -H 127.0.0.1 -p 6000 -s "./lib/server_files/"


upload_sr:
	python3 -m upload -r -v -H 127.0.0.1 -p 6000 -s $(p) -n $(n)

upload_sw:
	python3 -m upload -v -H 127.0.0.1 -p 6000 -s $(p) -n $(n)


download_sr:
	python3 -m download -r -v -H 127.0.0.1 -p 6000 -d $(p) -n $(n)

download_sw:
	python3 -m download -v -H 127.0.0.1 -p 6000 -d $(p) -n $(n)
	

ls:
	python3 -m src.ls -H 127.0.0.1 -p 6000