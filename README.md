# Scientific Data Exploration App

## Opis systemu
Aplikacja służy do eksploracji danych naukowych związanych z obrazami komórek na podstawie zestawu BBBC021. Pozwala użytkownikom na wizualizację związków chemicznych oraz ich obrazów, umożliwiając filtrowanie danych, generowanie współrzędnych oraz eksport do formatu JSON.

## Zastosowane wzorce projektowe
1. **Factory Method** – do tworzenia instancji obiektów bazy danych (`SQLiteDatabase`).
2. **Singleton** – zapewnienie globalnego dostępu do połączenia z bazą danych.
3. **Observer** – do powiadamiania komponentów o zmianach w danych.
4. **Facade** – uproszczenie dostępu do bazy danych przez `DatabaseInterface`.
5. **Decorator** – rozszerzenie funkcjonalności współrzędnych dla związków chemicznych.
6. **Strategy** – do obsługi różnych formatów eksportu danych (np. JSON, CSV).

## Implementacja zasad SOLID
- **Single Responsibility Principle**: Każda klasa ma jedno odpowiedzialne zadanie, np. `DatabaseFiller` wypełnia tabele, a `CoordinatesCreator` generuje współrzędne.
- **Open/Closed Principle**: Moduły takie jak `CoordinatesCreator` są otwarte na rozbudowę (np. nowe algorytmy), ale zamknięte na modyfikacje istniejącego kodu.
- **Liskov Substitution Principle**: Klasy implementujące wspólny interfejs mogą być używane zamiennie, np. różne implementacje `DatabaseInterface`.
- **Interface Segregation Principle**: Interfejsy są małe i wyspecjalizowane, np. `DatabaseInterface` ogranicza się do operacji bazodanowych.
- **Dependency Inversion Principle**: Moduły wyższego poziomu (np. `Program`) nie zależą bezpośrednio od implementacji, lecz od abstrakcji (`DatabaseInterface`).

## Struktura projektu
- `Program.py` – główny plik uruchamiający aplikację.
- `SQLiteDatabase.py` – zarządzanie połączeniem z bazą danych.
- `DatabaseCreator.py` – tworzenie struktury bazy danych.
- `DatabaseFiller.py` – wypełnianie bazy danych na podstawie CSV.
- `DatabaseInterface.py` – abstrakcja do interakcji z bazą danych.
- `CoordinatesCreator.py` – generowanie współrzędnych.
- `UsablePaths.py` – zarządzanie ścieżkami w projekcie.

## Autorzy
- Projekt opracowany w ramach zajęć Instytutu Informatyki UJ.
