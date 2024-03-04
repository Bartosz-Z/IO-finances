# IO-finances

Kursem badanym będzie frank szwajcarski do złotówek (CHF PLN).

Model będzie brał pod uwagę pięć poprzednich nakładających się na siebie regionów w danych historycznych, jak przedstawiono na poniższym rysunku.

![expl](https://github.com/Bartosz-Z/IO-finances/assets/48770711/1fde8e97-adcf-443d-a67b-8a4481638d14)

Dla każdego regionu zostanie obliczona średnia wartość w każdym punkcie na podstawie filtru wykłądniczego, któgo współcznnik wygładzenia będzie częścią genotypu.
Na podstawie 3 ostatnich wartości (najnowszych) z każdego regionu + ostatnich dwóch wartości określających zmiane w kursie w regionie będzie określana decyzja kupna bądź sprzedarzy akcji.

Genotyp będzie miał 30 genoów (po 6 na każdy region).

Na podstawie genotypu (z wyłączeniem pięciu współczynników do filtru wykładniczego) będzie podejmowana decyzja czy sprzedać/kupić i ile akcji.
Modelem będzie kombinacja liniowa wyliczonych parametrów bądź drzewo decyzjne.

Ewaluacją będzie zastosowanie modelu po kolei po całym zbiorze historycznych danych od początku do końca.
Wynikiem będą dwie wartości:
- Posiadane pieniądze na końcu ewaluacji przez model (suma akcji po aktualnym kursie + posiadane rezerwy) (ROI)
- Współcznnik MDD (Maximum Drawdown)

Pierwszy z tych współcznników  będzie maksymalizowany, a drugi minimalizowany.
Posiadane pieniądze na końcu iwestycji są ważne, ale nie każdy będzie w stanie zaufać modelowi do podejmowania decyzji.
Dlatego minimalizacja drugiego współcznnika jest ważna. Określa on, jak jak wielka największa była różnica między lokalnym maksimum zarobionych pieniędzy, a następującym po nim lokalnym minimum.
