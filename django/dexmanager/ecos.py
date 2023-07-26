import requests
from .models import SrcDex

def get_url_period(index_period):
    period_dict = {"D": "/D/20230715/20230724/", "M": "/M/202207/202304/", "Q": "/Q/2021Q1/2023Q2/", "A": "/A/2015/2021/"}
    return period_dict[index_period]

def truncate_string(original_string):
    last_dot_index = original_string.rfind(".")
    if "2008.9" in original_string: last_dot_index = 5
    if last_dot_index != -1:
        truncated_string = original_string[last_dot_index + 1 :]
        return truncated_string.strip()
    return original_string

def validate_title(title):
    if title[-2:] in ["1)", "2)", "4)"]: title = title[:-3]
    elif title == "C 제조업": title = "제조업"
    elif title == "C-1.2.대출금": title = "대출금"
    return title

def get_statistic(index_period, table_code, index_code):
    url_prefix = "http://ecos.bok.or.kr/api/StatisticSearch/1AJBYOG5GZJC0OMYBOSO/json/kr/1/10/"
    url_period = get_url_period(index_period)
    url = url_prefix + table_code + url_period + index_code

    response = requests.get(url)

    if response.status_code == 200:
        try:
            row_list = response.json().get('StatisticSearch').get('row')
            category = row_list[0].get('STAT_NAME')
            title = validate_title(row_list[0].get('ITEM_NAME1'))
            unit = row_list[0].get('UNIT_NAME')

            values = dict()
            for row in row_list:
                values[row.get('TIME')] = row.get('DATA_VALUE')
        except:
            return "Failed to parse data"
        try:
            Dex, created = SrcDex.objects.get_or_create(title=title)
            if created:
                Dex.category = truncate_string(category)
                Dex.unit = unit
                Dex.isInvest = False
            Dex.values = values
            Dex.save()

            return f"{title} created" if created else f"{title} updated"
        except:
            return "Failed to save data"
    else:
        print(f"Request failed with status code {response.status_code} while processing code {index_code}")