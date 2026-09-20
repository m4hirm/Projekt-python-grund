"""
auth.py
Fejkad inloggning — bara för känslan av att logga in.
Ingen riktig kontroll mot sparade uppgifter, all input accepteras.
"""


def fake_inloggning():
    """Frågar efter användarnamn och lösenord och låtsas logga in, oavsett vad som skrivs."""
    anvandarnamn = input("Användarnamn: ")
    losenord = input("Lösenord: ")
    print(f"Inloggad som {anvandarnamn}!")
    return anvandarnamn


if __name__ == "__main__":
    fake_inloggning()