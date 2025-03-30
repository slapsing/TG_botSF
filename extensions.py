import requests
import json
from config import keys


class APIException(Exception):  # классификация ошибок пользователя
    pass

#обработчик ошибок пользователя
class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException('Невозможно перевести одинаковые валюты!')

        try:
            quote_tiker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_tiker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except:
            raise APIException(f'Не удалось обработать количество, вводите дробные числа через точку\nНапример: 0.1')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_tiker}&tsyms={base_tiker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
