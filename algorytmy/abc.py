from algorytmy.wynik_algorytmu import WynikAlgorytmu
class ABC:
    def __init__(self, liczba_zrodel_pokarmu=20, limit=40):
        self.liczba_zrodel_pokarmu = liczba_zrodel_pokarmu
        self.limit = limit
    def optymalizuj(self, problem, generator_losowy, maksymalna_liczba_ocen):
        zrodla = []
        koszty = []
        liczby_prob = []
        historia = []
        liczba_ocen = 0
        najlepsze_rozwiazanie = None
        najnizszy_koszt = float('inf')

        def ocena(rozwiazanie):
            nonlocal liczba_ocen, najlepsze_rozwiazanie, najnizszy_koszt
            koszt = problem.koszt(rozwiazanie)
            liczba_ocen+=1
            if koszt < najnizszy_koszt:
                najnizszy_koszt = koszt
                najlepsze_rozwiazanie = rozwiazanie.copy()
            historia.append(najnizszy_koszt)
            return koszt
# Tworzenie początkowytch, losowych źródeł pokarmu.
        for _ in range(self.liczba_zrodel_pokarmu):
            if liczba_ocen>=maksymalna_liczba_ocen:
                break
            rozwiazanie = problem.losowe_rozwiazanie(generator_losowy)
            zrodla.append(rozwiazanie)
            koszty.append(ocena(rozwiazanie))
            liczby_prob.append(0)

        while liczba_ocen < maksymalna_liczba_ocen:
            # Pszczoły zatrudnione przeszukują sąsiedztwo każdego źródła.
            for indeks in range(len(zrodla)):
                if liczba_ocen >= maksymalna_liczba_ocen:
                    break
                kandydat = problem.sasiad(
                    zrodla[indeks],
                    generator_losowy,
                )
                koszt_kandydata = ocena(kandydat)
                self._zachlanna_aktualizacja(
                    indeks,
                    kandydat,
                    koszt_kandydata,
                    zrodla,
                    koszty,
                    liczby_prob,
                )
            # Pszczoły obserwatorki częściej wybierają lepsze źródła pokarmu.
            for _ in range(len(zrodla)):
                if liczba_ocen >=maksymalna_liczba_ocen:
                    break
                wagi = [1.0/(1.0+koszt) for koszt in koszty]
                indeks = generator_losowy.choices(
                    range(len(zrodla)),
                    weights=wagi,
                    k=1,
                )[0]
                kandydat = problem.sasiad(
                    zrodla[indeks],
                    generator_losowy,
                )
                koszt_kandydata = ocena(kandydat)
                self._zachlanna_aktualizacja(
                    indeks,
                    kandydat,
                    koszt_kandydata,
                    zrodla,
                    koszty,
                    liczby_prob,
                )
            # Porzucone źródła są zastępowane losowymi roziwązaniami.
            for indeks in range(len(zrodla)):
                if liczba_ocen >= maksymalna_liczba_ocen:
                    break
                if liczby_prob[indeks]>=self.limit:
                    rozwiazanie=problem.losowe_rozwiazanie(generator_losowy)
                    zrodla[indeks]=rozwiazanie
                    koszty[indeks]=ocena(rozwiazanie)
                    liczby_prob[indeks]=0
        return WynikAlgorytmu(
            najlepsze_rozwiazanie=najlepsze_rozwiazanie,
            najnizszy_koszt=najnizszy_koszt,
            historia=historia,
            ocena=liczba_ocen,
        )
    @staticmethod
    def _zachlanna_aktualizacja(
            indeks,
            kandydat,
            koszt_kandydata,
            zrodla,
            koszty,
            liczby_prob,
    ):
        if koszt_kandydata<koszty[indeks]:
            zrodla[indeks]=kandydat
            koszty[indeks]=koszt_kandydata
            liczby_prob[indeks]=0
        else:
            liczby_prob[indeks]+=1
