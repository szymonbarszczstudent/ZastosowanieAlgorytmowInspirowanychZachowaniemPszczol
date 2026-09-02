class ProblemNHetmanow:
    def __init__(self,rozmiar):
        if rozmiar < 4:
            raise ValueError("Liczba hetmanów musi być co najmniej = 4.")
        self.rozmiar = rozmiar
        self.nazwa = f"problem{rozmiar}hetmanow"
    def losowe_rozwiazanie(self, generator_losowy):
        rozwiazanie = list(range(self.rozmiar))
        generator_losowy.shuffle(rozwiazanie)
        return rozwiazanie
    def sasiad(self, rozwiazanie, generator_losowy, sila=1):
        kandydat = rozwiazanie.copy()
        for _ in range(sila):
            kolumny_w_konflikcie = self._znajdz_kolumny_w_konflikcie(kandydat)

            if kolumny_w_konflikcie:
                pierwsza_kolumna = generator_losowy.choice(kolumny_w_konflikcie)
            else:
                pierwsza_kolumna = generator_losowy.randrange(self.rozmiar)
                mozliwe_kolumny = [
                    kolumna
                    for kolumna in range(self.rozmiar)
                    if kolumna != pierwsza_kolumna
                ]
                druga_kolumna = generator_losowy.choice(mozliwe_kolumny)
                kandydat[pierwsza_kolumna], kandydat[druga_kolumna]=kandydat[druga_kolumna], kandydat[pierwsza_kolumna]
        return kandydat
    def koszt(self, rozwiazanie):
        liczba_konfliktow = 0
        for pierwsza_kolumna in range(self.rozmiar):
            for druga_kolumna in range(pierwsza_kolumna+1, self.rozmiar):
                odleglosc_wierszy = abs(rozwiazanie[pierwsza_kolumna]- rozwiazanie[druga_kolumna])
                odleglosc_kolumn = druga_kolumna - pierwsza_kolumna

                if odleglosc_wierszy == odleglosc_kolumn:
                    liczba_konfliktow += 1
        return float(liczba_konfliktow)
    def czy_rozwiazany(self, rozwiazanie):
        return self.koszt(rozwiazanie) == 0
    def _znajdz_kolumny_w_konflikcie(self, rozwiazanie):
        kolumny_w_konflikcie = set()
        for pierwsza_kolumna in range(self.rozmiar):
            for druga_kolumna in range(pierwsza_kolumna+1, self.rozmiar):
                odleglosc_wierszy = abs(rozwiazanie[pierwsza_kolumna]-rozwiazanie[druga_kolumna])
                odleglosc_kolumn = druga_kolumna - pierwsza_kolumna

                if odleglosc_wierszy == odleglosc_kolumn:
                    kolumny_w_konflikcie.add(pierwsza_kolumna)
                    kolumny_w_konflikcie.add(druga_kolumna)
        return list(kolumny_w_konflikcie)