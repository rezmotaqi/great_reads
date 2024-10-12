import base64

header = (
    "yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"  # Replace with the actual header
)

# Calculate the required padding
missing_padding = len(header) % 4
if missing_padding != 0:
    header += "=" * (4 - missing_padding)

decoded_header = base64.b64decode(header).decode("utf-8", errors="ignore")
print(decoded_header)
