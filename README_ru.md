## python-pelco-lib
# Library for working with devices supporting PELCO-D and PELCO-P. 
Перед вами моя небольшая библиотека для упрощения работы с протоколом PELCO-P и PELCO-D. Опишу ее основные функции:
Касается всех функций!
Для корректной работы требуется каждой передать адрес камеры в формате "00" где нули это числа адреса камеры на шине.
til_speed - это скорость по оси наклона - tilt и она должна быть от 00 до 63. Желательно передавать число как int.
pan_speed - это скорость по оси вращения влево или вправо и она должна быть от 00 до 63. Желательно передавать число как int.

Ниже приведены функции для протокола PELCO-P. файл commands_pelco_p.py
1. pelco_p_stop(address) - остановка движения камеры.
2. pelco_p_tilt_up(address, til_speed) - движение камеры вверх.
3. pelco_p_tilt_down(address, til_speed) - движение камеры вниз.
4. pelco_p_tilt(address, up, down, til_speed) - движение камеры вниз и вверх. 
Если передать up = 1 то камера будет двигаться наверх. 
Если передать down = 1 то камера будет двигаться вниз.
5. pelco_p_pan_left(address, pan_speed) - движение камеры влево.
6. pelco_p_pan_right(address, pan_speed) - движение камеры вправо.
7. pelco_p_pan(address, right, left, pan_speed) - движение камеры влево или вправо. 
Если передать right = 1  то камера будет двигаться вправо.
Если передать  left = 1  то камера будет двигаться влево.
8. pelco_p_upleft(address, pan_speed, til_speed) - движение камеры вверх и влево.
9. pelco_p_upright(address, pan_speed, til_speed) - движение камеры вверх и вправо.
10. pelco_p_down_left(address, pan_speed, til_speed) - движение камеры вниз влево.
11. pelco_p_down_right(address, pan_speed, til_speed) - движение камеры вниз и вправо.
12. pelco_p_zoom_in(address) - зум объектива движется вперед.
13. pelco_p_zoom_out(address) - зум объектива движется назад.
14. pelco_p_focus_far(address) - фокус объектива движется вперед.
15. pelco_p_focus_near(address) - фокус объектива движется назад.

Ниже приведены функции для протокола PELCO-D. файл commands_pelco_d.py
16. pelco_d_stop(address) - остановка движения камеры.
17. pelco_d_tilt_up(address, til_speed) - движение камеры вверх.
18. pelco_d_tilt_down(address, til_speed) - движение камеры вниз.
19. pelco_d_tilt(address, up, down, til_speed) - движение камеры вниз и вверх. 
Если передать up = 1 то камера будет двигаться наверх. 
Если передать down = 1 то камера будет двигаться вниз.
20. pelco_d_pan_left(address, pan_speed) - движение камеры влево.
21. pelco_d_pan_right(address, pan_speed) - движение камеры вправо.
22. pelco_d_pan(address, right, left, pan_speed) - движение камеры влево или вправо. 
Если передать right = 1  то камера будет двигаться вправо.
Если передать  left = 1  то камера будет двигаться влево.
23. pelco_d_upleft(address, pan_speed, til_speed) - движение камеры вверх и влево.
24. pelco_d_upright(address, pan_speed, til_speed) - движение камеры вверх и вправо.
25. pelco_d_down_left(address, pan_speed, til_speed) - движение камеры вниз влево.
26. pelco_d_down_right(address, pan_speed, til_speed) - движение камеры вниз и вправо.
27. pelco_d_zoom_in(address) - зум объектива движется вперед.
28. pelco_d_zoom_out(address) - зум объектива движется назад.
29. pelco_d_focus_far(address) - фокус объектива движется вперед.
30. pelco_d_focus_near(address) - фокус объектива движется назад.
Также у нас есть транспортный модуль где есть две функции для работы с COM портом. Для работы с ним нужно добавить библиотеку pyserial
Для обоих функций есть параметры.
port - сюда мы передаем номер COM порта из системы. Виртуальный com порт что создается в системе когда вы подключаете ваш usb-rs485 адаптер.
baud - параметр baudrate для протокола что устанавливается настройками камеры. Обычно он равен(1200, 1800, 2400, 4800, 9600).
data - команда которую мы хотим отправить.
data_stop сюда мы передаем строку что сформировала stop команда. Пример приведен ниже.
delay - задежка между командами в секундах.
31. write_com_command(port, baud, data, data_stop, delay) отправляет команду и ждем заданый промежуток и отправляет стоп команду. Удобна для небольшого шага при движении.
32. write_com_action(port, baud, data) просто отправляет данные.

Стандартный пример работы с библиотекой выглядит так. 
Добавляем необходимое в наш файл с программой. 
```
from commands_pelco_d import pelco_d_stop, pelco_d_tilt_up
from pelco_transport import write_com_action, write_com_command
port = "/dev/ttyUSB1"
baud = "2400"
address = "01"
delay = 1
til_speed = "32"
data = pelco_d_tilt_up(address, til_speed)
data_stop = pelco_d_stop(address)
write_com_command(port, baud, data, data_stop, delay)
```
Вот у нас вышел код что отправляет по COM порту доступному по адресу "/dev/ttyUSB1" c baudrate 2400 команду по протоколу PELCO-D для того чтобы камера по ардесу "01" одну секунду поднимала объектив наверх и после остановилась.