# python-pelco-lib

*[English version](README_en.md)*

Небольшая библиотека для управления PTZ-камерами по протоколам **Pelco-D** и **Pelco-P**.

Она делает две вещи:

- **Сборщики команд** превращают команду движения в сообщение протокола и возвращают его строкой в hex.
- **Транспорт** отправляет эту строку в последовательный порт RS-485.

Обе части независимы — сборщики можно использовать отдельно, если байты вы отправляете
как-то иначе (по сети, другой библиотекой, в тестах).

## Установка

```bash
pip install .
```

Единственная зависимость — [pyserial](https://pypi.org/project/pyserial/), и нужна она
только для транспорта.

## Быстрый старт

```python
from python_pelco_lib import pelco_d_tilt_up, pelco_d_stop, write_com_command

port = "/dev/ttyUSB0"   # виртуальный COM-порт вашего USB-RS485 адаптера
baud = 2400             # должен совпадать со скоростью, заданной в камере
address = "01"          # адрес камеры на шине

data = pelco_d_tilt_up(address, 32)
stop = pelco_d_stop(address)

# Поднимаем объектив одну секунду и останавливаем.
write_com_command(port, baud, data, stop, 1)
```

Каждый сборщик просто возвращает строку, поэтому команду можно посмотреть без железа:

```python
>>> from python_pelco_lib import pelco_d_pan_left, pelco_p_pan_left
>>> pelco_d_pan_left("01", 32)
'FF010004200025'
>>> pelco_p_pan_left("01", 32)
'A00100042000AF2A'
```

## Соглашения

Касается всех сборщиков.

**`address`** — адрес камеры на шине. Принимается либо двузначная hex-строка, как было
всегда (`"01"`, `"0A"`), либо обычный `int`, который читается как номер на шине и
переводится в hex, то есть `10` станет `"0A"`. Некорректный адрес вызывает `ValueError`.

> В Pelco-P камеры нумеруются с нуля, поэтому байт адреса обычно равен номеру камеры
> на шине **минус один**. В Pelco-D номер используется как есть.

**`pan_speed` / `til_speed`** — десятичная скорость от `0` до `63` (`0x00`–`0x3F`).
Значения вне диапазона обрезаются, а не отвергаются: камера, которую просят двигаться
быстрее, чем она может, всё равно поедет. Числовые строки (`"32"`) работают наравне с int.

Сборщики поворота Pelco-P дополнительно принимают значение `100` как *турбо*-поворот
(`0x40`), оно доступно как `TURBO_SPEED`. В Pelco-D турбо-значения нет.

## Команды

Оба протокола предоставляют одинаковый набор. Используйте префикс `pelco_d_` для Pelco-D
и `pelco_p_` для Pelco-P — например `pelco_d_zoom_in` и `pelco_p_zoom_in`.

| Функция | Аргументы | Описание |
| --- | --- | --- |
| `..._stop` | `address` | Остановка движения камеры |
| `..._tilt_up` | `address, til_speed` | Движение вверх |
| `..._tilt_down` | `address, til_speed` | Движение вниз |
| `..._tilt` | `address, up, down, til_speed` | Вверх, если задан `up`, вниз, если задан `down`, иначе стоп |
| `..._pan_left` | `address, pan_speed` | Движение влево |
| `..._pan_right` | `address, pan_speed` | Движение вправо |
| `..._pan` | `address, right, left, pan_speed` | Вправо, если задан `right`, влево, если задан `left`, иначе стоп |
| `..._upleft` | `address, pan_speed, til_speed` | Движение вверх и влево |
| `..._upright` | `address, pan_speed, til_speed` | Движение вверх и вправо |
| `..._down_left` | `address, pan_speed, til_speed` | Движение вниз и влево |
| `..._down_right` | `address, pan_speed, til_speed` | Движение вниз и вправо |
| `..._zoom_in` | `address` | Зум вперёд |
| `..._zoom_out` | `address` | Зум назад |
| `..._focus_far` | `address` | Фокус вперёд |
| `..._focus_near` | `address` | Фокус назад |

В `..._tilt` и `..._pan` при обоих заданных флагах побеждает первый.

## Транспорт

`port` — устройство, которым определяется ваш USB-RS485 адаптер (`/dev/ttyUSB0`, `COM3`).
`baud` — скорость, заданная в настройках камеры, обычно 1200, 1800, 2400, 4800 или 9600.

### `write_com_action(port, baud, data)`

Открывает порт, отправляет одну команду и закрывает порт.

### `write_com_command(port, baud, data, data_stop, delay)`

Отправляет `data`, выдерживает `delay` секунд и отправляет `data_stop`. Удобно для
небольшого шага при движении. `data_stop` отправляется даже если ожидание прервано,
поэтому Ctrl-C посреди движения не оставит камеру вращаться.

### `PelcoSerial(port, baud)`

Держит порт открытым между командами. Две функции выше переоткрывают порт на каждое
сообщение — это десятки миллисекунд и сброс линии, что заметно, когда команды идут
потоком: с джойстика, из GUI или из цикла патрулирования.

```python
from python_pelco_lib import PelcoSerial, pelco_d_pan_left, pelco_d_stop

with PelcoSerial("/dev/ttyUSB0", 2400) as link:
    stop = pelco_d_stop("01")
    link.send_for(pelco_d_pan_left("01", 32), stop, 0.5)   # движение, пауза, стоп
    link.send(stop)                                        # одно сообщение
```

## Примеры

В каталоге [examples/](examples/) лежат четыре рабочие программы. Каждая добавляет корень
репозитория в `sys.path`, поэтому они запускаются прямо из клона репозитория, без установки.

| Файл | Что делает |
| --- | --- |
| [console.py](examples/console.py) | Отправка одной команды из командной строки |
| [simple_dance.py](examples/simple_dance.py) | Интерактивный ввод и команда `all`, прогоняющая все направления |
| [gamepad_pelco_p.py](examples/gamepad_pelco_p.py) | Управление камерой с USB-геймпада (нужен `hid`) |
| [com_gui.py](examples/com_gui.py) | Пульт на PyQt5 (нужен `PyQt5`) |

```bash
python examples/console.py -p /dev/ttyUSB0 -b 2400 -a 01 -pr d -c right
```

## Форматы сообщений

Pelco-D, семь байт. Контрольная сумма — сумма пяти байт после байта синхронизации по
модулю 256:

```
FF | ADDRESS | DATA1 | DATA2 | PAN SPEED | TILT SPEED | CHECKSUM
```

Pelco-P, восемь байт. Контрольная сумма — XOR семи предшествующих байт, включая STX и ETX:

```
A0 | ADDRESS | DATA1 | DATA2 | PAN SPEED | TILT SPEED | AF | CHECKSUM
```

## Тесты

```bash
pip install pytest
python -m pytest
```

Тесты сверяют собранные сообщения со спецификациями протоколов и проверяют транспорт на
поддельном последовательном порту, поэтому железо не требуется.

## Переход с версии 0.1

Модули лежали в каталоге с именем `python-pelco-lib`, который Python не может
импортировать, поэтому программы импортировали файлы напрямую. Теперь это полноценный пакет:

```python
# было
from commands_pelco_d import pelco_d_stop, pelco_d_tilt_up
from pelco_transport import write_com_action, write_com_command

# стало
from python_pelco_lib import pelco_d_stop, pelco_d_tilt_up
from python_pelco_lib import write_com_action, write_com_command
```

Подмодули никуда не делись, если вам так удобнее
(`from python_pelco_lib.commands_pelco_d import pelco_d_stop`).

Все сборщики возвращают те же байты, что и раньше, с одним исключением: `pelco_d_tilt`,
`pelco_d_pan`, `pelco_p_tilt` и `pelco_p_pan` раньше при любом вызове падали с
`TypeError` — они передавали три аргумента в сборщики, принимающие два, — а теперь работают.

## Лицензия

GPL-3.0. См. [LICENSE](LICENSE).
