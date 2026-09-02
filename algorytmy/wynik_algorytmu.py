from dataclasses import dataclass
@dataclass
class WynikAlgorytmu:
    najlepsze_rozwiazanie: list[int]
    najnizszy_koszt: float
    historia: list[float]
    ocena: int