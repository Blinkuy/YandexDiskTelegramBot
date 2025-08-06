import yadisk
import datetime

client = yadisk.YaDisk(token="y0__xCd3P6GCBj1ojkgrODt-hO86orzv-QWUUlpshQ3BdPp51nWrQ")

def create_dir_date():
    date = datetime.date.today()

    year = date.year
    month = date.month
    day = date.day

    client.makedirs(f"{year}/{month}/{day}")


res = client.is_dir("2025/7/31")
print(res)

create_dir_date()

res = client.is_dir("2025/7/31")
print(res)