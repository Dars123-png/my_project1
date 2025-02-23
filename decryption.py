import cv2
def create_ascii_dict():
    return {i: chr(i) for i in range(256)}
def load_image(path):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Image at path '{path}' not found.")
    return img
def decrypt_message(img, msg_length):
    ascii_to_char = create_ascii_dict()
    binary_msg = ''
    idx = 0

    total_bits = msg_length * 8

    for _ in range(total_bits):
        row = idx // (img.shape[1] * 3)
        col = (idx // 3) % img.shape[1]
        channel = idx % 3

        pixel_value = int(img[row, col, channel])
        binary_msg += str(pixel_value & 1)
        idx += 1

    message = ''
    for i in range(0, len(binary_msg), 8):
        byte = binary_msg[i:i+8]
        message += ascii_to_char[int(byte, 2)]

    return message

def main():
    img_path = "encryptedImage.png"
    img = load_image(img_path)

    pas = input("Enter passcode for Decryption: ")
    with open("password.txt", "r") as f:
        saved_password, msg_length = f.read().split("\n")

    if pas == saved_password:
        decrypted_msg = decrypt_message(img, int(msg_length))
        print("Decrypted message:", decrypted_msg)
    else:
        print("YOU ARE NOT AUTHORIZED!")

if __name__ == "__main__":
    main()
