# Generator for private key seed phrases (for bitcoin and other cryptos)

import hashlib
import hmac
import codecs
import random

# Define the word list
word_list = [line.strip() for line in open('english.txt')]

def generate_seed_phrase(input_str):
    # Convert the input string to bytes
    input_bytes = input_str.encode('utf-8')

    # Generate the master seed using HMAC-SHA512 with a blank key and the input string as the message
    seed = hmac.new(b"", input_bytes, hashlib.sha512).digest()

    # Convert the seed to a hex string
    seed_hex = codecs.encode(seed, 'hex').decode('utf-8')

    # Calculate the checksum by taking the first byte of the double SHA256 hash of the seed
    checksum = hashlib.sha256(codecs.decode(seed_hex, 'hex')).digest()
    checksum = hashlib.sha256(checksum).digest()[0]

    # Add the checksum to the end of the seed (as a single byte)
    seed_hex += '{:02x}'.format(checksum)

    # Convert the seed to a list of 11-bit integers
    seed_ints = [int(seed_hex[i:i+2], 16) for i in range(0, len(seed_hex), 2)]
    seed_bits = ''.join('{:0>8b}'.format(i) for i in seed_ints)
    chunks = [seed_bits[i:i+11] for i in range(0, len(seed_bits), 11)]

    # Select 12 words from the word list
    words = [word_list[int(chunk, 2)] for chunk in chunks[:12]]

    # Return the seed phrase as a space-separated string
    return ' '.join(words)

# Prompt the user to enter the input string
input_str = input("Enter your input string: ")
input_num = input("Enter the number of words you want to generate (12 or 24): ")

# Generate the seed phrase and print it
seed_phrase = generate_seed_phrase(input_str)

if (input_num=="12"):
	print("Your 12-word seed phrase is:", seed_phrase)

if (input_num=="24"):
	print("Your 24-word seed phrase is:", seed_phrase, seed_phrase)

if (input_num!="24" and input_num!="12"):
	print("Wrong input number")

