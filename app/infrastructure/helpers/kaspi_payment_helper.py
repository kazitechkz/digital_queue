from datetime import datetime, date, time


class KaspiPaymentHelper:
    AVAILABLE_FOR_PAYMENT = 0  # абонент/счёт/заказ найден и доступен для пополнения/оплаты
    NOT_FOUND = 1  # "абонент/счёт не найден" или "заказ не найден", если запрос check был на проверку состояния заказа
    CANCELLED = 2  # заказ отменен
    ALREADY_PAID = 3  # заказ уже оплачен
    PROCESSING = 4  # платеж в обработке
    PROVIDER_ERROR = 5  # Другая ошибка провайдера

    CHECK_COMMAND = "check"
    PAY_COMMAND = "pay"

    @staticmethod
    def convert_to_tiin(price:float)->int:
        return int(price * 100)

    @staticmethod
    def get_paid_date_and_time(paid_at:str)->[date,time,datetime]:
        dt_object:datetime = datetime.strptime(paid_at, "%Y%m%d%H%M%S")
        return [dt_object.date(), dt_object.time(),dt_object]