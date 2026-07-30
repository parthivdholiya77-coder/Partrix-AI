import hashlib


def calculate_file_hash(file_path: str) -> str:
    """
    Calculate SHA256 hash of a file.
    """

    sha = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            sha.update(chunk)

    return sha.hexdigest()