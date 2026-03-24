import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

API_KEY = "a07ff9c823cc8e6af7bc0568"

class ActionConverterMoeda(Action):

    def name(self):
        return "action_converter_moeda"

    def run(self, dispatcher, tracker, domain):

        valor = tracker.get_slot("valor")
        origem = tracker.get_slot("moeda_origem")
        destino = tracker.get_slot("moeda_destino")

        if not valor or not origem or not destino:
            dispatcher.utter_message(text="Informe valor e moedas para converter.")
            return []

        # 🔄 Normalização básica
        mapa = {
            "real": "BRL",
            "reais": "BRL",
            "dolar": "USD",
            "dolares": "USD",
            "dólares": "USD",
            "usd": "USD",
            "euro": "EUR",
            "euros": "EUR"
        }

        origem = mapa.get(origem.lower(), origem.upper())
        destino = mapa.get(destino.lower(), destino.upper())

        # 🌐 Chamada da API
        url = f"https://v6.exchangerate-api.com/v6/a07ff9c823cc8e6af7bc0568/latest/USD"
        response = requests.get(url).json()

        taxa = response["conversion_rates"][destino]
        resultado = float(valor) * taxa

        dispatcher.utter_message(
            text=f"{valor} {origem} = {resultado:.2f} {destino}"
        )

        return []