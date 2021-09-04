import datetime as dt
from typing import List, Union


class Calculator:
    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records: List[Union[float, str]] = []

    def add_record(self, obj) -> None:
        self.records.append(obj)

    def get_today_stats(self):
        self.today = dt.date.today()
        stat = sum(
            record.amount
            for record in self.records
            if record.date == self.today
        )
        return stat

    def get_today_remained(self):
        remained = self.limit - self.get_today_stats()
        return remained

    def get_week_stats(self):
        self.today = dt.date.today()
        week = dt.date.today() - dt.timedelta(days=7)
        stat_week = sum(
            record.amount
            for record in self.records
            if week < record.date <= self.today
        )
        return stat_week


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()
        else:
            self.date = dt.date.today()

    def __str__(self) -> str:
        return (
            "Запись содержит: "
            f"количество - {self.amount}, "
            f"дата - {self.date}, "
            f"комментарий - {self.comment}."
        )


class CaloriesCalculator(Calculator):
    answers = {
        "allowed": "Сегодня можно съесть что-нибудь ещё, "
                "но с общей калорийностью не более {0} кКал",
        "forbidden": "Хватит есть!",
    }

    def get_calories_remained(self):
        left = self.get_today_remained()
        if 0 < left:
            return (
                self.answers["allowed"].format(left)
            )
        return self.answers["forbidden"]


class CashCalculator(Calculator):

    USD_RATE = 70.00
    EURO_RATE = 80.00
    RUB_RATE = 1.00

    answers = {
        "forbidden": {
            "spent_limit": "Денег нет, держись",
            "exceeded_limit": "Денег нет, держись: твой долг - {0} {1}",
            "unspent_limit": "На сегодня осталось {0} {1}",
        },
        "ERROR": "Неизвестная валюта",
    }

    def get_today_cash_remained(self, currency):
        left = self.get_today_remained()
        if left == 0:
            return self.answers["forbidden"]["spent_limit"]
        rate_dict = {
            "rub": ("руб", self.RUB_RATE),
            "usd": ("USD", self.USD_RATE),
            "eur": ("Euro", self.EURO_RATE),
        }
        rate_name, currency_rate = rate_dict[currency]
        cash_sum = round(left / currency_rate, 2)
        if currency in rate_dict:
            if 0 < left:
                return self.answers["forbidden"]["unspent_limit"].format(
                    cash_sum, rate_name)

            else:
                debt = abs(cash_sum)
                return self.answers["forbidden"]["exceeded_limit"].format(
                    debt, rate_name)
        return self.answers["ERROR"]
