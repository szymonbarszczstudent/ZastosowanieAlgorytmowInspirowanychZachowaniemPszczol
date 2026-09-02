from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
KOLORY = {
    "ABC": "#1f77b4",
    "BA": "#ff7f0e",
}

def utworz_wykres_pudelkowy(wiersze, katalog_wyjscia):
    pogrupowane_wyniki = defaultdict(lambda: defaultdict(list))
    for wiersz in wiersze:
        problem = wiersz["problem"]
        algorytm = wiersz["algorytm"]
        pogrupowane_wyniki[problem][algorytm].append(wiersz)
    katalog_wyjscia.mkdir(parents=True, exist_ok=True)
    for problem, algorytmy in pogrupowane_wyniki.items():
        nazwy_algorytmow = [
            nazwa for nazwa in ("ABC", "BA")
            if nazwa in algorytmy
        ]
        if not nazwy_algorytmow:
            continue
        rysunek, osie = plt.subplots(1, 2, figsize=(10, 4))
        ustawienia_miar = [
            (
                osie[0],
                "najnizszy koszt",
                "Najnizszy koszt",
            ),
            (
                osie[1],
                "auc",
                "Średni koszt w trakcie wyszukiwania AUC",
            ),
        ]
        for os, miara, tytul in ustawienia_miar:
            wartosci = []
            for nazwa_algorytmu in nazwy_algorytmow:
                seria = np.asarray(
                    [
                        wiersz[miara]
                        for wiersz in algorytmy[nazwa_algorytmu]
                        if wiersz.get(miara) is not None
                    ],
                    dtype = float,
                ).reshape(-1)
                wartosci.append(seria)
            pozycje = np.arange(1, len(nazwy_algorytmow)+1)
            wykresy_pudelkowe = os.boxplot(
            wartosci,
            positions=pozycje,
            patch_artist=True,
            )
            os.set_xticks(pozycje)
            os.set_xticklabels(nazwy_algorytmow)

            for pudelko, nazwa_algorytmu in zip(
                wykresy_pudelkowe["boxes"],
                nazwy_algorytmow,
            ):
                pudelko.set_facecolor(KOLORY[nazwa_algorytmu])
                pudelko.set_alpha(0.7)
            os.set_title(tytul)
            os.set_ylabel("Mniejsza wartość oznacza lepszy wynik.")
            os.grid(axis="y", alpha=0.3)
        rysunek.suptitle(str(problem))
        rysunek.tight_layout()

        sciezka_wyjscia = (katalog_wyjscia/f"wykres_pudelkowy_{problem}.png")
        rysunek.savefig(sciezka_wyjscia, dpi=160)
        plt.close(rysunek)
def utworz_wykres_zbieznosci(hisorie, katalog_wyjscia):
    for problem, algorytmy in hisorie.items():
        rysunek, os = plt.subplots(figsize=(8,5))
        for nazwa_algorytmu in ("ABC", "BA"):
            macierz_wynikow = np.array(
                algorytmy[nazwa_algorytmu],
                dtype=float,
            )
            mediana = np.median(macierz_wynikow, axis=0)
            pierwszy_kwartyl = np.percentile(macierz_wynikow, 25, axis=0,)
            trzeci_kwartyl = np.percentile(macierz_wynikow, 75, axis=0,)
            liczby_ocen = np.arange(1, macierz_wynikow.shape[1]+1,)
            os.plot(
                liczby_ocen,
                mediana,
                label=nazwa_algorytmu,
                color=KOLORY[nazwa_algorytmu],
            )
            os.fill_between(
                liczby_ocen,
                pierwszy_kwartyl,
                trzeci_kwartyl,
                color=KOLORY[nazwa_algorytmu],
                alpha=0.18,
            )
        os.set_title(f"Zbieżność algortymów - {problem}")
        os.set_xlabel("Liczba ocen funkcji celu")
        os.set_ylabel("Najniższy dotychczasowy koszy")
        os.grid(alpha=0.3)
        os.legend(title="Mediana oraz przedział międzykwartylowy")

        rysunek.tight_layout()
        sciezka_wyjscia = (katalog_wyjscia/f"zbieznosc_{problem}.png")
        rysunek.savefig(sciezka_wyjscia, dpi=160)
        plt.close(rysunek)