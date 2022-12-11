from Crypto.PublicKey import RSA


class Owner:
    def __init__(self, private_key: str = ""):
        if private_key:
            self.private_key = RSA.importKey(private_key)
        else:
            self.private_key = RSA.generate(2048)
        self.public_key = self.private_key.publickey().export_key()
