# Relext
Код для курсовой работы по unsupervised relation extraction.

/bootstrap/ - файлы основного алгоритма для извлечения отношений.

/crawler/ - файлы для сбора корпуса из новостных ресурсов (пока лента и рбк)

/preprocessing/ - файлы для подготовки корпуса для основого алгоритма (pos-tagging, named entity recognition, raw-text -> xml, etc.)

/evaluation/ - файлы для оценивания работы алгоритма

Текст работы - https://drive.google.com/open?id=0B-QijVL2ftMvdUZ4ajFWODFGcms

В курсовой работе проведены первычные эксперимены, получены первые результаты
(неудовлетворительные). На данном этапе система не готова к использованию.
Чтобы это исправить, нужно:
1. Оптимизировать работу ключевой функции (find_pairs)
2. Связать все этапы в единый управляемый процесс
3. Добивить интрефейс для командной строки
4. Провести кучу экспериментов для улучшения качества
5. Подумать, что дальше
6. ....
