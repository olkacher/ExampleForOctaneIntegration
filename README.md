# Pytest-bdd Example Project

Простой пример проекта на `pytest-bdd` с POM и четырьмя фичами.

В проекте есть:

- `tests/pages/page_objects.py` — простая реализация Page Object Model
- `tests/features/login.feature`
- `tests/features/search.feature`
- `tests/features/cart.feature`
- `tests/features/profile.feature`
- `tests/test_app.py` — шаги и сценарии для всех фич

## Установка

```bash
python -m pip install -r requirements.txt
```

## Запуск тестов

```bash
pytest
```
