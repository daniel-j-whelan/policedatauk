from datetime import date, timedelta


def get_last_month() -> str:
    today = date.today().replace(day=1)
    last_month = today - timedelta(days=1)
    return last_month.strftime("%Y-%m")
