base_url = "https://ojk.go.id/"

from datetime import datetime


def convert_date(date_str):
    months = {
        'Januari': '01',
        'Februari': '02',
        'Maret': '03',
        'April': '04',
        'Mei': '05',
        'Juni': '06',
        'Juli': '07',
        'Agustus': '08',
        'September': '09',
        'Oktober': '10',
        'November': '11',
        'Desember': '12'
    }

    day, month_name, year = date_str.split()

    month = months.get(month_name, '01')
    formatted_date = f"{year}-{month}-{day}"

    return formatted_date
