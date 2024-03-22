import secrets

# Generate a secure token
token = secrets.token_hex(16)

# Specify the filename
filename = 'api_token.txt'

# Write the token to the file
with open(filename, 'w') as file:
    file.write(token)
