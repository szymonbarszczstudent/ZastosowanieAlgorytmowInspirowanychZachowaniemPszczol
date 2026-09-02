import json
import random
from collections import defaultdict
from time import perf_counter
import config
from algorytmy.abc import ABC
from algorytmy.ba import BA
from eksperymenty.pliki_csv import zapisz_do_csv
from eksperymenty.statystyki import utworz_podsumowanie, test_wilcoxona
from eksperymenty.wykresy import utworz_wykres_pudelkowy, utworz_wykres_zbieznosci
from problemy.nHetmanow import ProblemNHetmanow
from problemy.rozmieszczenie_maszyn_wirtualnych import utworz_problem_rozmieszczenia_maszyn

def zbuduj_problemy():
    problemy = [
        ProblemNHetmanow(rozmiar)
        for rozmiar in config.ROZMIARY_PROBLEMU_N_HETMANOW
    ]
    for parametry in config.INSTANCJE_MASZYN_WIRTUALNYCH:
        problemy.append(
            utworz_problem_rozmieszczenia_maszyn(
                parametry["nazwa"],
                parametry["liczba_maszyn_wirtualnych"],
                parametry["liczba_hostow"],
                parametry["ziarno"]
            )
        )
    return problemy

def zbuduj_algorytmy():
    return {
        "ABC": ABC(**config.PARAMETRY_ABC),
        "BA": BA(**config.PARAMETRY_BA),
    }
def uruchom_eksperymenty(liczba_uruchomien=None, maksymalna_liczba_ocen=None):
    liczba_uruchomien = (
        config.LICZBA_URUCHOMIEN
        if liczba_uruchomien is None
        else liczba_uruchomien
    )
    maksymalna_liczba_ocen = (
        config.MAKSYMALNA_LICZBA_OCEN
        if maksymalna_liczba_ocen is None
        else maksymalna_liczba_ocen
    )
    katalog_wynikow = config.WYNIKI
    katalog_wynikow.mkdir(parents=True, exist_ok=True)
    wyniki = []
    historie = defaultdict(lambda: defaultdict(list))
    for problem in zbuduj_problemy():
        print(f"Uruchamiam problem: {problem.nazwa}")
        for nr_uruchomienia in range (liczba_uruchomien):
            ziarno = config.ZIARNO_BAZOWE + nr_uruchomienia
            for nazwa_algorytmu, algorytm in zbuduj_algorytmy().items():
                generator_losowy = random.Random(ziarno)
                czas_rozpoczenia = perf_counter()
                rezultat = algorytm.optymalizuj(problem, generator_losowy, maksymalna_liczba_ocen)
                czas_wykonania = perf_counter() - czas_rozpoczenia
                sredni_koszt_historii = (
                    sum(rezultat.historia)/ len(rezultat.historia)
                )
                wyniki.append({
                    "problem": problem.nazwa,
                    "algorytm": nazwa_algorytmu,
                    "uruchomienie": nr_uruchomienia,
                    "ziarno":ziarno,
                    "najnizszy koszt": round(rezultat.najnizszy_koszt,3),
                    "auc": round(sredni_koszt_historii,3),
                    "czas w sekundach": round(czas_wykonania,3),
                    "liczba ocen": rezultat.ocena,
                    "sukces": problem.czy_rozwiazany(rezultat.najlepsze_rozwiazanie),
                    "najlepsze rozwiazanie":json.dumps(rezultat.najlepsze_rozwiazanie),
                })
                historie[problem.nazwa][nazwa_algorytmu].append(
                    rezultat.historia
                )
    podsumowanie = utworz_podsumowanie(wyniki)
    testy_wilcoxona = test_wilcoxona(wyniki)
    zapisz_do_csv(katalog_wynikow/ "surowe_wyniki.csv", wyniki,)
    zapisz_do_csv(katalog_wynikow/"podsumowanie.csv", podsumowanie,)
    zapisz_do_csv(katalog_wynikow/"testy_wilcoxona.csv", testy_wilcoxona)
    utworz_wykres_pudelkowy(wyniki, katalog_wynikow)
    utworz_wykres_zbieznosci(historie, katalog_wynikow)

    return katalog_wynikow
