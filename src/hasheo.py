import hashlib
import sys


def calculate_file_hash(file_path, hash_algorithm="sha256"):
    """Calculate the hash of a file."""
    hash_obj = hashlib.new(hash_algorithm)
    with open(file_path, "rb") as file:
        while True:
            data = file.read(65536)  # Read the file in 64k chunks
            if not data:
                break
            hash_obj.update(data)
    return hash_obj.hexdigest()


def main():

    if len(sys.argv) != 3:
        print("Usage: python script.py <server_file> <another_file>")
        return

    file1 = sys.argv[1]
    file_1 = "lib/server_files/" + file1
    file_2 = sys.argv[2]
    hash1 = calculate_file_hash(file_1)
    hash2 = calculate_file_hash(file_2)
    print("Hash of file 1:", hash1)
    print("Hash of file 2:", hash2)
    if hash1 == hash2:
        print("The files are the same.")
    else:
        print("The files are different.")

if __name__ == '__main__':
    main()

