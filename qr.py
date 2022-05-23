# Ce fichier contient les fonctions d'encodage 

# partie Corps de Galois
def degre(n):
    d = -1
    while n > 0:
        n = n >> 1
        d += 1
    return d

def modulo(dividende, diviseur):
    degre_diviseur = degre(diviseur)
    degre_dividende = degre(dividende)
    while degre_dividende >= degre_diviseur:
        dividende = dividende ^ (diviseur << (degre_dividende - degre_diviseur))
        degre_dividende = degre(dividende)
    return dividende

class CorpsGalois(object):

    def __init__(self, p):
        self.degre_max = (2 ** degre(p)) - 1
        self.exps = [0] * self.degre_max
        self.logs = [0] * (self.degre_max + 1)
        
        degre_p = 1 << degre(p)
        
        a = 1
        for i in range(0, self.degre_max):
            self.exps[i] = a
            self.logs[a] = i
            a <<= 1
            if a & degre_p != 0:
                a ^= p

    def plus(self, a, b):
        return a ^ b

    def fois(self, a, b):
        if a == 0 or b == 0:
            return 0
        return self.exps[(self.logs[a] + self.logs[b]) % self.degre_max]

    def division(self, a, b):
        if b == 0:
            raise ZeroDivisionError()
        if a == 0:
            return 0
        return self.exps[(self.logs[a] + self.degre_max - self.logs[b]) % self.degre_max]

    def puissance(self, a, b):
        if a == 0:
            return 0
        if b < 0:
            return self.exps[((self.logs[a] - self.degre_max) * b) % self.degre_max]
        return self.exps[(self.logs[a] * b) % self.degre_max]

class AnneauPolynome(object):

    def __init__(self, corps):
        self.corps = corps

    def fois(self, p, q):
        r = [0] * (len(p) + len(q) - 1)
        for i in range(len(p)):
            for j in range(len(q)):
                produit = self.corps.fois(p[i], q[j])
                r[i + j] = self.corps.plus(r[i + j], produit)
        return r

    def reste_division(self, p, q):
        if len(q) == 0:
            raise ZeroDivisionError()
        while len(p) >= len(q):
            a = self.corps.division(p[0], q[0])
            for i in range(1, len(q)):
                p[i] = self.corps.plus(p[i], self.corps.fois(q[i], a))
            p = p[1:]
        return p

    def generateur(self, n):
        g = [1]
        for i in range(n):
            g = self.fois(g, [1, self.corps.puissance(2, i)])
        return g

class Correcteur(object):

    def __init__(self, n_extra, irreducible):
        self.anneau = AnneauPolynome(CorpsGalois(irreducible))
        self.generateur = self.anneau.generateur(n_extra)

    def encode(self, donnees):
        avec_extra = donnees + [0] * (len(self.generateur) - 1)
        return self.anneau.reste_division(avec_extra, self.generateur)
    

def bit(n, i):
    return (n >> i) & 1
    
def int2binarystr(value, strsize=8):
    msg = ''
    for i in range(strsize):
        msg += str(bit(value,i)) 
    return msg   
    
def octet2str(octet):
	oc = str(bin(octet)).replace('0b','')
	return '0'*(8-len(oc)) + oc

def data2str(data):
    msg = ''
    for d in data:
        #msg += octet2str(d)
        msg += int2binarystr(d)[::-1]
    return msg    
        
def encode_format(mode, masque):
    donnees = ((mode << 3) ^ masque) << 10
    extra = modulo(donnees, 0b10100110111)
    return (donnees + extra) ^ 0b101010000010010

def encode_message(message):
    bits = 0b0100
    octets_message = message.encode('iso-8859-1')
    longueur = len(octets_message)
    if longueur > 17:
        raise ValueError('Le message est trop long')
    bits <<= 8
    bits ^= longueur
	
    for octet in octets_message:
        bits <<= 8
        bits ^= octet
		
    bits <<= 4
    
    for i in range(17 - longueur):
        bits <<= 8
        if i % 2 == 0:
            bits ^= 236
        else:
            bits ^= 17
            
    	
    octets = []
    for i in range(19):
        octets.insert(0, bits & 255)
        bits >>= 8
    return octets

def message2bits(message):
    donnees = encode_message(message)
    correcteur = Correcteur(7, 0b100011101)
    donnees += correcteur.encode(donnees)
    bits = data2str(donnees)
    return bits

def format2bits(level=1, mask=3):
    format_encode = encode_format(1, 3) #une autre valeur que 3 ne donne pas de QR Code lisible !?
    bits = int2binarystr(format_encode,15)  
    return bits