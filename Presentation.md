# PRESENTATION.md

## Kluczowe elementy diagramu klas
Diagram klas aplikacji przedstawia strukturę systemu oraz relacje między kluczowymi komponentami:
1. **Moduł Bazy Danych**:
   - Klasy `DatabaseCreator`, `DatabaseFiller`, `SQLiteDatabase` i `DatabaseInterface` odpowiadają za tworzenie, wypełnianie oraz interakcję z bazą danych.
   - Relacje między tymi klasami uwzględniają zależności i abstrakcję.
2. **Moduł Ścieżek**:
   - Klasa `Paths` zarządza dynamicznym określaniem ścieżek plików i zasobów.
3. **Moduł Koordynatów**:
   - Klasa `CoordinatesCreator` odpowiada za generowanie współrzędnych na wykresie dla związków chemicznych.
4. **Moduł Logiki Aplikacji**:
   - Klasy `Compound` i `Image` modelują dane naukowe, z relacją kompozycji między nimi.
5. **Moduł Głównej Logiki**:
   - Klasa `Program` integruje wszystkie moduły i odpowiada za uruchomienie systemu.

## Zastosowane wzorce projektowe i ich uzasadnienie
1. **Factory Method** – pozwala na dynamiczne tworzenie połączeń z bazą danych, ułatwiając testowanie i rozbudowę (`SQLiteDatabase`).
2. **Singleton** – zapewnia jedną globalną instancję bazy danych, zapobiegając konfliktom w dostępie.
3. **Observer** – umożliwia reagowanie na zmiany w danych, np. w wykresach interaktywnych.
4. **Facade** – upraszcza interakcję z bazą danych poprzez `DatabaseInterface`.
5. **Decorator** – pozwala na dodawanie dodatkowych funkcji do obiektów związków chemicznych, np. wizualizacji na wykresie.
6. **Strategy** – umożliwia różne podejścia do eksportu danych (np. JSON, CSV).

## Sposób implementacji zasad SOLID
- **SRP**: Każda klasa realizuje jedną odpowiedzialność (np. `DatabaseFiller` skupia się na wypełnianiu danych).
- **OCP**: Możliwość rozszerzenia modułów bez ingerencji w istniejący kod, np. `CoordinatesCreator`.
- **LSP**: Wszystkie klasy i interfejsy mogą być używane zamiennie zgodnie z ich typem, np. `DatabaseInterface`.
- **ISP**: Interfejsy są małe i wyspecjalizowane.
- **DIP**: Moduły wyższego poziomu (np. `Program`) współpracują z abstrakcjami, nie implementacjami (`DatabaseInterface`).

## Doświadczenia związane z pracą zespołową
1. **Planowanie zadań**:
   - Zadania zostały podzielone na moduły, co umożliwiło równoległą pracę nad aplikacją.
   - Korzystaliśmy z GitHub Project Board do zarządzania postępami.
2. **Korzystanie z PlantUML**:
   - Narzędzie umożliwiło wizualizację struktury aplikacji, co ułatwiło projektowanie.
   - Diagram został zintegrowany z GitHub Actions, aby automatycznie generować wersje graficzne.
3. **Praca zespołowa**:
   - Każdy członek zespołu miał przypisaną konkretną rolę, np. tworzenie diagramów, kodowanie bazy danych czy logiki aplikacji.
   - Wyzwania: synchronizacja między członkami zespołu podczas aktualizacji kodu.
4. **Korzystanie z GitHub**:
   - Pull requesty i code review pomogły zachować spójność kodu.
   - Integracja z GitHub Actions usprawniła automatyzację zadań.

## Testowanie
1. **Przetestowane pliki:**
  - `UsablePaths.py`
  - `DatabaseInterface.py`

2. **Problemy z testowaniem:**
  - Pliki operujące na bazie danych:  
    - `SQLiteDatabase.py`  
    - `DatabaseCreator.py`  
    - `DatabaseFiller.py`  
  - Aktualnie pracujemy nad użyciem mocków, aby umożliwić testowanie tych modułów.

3. **Pliki do przetestowania:**
    - `SQLiteDatabase.py`  
    - `DatabaseCreator.py`  
    - `DatabaseFiller.py`  
    - `Program.py`


## Link do repozytorium
[Scientific Data Exploration App](https://github.com/teamteamteamteamteam/ScientificDataExtractionApp)
