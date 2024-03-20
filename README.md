# Veni, vidi, vici

### InfluxDB

-   Адрес брокера: `influx.cfeee1e5e4e00a.ru:8086` (WIP)
-   Пользователь: `nti`
-   Пароль: `cfeee1e5e4e00a`
-   API Token: `oGxyaChur5XTvoGRBE3FKJMtGSFxQ--GEZtUqmDhr18cMNDcBEMAQNPgtGimgUvvZMyrGrv58IXUj0D-eDO1ZQ==`

### Grafana

-   Адрес: `http://grafana.cfeee1e5e4e00a.ru:3000` (WIP)
-   Пользователь: `nti`
-   Пароль: `ac4e70e488ffd4e525c8996573d3158e`

### MQTT

-   Адрес брокера: `mqtt://mqtt.cfeee1e5e4e00a.ru:1883`
-   Пользователь: `nti`
-   Пароль: `nti`

#### Топики

-   `/sensors` - Формат данных [InfluxDB Line Protocol](https://docs.influxdata.com/influxdb/v2/reference/syntax/line-protocol/). Важно НЕ ставить символ переноса строки в конце данных при отправке по MQTT.

    -   Для температуры: `temp,flat=<номер_квартиры> value=<температура>`
    -   Для температуры на улице: `outside_temp value=<температура>`
    -   Для влажности: `humd,flat=<номер_квартиры> value=<влажность>`
    -   Для тока потребления: `curr,flat=<номер_квартиры> value=<энергия>`
    -   Для состояний реле: `relay,flat=<номер_квартиры>,dc=<номер_блока_питания> value=<true | false>`

-   `/mode/<номер квартиры>` - Топик для задания режима работы.
    Формат данных:

    ```typescript
    enum Mode = {
        TARGET = 0,
        TARGET_ECONOMY = 1,
        BY_PROFILE = 2,
        OFF = 3,
    };

    type TargetPayload = number /* target temperature */;
    type TargetEconomyPayload = number /* target temperature in economy mode */;
    type ByProfilePayload = `${number/* target temperature */} ${number /* estimated time in seconds */}`;
    type OffPayload = void;

    type Payload = TargetPayload | TargetEconomyPayload | ByProfilePayload | OffPayload;

    type Message = `${Mode} ${Payload}`;
    ```

-   `/startup/<номер квартиры>` - Топик для уведомления сервера о подключении ESP к сети.
    Формат данных: Любое содержимое.

### PostgresSQL

-   Адрес: `diarrhea.cfeee1e5e4e00a.ru:5432` (WIP)
-   Пользователь: `nti`
-   Пароль: `nti`
-   База данных: `nti`

Организован сбор метрик с топиков c помощью Telegraf в InfluxDB для дальнейшего отображения в Grafana.
Конфигурация Telegraf лежит в `.config/telegraf/telegraf.conf`.
Для сбора в InfluxDB метрики нужно отправлять в формате [InfluxDB Line Protocol](https://docs.influxdata.com/influxdb/v2/reference/syntax/line-protocol/).

Синтаксис:

```

<measurement>[,<tag_key>=<tag_value>[,<tag_key>=<tag_value>]] <field_key>=<field_value>[,<field_key>=<field_value>] [<timestamp>]

```

Пример:

```

temp value=36.6

```

### Docker

Рекомендую использовать context для работы с кластером на стенде.

```

docker context create nti --docker "host=ssh://zhenya@diarrhea.cfeee1e5e4e00a.ru"

```

#### Linux

Дополнительных действий не требуется.

#### MacOS

Рекомендую использовать [Colima](https://github.com/abiosoft/colima).

```bash
brew install colima
```

Для корректной работы volumes нужна дополнительная конфигурация.

1. Создать файлы `~/.colima/_lima/_config/override.yaml` и `~/.lima/_config/override.yaml` с таким содержимым:

```yaml
mountType: 9p
mounts:
    - location: "/Users/<username>"
      writable: true
      9p:
          securityModel: mapped-xattr
          cache: mmap
    - location: "~"
      writable: true
      9p:
          securityModel: mapped-xattr
          cache: mmap
    - location: "/tmp/colima"
      writable: true
      9p:
          securityModel: mapped-xattr
          cache: mmap
```

2. `colima delete`

3. `colima start --mount-type 9p`
