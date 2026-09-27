"""
========================================================================
 MODULO: pubsub.py
 DESCRICAO: Implementacao do Broker (Gerenciador de Topicos) do padrao
            Publish-Subscribe (Pub/Sub).
 CENARIO: Plataforma de E-commerce / Gestao de Pedidos
========================================================================
"""


class PubSubBroker:
    """
    Classe central do padrao Pub/Sub.

    Responsavel por manter o registro de quais assinantes (subscribers)
    estao inscritos em quais topicos, e por notificar esses assinantes
    sempre que um publisher publica uma nova mensagem em um topico.

    O Broker eh o unico ponto que conhece tanto publishers quanto
    subscribers, garantindo o DESACOPLAMENTO entre eles: um publisher
    nunca chama diretamente um subscriber, e vice-versa.
    """

    def __init__(self):
        # Estrutura: { "NomeDoTopico": [assinante1, assinante2, ...] }
        self._topicos = {}

    def subscribe(self, topico, assinante):
        """
        Inscreve um assinante (subscriber) em um topico especifico.

        :param topico: string com o nome do topico (ex: "PedidoCriado")
        :param assinante: objeto que implementa o metodo notificar(topico, mensagem)
        """
        if topico not in self._topicos:
            self._topicos[topico] = []

        if assinante not in self._topicos[topico]:
            self._topicos[topico].append(assinante)
            print(f"[BROKER] {assinante.nome} inscrito no topico '{topico}'")

    def unsubscribe(self, topico, assinante):
        """
        Remove um assinante de um topico. A partir desse momento ele
        deixa de receber notificacoes referentes a esse topico.

        :param topico: string com o nome do topico
        :param assinante: objeto previamente inscrito no topico
        """
        if topico in self._topicos and assinante in self._topicos[topico]:
            self._topicos[topico].remove(assinante)
            print(f"[BROKER] {assinante.nome} removido do topico '{topico}'")

    def publish(self, topico, mensagem):
        """
        Publica uma mensagem em um topico. Todos os assinantes ativos
        naquele topico sao notificados de forma assincrona (simulada).

        :param topico: string com o nome do topico
        :param mensagem: dicionario (ou qualquer objeto) com os dados do evento
        """
        print(f"\n[BROKER] >> Evento publicado no topico '{topico}'")

        assinantes = self._topicos.get(topico, [])
        if not assinantes:
            print(f"[BROKER] Nenhum assinante ativo em '{topico}' no momento.")
            return

        # Notifica cada assinante inscrito naquele topico
        for assinante in assinantes:
            assinante.notificar(topico, mensagem)
