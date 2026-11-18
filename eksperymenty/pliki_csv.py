import csv
from numbers import Real


def zapisz_do_csv(sciezka, wiersze):
    if not wiersze:
        return

    sciezka.parent.mkdir(parents=True, exist_ok=True)

    def formatuj(wartosc):
        if isinstance(wartosc, Real) and not isinstance(wartosc, (int, bool)):
            return f"{wartosc:.3f}"
        return wartosc

    with sciezka.open(mode="w", newline="", encoding="utf-8") as plik:
        zapisywacz = csv.DictWriter(
            plik,
            fieldnames=wiersze[0].keys(),
        )
        zapisywacz.writeheader()
        zapisywacz.writerows(
            {
                klucz: formatuj(wartosc)
                for klucz, wartosc in wiersz.items()
            }
            for wiersz in wiersze
        )