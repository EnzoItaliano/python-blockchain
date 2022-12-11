from owner import Owner

owner = Owner()
print(f"Private key: {owner.private_key.export_key(format='DER')}\n")
print(f"Public key hash: {owner.public_key_hash}\n")
print(f"Public key hex: {owner.public_key_hex}")
