# Wprowadzone zmiany

- Naprawiono poważny błąd w programie, przez który każda ewaluacja osobnika zależała od poprzedniej.

Po naprawieniu tego błędu, algorytm znacznie lepiej radzi sobie z prowizją.
Okazało się, że aktualnie najlepszym algorytmem do optymalizacji jest NSGA2.
- Dodano wykresy w 3D przedstawiające zbieżność obu metryk, MDD oraz ROI.
- Przerobiono kod ekstraktorów cech, żeby dało się nimi łatwiej manipulować.
- Dodano możliwość konfiguracji eksperymentu za pomocą pliku JSON. Poniżej przykładtakiego pliku:
```json
{
    "seed": 106,
    "n_gen": 100,
    "processes": 6,

    "population_size": 400,
    "start_money": 1000,
 
    "slice_count": 5,
    "slice_size": 20,
    "slice_overlap": 5,

    "use_polynomial_extractor": true,
    "polynomial_degree": 5,

    "use_exponential_extractor": true,
    "exp_parameters_per_slice": 4,

    "use_mdd_extractor": true
}
```
Wraz z rozwojem programu, będę zmieniane/dokładane nowe pola.
- Uwspółbieżniono ewaluację populacji, dzięki temu można przeprowadzać dłuższe i większe eksperymenty w znacznie krótszym czasie.

# Aktualne wyniki

Przeprowadzono eksperyment z użyciem NSGA2 na populacji liczącej 400 osobniów trwający 100 iteracji na kursie franka.
Eksperyment zają około 40 minut. Poniżej przedstawiono wybranych osobników z populacji:

![nsga2_history.png](Images%2FRaports%2FRaport6%2FPOP%2FFigure_1.png)
![nsga2_history.png](Images%2FRaports%2FRaport6%2FPOP%2FFigure_6.png)
![nsga2_history.png](Images%2FRaports%2FRaport6%2FPOP%2FFigure_9.png)

Poniżej znajdują się kolejne metryki zbierzności dla ROI oraz MDD:

![nsga2_history.png](Images%2FRaports%2FRaport6%2FCOV_ROI.PNG)
![nsga2_history.png](Images%2FRaports%2FRaport6%2FCOV_MDD.PNG)

Ostanim wykresem jest pokazana cała populacja rozwiązań:

![nsga2_history.png](Images%2FRaports%2FRaport6%2FROI_MDD.png)

Można zauważyć, że im większe ryzyko, tym większe zyski przynosi algorytm.
