UID = "2024300027"

digit_sum = sum(map(int, UID))
caesar_key = digit_sum % 25 + 1
def caesar_encrypt(t):
    return "".join(chr((ord(c.upper())-65+caesar_key)%26+65) for c in str(t))
def caesar_decrypt(t):
    return "".join(chr((ord(c.upper())-65-caesar_key)%26+65) for c in str(t))

random.seed(int(UID))
a = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
random.shuffle(a)
mono_key = "".join(a)
def mono_encrypt(t):
    return "".join(mono_key[ord(c.upper())-65] for c in str(t))
def mono_decrypt(t):
    return "".join(chr(mono_key.index(c.upper())+65) for c in str(t))

vigenere_key = "".join(chr(int(UID[i:i+2]) % 26 + 65) for i in range(0, 10, 2))
def vigenere_encrypt(t):
    r=""
    j=0
    for c in str(t):
        if c.isalpha():
            r+=chr((ord(c.upper())-65+ord(vigenere_key[j%len(vigenere_key)])-65)%26+65)
            j+=1
        else:
            r+=c
    return r

def vigenere_decrypt(t):
    r=""
    j=0
    for c in str(t):
        if c.isalpha():
            r+=chr((ord(c.upper())-65-(ord(vigenere_key[j%len(vigenere_key)])-65))%26+65)
            j+=1
        else:
            r+=c
    return r


playfair_key = ""
for c in vigenere_key:
    if c not in playfair_key:
        playfair_key += c
for c in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
    if c not in playfair_key:
        playfair_key += c

playfair_matrix = [list(playfair_key[i:i+5]) for i in range(0, 25, 5)]

def prepare(t):
    return "".join("I" if c=="J" else c for c in str(t).upper() if c.isalpha())

def pos(c):
    c="I" if c=="J" else c
    for i in range(5):
        for j in range(5):
            if playfair_matrix[i][j]==c:
                return i,j

def make_pairs(t):
    t=prepare(t)
    p=[]
    i=0
    while i<len(t):
        if i==len(t)-1:
            p.append(t[i]+"X")
            i+=1
        elif t[i]==t[i+1]:
            p.append(t[i]+("Q" if t[i]=="X" else "X"))
            i+=1
        else:
            p.append(t[i:i+2])
            i+=2
    return p

def playfair_encrypt(t):
    r=""
    for a,b in make_pairs(t):
        r1,c1=pos(a)
        r2,c2=pos(b)
        if r1==r2:
            r+=playfair_matrix[r1][(c1+1)%5]
            r+=playfair_matrix[r2][(c2+1)%5]
        elif c1==c2:
            r+=playfair_matrix[(r1+1)%5][c1]
            r+=playfair_matrix[(r2+1)%5][c2]
        else:
            r+=playfair_matrix[r1][c2]
            r+=playfair_matrix[r2][c1]
    return r


def playfair_decrypt(t):
    r=""
    for i in range(0,len(t),2):
        a,b=t[i:i+2]
        r1,c1=pos(a)
        r2,c2=pos(b)
        if r1==r2:
            r+=playfair_matrix[r1][(c1-1)%5]
            r+=playfair_matrix[r2][(c2-1)%5]
        elif c1==c2:
            r+=playfair_matrix[(r1-1)%5][c1]
            r+=playfair_matrix[(r2-1)%5][c2]
        else:
            r+=playfair_matrix[r1][c2]
            r+=playfair_matrix[r2][c1]
    return r











def make_hill(uid):
    m = [[int(uid[0:2]) % 26, int(uid[2:4]) % 26],
        [int(uid[4:6]) % 26, int(uid[8:10]) % 26]]
    for r in range(2):
        for c in range(2):
            v = m[r][c]
            for k in range(26):
                x = [row[:] for row in m]
                x[r][c] = (v+k) % 26
                d = (x[0][0]*x[1][1]-x[0][1]*x[1][0]) % 26
                if math.gcd(d,26) == 1:
                    return x
    cells = [(0,0),(0,1),(1,0),(1,1)]
    for i in range(4):
        for j in range(i+1, 4):
            r1,c1 = cells[i]; r2,c2 = cells[j]
            for k1 in range(26):
                for k2 in range(26):
                    x = [row[:] for row in m]
                    x[r1][c1] = (m[r1][c1]+k1) % 26
                    x[r2][c2] = (m[r2][c2]+k2) % 26
                    d = (x[0][0]*x[1][1]-x[0][1]*x[1][0]) % 26
                    if math.gcd(d,26) == 1:
                        return x
    return [[1,0],[0,1]]

hill = make_hill(UID) 

def inverse(n):
    for i in range(1,26):
        if n*i%26==1:
            return i

def hill_encrypt(t):
    t=prepare(t)
    if len(t)%2:
        t+="X"
    r=""
    for i in range(0,len(t),2):
        x,y=ord(t[i])-65,ord(t[i+1])-65
        r+=chr((hill[0][0]*x+hill[0][1]*y)%26+65)
        r+=chr((hill[1][0]*x+hill[1][1]*y)%26+65)
    return r

def hill_decrypt(t):
    det=(hill[0][0]*hill[1][1]-hill[0][1]*hill[1][0])%26
    q=inverse(det)
    a=hill[1][1]*q%26
    b=-hill[0][1]*q%26
    c=-hill[1][0]*q%26
    d=hill[0][0]*q%26
    r=""
    for i in range(0,len(t),2):
        x,y=ord(t[i])-65,ord(t[i+1])-65
        r+=chr((a*x+b*y)%26+65)
        r+=chr((c*x+d*y)%26+65)
    return r


