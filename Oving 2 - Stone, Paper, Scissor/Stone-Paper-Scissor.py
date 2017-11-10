import random
import matplotlib.pyplot as plt
__author__ = "Henrik Høiness"


class Aksjon:

    def __init__(self, action):
        #0 - stein, 1 - saks, 2 - papir
        self.action = action

    #Equals
    def __eq__(self, other):
        return self.action == other.action

    #Greater than
    def __gt__(self, other):
        a = {0:2,1:0,2:1}
        return a[self.action] != other.action

    def __str__(self):
        ordliste = ["Stein", "Saks", "Papir"]
        return ordliste[self.action]

    def getAction(self):
        return self.action


class Spiller:

    #Lager en dictionary med info om alle Spilleres trekk.
    # På formatet {Spiller1: [0,1,2,1,2], Spiller2: [0,2,3,1,2]}
    spiller_info = {}

    _trekk = {0:"Stein",1:"Saks",2:"Papir"}

    def __init__(self, spillernavn):
        self.spillernavn =  spillernavn
        Spiller.spiller_info[self] = []


    def velg_aksjon(self, motstander):
        return

    #Her mottas resultat fra hvert enkelt spill. Legger til i dictionarien
    def motta_resultat(self, motstander, trekk):
        Spiller.spiller_info[motstander].append(trekk)


    def oppgi_navn(self,navn):
        self.spillernavn = navn

    def __str__(self):
        return self.spillernavn




class Tilfeldig(Spiller):

    def __init__(self, spillernavn):
        Spiller.__init__(self,spillernavn)

    def velg_aksjon(self, motstander):
        return Aksjon(random.randint(0,2))



class Sekvensiell(Spiller):

    def __init__(self, spillernavn):
        Spiller.__init__(self,spillernavn)
        self.a = 0

    def velg_aksjon(self, motstander):
        aksjon = Aksjon(self.a%3)
        self.a += 1
        return aksjon


class MestVanlig(Spiller):

    def __init__(self, spillernavn):
        Spiller.__init__(self,spillernavn)

    def velg_aksjon(self,motstander):
        antall_trekk = [0,0,0]

        if (len(Spiller.spiller_info[motstander])>0):
            for trekk in Spiller.spiller_info[motstander]:
                antall_trekk[trekk.getAction()] += 1

        if antall_trekk != [0,0,0]:
            return Aksjon(motsatt_trekk(antall_trekk.index(max(antall_trekk))))

        return Aksjon(random.randint(0,2))


#Returnerer det motsatte trekket av det som blir sendt inn i funksjonen
def motsatt_trekk(num):
    a = {0: 2, 1: 0, 2: 1}
    return a[num]


class Historiker(Spiller):

    def __init__(self, spillernavn, husk):
        Spiller.__init__(self,spillernavn)
        self.husk = husk

    def velg_aksjon(self, motstander):
        historie = Spiller.spiller_info[motstander]

        subsequence = historie[-self.husk:]

        #[Stein, saks, papir]
        neste_trekk = [0,0,0]

        for i in range(len(historie) - self.husk): #minus husk fordi vi må stoppe når vi har de husk-siste elementene i listen

            #sjekker om det finnes en subsequence som er lik subsequencen med lengde husk
            if historie[i:i+self.husk] == subsequence:

                #Dersom neste_trekk etter subsequence, plusser på tilsvarende plass i listen
                neste_trekk[historie[i+self.husk].getAction()] += 1


        # OBS: Velger første og største i listen, ikke det største trekket som ble gjort sist
        if neste_trekk != [0,0,0]:
            return Aksjon(motsatt_trekk(neste_trekk.index(max(neste_trekk))))

        return Aksjon(random.randint(0,2))


# __init__ (self, spiller1, spiller2): Initiere en instans av klassen, der spiller1 og spiller2 er de to spillerne.
# gjennomfoer spill: Spør hver spiller om deres valg. Bestem resultatet ut fra regelen at det gis ett poeng til vinneren og null poeng til taperen (ved uavgjort f ̊ar begge spillere et halvt poeng). Rapporter valgene og resul- tatene tilbake til spillerne.
# __str__     : Tekstlig rapportering av enkelt-spillet: Hva ble valgt, og hvem vant?

