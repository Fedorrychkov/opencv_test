# opencv_test
Для теста необходима третья версия пакета opencv.
## Установка
В archlinux такого пакета нет, поможет пакет [opencv-git из AUR](https://aur.archlinux.org/packages/opencv-git/). По умолчанию пакет не содержит python биндингов для методов `cv2.drawMatchesKnn` и `cv2.drawMatches`, поэтому необходимо заранее склонировать репозиторий https://github.com/itseez/opencv_contrib/ и в опциях cmake в PKGBUILD указать дополнительный флаг `-DOPENCV_EXTRA_MODULES_PATH=<path_to_opencv_contrib_repo>/modules`. Разобраться во всех этих тонкостях сильно помог [ответ от **berak** на StackOverflow](http://stackoverflow.com/questions/27156632/opencv-python-drawmatchesknn-function).

Если используется virtualenv, то для работы cv2 необходимо создать симлинк на cv2.so из site-packages нужной версии интерпретатора.
## Описание
Примеры взяты из документации к python биндингу opencv: http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html

Метод `cv2.drawMatches` отличается сигнатурой от описанного в документации, поэтому было использовано решение для второй ветки, предложенное **rayryeng** на [StackOverflow](http://stackoverflow.com/a/26227854). Так же были заменены вызовы `cv2.ORB` и `cv2.SIFT` на их текущие варианты в opencv третьей ветки.

Для запуска примеров необходимы пакеты, перечисленные в requirements.txt, управляется пример через переменные окружения:
* **`OPENCV_TEST_MODE`** - принимает два значения, _flann_ и _orb_, переключающие режим распознавания совпадений в opencv.
* **`OPENCV_TEST_PATH`** - путь до директории с тестируемыми изображениями.
* **`OPENCV_TEST_QUERY`** - имя файла для поиска соответствий. По умолчанию pig.jpg.
* **`OPENCV_TEST_BASE`** - имя оригинального файла, в котором будут искаться соответствие. По умолчанию normal.png.
