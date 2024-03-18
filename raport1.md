W celu ekstrakcji cech przygotowany zostanie dodatkowy moduł przetwarzający dataset historycznego kursu walut na dataset cech, który zostanie wykorzystany przez model.

Ektrakcja cech opiera się na metodzie filtra wykładniczego aplikowanego w wybranych oknach czasowych. Z każdego okna, po zaaplikowaniu filtra wyciągane jest kilka ostatnich wartości utworzonej serii. Zestawy wartości z różnych okien są umieszczane w macierzy a następnie przekazywane jako dane wejściowe do modelu.

Docelowo model ma być w stanie kontrolować parametr alfa filtru wykładniczego, a także liczbę elementów pobieranych z okna.