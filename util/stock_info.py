import requests


stock = "AC"
stock_info_url = "https://www.bmv.com.mx/es/emisoras/estadisticas/AC-6081-1959"


def get_info(stock):

    text = requests.get(stock_info_url).text


def extract_tables(text):
    tables_of_interest = ["COTIZACIONES SERIE", "INDICADORES SERIE"]
    indicator = tables_of_interest[0]
    start_table = "<table"
    end_table = "</table"

    start_table + text.split(indicator)[-1].split(start_table)[1].split(end_table)[0] + end_table

    len(text.split(start_table))

    start_table in text