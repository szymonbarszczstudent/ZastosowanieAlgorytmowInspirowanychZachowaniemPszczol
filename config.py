from pathlib import Path
LICZBA_URUCHOMIEN = 30
MAKSYMALNA_LICZBA_OCEN = 5000
ZIARNO_BAZOWE = 42
ROZMIARY_PROBLEMU_N_HETMANOW = [8,16]
INSTANCJE_MASZYN_WIRTUALNYCH = [
    {
        "nazwa": "mała instancja VM",
        "liczba_maszyn_wirtualnych": 20,
        "liczba_hostow":8,
        "ziarno":100,
    },
    {
        "nazwa":"duża instancja VM",
        "liczba_maszyn_wirtualnych": 50,
        "liczba_hostow":18,
        "ziarno":200,
    },
]
PARAMETRY_ABC = {
    "liczba_zrodel_pokarmu":20,
    "limit":40,
}
PARAMETRY_BA={
    "rozmiar_populacji":20,
    "liczba_wybranych_miejsc":6,
    "liczba_elitarnych_miejsc":2,
    "liczba_elitarnych_rekrutow":6,
    "liczba_pozostalych_rekrutow":3,
    "poczatkowy_rozmiar_obszaru":3,
}
WYNIKI = Path(__file__).parent / "wyniki"