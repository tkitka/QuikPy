from datetime import datetime
import time  # Подписка на события по времени
from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp


def print_callback(data):
    """Пользовательский обработчик событий:
    - Изменение стакана котировок
    - Получение обезличенной сделки
    - Получение новой свечки
    """
    print(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} - {data["data"]}')  # Печатаем полученные данные


def changed_connection(data):
    """Пользовательский обработчик событий:
    - Соединение установлено
    - Соединение разорвано
    """
    print(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} - {data}')  # Печатаем полученные данные


if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    qp_provider = QuikPy()  # Подключение к локальному запущенному терминалу QUIK

    # classCode = 'TQBR'  # Класс тикера
    # secCode = 'SBER'  # Тикер

    classCode = 'SPBFUT'  # Класс тикера
    secCode = 'SiU3'  # Для фьючерсов: <Код тикера><Месяц экспирации: 3-H, 6-M, 9-U, 12-Z><Последняя цифра года>

    # Запрос текущего стакана. Чтобы получать, в QUIK открыть Таблицу Котировки, указать тикер
    # print(f'Текущий стакан {classCode}.{secCode}:', qpProvider.GetQuoteLevel2(classCode, secCode)['data'])

    # Стакан. Чтобы отмена подписки работала корректно, в QUIK должна быть ЗАКРЫТА таблица Котировки тикера
    # qpProvider.OnQuote = print_callback  # Обработчик изменения стакана котировок
    # print(f'Подписка на изменения стакана {classCode}.{secCode}:', qpProvider.SubscribeLevel2Quotes(classCode, secCode)['data'])
    # print('Статус подписки:', qpProvider.IsSubscribedLevel2Quotes(classCode, secCode)['data'])
    # sleepSec = 3  # Кол-во секунд получения котировок
    # print('Секунд котировок:', sleepSec)
    # time.sleep(sleepSec)  # Ждем кол-во секунд получения котировок
    # print(f'Отмена подписки на изменения стакана:', qpProvider.UnsubscribeLevel2Quotes(classCode, secCode)['data'])
    # print('Статус подписки:', qpProvider.IsSubscribedLevel2Quotes(classCode, secCode)['data'])
    # qpProvider.OnQuote = qpProvider.DefaultHandler  # Возвращаем обработчик по умолчанию

    # Обезличенные сделки. Чтобы получать, в QUIK открыть Таблицу обезличенных сделок, указать тикер
    # qpProvider.OnAllTrade = print_callback  # Обработчик получения обезличенной сделки
    # sleepSec = 1  # Кол-во секунд получения обезличенных сделок
    # print('Секунд обезличенных сделок:', sleepSec)
    # time.sleep(sleepSec)  # Ждем кол-во секунд получения обезличенных сделок
    # qpProvider.OnAllTrade = qpProvider.DefaultHandler  # Возвращаем обработчик по умолчанию

    # Просмотр изменений состояния соединения терминала QUIK с сервером брокера
    qp_provider.OnConnected = changed_connection  # Нажимаем кнопку "Установить соединение" в QUIK
    qp_provider.OnDisconnected = changed_connection  # Нажимаем кнопку "Разорвать соединение" в QUIK

    # Новые свечки. При первой подписке получим все свечки с начала прошлой сессии
    # TODO В QUIK 9.2.13.15 перестала работать повторная подписка на минутные бары. Остальные работают
    #  Перед повторной подпиской нужно перезапустить скрипт QuikSharp.lua Подписка станет первой, все заработает
    qp_provider.OnNewCandle = print_callback  # Обработчик получения новой свечки
    for interval in (60,):  # (1, 60, 1440) = Минутки, часовки, дневки
        print(f'Подписка на интервал {interval}:', qp_provider.SubscribeToCandles(classCode, secCode, interval)['data'])
        print(f'Статус подписки на интервал {interval}:', qp_provider.IsSubscribed(classCode, secCode, interval)['data'])
    input('Enter - отмена\n')
    for interval in (60,):  # (1, 60, 1440) = Минутки, часовки, дневки
        print(f'Отмена подписки на интервал {interval}', qp_provider.UnsubscribeFromCandles(classCode, secCode, interval)['data'])
        print(f'Статус подписки на интервал {interval}:', qp_provider.IsSubscribed(classCode, secCode, interval)['data'])

    # Выход
    qp_provider.CloseConnectionAndThread()  # Перед выходом закрываем соединение и поток QuikPy из любого экземпляра
