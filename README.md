W ramach projektu stworzona została aplikacja konsolowa implementująca metodę Fiszek.
Oryginalny opis projektu znajduje się w pliku [`description.md`](description.md).

## Do uruchomienia potrzebne są
- Python 3
    - mongoengine
    - curses
- Uruchomiona lokalnie instancja MongoDB
- System Operacyjny wspierający bibliotekę curses

Kod domyślne dla mongoengine parametry połączenia z bazą lokalną:
`connect('flashcards')`, w niektórych przypadkach może być konieczna modyfikacja
metody połączenia w [pliku `model/__init__.py`](model/__init__.py).

## Opis kodu
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
**Kolekcja `login_credentials`**

Przechowuje dane logowania zarejestrowanych użytkowników
```json
/* 1 */
{
    "_id" : ObjectId("5ee8925b9d621a55e736e151"),
    "password_hash" : "0e2355797a60162f3d384568adcaf08e5808adb507042200304a008919f7d5c3",
    "email" : "danjod40@gmail.com",
    "user" : ObjectId("5ee8925b9d621a55e736e150")
}
```

**Kolekcja `shared_deck`**

Przechowuje talie udostępnione przez użytkowników

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

**Kolekcja `user`**

Przechowuje informacje przekazywane do klienta po zalogowaniu użytkownika

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