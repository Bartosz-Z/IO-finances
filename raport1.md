W celu ekstrakcji cech przygotowany zostanie dodatkowy moduł przetwa
rzający dataset historycznego kursu walut na dataset cech, który zostanie wykorzystany przez model.

Ektrakcja cech opiera się na metodzie filtra wykładniczego aplikowanego w wybranych oknach czasowych. Z każdego okna, po zaaplikowaniu filtra wyciągane jest kilka ostatnich wartości utworzonej serii. Zestawy wartości z różnych okien są umieszczane w macierzy a następnie przekazywane jako dane wejściowe do modelu.

Docelowo model ma być w stanie kontrolować parametr alfa filtru wykładniczego, a także liczbę elementów pobieranych z okna.


# Aktualne wyniki

Szybkie symulacje wykazały, że algorytm MOEAD daje znacznie bardziej zróżnicowane wyniki niż pozostałe:
- NSGA2
- NSGA3
- AGEMOEA
- SMSEMOA

Poniższny wykres przedstawia wyniki algorytmu NSGA2:

![nsga2_history.png](Images%2FRaports%2FRaport1%2Fnsga2_history.png)

oraz różnorodność rozwiązań:

![nsga2_population.png](Images%2FRaports%2FRaport1%2Fnsga2_population.png)

Zaś algorytm MOEAD dał znacznie lepsze rezultaty pod względem różnorodności:

![moead_history.png](Images%2FRaports%2FRaport1%2Fmoead_history.png)

![moead_population.png](Images%2FRaports%2FRaport1%2Fmoead_population.png)

Nie brano pod uwagę algorytmów bazujących na punktach referencyjnych, ponieważ trudne je zdefiniować w tym problemie.