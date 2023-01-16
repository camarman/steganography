from main import run_encryption

# ========== INPUTS ==========

# The message that needs to be encrypted
secret_message = '''You discover that home is not a person or a place
But a feeling you can't get back'''

# Full or relative path of the original image
original_imagePATH = 'image.jpg'

# Full or relative path of the image, in which the message is hidden
# Note that .jpg does not work as the path of the encrypted image
encrypted_imagePATH = 'encoded_image.png'

# The initial position of the color code that the encryption starts. Defaults to (0,0)
initial_colorCode = (0, 0)

# Each bit of the message is encrypted with a given step size. Defaults to 1
step_size = 1

# ========== RUNNING THE PROGRAM ==========

run_encryption(secret_message, original_imagePATH, encrypted_imagePATH, initial_colorCode, step_size)
