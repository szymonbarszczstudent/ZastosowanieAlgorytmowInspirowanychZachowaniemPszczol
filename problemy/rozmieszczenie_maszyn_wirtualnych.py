import math
import random
import numpy as np
class ProblemRozmieszczeniaMaszynWirtualnychNaHostachFizycznychWChmurze:
    def __init__(self, nazwa, maszyny_wirtualne, hosty):
        self.nazwa = nazwa
        self.maszyny_wirtualne = maszyny_wirtualne
        self.hosty = hosty

    def losowe_rozwiazanie(self, generator_losowy):
        liczba_hostow = len(self.hosty)
        return [
            generator_losowy.randrange(liczba_hostow)
            for _ in self.maszyny_wirtualne
        ]
    def sasiad(self, rozwiazanie, generator_losowy, sila=1):
                kandydat = rozwiazanie.copy()
                liczba_hostow = len(self.hosty)

                if liczba_hostow < 2:
                    return kandydat

                for _ in range(sila):
                    indeks_maszyny = generator_losowy.randrange(len(kandydat))
                    start_host = kandydat[indeks_maszyny]
                    nowy_host = generator_losowy.randrange(liczba_hostow-1)

                    if nowy_host >= start_host:
                        nowy_host+=1
                    kandydat[indeks_maszyny] = nowy_host
                return kandydat
    def _oblicz_wykorzystanie_zasobow(self, rozwiazanie):
        wykorzystanie_cpu  = [0] * len(self.hosty)
        wykorzystanie_ram = [0] * len(self.hosty)

        for indeks_maszyny, indeks_hosta in enumerate(rozwiazanie):
            maszyna = self.maszyny_wirtualne[indeks_maszyny]
            wykorzystanie_cpu[indeks_hosta]+=(maszyna["cpu"])
            wykorzystanie_ram[indeks_hosta]+=(maszyna["ram"])
        return wykorzystanie_cpu, wykorzystanie_ram

    def koszt(self, rozwiazanie):
        (
            wykorzystanie_cpu,
            wykorzystanie_ram
        ) = self._oblicz_wykorzystanie_zasobow(rozwiazanie)

        przekroczenie_zasobow = 0.0
        obciazenia = []

        for indeks, host in enumerate(self.hosty):
            stosunek_cpu = (wykorzystanie_cpu[indeks]/host["cpu"])
            stosunek_ram = (wykorzystanie_ram[indeks]/host["ram"])
            przekroczenie_zasobow+=max(0.0,stosunek_cpu-1.0)
            przekroczenie_zasobow+=max(0.0,stosunek_ram-1.0)
            host_jest_aktywny = (
                wykorzystanie_cpu[indeks]>0
                or wykorzystanie_ram[indeks]>0
            )
            if host_jest_aktywny:
                srednie_obciazenie=(
                    stosunek_cpu+stosunek_ram
                )/2.0
                obciazenia.append(srednie_obciazenie)
        liczba_aktywnych_hostow = len(obciazenia)
        nierownomiernosc_obciazenia = float(np.std(obciazenia)) if obciazenia else 0.0
        # Najpierw wykonalność, a następnie liczba aktywnych hostów.
        # Dopiero na końcu równomierność ich obciążenia.
        return (
            1000.0*przekroczenie_zasobow+liczba_aktywnych_hostow+nierownomiernosc_obciazenia
        )

    def czy_rozwiazany(self, rozwiazanie):
        (
            wykorzystanie_cpu,
            wykorzystanie_ram
        ) = self._oblicz_wykorzystanie_zasobow(rozwiazanie)
        for indeks, host in enumerate(self.hosty):
            if wykorzystanie_cpu[indeks] > host["cpu"]:
                return False
            if wykorzystanie_ram[indeks] > host["ram"]:
                return False
        return True

def utworz_problem_rozmieszczenia_maszyn(nazwa, liczba_maszyn, liczba_hostow, ziarno_losowosci):
    generator_losowy =random.Random(ziarno_losowosci)
    dozwolone_rozmiary = [(1,2),(2,4),(4,8),(6,12),(8,16)]
    maszyny_wirtualne = []
    for id_maszyny in range(liczba_maszyn):
        liczba_cpu, ilosc_ram = generator_losowy.choice(dozwolone_rozmiary)
        maszyny_wirtualne.append({
            "id":id_maszyny,
            "cpu":liczba_cpu,
            "ram":ilosc_ram,
        })
    hosty = []

    for id_hosta in range(liczba_hostow):
        hosty.append({
            "id":id_hosta,
            "cpu":16,
            "ram":32,
        })
    laczna_liczba_cpu = sum(maszyna["cpu"] for maszyna in maszyny_wirtualne)
    laczna_ilosc_ram = sum(maszyna["ram"] for maszyna in maszyny_wirtualne)
    laczna_pojemnosc_cpu = sum(host["cpu"] for host in maszyny_wirtualne)
    laczna_pojemnosc_ram = sum(host["ram"] for host in maszyny_wirtualne)

    if laczna_liczba_cpu > laczna_pojemnosc_cpu or laczna_ilosc_ram >laczna_pojemnosc_ram:
        raise ValueError("Instancja ma za mało zasobów hostów.")
    return ProblemRozmieszczeniaMaszynWirtualnychNaHostachFizycznychWChmurze(
        nazwa,
        maszyny_wirtualne,
        hosty,
    )