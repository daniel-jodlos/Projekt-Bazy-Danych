# Opis projektu


## OMÓWIENIE

Celem projektu jest projekt oraz implementacja bazy danych fiszek do aplikacji do nauki metodą fiszek. Aplikacja posiada też możliwość udostępnienia gotowych zestawów innym użytkownikom, oraz raportowanie ewentualnych błędów autorowi.


## SPECYFIKACJA


### Użytkownicy

Autoryzacją użytkowników zajmuje się usługa zewnętrzna, np. Firebase Auth. Baza danych przechowuje jedynie informacje o użytkownikach związane bezpośrednio z ich aktywnością w aplikacji


### Zestaw fiszek

Zestaw fiszek zawiera:

*   nazwę zestawu
*   listę tagów
*   informacje o autorze
*   listę fiszek

Zestawy mogą być wyszukiwane po ich nazwie oraz tagach, jeżeli autor zdecyduje się je udostępnić.


### Fiszka

Fiszka to pojedynczy zestaw: pytanie, możliwe odpowiedzi, poprawna odpowiedź oraz opcjonalne wytłumaczenie. Ponadto powinna istnieć możliwość dołączenia obrazka lub pliku dźwiękowego.


### Historia nauki

Historia nauki jest powiązana z użytkownikiem, oraz zestawem. Dla każdej fiszki zapisuje ilość oraz czasy ostatnich poprawnych i błędnych odpowiedzi.


### Zgłoszenia błędów

Są to wiadomości tekstowe o długości do kilku tysięcy znaków, przypisane do konkretnej fiszki. Powinny być przekazywane autorowi zestawu w formie powiadomienia.


## TECHNOLOGIA

Ponieważ tematyka projektu nie wymusza ani silnych warunków integralnościowych, ani skomplikowanych zależności pomiędzy modelami, dobrym pomysłem wydaje się wykorzystanie baz **NoSQL**, w szczególności bazy dokumentowej **MongoDB**.

Do stworzenia aplikacji można wykorzystać język **Python**, z interfejsem opartym o konsolę


## ETAPY



1. Modelowanie zestawu fiszek
   
    Celem tego etapu jest wprowadzenie podstawowej funkcjonalności bazy danych, na której będą dodawane kolejne funkcjonalności.



2. Implementacja historii nauki
   
    Po zakończeniu tego etapu, baza danych powinna mieć formę pozwalającą na pełne wykorzystanie aplikacji do pracy z własnymi zestawami.



3. Implementacja udostępniania oraz wyszukiwania zestawów
   
   Celem tego etapu jest dodanie podstawowej funkcjonalności społecznościowej - udostępniania własnych zestawów innym użytkownikom oraz korzystania z zestawów udostępnionych przez innych.



4. Implementacja zgłoszeń błędów
   
   Rozwinięcie funkcji społecznościowej o możliwość zgłoszenia autorowi błędów w jego fiszce. Po zakończeniu tego etapu, powinny zostać spełnione wszystkie wymagania dotyczące projektu, zawarte w tym dokumencie.