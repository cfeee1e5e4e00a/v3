# Veni, vidi, vici

### InfluxDB

-   Адрес брокера: `influx.cfeee1e5e4e00a.ru:8086` (WIP)
-   Пользователь: `nti`
-   Пароль: `cfeee1e5e4e00a`
-   API Token: `oGxyaChur5XTvoGRBE3FKJMtGSFxQ--GEZtUqmDhr18cMNDcBEMAQNPgtGimgUvvZMyrGrv58IXUj0D-eDO1ZQ==`

### Grafana

-   Адрес: `http://grafana.cfeee1e5e4e00a.ru:3000` (WIP)
-   Пользователь: `nti`
-   Пароль: `cfeee1e5e4e00a`

### MQTT

-   Адрес брокера: `mqtt://mqtt.cfeee1e5e4e00a.ru:1883`
-   Пользователь: `nti`
-   Пароль: `nti`

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
