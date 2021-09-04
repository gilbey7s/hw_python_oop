import datetime as dt
from typing import List, Union


class Calculator:
    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records: List[Union[float, str]] = []
        self.today = dt.datetime.now().date()

    def add_record(self, obj) -> None:
        self.records.append(obj)

    def get_today_stats(self):
        stat = sum(
            [
                record.amount
                for record in self.records
                if record.date == self.today
            ]
        )
        return stat

    def get_today_remained(self):
        remained = self.limit - Calculator.get_today_stats(self)
        return remained

    def get_week_stats(self):
        week = dt.date.today() - dt.timedelta(days=7)
        stat_week = sum(
            [
                record.amount
                for record in self.records
                if week <= record.date <= self.today
            ]
        )
        return stat_week


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()
        else:
            self.date = dt.datetime.now().date()

    def __str__(self) -> str:
        return (
            "Запись содержит: "
            f"количество - {self.amount}, "
            f"дата - {self.date}, "
            f"комментарий - {self.comment}."
        )


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        answers = {
            "allowed": {
                "prefix": (
                    "Сегодня можно съесть что-нибудь ещё, "
                    "но с общей калорийностью не более "
                ),
                "suffix": " кКал",
            },
            "forbidden": "Хватит есть!",
        }
        left = Calculator.get_today_remained(self)
        if 0 < left < self.limit:
            return (
                answers.get("allowed")["prefix"]
                + str(left)
                + answers.get("allowed")["suffix"]
            )
        else:
            return answers["forbidden"]


class CashCalculator(Calculator):

    USD_RATE = 70.00
    EURO_RATE = 80.00
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        answers = {
            "forbidden": {
                "spent_limit": "Денег нет, держись",
                "exceeded_limit": "Денег нет, держись: твой долг - ",
                "unspent_limit": "На сегодня осталось ",
            },
            "ERROR": "Неизвестная валюта",
        }
        rate_dict = {
            "rub": ("руб", self.RUB_RATE),
            "usd": ("USD", self.USD_RATE),
            "eur": ("Euro", self.EURO_RATE),
        }
        rate_name, currency_rate = rate_dict[currency]
        left = Calculator.get_today_remained(self)
        cash_sum = round(left / currency_rate, 2)
        if currency in rate_dict:
            if left == 0:
                return answers.get("forbidden")["spent_limit"]
            elif 0 < left < self.limit:
                return (
                    answers.get("forbidden")["unspent_limit"]
                    + str(cash_sum)
                    + " "
                    + str(rate_name)
                )
            else:
                debt = abs(cash_sum)
                return (
                    answers.get("forbidden")["exceeded_limit"]
                    + str(debt)
                    + " "
                    + str(rate_name)
                )
        else:
            return answers.get("ERROR")
