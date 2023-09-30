import hashlib

def calculate_file_hash(file_path, hash_algorithm='sha256'):
    """Calculate the hash of a file."""
    hash_obj = hashlib.new(hash_algorithm)
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)  # Read the file in 64k chunks
            if not data:
                break
            hash_obj.update(data)
    return hash_obj.hexdigest()

# Example usage:
file1 = 'server_files/usa.jpeg'  # Replace with the path to your first file
file2 = 'imagen.jpeg'  # Replace with the path to your second file

hash1 = calculate_file_hash(file1)
hash2 = calculate_file_hash(file2)

if hash1 == hash2:
    print("The files are the same.")
else:
    print("The files are different.")