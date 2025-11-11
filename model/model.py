from database.impianto_DAO import ImpiantoDAO

from database.consumo_DAO import ConsumoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        # TODO
        lista_tuple = []

        for impianto in self._impianti :
            consumi = ConsumoDAO.get_consumi (impianto.id)
            valori_mensili = []
            for consumo in consumi :
                if consumo.data.month == mese :
                    valori_mensili.append (consumo.kwh)

            media_giornaliera = 0.0
            if len (valori_mensili) > 0 :
                somma_consumi = sum (valori_mensili)
                media_giornaliera = somma_consumi / len (valori_mensili)

            lista_tuple.append( (impianto.nome, media_giornaliera) )

        return lista_tuple

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        # TODO
        sequenza_parziale = []
        giorno = 1

    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        # TODO
        consumi_prima_settimana = {}

        for impianto in self._impianti :
            consumi = ConsumoDAO.get_consumi (impianto.id)
            valori_prima_settimana = []

            for consumo in consumi :
                if consumo.data.month == mese and consumo.data.day in range (1, 8) :

                    valori_prima_settimana.append (consumo.kwh)
                    consumi_prima_settimana [impianto.id] = valori_prima_settimana

        return consumi_prima_settimana


