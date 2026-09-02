import csv
def zapisz_do_csv(sciezka, wiersze):
    if not wiersze:
        return
    sciezka.parent.mkdir(parents=True, exist_ok=True)
    with sciezka.open(mode="w", newline="", encoding="utf-8") as plik:
        zapisywacz = csv.DictWriter(plik, fieldnames=wiersze[0].keys(),
                                    )
        zapisywacz.writeheader()
        zapisywacz.writerows(wiersze)