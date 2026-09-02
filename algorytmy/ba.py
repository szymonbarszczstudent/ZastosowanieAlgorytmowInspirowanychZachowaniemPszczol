from algorytmy.wynik_algorytmu import WynikAlgorytmu
class BA:
    def __init__(
            self,
            rozmiar_populacji=20,
            liczba_wybranych_miejsc=6,
            liczba_elitarnych_miejsc=2,
            liczba_elitarnych_rekrutow=6,
            liczba_pozostalych_rekrutow=3,
            poczatkowy_rozmiar_obszaru=3,
    ):
        if not(
            0
            <liczba_elitarnych_miejsc
            <=liczba_wybranych_miejsc
            <=rozmiar_populacji
        ):
            raise ValueError("Niepoprawna liczba miesjc algorytmu.")
        self.rozmiar_populacji = rozmiar_populacji
        self.liczba_wybranych_miejsc =liczba_wybranych_miejsc
        self.liczba_elitarnych_miejsc= liczba_elitarnych_miejsc
        self.liczba_elitarnych_rekrutow = liczba_elitarnych_rekrutow
        self.liczba_pozostalych_rekrutow = liczba_pozostalych_rekrutow
        self.poczatkowy_rozmiar_obszaru = poczatkowy_rozmiar_obszaru
    def optymalizuj(self, problem, generator_losowy, maksymalna_liczba_ocen):
        populacja=[]
        koszty=[]
        historia=[]
        liczba_ocen=0
        najlepsze_rozwiazanie = None
        najnizszy_koszt = float("inf")

        def ocen(rozwiazanie):
            nonlocal liczba_ocen, najlepsze_rozwiazanie, najnizszy_koszt
            koszt = problem.koszt(rozwiazanie)
            liczba_ocen+=1
            if koszt < najnizszy_koszt:
                najnizszy_koszt = koszt
                najlepsze_rozwiazanie = rozwiazanie.copy()
            historia.append(najnizszy_koszt)
            return koszt
        # Tworzenie początkowej populacji losowych rozwiązań.
        for _ in range(self.rozmiar_populacji):
            if liczba_ocen >= maksymalna_liczba_ocen:
                break
            rozwiazanie = problem.losowe_rozwiazanie(generator_losowy)
            populacja.append(rozwiazanie)
            koszty.append(ocen(rozwiazanie))
        while liczba_ocen<maksymalna_liczba_ocen:
            ranking = sorted(
                zip(koszty, populacja),
                key=lambda element: element[0],
            )
            nowa_populacja = []
            nowe_koszty = []
            postep = liczba_ocen/maksymalna_liczba_ocen
            rozmiar_obszaru=max(
                1,
                round(self.poczatkowy_rozmiar_obszaru *( 1- postep)),
            )
            # W najlepszych miejscacn prowadzimy intensywne przeszukiwanie lokalne.
            liczba_przeszukiwanych_miejsc = min(
                self.liczba_wybranych_miejsc,
                len(ranking),
            )
            for indeks_miejsca in range(liczba_przeszukiwanych_miejsc):
                koszt_miejsca, miejsce = ranking[indeks_miejsca]
                najlepsze_lokalne_rozwiazanie = miejsce.copy()
                najnizszy_lokalny_koszt = koszt_miejsca

                if indeks_miejsca< self.liczba_elitarnych_miejsc:
                    liczba_rekrutow = self.liczba_elitarnych_rekrutow
                else:
                    liczba_rekrutow = self.liczba_pozostalych_rekrutow
                for _ in range(liczba_rekrutow):
                    if liczba_ocen>= maksymalna_liczba_ocen:
                        break
                    kandydat = problem.sasiad(
                        miejsce,
                        generator_losowy,
                        rozmiar_obszaru,
                    )
                    koszt_kandydata=ocen(kandydat)
                    if koszt_kandydata<najnizszy_lokalny_koszt:
                        najlepsze_lokalne_rozwiazanie = kandydat
                        najnizszy_lokalny_koszt = koszt_kandydata
                nowa_populacja.append(najlepsze_lokalne_rozwiazanie)
                nowe_koszty.append(najnizszy_lokalny_koszt)
                if liczba_ocen>=maksymalna_liczba_ocen:
                    break
            if liczba_ocen>=maksymalna_liczba_ocen:
                break
            # Pozostałe pszczoły zwiadowczynie eksploruja nowe, losowe miejsca.
            liczba_zwiadowczyn = (
                self.rozmiar_populacji - len(nowa_populacja)
            )

            for _ in range(liczba_zwiadowczyn):
                if liczba_ocen >=maksymalna_liczba_ocen:
                    break
                rozwiazanie = problem.losowe_rozwiazanie(generator_losowy)
                nowa_populacja.append(rozwiazanie)
                nowe_koszty.append(ocen(rozwiazanie))
            populacja = nowa_populacja
            koszty = nowe_koszty

        return WynikAlgorytmu(
                    najlepsze_rozwiazanie=najlepsze_rozwiazanie,
                    najnizszy_koszt=najnizszy_koszt,
                    historia=historia,
                    ocena=liczba_ocen,
                )