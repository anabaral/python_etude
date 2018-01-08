import struct, hashlib, time
import binascii
import os
# NEED> pip install pycryptodome
from Crypto.Cipher import AES


def decrypt_file(key, in_filename, out_filename, chunksize=24 * 1024):
    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)


def encrypt_file(key, in_filename, out_filename=None, chunksize=65536):
    if not out_filename:
        out_filename = in_filename + '.enc'
    iv = b'initialvector123'
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)
    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)
                outfile.write(encryptor.encrypt(chunk))


def make_pass():
    timekey = int(time.time())
    return str(timekey)



def main():
    key_filepath = "C:/key.bin"
    if not os.path.exists(key_filepath):
        password = make_pass()
        key = hashlib.sha256(password.encode("utf-8")).digest()
        key_file_out = open(key_filepath, 'wb')
        key_file_out.write(binascii.hexlify(key))
        key_file_out.close()
    key_file_in = open(key_filepath, 'rb')
    key = binascii.unhexlify(key_file_in.read())
    key_file_in.close()

    print (binascii.hexlify(bytearray(key)))
    in_filename = 'C:/Users/Administrator/Pictures/book.jpg'
    encrypt_file(key, in_filename, out_filename='C:/Users/Administrator/Pictures/book_encrypted')
    print ('Encrypte Done !')

    #delete original file

    #decrypt
    decrypt_file(key, in_filename='C:/Users/Administrator/Pictures/book_encrypted', out_filename='C:/Users/Administrator/Pictures/book_decrypted.jpg')
    #outfile = open('original.hwp')
    #magic = outfile.read(8)
    #print 'Magic Number : ' + magic.encode('hex')
    #if magic.encode('hex') == 'd0cf11e0a1b11ae1':
    #    print 'This document is a HWP file.'


main()