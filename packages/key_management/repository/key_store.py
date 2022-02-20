from pyfuncify import singleton

class KeyStore(singleton.Singleton):
    kids = {}
    uses = {}

    def add_key(self, kid, cyphertext, alg, use, state):
        self.kids[kid] = {'kid': kid, 'cyphertext': cyphertext, 'alg': alg, 'use': use, 'state': state}
        if not self.uses.get('use', None):
            self.uses[use] = []
        self.uses[use].append({'kid': kid, 'cyphertext': cyphertext, 'alg': alg, 'use': use, 'state': state})
        self

    def get_key_by_kid(self, kid):
        return self.kids[kid]