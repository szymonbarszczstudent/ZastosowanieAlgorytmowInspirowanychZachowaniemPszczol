from collections import defaultdict
from statistics import mean, median, stdev
from scipy.stats import wilcoxon
from statsmodels.stats.multitest import multipletests

MIARY = ["najnizszy koszt","auc","czas w sekundach"]

def utworz_podsumowanie(wiersze):
    grupy = defaultdict(list)
    for wiersz in wiersze:
        klucz = (wiersz["problem"],wiersz["algorytm"])
        grupy[klucz].append(wiersz)
    podsumowanie = []

    for (problem, algorytm), grupa in sorted(grupy.items(), key=lambda element:( str(element[0][0]), str(element[0][1]),),):
        koszty = [wiersz["najnizszy koszt"] for wiersz in grupa]
        auc = [wiersz["auc"] for wiersz in grupa]
        czasy = [wiersz["czas w sekundach"] for wiersz in grupa]
        powodzenia = [wiersz["sukces"] for wiersz in grupa]
        podsumowanie.append(
            {
                "problem": problem,
                "algorytm": algorytm,
                "liczba uruchomien":len(grupa),
                "sredni_najnizszy koszt": round(mean(koszty),3),
                "mediana najnizszego kosztu": round(median(koszty),3),
                "odchylenie standardowe": round(stdev(koszty) if len(koszty) >= 2 else 0.0,3),
                "srednie auc": round(mean(auc),3),
                "sredni czas": round(mean(czasy),3),
                "odsetek powodzen": round(sum(powodzenia)/len(powodzenia),3),
            }
        )
    return podsumowanie

def test_wilcoxona(wiersze, alpha=0.05):
    pogrupowane_wyniki = defaultdict(dict)
    for wiersz in wiersze:
        klucz = (wiersz["problem"], wiersz["ziarno"])
        pogrupowane_wyniki[klucz][wiersz["algorytm"]] =wiersz
    problemy = sorted({wiersz["problem"] for wiersz in wiersze})
    wyniki_testow = []
    for problem in problemy:
        pary_wynikow = [
            wyniki_algorytmow
            for (nazwa_problemu, _), wyniki_algorytmow in pogrupowane_wyniki.items()
            if nazwa_problemu == problem and "ABC" in wyniki_algorytmow and "BA" in wyniki_algorytmow
        ]
        for miara in MIARY:
            roznice = [
                round(para["ABC"][miara] - para["BA"][miara],
                      10,
                )
                for para in pary_wynikow
            ]
            if not roznice:
                continue
            if all(roznica == 0 for roznica in roznice):
                statystyka = 0.0
                surowa_wartosc_p = 1.0
            else:
                statystyka, surowa_wartosc_p = wilcoxon(roznice)
            wyniki_testow.append(
                {
                    "problem": problem,
                    "miara": miara,
                    "liczba par": len(roznice),
                    "statystyka": statystyka,
                    "surowa wartosc p": round(surowa_wartosc_p,3),
                    "mediana roznicy abc-ba": round(median(roznice),3),
                }
            )
    if not wyniki_testow:
        return []
    _, skorygowane_wartosci_p, _, _ = multipletests(
        [
            wynik_testu["surowa wartosc p"]
            for wynik_testu in wyniki_testow
        ]
    )
    for wynik_testu, wartosc_p_po_korekcie in zip(
        wyniki_testow,
        skorygowane_wartosci_p,
    ):
        wynik_testu["wartosc p po korekcie"] = round(wartosc_p_po_korekcie,3)
        wynik_testu["wniosek"] = wniosek(
            wynik_testu["mediana roznicy abc-ba"],
            wartosc_p_po_korekcie,
            alpha,
        )
    return wyniki_testow
def wniosek(mediana_roznicy, wartosc_p, poziom_istotnosci):
    if wartosc_p >= poziom_istotnosci or mediana_roznicy == 0:
        return "Brak istotnej różnicy."
    if mediana_roznicy < 0:
        return "ABC ma lepszy wynik."
    return "BA ma lepszy wynik."
