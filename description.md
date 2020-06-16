# Opis projektu

## OMÓWIENIE

Celem projektu jest zaprojektowanie oraz implementacja aplikacji bazodanowej do nauki metodą fiszek. Aplikacja posiada też możliwość udostępnienia gotowych zestawów innym użytkownikom, oraz raportowanie ewentualnych błędów autorowi.


## SPECYFIKACJA

### Użytkownicy

<s>Autoryzacją użytkowników zajmuje się usługa zewnętrzna, np. Firebase Auth. Baza danych przechowuje jedynie informacje o użytkownikach związane bezpośrednio z ich aktywnością w aplikacji</s>
Z powodu problemów z biblioteką Firebase zaimplementowałem prosty system logowania.


### Zestaw fiszek

Zestaw fiszek zawiera:

*   nazwę zestawu
*   informacje o autorze
*   listę fiszek

Zestawy mogą być wyszukiwane po ich nazwie, jeżeli autor zdecyduje się je udostępnić.


### Fiszka

Fiszka to pojedynczy zestaw: pytanie, możliwe odpowiedzi, poprawna odpowiedź oraz opcjonalne wytłumaczenie. Ponadto powinna istnieć możliwość dołączenia obrazka lub pliku dźwiękowego.


### Historia nauki

Historia nauki jest powiązana z użytkownikiem, oraz zestawem. Dla każdej fiszki zapisuje ilość oraz czasy ostatnich poprawnych i błędnych odpowiedzi.


## Wykorzystane technologie
- MongoDB
- Python 3.8
    - ncurses (biblioteka do UI w terminalu)
    - mongoengine
