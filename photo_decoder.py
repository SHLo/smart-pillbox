import sys
import base64

encoded_filename = sys.argv[1]

encoded_filename_prefix, _ = encoded_filename.split('.')

file_str = None

with open(encoded_filename, 'r') as f:
    file_str = f.read()

file_bytes = base64.b64decode(file_str.encode('utf-8'))

with open(f'{encoded_filename_prefix}.jpg', 'wb') as f:
    f.write(file_bytes)
