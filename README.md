# Opis projektu
W ramach projektu stworzona została aplikacja konsolowa implementującą metodę fiszek. Technologie wykorzystane w projekcie to baza danych **MongoDB** i **Python3** z biblioteką **mongoengine**.

Pojedyncza fiszka jest tradycyjnie kartą, z zapisanym pytaniem i poprawną odpowiedzią na odwrocie. Z założenia ucząć się tą metodą najpierw próbujemy odpowiedzieć na pytanie, później weryfikując z odpowiedzią. Metoda rozszerzona posiada dodatkowo mechanizm pozwalający na zaplanowanie kolejnego zobaczenia karty, na podstawie tego, czy znaliśmy odpowiedź w ostatniej iteracji oraz jej wcześniejszego stanu (*nowa*, *widziana*, *opanowana*). Stany zmieniają się na podstawie kilku ostatnich odpowiedzi, na poniższych zasadach:
- fiszka dotychczas nie pokazana użytkownikowi jest *nowa*
- fiszka po udzieleniu przez użytkownika informacji zwrotnej staje się *widziana*, jeżeli wcześniej była *nowa*
- fiszka staje się *opanowana*, jeżeli ostatnie dwie odpowiedzi były pozytywne
- fiszka staje się *widziana*, jeżeli jest *opanowana* i została udzielona odpowiedź negatywna
  
Fiszki mogą być zbierane w talie, czyli inaczej zbiory.

## Zaimplementowane funkcjonalności
- prosty system logowania oparty o adres email i hash hasła
- **tworzenie i modyfikacja talii fiszek**
- **mechanizm nauki**

    W pierwszym kroku aplikacja pobiera zestaw fiszek zaplanowanych na dzisiejszy dzień, oraz zestaw nowych kart, jeżeli takie istnieją. Następnie każda z fiszek zostaje pokazana użytkownikowi, który po odkryciu odpowiedzi jest proszony o udzielenie informacji zwrotnej. Jeżeli jest negatywna, fiszka trafia na koniec kolejki, w przeciwnym wypadku zostaje zaplanowana na dzień w przyszłości, według reguł zdefiniowanych w zmiennej [`FEEDBACK_SETTINGS`](model/Card.py). W tym miejscu są również dokonywane zmiany stanów opisane wyżej.

- **możliwość udostępniania swoich talii społeczności, ich wyszukiwania i importowania do swojego konta**
  
  Talie udostępnione są okrojoną wersją talii użytkownika, poprzez usunięcie informacji związanych z historią nauki, stanem itd. Są ponadto rozszerzeniem, dodając informacje o autorze oraz opis.

  Importowanie odbywa się po wyszukaniu talii. Wyszukiwanie odbywa się poprzez sprawdzenie czy zapytanie jest podciągiem nazwy, z pominięciem wielkości znaków. Talia po zaimportowaniu do konta użytkownika zostaje roszerzona o informacje unikalne dla użytkownika i nie różni się niczym od tej utworzonej samodzielnie.

*Oryginalny opis projektu przekazany na etapie propozycji znajduje się w pliku pliku [`description.md`](description.md). Aplikacja została zaimplementowana w większości zgodnie z oryginalnymi założeniami.*

## Architektura aplikacji
Aplikacja łączy się bezpośrednio z bazą danych.

## Instrukcja uruchomienia

**Do uruchomienia konieczne są poniższe zależności**
- Python 3
    - mongoengine
    - curses
- Uruchomiona lokalnie instancja MongoDB
- System Operacyjny wspierający bibliotekę curses, np. dowolna dystrybucja Linuxa

W celu **uruchomienia aplikacji**, konieczne jest wywołanie komendy w głównym folderze projektu
```
python3 main.py
```
Jeżeli aplikacja zawiesza się przy próbie zalogowania, najprawdopodobniej mongoengine nie jest w stanie połączyć się z bazą danych. Proszę zweryfikować, że na komputerze uruchomiona jest usługa MongoDB i obecny użytkownik ma uprawnienia do korzystania z niej.

Kod domyślne dla mongoengine parametry połączenia z bazą lokalną:
`connect('flashcards')`, w niektórych przypadkach może być konieczna modyfikacja
metody połączenia w [pliku `model/__init__.py`](model/__init__.py).

# Opis kodu
**Na aplikacje składają się 2 elementy:**
1. Aplikacja klienta
1. Baza danych MongoDB

**W projekcie możemy wyróżnić następujące elementy:**
- pakiet `model` - model danych bazy danych
    - `Card.py` - klasy opisujące pojedynczą fiszkę
    - `Deck.py` - klasy opisujące talie
    - `LoginCredentials.py` - model przechowujący dane logowania, oraz kod do logowania i rejestracji
    - `User.py` - model użytkownika
- `DeckCreationWizard.py` - klasa pomocnicza przy tworzeniu i edycji talii
- `main.py` - główna logika aplikacji
- `ui.py` - funkcje pomocnicze do interfejsu użytkownika
- `example.csv` - przykładowa talia do zaimportowania

## Struktura bazy danych
### Kolekcja `login_credentials`

Przechowuje dane logowania zarejestrowanych użytkowników:
- adres email, wykorzystywany jako identyfikator użytownika
- hash hasła
- informację do którego użytkownika należą dane

