# VKGroupsBirthdayParser

Таск:  
В этой задачке вам предстоит проверить парадокс дней рождений на эмпирических данных.

От вас требуется: 
1. Выбрать какое-то большое сообщество в Vk. С помощью VkAPI выкачать инфорацию по ее подписчикам (самое главное это дата рождения, а также id пользователя, который будет его характеризовать. Не оставляйте свой токен 
2. Удалите из данных всех, кто не указал когда он родился. Приведите колонку с датами рождений к удобному, однообразному виду. 
3. Постройте гистограмму, на которой было бы понятно, в какой месяц родилось какое количество людей. Правда ли, что рождаемость людей в течение года распределена равномерно? 
4. Эмпирически оцените вероятность того, что в группе из 50 произвольных людей найдутся хотя бы двое с одинаковым днём рождения. Для этого напишите цикл, в ходе которого из таблички будет делаться подвыборка из 50 строк. Для этих 50 строк внутри условия вы должны проверить совпадение дней рождений. Если совпало, то нужно запомнить это в переменную счётчик, которую вы впоследствии, чтобы получить вероятность, поделите на длину цикла. 

Дополнения тасков
1. Из сообщества нужно выкачать данные только о 10к подписчиках. табличка - это контейнер, нет определенного формата 
2. Если возможно сразу отсекать, то конечно так надо сделать 
3. Аутентификация по токену