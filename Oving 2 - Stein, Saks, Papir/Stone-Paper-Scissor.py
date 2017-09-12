


class Aksjon:

    def __init__(self, action):
        self.action = action

    #Equals
    def __eq__(self, other):
        return self.action == other.action

    #Greater than
    def __gt__(self, other):
        if self.action == 'Stein' and other.action =='Saks':
            return True

        elif self.action == 'Saks' and other.action == 'Papir':
            return True

        elif self.action == 'Papir' and other.action == 'Stein':
            return True

        return False


class Spiller:




class Tilfeldig(Spiller):





class Sekvensiell(Spiller):





class MestVanlig(Spiller):





class Historiker(Spiller):





class EnkeltSpill:





class MangeSpill:





def main():
    a = Aksjon('Stein')
    b = Aksjon('Papir')
    print(b<a)


main()
