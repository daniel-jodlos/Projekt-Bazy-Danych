W ramach projektu stworzona została aplikacja konsolowa implementująca metodę Fiszek.
Oryginalny opis projektu znajduje się w pliku [description.md](description.md).

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
