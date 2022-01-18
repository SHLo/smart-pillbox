import sys
import base64

photo_filename = sys.argv[1]

photo_filename_prefix, _ = photo_filename.split('.')

file_bytes = None

with open(photo_filename, 'rb') as f:
    file_bytes = f.read()

file_bytes_b64 = base64.b64encode(file_bytes)
file_bytes_b64_str = file_bytes_b64.decode('utf-8')

with open(f'{photo_filename_prefix}.txt', 'w') as f:
    f.write(file_bytes_b64_str)
