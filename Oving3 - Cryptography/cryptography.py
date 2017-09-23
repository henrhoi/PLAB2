from Oving3 - Cryptography import crypto_utils
import random


__author__ = "Henrik Høiness"


## SUPERKLASSE CIPHER
class Cipher:

    def __init__(self):
        self.alphabet = [chr(x) for x in range(32,127)]

    def encode(self,text,key):
        return

    def decode(self,text,key):
        return

    # Skjekker at input-teksten er lik output-teksten, etter at den er blitt encoded og decoded
    def verify(self,text,key):
        encoded_text = self.encode(text,key)
        decoded_text = self.decode(encoded_text,key)
        return text == decoded_text


## SUPERKLASSE PERSON
class Person:

    # Hver person har en tilhørende key og cipher
    def __init__(self, key, cipher):
        self.key = key
        self.cipher = cipher

    def set_key(self,key):
        self.key = key

    def get_key(self):
        return self.key

    def operate_cipher(self,text):
        return



## SUBKLASSE AV PERSON
class Sender(Person):

    # Krypterer teksten, utfra personens tilhørende cipher og key
    def operate_cipher(self,text):
        self.decoded_text = text
        self.encoded_text = self.cipher.encode(text,self.key)
        return self.encoded_text

    # Sender den krypterte meldingen til mottakeren
    def send_cipher(self,receiver,text):
        # Dersom ciphern er RSA så må mottakeren generere private og offentlige nøkkel, og gir senderen den offentlige nøkkelen
        if isinstance(self.cipher,RSA):
            receiver.generate_keypairs()
            self.key = self.get_receivers_publickey(receiver)

        #Sender den krypterte meldingen, ved å kalle på operate_cipher - som krypterer meldingen
        receiver.recieve_cipher(self.operate_cipher(text))

    # Returnerer mottakerens offentlige nøkkel
    def get_receivers_publickey(self,receiver):
        return receiver.get_publickey()

    # Metode for å gi den encryptede teksten til hackeren vår
    def get_encoded_text(self,text):
        return self.operate_cipher(text)

    #Printer hva senderen har fått inn, og hva han sender ut
    def print_input(self):
        print("Sender:\nInput: "+ str(self.decoded_text) + "\nEncoded text: "+str(self.encoded_text)+"\n")



## SUBKLASSE AV PERSON
class Receiver(Person):

    # Dekrypterer teksten, utfra personens tilhørende cipher og key
    def operate_cipher(self,encoded_text):
        self.encoded_text = encoded_text
        self.decoded_text = self.cipher.decode(encoded_text, self.key)
        return self.decoded_text

    # Mottar kryptert melding fra sender
    def recieve_cipher(self,encoded_text):
        self.operate_cipher(encoded_text)

    # Returnerer sin offentlige nøkkel
    def get_publickey(self):
        return self.public_key

    # Genererer privat og offentlig nøkkel i tupler, i henhold til RSAs oppførsel i oppgavebeskrivelsen
    def generate_keypairs(self):

        p,q = 0,0
        gcd_value = 2
        while p == q or gcd_value != 1:
            p = crypto_utils.generate_random_prime(8)
            q = crypto_utils.generate_random_prime(8)
            phi = (p-1) * (q-1)
            e = random.randint(3, phi-1)
            gcd_value = check_gcd_previous_remainder(e,phi)

        n = p * q
        d = crypto_utils.modular_inverse(e, phi)

        # Offentlig nøkkel
        self.public_key = (n,e)

        # Privat nøkkel
        self.key = (n,d)

    #Printer hva mottakeren har fått inn, og hva han returnerer
    def print_output(self):
        print("Receiver:\nEncoded text: " + str(self.encoded_text) + "\nDecoded text: " + str(self.decoded_text))




## SUBKLASSE AV CIPHER
class Caesar(Cipher):

    # Encoder input-teksten utifra key-en i henhold til Ceasars oppførsel i oppgavebeskrivelsen
    def encode(self,text,key):
        encoded_text = ""

        for character in text:
            new_index = (self.alphabet.index(character)+key) % 95
            encoded_text += self.alphabet[new_index]

        return encoded_text

    # Decoder input-teksten utifra key-en i henhold til Ceasars oppførsel i oppgavebeskrivelsen
    def decode(self,text,key):
        decoded_text = ""

        for character in text:
            new_index = (self.alphabet.index(character)-key) % 95
            decoded_text += self.alphabet[new_index]

        return decoded_text



