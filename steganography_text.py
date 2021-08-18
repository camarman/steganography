# Implementing a Steganography Machine that can encrypt and decrypt messages.
# I have included two new features; initial_colorCode and step_size to improve the encryption

from math import floor
from time import sleep

import numpy as np
from PIL import Image

#---------- HELPFUL FUNCTIONS ----------#


def add_leadingzero(byte):
    """
    Adding leading zeros to a given byte. Python removes the leading zeros by default,
    whereas each byte should consist of 8 bits.
    """
    while len(byte) != 8:
        byte = '0' + byte
    return byte


def colorByte(colorCode):
    return add_leadingzero(bin(colorCode)[2:])


def format_pixels(pixelValues):
    """
    Changing the format of the get_pixels() function to apply
    encryption and decryption more easily.
    """
    return [colorCode for pixel in pixelValues for colorCode in pixel]


def image_size(imagePATH):
    """
    Returns the size of a given image.

    Args:
        imagePATH [str]: The path of the image (It can also be a relative path)
    """
    im = Image.open(imagePATH)
    width, height = im.size
    im.close()
    return (width, height)


def get_pixels(imagePATH):
    """
    Returns the pixel values of a given image.

    Args:
        imagePATH [str]: The path of the image (It can also be a relative path)
    """
    im = Image.open(imagePATH)
    pixelValues = list(im.getdata())
    im.close()
    return pixelValues


def encodeMessage(message):
    """
    Turning the message into binary code with a unique adjustment. This adjustment is necessary
    to decrypt the image.

    Args:
        messsage [str]: The message provided by the user
    """
    binaryMessage = ''
    for i in range(len(message)):
        current_char = message[i]
        binaryMessage += add_leadingzero(bin(ord(current_char))[2:])
        try:
            # If the next character exists in the message, put a marker, '0'
            next_char = message[i+1]
            binaryMessage += '0'
        except:  # If the next character does not exist, put a marker, '1', to indicate end of message
            binaryMessage += '1'
    # Note that this length is not equal to len(message) * 8
    return binaryMessage, len(binaryMessage)

#---------- MAIN FUNCTIONS ----------#


def encryptMessage(messsage, original_imagePATH, encrypted_imagePATH, initial_colorCode, step_size):
    """
    Encrypting the message into an image.

    Args:
        messsage [str]: The message provided by the user
        original_imagePATH [str]: The path of the original image
        (It can also be a relative path)
        encrypted_imagePATH [str]: The path of the image, in which the message is hidden
        (It can also be a relative path)
        initial_colorCode [list]: The initial point, where the encryption starts. It takes two values
        (x, y) that represents the location of the point. Note that x>=0 and y>=0
        step_size [int]: Each bit in the message is encrypted in a color byte with a distace,
        given by the step size
    """
    # Obtaining/Defining some important parameters
    width, height = image_size(original_imagePATH)
    binaryMessage, binaryMessageLength = encodeMessage(messsage)
    org_colorCodeValues = format_pixels(get_pixels(original_imagePATH))
    enc_colorCodeValues = org_colorCodeValues.copy()
    initial_colorCode_loc = initial_colorCode[0] * initial_colorCode[1]
    final_pixel_loc = initial_colorCode_loc + (binaryMessageLength*step_size)
    bit_counter = 0
    # Starting the encryption process
    for i in range(initial_colorCode_loc, final_pixel_loc, step_size):
        org_colorCode = org_colorCodeValues[i]
        messageBit = binaryMessage[bit_counter]
        # Changing the Least Significant Bit of a given color code and then converting it into an integer
        enc_colorCodeValues[i] = int(colorByte(org_colorCode)[:7] + messageBit, 2)
        bit_counter += 1
    # Some reformatting and saving the image
    updated_pixelValues = np.reshape(
        np.array(enc_colorCodeValues, dtype=np.uint8), newshape=(height, width, 3))
    enc_image = Image.fromarray(updated_pixelValues)
    enc_image.save(encrypted_imagePATH)
    enc_image.close()


