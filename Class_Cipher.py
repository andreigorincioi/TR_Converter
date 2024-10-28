'''
CipherHandler
Class used to encrypt and decrypt passwords
-------------------------------------------
Log:
AG - 2023.11.03: encrypt and decrypt now returns strings and encrypt take argument in string format
AG - 2023.11.30: added replace on decrypt final string for \ escape caracter
'''
from base64 import b64encode, b64decode
from Crypto.Cipher import Salsa20

PROGRAM_VERSION = "1.0.0"
PROGRAM_DATE = "21-02-2024"
PROGRAM_AUTHOR = "AG"


class CipherHandler:
    '''This class is utilized to encrypt and decrypt data based on the nonce and the key. '''

    def __init__(self) -> None:
        # the vector utilized to initiliaze the encoding algorithm, must be 16 or 32 bytes long
        self.nonce: bytes = b'\xb1\x9e|\xf3B\xf9FC'
        # the key used to encrypt the data no format requested
        self.key: bytes = b'LRH0l77b8TczE5ExNVFq567v2ngresnf'

    def encrypt(self, plain_text: str) -> str:
        '''
        encrypt passed message
        param plain_text: data to encrypt
        return : the encrypted data
        '''
        cipher = Salsa20.new(self.key, self.nonce)
        encrypted_data = cipher.encrypt(plain_text.encode("utf-8"))
        return b64encode(encrypted_data).decode('utf-8')

    def decrypt(self, encrypted_data: str) -> str:
        '''
        decrypt passed encrypted message
        param encrypted_data: data to decrypt, data must be in byte array format
        return: the decrypted data 
        '''
        encrypted_data = encrypted_data.encode('utf-8')
        encrypted_data = b64decode(encrypted_data)
        decrypt_data = Salsa20.new(self.key, self.nonce)
        decrypted_data = decrypt_data.decrypt(encrypted_data)
        return decrypted_data.decode('utf-8').replace('\\\\', '\\')


if __name__ == "__main__":
    selected = input("1) encrypt plain text.\n2) decrypt encrypted text\n")
    match selected:
        case "1":
            print(CipherHandler().encrypt(input("Write plain text:")))
        case "2":
            print(CipherHandler().decrypt(
                input("Write encrypted text: ")))
