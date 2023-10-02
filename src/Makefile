.PHONY: server client-upload

server:
	python3 -m start_server

upload_sr:
	python3 -m uploader -r -v -H 127.0.0.1 -p 6000 -s $(p) -n $(n)

download_sr:
	python3 -m downloader -r -v -H 127.0.0.1 -p 6000 -d $(p) -n $(n)

upload_sw:
	python3 -m uploader -w -v -H 127.0.0.1 -p 6000 -s $(p) -n $(n)

download_sr:
	python3 -m downloader -w -v -H 127.0.0.1 -p 6000 -d $(p) -n $(n)


ls:
	python3 -m client_ls -H 127.0.0.1 -p 6000