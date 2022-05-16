import os
import shutil
import base64
try:
    import nacl.public
except ImportError:
    print('PyNaCl is required: "pip install pynacl" or similar')
    exit(1)

from stem.control import Controller

class Tor:
    def __init__(self):
        self.controller = None
        self.connected = False
        self.tmp_service_id = None

    def connect(self):
        self.controller = Controller.from_port()
        self.controller.authenticate()

    def create_hidden_service(self):
        (auth_pubkey, auth_privkey) = self.get_new_auth_keys()
        result = self.controller.create_ephemeral_hidden_service({80: 5000}, await_publication=True, client_auth_v3=self.key_str(auth_pubkey))

        if result.service_id:
            self.tmp_service_id = result.service_id
            print(" * Our service is available at %s.onion, press ctrl+c to quit" % self.tmp_service_id)
            print(f"Private key: {self.key_str(auth_privkey)}")
        else:
            print(" * Unable to determine our service's hostname, probably due to being unable to read the hidden service directory")

    def remove_hidden_service(self):
        if self.tmp_service_id:
            self.controller.remove_ephemeral_hidden_service(self.tmp_service_id)

    def get_new_auth_keys(self):
        priv_key = nacl.public.PrivateKey.generate()
        pub_key = pub_key = priv_key.public_key
        return (pub_key, priv_key)

    # https://github.com/pastly/python-snippits/blob/master/src/tor/x25519-gen.py
    def key_str(self, key):
        # bytes to base 32
        key_bytes = bytes(key)
        key_b32 = base64.b32encode(key_bytes)
        # strip trailing ====
        assert key_b32[-4:] == b'===='
        key_b32 = key_b32[:-4]
        # change from b'ASDF' to ASDF
        s = key_b32.decode('utf-8')
        return s