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

По умолчанию сервис запущен на 0.0.0.0:8081 и подключается к редису redis://localhost (значение переменной окружения REDIS_URL) 

### Описание проекта
В процессе работы, был написан маленький веб-фреймворк на asyncio и uvloop под названием keklik
(Так как он должен быть маленьким и быстрым) 

<img src="https://media.izi.travel/263fc413-3ed9-44da-a34c-f86a9ffd0ac6/5b3b0d27-03a6-46f0-9fbd-dbf237a4136f_800x600.jpg" alt="drawing" width="300"/> 

Он поддерживает минимум функционала, но его было достаточно для выполнения проекта

Само приложение(converter, находящийся в src) написано с использованием CleanArchitecture, 
так что все компоненты взаимо заменяемы, и мы можем легко перейти от использования keklik framework на, например, aiohttp

При подсчете курса, предполагается что пользователь вводит отношение заданной валюты к базовой(например USD), тогда курс подсчитывается по формуле:
converted_value = amount * (cur_from / cur_to)

### Где можно потыкать? Примеры

#### <b>Сервиc задеплоен на http://165.227.162.244:8101 </b>
Так что можно будет его потыкать там
```GET http://165.227.162.244:8101/convert?from=USD&&to=EUR&&amount=4```
```POST http://165.227.162.244:8101/database?merge=1```

#### Примеры запросов на локалхосте


Запрос: ```GET http://0.0.0.0:8081/convert?from=USD&&to=EUR&&amount=4``` 

Ответ:  <img src="https://cdn1.savepice.ru/uploads/2020/11/12/92cf266a8abbc885ae8bfd7ee9c7b3cd-full.png" alt="drawing" width="200"/> 

Запрос: ```GET http://0.0.0.0:8081/convert?from=USD&&to=NOTEXIST&&amount=4``` 

Ответ:  <img src="https://cdn1.savepice.ru/uploads/2020/11/12/2fc80d534a312c5ffe2521dfad244c4c-full.png" alt="drawing" width="200"/> 

Запрос: <img src="https://cdn1.savepice.ru/uploads/2020/11/12/8b56a6e95c494ddb6062d03bfaf8be45-full.png" alt="drawing" width="200"/>  

Ответ: <img src="https://cdn1.savepice.ru/uploads/2020/11/12/c863742e51514918bb361101dc07196a-full.png" alt="drawing" width="200"/>  

