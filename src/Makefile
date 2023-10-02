.PHONY: server client-upload

server:
	python3 -m start_server

upload:
	python3 -m uploader -v -H 127.0.0.1 -p 6000 -s $(p) -n $(n)

download:
	python3 -m downloader -v -H 127.0.0.1 -p 6000 -d $(p) -n $(n)

ls:
	python3 -m client_ls -H 127.0.0.1 -p 6000