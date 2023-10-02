# IP address and port for the server
HARDCODED_HOST = "127.0.0.1"
HARDCODED_PORT = 6000


# Timeout for certain operations in seconds
HARDCODED_TIMEOUT = 1

# Maximum number of times to try a timeout operation

HARDCODED_MAX_TIMEOUT_TRIES = 10

# Timeout for receiving input from the user
HARDCODED_TIMEOUT_FOR_RECEIVING_INPUT = 40

# Chunk size for file transfer
HARDCODED_CHUNK_SIZE = 1024

# Buffer size for file transfer
HARCODED_BUFFER_SIZE_FOR_FILE = 2000

# Size of the packet headers, is 1 on S&W
PACKET_HEADER_SIZE = 1
# Buffer size for socket communication
HARDCODED_BUFFER_SIZE = HARDCODED_CHUNK_SIZE + PACKET_HEADER_SIZE

# Message indicating the end of an upload
UPLOAD_FINISH_MSG = "FINARDO"


LIST_FILES_FINISH = "FINARDO"

# Mount path for server files (directory where files are stored)
HARDCODED_MOUNT_PATH = "./server_files/"