## SUBKLASSE AV CIPHER
class Multiplicative(Cipher):

    # Encoder input-teksten utifra key-en i henhold til Multiplicatives oppførsel i oppgavebeskrivelsen
    def encode(self,text,key):
        encoded_text = ""

        for character in text:
            new_index = (self.alphabet.index(character)*key) % 95
            encoded_text += self.alphabet[new_index]

        return encoded_text

    # Decoder input-teksten utifra key-en i henhold til Multiplicatives oppførsel i oppgavebeskrivelsen
    def decode(self,text,key):
        new_key = self.generate_inverted_key(key)
        decoded_text = self.encode(text,new_key)

        return decoded_text

    # Genererer den motsatte nøkkelen, slik at den krypterte meldingen kan dekrypteres
    # Gjøres ved modulo invers, som vi har fått tildelt til oppgaven
    def generate_inverted_key(self,key):
        return crypto_utils.modular_inverse(key,95)




## SUBKLASSE AV CIPHER
class Affine(Cipher):

    # Encoder input-teksten utifra key-en i henhold til Affines oppførsel i oppgavebeskrivelsen
    # Først skal input-teksten krypteres med Multiplicative, deretter igjen krypteres med Caesar
    # Key kommer som tupler ~ (k_1, k_2)
    def encode(self,text,key):
        multiplicative = Multiplicative()
        encoded_text_mult = multiplicative.encode(text,key[0])

        caesar = Caesar()
        encoded_text_caesar = caesar.encode(encoded_text_mult,key[1])

        return encoded_text_caesar

    # Motsatt av kryptering!
    # Først skal input-teksten dekrypteres med Caesar, deretter igjen dekrypteres med Multiplicative
    # Key kommer igjen som tupler ~ (k_1, k_2)
    def decode(self,text,key):
        caesar = Caesar()
        decoded_text_caesar = caesar.decode(text,key[1])

        multiplicative = Multiplicative()
        decoded_text_mult = multiplicative.decode(decoded_text_caesar,key[0])

        return decoded_text_mult





## SUBKLASSE AV CIPHER
class Unbreakable(Cipher):

    # Encoder input-teksten utifra key-en i henhold til Unbreakables oppførsel i oppgavebeskrivelsen
    def encode(self,text,key):
        i = 0
        encoded_text = ""
        for character in text:
            # Repterer igjennom nøkkel-ordet, helt til vi har gått igjennom alle tegnene i input-texten
            new_index = (self.alphabet.index(key[i % len(key)]) + self.alphabet.index(character)) % 95
            encoded_text += self.alphabet[new_index]
            i += 1

        return encoded_text

    # Decoder input-teksten utifra key-en i henhold til Unbreakables oppførsel i oppgavebeskrivelsen
    # Lager en ny nøkkel, der jeg gjør det motsatte som i encode()
    def decode(self,text,key):
        new_key = self.generate_inverted_key(key)

        # Kaller på encode, med den nye (motsatte) nøkkelen
        return self.encode(text,new_key)

    # Genererer den motsatte nøkkelen i henhold til nøkkelen som ble brukt til å krypterer meldingen
    def generate_inverted_key(self,key):
        new_key = ""
        for character in key:
            new_key += self.alphabet[(95-self.alphabet.index(character)) % 95]
        return new_key





## SUBKLASSE AV CIPHER
class RSA(Cipher):

    # Encoder input-teksten etter RSAs oppførsel beskrevet i oppgavebeskrivelsen
    # Key kommer som tuple ~ (n, public_key)
    def encode(self,text,key):
        n, public_key = key

        # Deler inn i blokker med 2 bits (b/4 | b = 8 i genereringen av av nøkler)
        blocks = crypto_utils.blocks_from_text(text,2)

        # Lager cipheren (den krypterte meldingen)
        cipher = [pow(t,public_key,n) for t in blocks]
        return cipher

    # Decoder input-teksten etter RSAs oppførsel beskrevet i oppgavebeskrivelsen
    # Key kommer som tuple ~ (n, private_key)
    def decode(self,text,key):
        n, private_key = key

        # Dekrypterer cipheren
        blocks = [pow(t,private_key,n) for t in text]

        # Gjør om fra dekrypterte blokker til tekst
        decoded_text = crypto_utils.text_from_blocks(blocks,2)

        return decoded_text


# Metode som brukes under generering av nøkler, for å skjekke at resten av e og phi, stemmer med det RSA-cipheren krever
def check_gcd_previous_remainder(_a, _b):
        previous_remainder, remainder = _a, _b
        current_x, previous_x, current_y, previous_y = 0, 1, 1, 0
        while remainder > 0:
            previous_remainder, (quotient, remainder) = remainder, divmod(previous_remainder, remainder)
            current_x, previous_x = previous_x - quotient * current_x, current_x
            current_y, previous_y = previous_y - quotient * current_y, current_y
        return previous_remainder


