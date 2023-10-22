# Tokodust
Описание программного кода команды "Погромисты" развертки видео с камеры в 2d плоскость

### Предобработка данных
При помощи модулей openCV и numpy видеозаписи были считаны в формате массива фреймов. 
Каждый отдельный фрейм был отцентрирован относительно предполагаемого обратного конца трубы. Также посчитаны углы, на которые отклоняются отверстия от вертикального положения. 
Данные отверстия служили "маяком" для наших измерений. Для уточнения эффективности этого метода, изображения были отфильтрованы от низких пространственных частот, после чего бинаризованы. Таким образом было установлено, что блики от отверстий, вызванные светодиодом камеры, имеют наибольшую интенсивность. Далее параметры для поворота и трансляции изображений были расчитаны относительно этих бликов.

### Развертка
Для развертки было принято решение преобразовывать сегменты видимого конуса в трапеции. Высота трапеции расчитывалась относительно скорости перемещения камеры. В силу отсутствия параеметров камеры, точно подсчитать скорость не удалось, поэтому скорость передвижения была найдена эмпирическим методом и принята за константу.
"Разрез" сегмента производился по местоположению отверстий (что известно из предобработки).

Полученная трапеция сначала приводилась к форме прямоугольника. Позже все прямоугольники в наборе приведены к одному размеру. Данные преобразования проводились с использованием методов интерполяции при растяжении изображений.
Таким образом из полученных прямоугольников при помощи конкатенации выстраивается искомая карта трубы.

### Постобработка
Для улучшения качества полученной карты были опробованы различные методы фильтрации и обработки изображений: фильтрация в Фурье-плоскости, коррелляция с ядром Гаусса, домножение на гауссов профиль. По итогу численных экспериментов мы остановились на последнем методе в силу высокого визуального качества, а также отличного устранения шумов и изображений отверстий трубы.

### Сегментация
Для сегментации пыли для нашего метода подходит множество методов: от свёрточных нейронных сетей до простейшей бинаризации. Мы выбрали "срединный" вариант, а именно модели кластеризации из модуля scikit-learn.

### Приложение
Наше решение содержит пользовательский интерфейс. Он обладает очень низким порогом входа для пользователя, однако высокой эффективностью. Но как же так? Все просто! Интерфейс содержит всего лишь две кнопки, в которых тяжело запутаться! Одна кнопка (Browse) позволяет выбрать путь к видео, который по предположению снимает камера в трубе под токамаком. Вторая - запускает наш метод, а на выход пользователь получает изображение карты внутренней поверхности трубы, которое можно еще и масштабировать! Помимо этого, желанная карта сохраняется к Вам на ПК, а это значит, что ее можно будет открыть позже, когда только пожелаете!

### Перспективы
Наш метод решения обладает высоким потенциалом для дальнейшей работы. Например, знание необходимых параметров камеры позволит вычислить скорость передвижения по трубе вне зависимости от ее размеров и формы. Используемые алгоритмы заведомо учитывают аберрации камеры, проворот относительно выборной вертикали и простейшую стабилизацию (которую в том числе можно улучшить, зная параметры камеры). 
Интерфейс приложения можно дополнить исследованием обнаруженной пыли (например, распределением населенности в зависимости от координаты).
