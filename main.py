"""
========================================================================
 MODULO: main.py
 DESCRICAO: Script principal que simula o funcionamento do padrao
            Pub/Sub aplicado a uma Plataforma de E-commerce / Gestao
            de Pedidos.

 FLUXO SIMULADO:
   1. Cliente cria um pedido               -> topico "PedidoCriado"
   2. Pagamento eh aprovado                -> topico "PagamentoAprovado"
   3. Pedido eh enviado pela transportadora -> topico "EnvioRealizado"
   4. Pedido eh entregue ao cliente         -> topico "PedidoEntregue"

 Tambem demonstramos o unsubscribe: o Setor Fiscal se desinscreve
 apos o primeiro pedido e deixa de receber notificacoes do segundo.
========================================================================
"""

from pubsub import PubSubBroker
from publishers import Loja, GatewayPagamento, CentroDistribuicao
from subscribers import ServicoNotificacaoCliente, SetorEstoque, SetorFiscal


def linha(titulo):
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)


def main():
    # ------------------------------------------------------------
    # 1. Instancia o Broker (unico ponto central de comunicacao)
    # ------------------------------------------------------------
    broker = PubSubBroker()

    # ------------------------------------------------------------
    # 2. Instancia os publishers
    # ------------------------------------------------------------
    loja = Loja(broker)
    gateway_pagamento = GatewayPagamento(broker)
    centro_distribuicao = CentroDistribuicao(broker)

    # ------------------------------------------------------------
    # 3. Instancia os subscribers
    # ------------------------------------------------------------
    notificacao_cliente = ServicoNotificacaoCliente()
    estoque = SetorEstoque()
    fiscal = SetorFiscal()

    # ------------------------------------------------------------
    # 4. Inscreve os subscribers nos topicos de interesse
    # ------------------------------------------------------------
    linha("INSCRICOES INICIAIS")
    broker.subscribe("PedidoCriado", notificacao_cliente)

    broker.subscribe("PagamentoAprovado", notificacao_cliente)
    broker.subscribe("PagamentoAprovado", estoque)
    broker.subscribe("PagamentoAprovado", fiscal)

    broker.subscribe("EnvioRealizado", notificacao_cliente)
    broker.subscribe("EnvioRealizado", estoque)

    broker.subscribe("PedidoEntregue", notificacao_cliente)

    # ------------------------------------------------------------
    # 5. Simula o ciclo de vida do PEDIDO #1
    # ------------------------------------------------------------
    linha("PEDIDO #1001 - CICLO COMPLETO")

    loja.criar_pedido(
        id_pedido=1001,
        cliente="Adriano Alves",
        itens=["Teclado mecanico", "Mouse gamer"],
    )
    gateway_pagamento.aprovar_pagamento(id_pedido=1001, valor=459.90)
    centro_distribuicao.realizar_envio(
        id_pedido=1001, transportadora="Correios", codigo_rastreio="BR123456789"
    )
    centro_distribuicao.confirmar_entrega(id_pedido=1001)

    # ------------------------------------------------------------
    # 6. Demonstra o UNSUBSCRIBE: setor fiscal se desinscreve
    # ------------------------------------------------------------
    linha("SETOR FISCAL SE DESINSCREVE DO TOPICO 'PagamentoAprovado'")
    broker.unsubscribe("PagamentoAprovado", fiscal)

    # ------------------------------------------------------------
    # 7. Simula o ciclo de vida do PEDIDO #2
    #    (repare que o Setor Fiscal NAO recebe mais notificacoes)
    # ------------------------------------------------------------
    linha("PEDIDO #1002 - APOS O UNSUBSCRIBE DO SETOR FISCAL")

    loja.criar_pedido(
        id_pedido=1002,
        cliente="Maria Souza",
        itens=["Monitor 24 polegadas"],
    )
    gateway_pagamento.aprovar_pagamento(id_pedido=1002, valor=899.00)
    centro_distribuicao.realizar_envio(
        id_pedido=1002, transportadora="Jadlog", codigo_rastreio="JD987654321"
    )
    centro_distribuicao.confirmar_entrega(id_pedido=1002)


if __name__ == "__main__":
    main()
