# ChainLinker

**ChainLinker** — утилита для нахождения связанных Bitcoin-адресов по входам и выходам транзакций.

## Возможности

- Находит отправителей на указанный адрес
- Показывает адреса, на которые были переводы
- Работает по 10 последним транзакциям

## Применение

- Построение графов связей
- Анализ миксеров, мостов, биржевых кошельков
- Расследования и аудит

## Установка

```bash
pip install -r requirements.txt
```

## Использование

```bash
python chainlinker.py <bitcoin_address>
```

Пример:

```bash
python chainlinker.py 1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY
```

## Лицензия

MIT License
