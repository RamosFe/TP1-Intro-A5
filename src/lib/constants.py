# IP address and port for the server
HARDCODED_HOST = "127.0.0.1"
HARDCODED_PORT = 6000


# Timeout for certain operations in seconds
HARDCODED_TIMEOUT = 0.8

# Timeout for Stop and wait:
HARDCODED_TIMEOUT_SW = 0.1

# Maximum number of times to try a timeout operation

HARDCODED_MAX_TIMEOUT_TRIES = 10

# Timeout for receiving input from the user
HARDCODED_TIMEOUT_FOR_RECEIVING_INPUT = 40

# Chunk size for file transfer
HARDCODED_CHUNK_SIZE = 4096

# Buffer size for file transfer
HARCODED_BUFFER_SIZE_FOR_FILE = 8000

# Size of the packet headers, is 1 on S&W
PACKET_HEADER_SIZE = 1

# Buffer size for socket communication
HARDCODED_BUFFER_SIZE = HARDCODED_CHUNK_SIZE + PACKET_HEADER_SIZE

PACKET_HEADER_SIZE_SR = 4

HARDCODED_BUFFER_SIZE_SR = HARDCODED_CHUNK_SIZE + PACKET_HEADER_SIZE_SR

# Message indicating the end of an upload
UPLOAD_FINISH_MSG = "FINARDO"

LIST_FILES_FINISH = "FINARDO"

# Mount path for server files (directory where files are stored)
HARDCODED_MOUNT_PATH = "./lib/server_files/"


WINDOW_SIZE = 60