ECC_P = 233
ECC_A = 1
ECC_B = 1
ECC_G = (0, 1)
ECC_ORDER = 79

def ecc_inverse(n, p):
    return pow(n % p, -1, p)

def ecc_add(P, Q, a, p):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P != Q:
        numerator = (y2 - y1) % p
        denominator = (x2 - x1) % p
        slope = (numerator * ecc_inverse(denominator, p)) % p
    else:
        numerator = (3 * x1 * x1 + a) % p
        denominator = (2 * y1) % p
        slope = (numerator * ecc_inverse(denominator, p)) % p
    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return (x3, y3)

def ecc_scalar_multiply(k, P, a, p):
    result = None
    current = P
    while k > 0:
        if k % 2 == 1:
            result = ecc_add(result, current, a, p)
        current = ecc_add(current, current, a, p)
        k //= 2
    return result

def ecc_scalar_multiply_check(k, P, a, p):
    result = None
    for _ in range(k):
        result = ecc_add(result, P, a, p)
    return result

def generate_ecc_private_key():
    return random.randint(1, ECC_ORDER - 1)

def ecc_point_to_string(point):
    if point is None:
        return "INF"
    return "(" + str(point[0]) + "," + str(point[1]) + ")"










random.seed(int(UID))

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m

def is_prime(n):
    //euler
    return True

def generate_prime(low=10000, high=50000):
    while True:
        n = random.randint(low, high)
        if n % 2 == 0:
            n += 1
        while n <= high:
            if is_prime(n):
                return n
            n += 2

def primitive_root(p):
    factors = []
    phi = p - 1
    n = phi
    f = 2
    while f * f <= n:
        if n % f == 0:
            factors.append(f)
            while n % f == 0:
                n //= f
        f += 1
    if n > 1:
        factors.append(n)
    for g in range(2, p):
        valid = True
        for factor in factors:
            if pow(g, phi // factor, p) == 1:
                valid = False
                break
        if valid:
            return g
    return None

def generate_rsa_parameters():
    while True:
        p = generate_prime(1000, 5000)
        q = generate_prime(1000, 5000)
        if p == q:
            continue
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537
        if e >= phi or gcd(e, phi) != 1:
            continue
        d = mod_inverse(e, phi)
        if d is not None:
            return p, q, n, phi, e, d

def rsa_encrypt(message, e, n):
    return pow(message, e, n)
def rsa_decrypt(ciphertext, d, n):
    return pow(ciphertext, d, n)

def generate_elgamal_parameters():
    p = generate_prime(10000, 50000)
    g = primitive_root(p)
    x = random.randint(2, p - 2)
    y = pow(g, x, p)
    return p, g, x, y

def elgamal_encrypt(message, p, g, y):
    k = random.randint(2, p - 2)
    while gcd(k, p - 1) != 1:
        k = random.randint(2, p - 2)
    c1 = pow(g, k, p)
    shared = pow(y, k, p)
    c2 = (message * shared) % p
    return k, c1, c2

def elgamal_decrypt(c1, c2, x, p):
    shared = pow(c1, x, p)
    inverse_shared = mod_inverse(shared, p)
    return (c2 * inverse_shared) % p

def generate_dh_parameters():
    p = generate_prime(10000, 50000)
    g = primitive_root(p)
    a = random.randint(2, p - 2)
    b = random.randint(2, p - 2)
    A = pow(g, a, p)
    B = pow(g, b, p)
    alice_secret = pow(B, a, p)
    bob_secret = pow(A, b, p)
    return p, g, a, A, b, B, alice_secret, bob_secret













import hashlib
import hmac

UID = "2024300027"

def generate_key(uid):
    return hashlib.sha256((uid + "CNS-HMAC-KEY").encode()).digest()

SECRET_KEY = generate_key(UID)

def compute_hash(message, algo):
    return algo(message.encode()).hexdigest()

def compute_hmac(message, key, algo):
    return hmac.new(
        key,
        message.encode(),
        digestmod=algo
    ).hexdigest()

def changed_bits(hex1, hex2):
    b1 = bin(int(hex1, 16))[2:].zfill(len(hex1) * 4)
    b2 = bin(int(hex2, 16))[2:].zfill(len(hex2) * 4)
    return sum(a != b for a, b in zip(b1, b2))

message = input("Enter original message: ")
modified = input("Enter modified message: ")

algorithms = {
    "MD5": hashlib.md5,
    "SHA-1": hashlib.sha1,
    "SHA-256": hashlib.sha256,
    "SHA-512": hashlib.sha512
}

for name, algo in algorithms.items():
    h1 = compute_hash(message, algo)
    h2 = compute_hash(modified, algo)
    print("\n", name)
    print("Original Hash:", h1)
    print("Modified Hash:", h2)
    print("Changed Bits:", changed_bits(h1, h2))

hmac_algorithms = {
    "HMAC-MD5": hashlib.md5,
    "HMAC-SHA1": hashlib.sha1,
    "HMAC-SHA256": hashlib.sha256,
    "HMAC-SHA512": hashlib.sha512
}

for name, algo in hmac_algorithms.items():
    h1 = compute_hmac(message, SECRET_KEY, algo)
    h2 = compute_hmac(modified, SECRET_KEY, algo)
    print("\n", name)
    print("Original HMAC:", h1)
    print("Modified HMAC:", h2)
    print("Changed Bits:", changed_bits(h1, h2))

received_mac = compute_hmac(message, SECRET_KEY, hashlib.sha256)
recalculated_mac = compute_hmac(modified, SECRET_KEY, hashlib.sha256)

if hmac.compare_digest(received_mac, recalculated_mac):
    print("\nMessage is authentic")
else:
    print("\nTampering detected")

