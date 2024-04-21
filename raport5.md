Dodany zostały dwa dodatkowe zestawy parametrów wejściowych dla modelu:
- współczynniki aproksymacji wielomianowej,
- wartość maksimum drawdown.

Moduł do ekstrakcji cech został zmodularyzowany, tak że możliwe jest wykorzystanie dowolnej kombinacji filtrów i aproksymacji w celu generacji parametrów wejściowych.

# Aktualne wyniki

Przeprowadzono eksperyment z długim szkoleniem (1000 iteracji) z wykorzystaniem samego filtru wykładniczego na podstawie kursu CHF/PLN:

![nsga2_history.png](Images%2FRaports%2FRaport5%2FFigure_4.jpg)

Przeprowadzo też szkolenia dla różnej kombinacji parametrów na podstawie kursu USD/PLN. Poniższe wyniki pochodzą ze szkolenia na 400 elementach datasetu.

Wyniki dla filtru wykładniczego, wartości drawdown i aproksymacji wielomianowej (100 iteracji, aproksymacja 5 stopnia):

![nsga2_history.png](Images%2FRaports%2FRaport5%2FFigure_1.png)

Wyniki dla aproksymacji wielomianowej (100 iteracji):

![nsga2_history.png](Images%2FRaports%2FRaport5%2FFigure_2.png)

Wyniki dla filtru wykładniczego i aproksymacji wielomianwej (100 iteracji, aproksymacja 5 stopnia):

![nsga2_history.png](Images%2FRaports%2FRaport5%2FFigure_3.png)

Poniższe wyniki pochodzą ze szkolenia na całości datasetu:

Wyniki dla filtru wykładniczego, wartości drawdown i aproksymacji wielomianowej (100 iteracji, aproksymacja 5 stopnia):

![nsga2_history.png](Images%2FRaports%2FRaport5%2FFigure_5.png)

Wyniki dla aproksymacji wielomianowej (100 iteracji):

![nsga2_history.png](Images%2FRaports%2FRaport5%2FFigure_6.png)

Wyniki dla filtru wykładniczego i aproksymacji wielomianwej (100 iteracji, aproksymacja 5 stopnia):

![nsga2_history.png](Images%2FRaports%2FRaport5%2FFigure_7.png)


