"""
========================================================================
 MODULO: publishers.py
 DESCRICAO: Publishers (produtores de eventos) do cenario de e-commerce.
            Cada publisher representa uma parte do sistema que GERA
            eventos de mudanca de status do pedido, sem saber quem
            vai consumir essa informacao (desacoplamento).
========================================================================
"""


class Loja:
    """
    Representa a plataforma de vendas (frontend/backend da loja).
    Publica o evento inicial: quando um cliente finaliza uma compra.
    """

    def __init__(self, broker):
        self.broker = broker

    def criar_pedido(self, id_pedido, cliente, itens):
        mensagem = {
            "id_pedido": id_pedido,
            "cliente": cliente,
            "itens": itens,
            "status": "PedidoCriado",
        }
        self.broker.publish("PedidoCriado", mensagem)


class GatewayPagamento:
    """
    Representa o gateway de pagamento (ex: integracao com um provedor
    de pagamentos). Publica o evento quando um pagamento eh aprovado.
    """

    def __init__(self, broker):
        self.broker = broker

    def aprovar_pagamento(self, id_pedido, valor):
        mensagem = {
            "id_pedido": id_pedido,
            "valor": valor,
            "status": "PagamentoAprovado",
        }
        self.broker.publish("PagamentoAprovado", mensagem)


class CentroDistribuicao:
    """
    Representa o centro de distribuicao/logistica. Publica os eventos
    de envio e de entrega do pedido.
    """

    def __init__(self, broker):
        self.broker = broker

    def realizar_envio(self, id_pedido, transportadora, codigo_rastreio):
        mensagem = {
            "id_pedido": id_pedido,
            "transportadora": transportadora,
            "codigo_rastreio": codigo_rastreio,
            "status": "EnvioRealizado",
        }
        self.broker.publish("EnvioRealizado", mensagem)

    def confirmar_entrega(self, id_pedido):
        mensagem = {
            "id_pedido": id_pedido,
            "status": "PedidoEntregue",
        }
        self.broker.publish("PedidoEntregue", mensagem)
