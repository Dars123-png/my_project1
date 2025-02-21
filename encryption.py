# encryption.py
import cv2
import os
import numpy as np

# Function to map characters to their ASCII values
def create_char_dict():
    return {chr(i): i for i in range(256)}

# Load the image
def load_image(path):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Image at path '{path}' not found.")
    return img

# Embed the message into the image using LSB
def encrypt_message(img, msg):
    char_to_ascii = create_char_dict()
    img_copy = np.copy(img)
    idx = 0

    # Convert message to binary
    binary_msg = ''.join([format(char_to_ascii[char], '08b') for char in msg])

    for bit in binary_msg:
        row = idx // (img.shape[1] * 3)
        col = (idx // 3) % img.shape[1]
        channel = idx % 3

        pixel_value = int(img_copy[row, col, channel])
        new_value = (pixel_value & ~1) | int(bit)
        img_copy[row, col, channel] = np.uint8(new_value)
        idx += 1

    return img_copy

# Main encryption function
def main():
    img_path = "mypic.jpg"  # Use PNG image
    img = load_image(img_path)

    msg = input("Enter secret message: ")
    password = input("Enter a passcode: ")

    encrypted_img = encrypt_message(img, msg)
    cv2.imwrite("encryptedImage.png", encrypted_img)
    os.system("start encryptedImage.png")

    # Save password and message length for decryption
    with open("password.txt", "w") as f:
        f.write(password + "\n" + str(len(msg)))

if __name__ == "__main__":
    main()
