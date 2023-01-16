from main import run_decryption

# ========== INPUTS ==========

# Full or relative path of the image, in which the message is hidden
# Note that .jpg does not work as the path of the encrypted image
encrypted_imagePATH = 'encoded_image.png'

# The initial position of the color code that the encryption starts. Defaults to (0,0)
initial_colorCode = (0, 0)

# Each bit of the message is encrypted with a given step size. Defaults to 1
step_size = 1

# ========== RUNNING THE PROGRAM ==========

run_decryption(encrypted_imagePATH, initial_colorCode, step_size)