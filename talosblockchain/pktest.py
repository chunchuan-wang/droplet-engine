from pybitcoin import BitcoinPrivateKey

private_key = BitcoinPrivateKey()
print("private_key: %s" % private_key)

private_key_hex = private_key.to_hex()
print("private_key_hex: %s" % private_key_hex)

pk = BitcoinPrivateKey(private_key_hex)
print("pk: %s" % pk)


