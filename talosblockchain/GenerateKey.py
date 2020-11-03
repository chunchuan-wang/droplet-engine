import bitcoin
from pybitcoin import BitcoinPrivateKey
 
# Generate a random private key
valid_private_key = False
while not valid_private_key:
    #private_key = bitcoin.random_key()
    private_key = BitcoinPrivateKey()
    private_key = private_key.to_hex()
    decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')
    compressed_private_key = private_key + '01'
    valid_private_key = 0 < decoded_private_key < bitcoin.N
print("Private Key (hex) is: ", private_key)
print("Private Key (decimal) is: ", decoded_private_key)
print("Private Key Compressed (hex) is: ", compressed_private_key)
 
# Convert private key to WIF format  bin_to_b58check(encode(priv, 256, 32)+b'\x01', 128+int(vbyte))
wif_encoding_private_key = bitcoin.encode_privkey(decoded_private_key, 'wif')
wif_compressed_private_key = bitcoin.encode_privkey(decoded_private_key, 'wif_compressed')
print("Private Key(WIF) is: ", wif_encoding_private_key)
print("Private Key(WIF-Compressed) is: ", wif_compressed_private_key)
 
# Multiply the EC generator point G with the private key to get a public key point
public_key = bitcoin.privkey_to_pubkey(decoded_private_key)
print("Public Key (x,y) coordinates is:", public_key)
 
# Encode as hex, prefix 04
hex_encoded_public_key = bitcoin.encode_pubkey(public_key,'hex')
print("Public Key (hex) is:", hex_encoded_public_key)
 
# Compress public key, adjust prefix depending on whether y is even or odd
hex_compressed_public_key = bitcoin.encode_pubkey(public_key,'hex_compressed')
print("Public Key (hex) is:", hex_compressed_public_key)
 
# Generate compressed bitcoin address from compressed public key
print("Compressed Bitcoin Address (b58check) is:", bitcoin.pubkey_to_address(hex_compressed_public_key))
