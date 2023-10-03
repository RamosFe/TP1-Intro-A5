.PHONY: server client-upload

server_sr:
	python3 -m start_server -r -v -H 127.0.0.1 -p 6000 -s "./server_files/"

server_sw:
	python3 -m start_server -v -H 127.0.0.1 -p 6000 -s "./server_files/"


upload_sr:
	python3 -m uploader -r -v -H 127.0.0.1 -p 6000 -s $(p) -n $(n)

upload_sw:
	python3 -m uploader -v -H 127.0.0.1 -p 6000 -s $(p) -n $(n)


download_sr:
	python3 -m downloader -r -v -H 127.0.0.1 -p 6000 -d $(p) -n $(n)

download_sw:
	python3 -m downloader -v -H 127.0.0.1 -p 6000 -d $(p) -n $(n)
	

ls:
	python3 -m client_ls -H 127.0.0.1 -p 6000