**Przykładowy dokument:**
```json
/* 1 */
{
    "_id" : ObjectId("5ee8925b9d621a55e736e151"),
    "password_hash" : "0e2355797a60162f3d384568adcaf08e5808adb507042200304a008919f7d5c3",
    "email" : "danjod40@gmail.com",
    "user" : ObjectId("5ee8925b9d621a55e736e150")
}
```

### Kolekcja `shared_deck`

Przechowuje talie udostępnione przez użytkowników. Każda talia zawiera:
- informacje o autorze (nazwę użytkownika oraz jego id)
- nazwę talii
- opis talii
- datę dodania
- listę fiszek zawartą w talii (pole `cards`)

Każda fiszka przechowywana w liście zawiera następujące atrybuty:
- `dc_id` - unikalny identyfikator fiszki w kontekście talii
- `question` - pytanie zawarte w fiszcze
- `answer` - poprawna odpowiedź na pytanie
- *`_cls` - wartośc nieistotna, atrybut wygenerowany automatycznie przez mongoengine, związany z uruchomieniem mechanizmu dziedzienia*

**Przykładowy dokument:**
```json
/* 1 */
{
    "_id" : ObjectId("5ee8927b9d621a55e736e152"),
    "cards" : [ 
        {
            "_cls" : "SharedCard",
            "dc_id" : 0,
            "question" : "Question 0",
            "answer" : "Answer 0"
        }, 
        {
            "_cls" : "SharedCard",
            "dc_id" : 1,
            "question" : "Question 1",
            "answer" : "Answer 1"
        }, 
        {
            "_cls" : "SharedCard",
            "dc_id" : 2,
            "question" : "Question 2",
            "answer" : "Answer 2"
        }, 
        {
            "_cls" : "SharedCard",
            "dc_id" : 3,
            "question" : "Question 3",
            "answer" : "Answer 3"
        }, 
        {
            "_cls" : "SharedCard",
            "dc_id" : 4,
            "question" : "Question 4",
            "answer" : "Answer 4"
        }, 
        {
            "_cls" : "SharedCard",
            "dc_id" : 5,
            "question" : "Question 5",
            "answer" : "Answer 5"
        }
    ],
    "author_id" : ObjectId("5ee8925b9d621a55e736e150"),
    "author_name" : "Daniel",
    "name" : "Random new deck",
    "description" : "no desc",
    "created" : ISODate("2020-06-16T11:35:09.742Z")
}
```

### Kolekcja `user`

Przechowuje informacje przekazywane do klienta po zalogowaniu użytkownika. Każdy dokument jest unikalny dla dokładnie jednego z użytkowników. Zawiera:
- `username` - nazwę użytkownika do którego się odnosi
- `email` - adres email użytkownika
- `decks` - listę talii utworzonych lub zaimportowanych do konta użytkownika. Każdy element listy zawiera:
  - `name` - nazwę talii
  - `size` - rozmiar
  - `cards` - listę fiszek zawartych w talii. Każda z nich może powstać z fiszki przechowywanej w talii współdzielonej i każda zawiera:
    - `dc_id` - unikalny numer identyfikacyjny w obrębie talii
    - `question` - pytanie
    - `answer` - poprawną odpowiedź na pytanie
    - `history` - historię nauki fiszki, zawierającą jej stan (wartość atrybutu `state`) w momencie nauki oraz wybraną odpowiedź
    - `scheduled_for` - infrmację kiedy użytkownik zobaczy daną fiszkę (jeżeli będzie taka możliwość)
    - `state` - informacja o aktualnym statusie fiszki. Wartość odnosi się do wartości zmiennych globalnych `UNSEEN`, `SEEN` i `LEARNT`, zdefyniowanych z pliku [`model/Card.py`](model/Card.py)
    - *nieistotny atrybut `_cls` związany z uruchomieniem dziedziczenia w mongoengine*

**Przykładowy dokument:**
```json
/* 1 */
{
    "_id" : ObjectId("5ee8925b9d621a55e736e150"),
    "username" : "Daniel",
    "email" : "danjod40@gmail.com",
    "decks" : [ 
        {
            "cards" : [ 
                {
                    "_cls" : "PrivateCard",
                    "dc_id" : 0,
                    "question" : "Question 0",
                    "answer" : "Answer 0",
                    "history" : [ 
                        {
                            "state" : 0,
                            "answer" : "Correct"
                        }
                    ],
                    "scheduled_for" : ISODate("2020-06-17T11:37:06.721Z"),
                    "state" : 1
                }, 
                {
                    "_cls" : "PrivateCard",
                    "dc_id" : 1,
                    "question" : "Question 1",
                    "answer" : "Answer 1",
                    "history" : [ 
                        {
                            "state" : 0,
                            "answer" : "Incorrect"
                        }, 
                        {
                            "state" : 1,
                            "answer" : "Incorrect"
                        }, 
                        {
                            "state" : 1,
                            "answer" : "Correct"
                        }
                    ],
                    "scheduled_for" : ISODate("2020-06-18T11:37:15.178Z"),
                    "state" : 1
                }, 
                {
                    "_cls" : "PrivateCard",
                    "dc_id" : 2,
                    "question" : "Question 2",
                    "answer" : "Answer 2",
                    "history" : [ 
                        {
                            "state" : 0,
                            "answer" : "Correct"
                        }
                    ],
                    "scheduled_for" : ISODate("2020-06-17T11:37:08.058Z"),
                    "state" : 1
                }
            ],
            "name" : "Random new deck",
            "size" : 100
        }
    ]
}
```