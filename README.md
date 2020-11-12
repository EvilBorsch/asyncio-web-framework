## Тестовое задание для Mail.ru

### Текст задания 

#### API конвертации валют

Нужно написать веб-сервис на asyncio, который предоставляет API для конвертации валют. Данные хранить в Redis. Все явно неописанные форматы и протоколы можно допридумать.

Должны работать следующие локейшены:

* `GET /convert?from=RUR&to=USD&amount=42`: перевести `amount` из валюты `from` в валюту `to`. Ответ в JSON.
* `POST /database?merge=1`: залить данные по валютам в хранилище. Если `merge == 0`, то старые данные инвалидируются. Если `merge == 1`, то новые данные перетирают старые, но старые все еще акутальны, если не перетерты.

### Запуск
Используя poetry: ```make build && make run```
Используя pip: ```make build-pip && make run-pip```

### 
