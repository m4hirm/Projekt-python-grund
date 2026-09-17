
class Anvandare:
    """Föräldraklass. Innehåller det som är gemensamt för alla användare."""

    def __init__(self, namn, epost):
        self.namn = namn
        self.epost = epost

    def visa_info(self):
        """Basversionen. Barnklasserna kommer bygga vidare på den här."""
        return f"Namn: {self.namn}\nE-post: {self.epost}"

    def __str__(self):
        return self.visa_info()


class Arbetssokande(Anvandare):
    """Barnklass. Ärver allt från Anvandare och lägger till CV-relaterad data."""

    def __init__(self, namn, epost, kompetenser=None):
        # super() = "kör förälderns __init__ först, så slipper jag skriva om namn/epost"
        super().__init__(namn, epost)
        self.kompetenser = kompetenser if kompetenser is not None else []

    def lagg_till_kompetens(self, kompetens):
        self.kompetenser.append(kompetens)

    def visa_info(self):
        # Override: vi återanvänder förälderns metod och bygger vidare på den
        basinfo = super().visa_info()
        kompetens_lista = ", ".join(self.kompetenser) if self.kompetenser else "Inga registrerade"
        return f"{basinfo}\nTyp: Arbetssökande\nKompetenser: {kompetens_lista}"


class Arbetsgivare(Anvandare):
    """Barnklass. Ärver allt från Anvandare och lägger till företagsdata."""

    def __init__(self, namn, epost, foretagsnamn, org_nummer):
        super().__init__(namn, epost)
        self.foretagsnamn = foretagsnamn
        self.org_nummer = org_nummer
        self.annonser = []  # här samlar vi annonserna arbetsgivaren skapar

    def skapa_annons(self, titel, beskrivning, krav):
        annons = Jobbannons(titel, beskrivning, krav, self)
        self.annonser.append(annons)
        return annons

    def visa_info(self):
        basinfo = super().visa_info()
        return f"{basinfo}\nTyp: Arbetsgivare\nFöretag: {self.foretagsnamn} (org.nr {self.org_nummer})"


class Jobbannons:
    """
    Fristående klass, inte en del av arvskedjan.
    En annons 'har en' Arbetsgivare (komposition) snarare än att 'vara en'.
    """

    def __init__(self, titel, beskrivning, krav, arbetsgivare):
        self.titel = titel
        self.beskrivning = beskrivning
        self.krav = krav  # lista med strängar, t.ex. ["Python", "SQL"]
        self.arbetsgivare = arbetsgivare  # referens till ett Arbetsgivare-objekt

    def matcha(self, arbetssokande):
        """
        Enkel matchningslogik: hur många av annonsens krav
        finns med i den sökandes kompetenser?
        """
        matchande_krav = [k for k in self.krav if k in arbetssokande.kompetenser]
        if not self.krav:
            return 0.0
        return round(len(matchande_krav) / len(self.krav) * 100, 1)

    def __str__(self):
        return f"{self.titel} @ {self.arbetsgivare.foretagsnamn} (krav: {', '.join(self.krav)})"


# Litet självtest — kör "python models.py" för att se att allt hänger ihop
if __name__ == "__main__":
    sokande = Arbetssokande("Maher", "maher@example.com")
    sokande.lagg_till_kompetens("Python")
    sokande.lagg_till_kompetens("SQL")

    arbetsgivare = Arbetsgivare(
        "Anna Chef", "anna@foretag.se",
        foretagsnamn="TechAB", org_nummer="556677-8899"
    )
    annons = arbetsgivare.skapa_annons(
        titel="Junior Pythonutvecklare",
        beskrivning="Vi söker en junior utvecklare.",
        krav=["Python", "SQL", "Git"]
    )

    print(sokande.visa_info())
    print()
    print(arbetsgivare.visa_info())
    print()
    print(annons)
    print(f"Matchningsgrad för {sokande.namn}: {annons.matcha(sokande)}%")