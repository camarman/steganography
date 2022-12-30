# Steganography

Implementing a steganography algorithm that can hide messages inside an image. Additional to the usual algorithm, I have added two special arguments.

`initial_colorCode`: The initial position of the color code that the encryption starts. Defaults to (0,0)

`step_size`: Each bit of the message is encrypted with a given step size. Defaults to 1

These two additional arguments makes it somewhat harder to decrypt the encoded message. The program also prints out the *number of pixels* and *maximum characters/bytes that can be stored in the image*.

## Running the program

You can install the requirements via

    python3 -m pip install -r requirements.txt

In order to start the encryption process go to `run_encryption.py` and adjust the given arguments. After that you can run the program by typing

    python3 run_encryption.py

Similarly, to start the decryption process, fill the arguments in the `run_decryption.py` and run the program by typing

    python3 run_decryption.py
