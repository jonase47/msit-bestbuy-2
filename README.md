# Best Buy 2.0

Ein kleiner Elektronik-Shop für die Kommandozeile. Übungsprojekt zur
objektorientierten Programmierung mit Python aus der MSIT-Weiterbildung
„AI for Developers“ und Fortsetzung des ersten Best-Buy-Projekts.

## Funktionen

- Produkte auflisten, Gesamtmenge anzeigen und Bestellungen aufgeben
- Drei Produkttypen:
  - `Product`: normales Produkt mit Lagerbestand
  - `NonStockedProduct`: ohne Lagerbestand, beliebig oft kaufbar (z. B. eine Lizenz)
  - `LimitedProduct`: pro Bestellung nur begrenzt kaufbar (z. B. Versand)
- Drei Rabatt-Aktionen, die sich einem Produkt zuweisen lassen:
  - `PercentDiscount`: prozentualer Rabatt
  - `SecondHalfPrice`: jedes zweite Stück zum halben Preis
  - `ThirdOneFree`: jedes dritte Stück gratis
- Bestellungen sind „alles oder nichts“: Erst wird die ganze Bestellung
  geprüft, dann gekauft. Schlägt eine Position fehl, wird nichts abgebucht.

## Aufbau

| Datei | Inhalt |
| --- | --- |
| `main.py` | Menü und Bestellablauf auf der Kommandozeile |
| `products.py` | `Product`, `NonStockedProduct`, `LimitedProduct` |
| `promotions.py` | abstrakte Klasse `Promotion` und die drei Aktionen |
| `store.py` | `Store` mit Produktliste und `order()` |
| `test_*.py` | Unit-Tests mit pytest |

## Starten

Das Programm braucht nur Python ab Version 3.12, keine weiteren Pakete:

```bash
python3 main.py
```

## Entwicklung

Für Tests und Typprüfung wird [uv](https://docs.astral.sh/uv/) verwendet:

```bash
uv sync            # Umgebung mit pytest und mypy anlegen
uv run pytest      # Unit-Tests ausführen
uv run mypy .      # Typprüfung (strict)
```

## Kurzbeispiel

```python
import products
import promotions
import store

mac = products.Product("MacBook Air M2", price=1450, quantity=100)
mac.promotion = promotions.SecondHalfPrice("Second Half price!")

best_buy = store.Store([mac])

print(mac)                         # MacBook Air M2, Price: $1450, Quantity: 100, ...
print(mac in best_buy)             # True
print(best_buy.order([(mac, 2)]))  # 2175.0
```
