.PHONY: server client-upload

server_sr:
	python3 -m src.start_server -r -v -H 127.0.0.1 -p 6000 -s "./server_files/"

server_sw:
	python3 -m src.start_server -v -H 127.0.0.1 -p 6000 -s "./server_files/"


upload_sr:
	python3 -m src.uploader -r -v -H 127.0.0.1 -p 6000 -s $(p) -n $(n)

upload_sw:
	python3 -m src.uploader -v -H 127.0.0.1 -p 6000 -s $(p) -n $(n)


download_sr:
	python3 -m src.downloader -r -v -H 127.0.0.1 -p 6000 -d $(p) -n $(n)

download_sw:
	python3 -m src.downloader -v -H 127.0.0.1 -p 6000 -d $(p) -n $(n)
	

ls:
	python3 -m src.client_ls -H 127.0.0.1 -p 6000