def decryptMessage(encrypted_imagePATH, initial_colorCode, step_size):
    """
    Decrypting the image, in which the message is hidden.

    Args:
        encrypted_imagePATH [str]: The path of the image, in which the message is hidden
        (It can also be a relative path)
        initial_colorCode [list]: The initial point, where the encryption starts. It takes two values
        (x, y) that represents the location of the point. Note that x>=0 and y>=0
        step_size [int]: Each bit in the message is encrypted in a color byte with a distace,
        given by the step size
    """
    enc_colorCodeValues = format_pixels(get_pixels(encrypted_imagePATH))
    initial_colorCode_loc = initial_colorCode[0] * initial_colorCode[1]
    step_counter = 0
    bitCounter = 1
    EOF_bit = '0'
    binaryMessage = ''
    while EOF_bit != '1':
        enc_colorCode = enc_colorCodeValues[initial_colorCode_loc + step_counter]
        decrypted_bit = colorByte(enc_colorCode)[-1]
        if bitCounter % 9 != 0:
            binaryMessage += decrypted_bit
        else:
            EOF_bit = decrypted_bit
            if EOF_bit == '1':
                break
            else:
                binaryMessage += ','
        step_counter += step_size
        bitCounter += 1
    decrypted_message = ''.join([chr(int(i, 2))
                                for i in binaryMessage.split(',')])
    return decrypted_message

#---------- RUNING FUNCTIONS ----------#


def run_encryption(message, original_imagePATH, encrypted_imagePATH, initial_colorCode=(0, 0), step_size=1):
    """
    The main function that runs the encryption process.

    Args:
        messsage [str]: The message provided by the user
        original_imagePATH [str]: The path of the original image
        (It can also be a relative path)
        encrypted_imagePATH [str]: The path of the image, in which the message is hidden
        (It can also be a relative path)
        initial_colorCode [tuple, optional]: The initial point, where the encryption starts. It takes two values
        (x, y) that represents the location of the point. Note that x>=0 and y>=0. Defaults to (0, 0)
        step_size [int, optional]: Each bit in the message is encrypted in a color byte with a distace,
        given by the step size. Defaults to 1
    """
    pixelnum = image_size(original_imagePATH)[
        0] * image_size(original_imagePATH)[1]
    max_char_num = floor(pixelnum / 3)
    messageLength = len(message)

    print('Welcome to Steganography Encryption Machine')
    print('------------------------')
    print('Pixel number: {}'.format(pixelnum))
    sleep(1)
    print('Maximum characters/bytes that can be stored in the image: {}'.format(max_char_num))
    sleep(1)
    print('Length of the message: {}'.format(messageLength))
    sleep(1)
    print('------------------------')
    print('Starting the encryption process...')
    sleep(2)
    encryptMessage(message, original_imagePATH,
                   encrypted_imagePATH, initial_colorCode, step_size)
    print('Encryption is successful')


def run_decryption(encrypted_imagePATH, initial_colorCode=(0, 0), step_size=1):
    """
    The main function that runs the decryption process.

    Args:
        messsage [str]: The message provided by the user
        encrypted_imagePATH [str]: The path of the image, in which the message is hidden
        (It can also be a relative path)
        initial_colorCode [tuple, optional]: The initial point, where the encryption starts. It takes two values
        (x, y) that represents the location of the point. Note that x>=0 and y>=0. Defaults to (0, 0)
        step_size [int, optional]: Each bit in the message is encrypted in a color byte with a distace,
        given by the step size. Defaults to 1
    """
    pixelnum = image_size(original_imagePATH)[
        0] * image_size(original_imagePATH)[1]
    max_char_num = floor(pixelnum / 3)

    print('Welcome to Steganography Decryption Machine')
    print('------------------------')
    print('Pixel number: {}'.format(pixelnum))
    sleep(1)
    print('Maximum characters/bytes that can be stored in the image: {}'.format(max_char_num))
    sleep(1)
    print('------------------------')
    print('Starting the decryption process...')
    sleep(2)
    print('Decryption is successful. Printing the result...')
    print(decryptMessage(encrypted_imagePATH, initial_colorCode, step_size))

#---------- INPUTS ----------#


# The message that needs to be encrypted
secret_message = 'In the Middle of this Nowhere'

# Full or relative path of the original image
original_imagePATH = r'Steganography\image.jpg'

# Full or relative path of the image, in which the message is hidden
encrypted_imagePATH = r'Steganography\encoded_image.png'

# The initial position of the color code that the encryption starts. Defaults to (0,0)
initial_colorCode = (99, 77)

# Each bit of the message is encrypted with a given step size. Defaults to 1
step_size = 120


#---------- RUNNING THE PROGRAM ----------#

# run_encryption(secret_message, original_imagePATH, encrypted_imagePATH,
#                initial_colorCode, step_size)

run_decryption(encrypted_imagePATH, initial_colorCode, step_size)