## SUBKLASSE AV PERSON
# Skal Brute-Force seg frem til nøkler for å dekryptere cipherne lagd over (med unntak av RSA)
class Hacker(Person):

    # Får tildelt en cipher, og lager en list med ord ut fra den engelske ordboken
    def __init__(self, cipher):
        self.cipher = cipher
        self.create_wordbook()

    # Åpner filen 'english_words.txt' og lager en liste med alle ordene
    def create_wordbook(self):
        self.wordbook = [line.rstrip('\n') for line in open('english_words.txt')]

    # Skjekker hvilken klasse hackerens tilhørende cipher er
    def get_possibleKeys(self):
        if isinstance(self.cipher, Caesar):
            print("Decoding Caesar-cryptation\n")

            # For å telle antall treff i ordboken til tilhørende mulige nøkkel
            self.count = [0]*95

            # Mulige nøkler
            return [x for x in range(0,95)]

        elif isinstance(self.cipher, Multiplicative):
            print("Decoding Multiplicative-cryptation\n")

            # For å telle antall treff i ordboken til tilhørende mulige nøkkel
            self.count = [0]*95

            # Mulige nøkler
            return [x for x in range(0,95)]

        elif isinstance(self.cipher,Affine):
            print("Decoding Affine-cryptation\n")
            # For å telle antall treff i ordboken til tilhørende mulige nøkkel
            self.count = [0]*9025

            # Mulige nøkler
            return [(x,y) for x in range(0,95) for y in range(0,95)]

        elif isinstance(self.cipher,Unbreakable):
            print("Decoding 'Unbreakable'-cryptation\n ")

            # For å telle antall treff i ordboken til tilhørende mulige nøkkel ~ lengde på count = ordbokens lengde
            self.count = [0]*len(self.wordbook)

            #Returnerer at alle mulige nøkler ligger i ordboken
            return "wordbook"


    # Prøver å dekryptere teksten med alle de mulige nøklene ~ Brute-Force
    def decode_text(self,text):
        print("Encrypted text: \n"+str(text)+"\n")
        possible_keys = self.get_possibleKeys()
        if possible_keys == "wordbook":
            # Splicer bare for å ikke få med siste tomme linje i ordboken (mulig unødvendig)
            possible_keys = self.wordbook[:109583]

        print("Possible keys:")
        for possible_key in possible_keys:

            # Dekoder den krypterte meldingen med hver mulige nøkkel
            decoded_text = self.cipher.decode(text,possible_key)
            for word in decoded_text.split():
                if self.wordbook.__contains__(word):

                    # Teller hvor mange treff i ordboken hver mulige nøkkel får
                    self.count[possible_keys.index(possible_key)] += 1
                    if (self.count[possible_keys.index(possible_key)]) == 1: print(possible_key)

        # Skjekker hvilken av de mulige nøklene som ga flest treff i ordboken
        best_key = possible_keys[self.count.index(max(self.count))]
        print("\nBest key option is: " + str(best_key))

        # Dekoder den krypterte meldingen, med den valgte nøkkelen
        decoded_text = self.cipher.decode(text,best_key)
        print("The decrypted text is: \n"+decoded_text)
        return decoded_text



def main():
    
# Input-tekst som skal krypteres/dekrypteres
    input_text = "coding is cool"
    print("Text to be encrypted: \n"+str(input_text)+"\n")

    caesar = Caesar()
    multiplicative = Multiplicative()
    affine = Affine()
    unbreakable = Unbreakable()
    rsa = RSA()

# Tester Caesar, Multiplicativ og Affine-klassene (bare å endre key og cipher)
    print("Testing Caesar:")
    sender1 = Sender(2,caesar)
    receiver1 = Receiver(2,caesar)
    sender1.send_cipher(receiver1,input_text)

    sender1.print_input()
    receiver1.print_output()


# Tester RSA-klassen:
    print("\nTesting RSA:")
    sender2 = Sender("RSA",rsa)
    receiver2 = Receiver("RSA",rsa)
    sender2.send_cipher(receiver2, input_text)
    sender2.print_input()
    receiver2.print_output()


# Tester Hacker-klassen:
    print("\nTesting Hacker:")
    hacker = Hacker(affine)
    sender = Sender((3,2),affine)

    hacker.decode_text(sender.get_encoded_text(input_text))


main()