class EnkeltSpill:

    #Lager et enkeltspill for to eksisterende spillere
    def __init__(self, spiller1, spiller2):
        self.spiller1 = spiller1
        self.spiller2 = spiller2
        self.poeng = [0,0]
        self.vinner = ""


    def gjennomfoer_spill(self):
        self.action1 = self.spiller1.velg_aksjon(self.spiller2)
        self.action2 = self.spiller2.velg_aksjon(self.spiller1)

        #Tildeler poeng utifra regler
        if self.action1 == self.action2:
            self.poeng = [0.5,0.5]
            self.vinner = "Uavgjort"

        elif self.action1 > self.action2:
            self.poeng = [1,0]
            self.vinner = ""+str(self.spiller1) + " vinner"

        elif self.action2 > self.action1:
            self.poeng = [0,1]
            self.vinner = ""+str(self.spiller2) + " vinner"

        self.spiller1.motta_resultat(self.spiller2,self.action2)
        self.spiller2.motta_resultat(self.spiller1,self.action1)


    def __str__(self):
        rapport = str(self.spiller1) + ": " + str(self.action1)+".  " + str(self.spiller2) + ": " + str(self.action2) + ". ->  " + str(self.vinner)
        return rapport

# • init (self, spiller1, spiller2, antall spill):
#           Sette opp instansen med de to spillerne, og husker at de skal spille antall spill ganger mot hverandre.

# • arranger enkeltspill:
#       For  ̊a arrangere et enkelt spill m ̊a systemet spørre begge spillere om hvilken aksjon de velger, sjekke hvem som vant,
#       rapportere val- gene og resultatet tilbake til spillerne,
#       og gi en tekstuell beskrivelse av resultatet for eksempel i form av en enkelt linje: Historiker(2):  Stein.  MestVanlig:  Saks -> Historiker(2) vinner

# Merk at mye av denne funksjonaliteten ligger i klassen EnkeltSpill, slik at MangeSpill.arranger_enkeltspill kan hente
# det meste av sin funksjonalitet derfra.

# • arranger turnering: Gjennomføre antall spill enkelt-spill mellom de to spillerne. Rapportere gevinst-prosenten for hver av dem
#       n̊ar turneringen er ferdig. Det er ogs ̊a interessant  ̊a vise hvordan gevinst-prosenten utvikler seg over tid
#       (se Figure 2, som viser score for Historiker(2) mot MestVanlig over 100 spill). Dette gjøres lettest ved  ̊a importere matplotlib.pyplot
#       og bruke plot-metoden derfra.


class MangeSpill:

    def __init__(self, spiller1, spiller2, antall_spill):
        self.spiller1 = spiller1
        self.spiller2 = spiller2
        self.antall_spill = antall_spill
        self.resultat = [0,0]
        self.gevinstprosent = [0,0]

    def arranger_enkeltspill(self):
        enkeltspill = EnkeltSpill(self.spiller1,self.spiller2)
        enkeltspill.gjennomfoer_spill()
        print(enkeltspill)
        return enkeltspill.poeng

    def arranger_turnering(self):
        #Antall spill gjort
        x_akse = []

        #Prosentandel i gevist
        y_akse = []

        spill_gjennomfoert = 0

        for x in range(self.antall_spill):
            spill_gjennomfoert += 1
            poeng = self.arranger_enkeltspill()
            self.resultat[0] = self.resultat[0] + poeng[0]
            self.resultat[1] = self.resultat[1] + poeng[1]
            self.gevinstprosent[0] = self.resultat[0]/spill_gjennomfoert
            self.gevinstprosent[1] = self.resultat[1]/spill_gjennomfoert

            #PYPLOT
            x_akse.append(spill_gjennomfoert)
            y_akse.append(self.gevinstprosent[0])

        print("\nTotal score i turneringen:\n" + str(self.spiller1) + ": " + str(self.resultat[0]) + " poeng" +
              "\n" + str(self.spiller2) + ": " + str(self.resultat[1]) + " poeng")
        #PYPLOT-spiller1
        plt.plot(x_akse, y_akse)

                #X-akse fra 0 til antall spill & Y-akse fra 0 til 1
        plt.axis([0,self.antall_spill,0,1])
        plt.grid(True)
        plt.axhline(y=0.5,linewidth=0.5, color="m")
        plt.xlabel("Antall spill")
        plt.ylabel("Gevinstprosent for " + str(self.spiller1))
        plt.show()






def main():
    spiller1 = Tilfeldig("Henrik")
    spiller2 = Sekvensiell("Kristoffer")
    spiller3 = MestVanlig("Martin")
    spiller4 = Historiker("Vilde",2)
    spill = MangeSpill(spiller4,spiller2,100)
    spill.arranger_turnering()



main()
