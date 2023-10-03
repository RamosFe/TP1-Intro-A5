# TP1-Intro-A5
TP 1 de Introducción a Sistemas Distribuidos - Grupo A5

## Integrantes
- [105103 - Franco Gazzola](https://github.com/franco-jyq)
- [106010 - Federico Martín Valsagna Indri](https://github.com/FedericoValsagna)
- [107205 - Eliana Harriet](https://github.com/ElianaHarriet)
- [108026 - Tomas Emanuel](https://github.com/tomasemanuel)
- [108193 - Tomás González](https://github.com/tomasgonzz)
- [101640 - Ramos Federico](https://github.com/RamosFe)

# Ejecución del programa

## Servidor

El server acepta los siguientes flags:  
- `-H` para indicar la IP en la que escuchará conexiones. 
- `-p` para indicar el puerto en el que escuchará conexiones.
- `-s` para indicar el directorio en el que se guardarán los archivos.
- `-v` para indicar que se desea que el servidor imprima por pantalla los eventos que ocurren.
- `-q` para indicar que se desea que el servidor no imprima por pantalla los eventos que ocurren. (Por defecto)
- `-r` para indicar que el protocolo de transferencia sea _Selective Repeat_, de lo contrario será _Stop and Wait_.

Ejemplo de ejecución usando Selective Repeat:
```bash
$ python3 -m start_server -r -v -H 127.0.0.1 -p 6000 -s "./server_files/"
```
_Puede correrse ese mismo comando de la forma `make server_sr`_

Ejemplo de ejecución usando Stop and Wait:
```bash
$ python3 -m start_server -v -H 127.0.0.1 -p 6000 -s "./server_files/"
```
_Puede correrse ese mismo comando de la forma `make server_sw`_

## Cliente

### Upload

El cliente para modo _upload_ acepta los siguientes flags:  
- `-H` para indicar la IP del servidor al que se conectará.
- `-p` para indicar el puerto del servidor al que se conectará.
- `-s` para indicar el archivo que se desea subir.
- `-n` para indicar el nombre con el que se guardará el archivo en el servidor.
- `-v` para indicar que se desea que el cliente imprima por pantalla los eventos que ocurren.
- `-q` para indicar que se desea que el cliente no imprima por pantalla los eventos que ocurren. (Por defecto)
- `-r` para indicar que el protocolo de transferencia sea _Selective Repeat_, de lo contrario será _Stop and Wait_.

Ejemplo de ejecución usando Selective Repeat:
```bash
$ python3 -m uploader -r -v -H 127.0.0.1 -p 6000 -s $(p) -n $(n)
```
_Puede correrse ese mismo comando de la forma `make upload_sr`_

Ejemplo de ejecución usando Stop and Wait:
```bash
$ python3 -m uploader -v -H 127.0.0.1 -p 6000 -s $(p) -n $(n)
```
_Puede correrse ese mismo comando de la forma `make upload_sw`_

### Download

El cliente para modo _download_ acepta los siguientes flags:
- `-H` para indicar la IP del servidor al que se conectará.
- `-p` para indicar el puerto del servidor al que se conectará.
- `-n` para indicar el nombre del archivo que se desea descargar.
- `-d` para indicar el path en el que se guardará el archivo descargado.
- `-v` para indicar que se desea que el cliente imprima por pantalla los eventos que ocurren.
- `-q` para indicar que se desea que el cliente no imprima por pantalla los eventos que ocurren. (Por defecto)
- `-r` para indicar que el protocolo de transferencia sea _Selective Repeat_, de lo contrario será _Stop and Wait_.

