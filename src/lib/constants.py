# IP address and port for the server
HARDCODED_HOST = "127.0.0.1"
HARDCODED_PORT = 6000


# Timeout for certain operations in seconds
HARDCODED_TIMEOUT = 1
HARDCODED_MAX_TIMEOUT_TRIES = 4

# Chunk size for file transfer
HARDCODED_CHUNK_SIZE = 20

# Size of the packet headers, is 1 on S&W
PACKET_HEADER_SIZE = 1
# Buffer size for socket communication
HARDCODED_BUFFER_SIZE = HARDCODED_CHUNK_SIZE + PACKET_HEADER_SIZE

# Message indicating the end of an upload
UPLOAD_FINISH_MSG = "FINARDO"

# Mount path for server files (directory where files are stored)
HARDCODED_MOUNT_PATH = "./server_files/"
