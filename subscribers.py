"""
========================================================================
 MODULO: subscribers.py
 DESCRICAO: Subscribers (consumidores de eventos) do cenario de
            e-commerce. Cada um implementa o metodo notificar(),
            que eh chamado automaticamente pelo Broker quando um
            evento de interesse eh publicado.
========================================================================
"""


class ServicoNotificacaoCliente:
    """
    Simula o servico responsavel por avisar o cliente por E-mail/SMS
    sobre cada mudanca de status do pedido.
    """

    def __init__(self, nome="ServicoNotificacaoCliente"):
        self.nome = nome

    def notificar(self, topico, mensagem):
        pedido = mensagem.get("id_pedido")

        if topico == "PedidoCriado":
            print(f"[{self.nome}] E-mail enviado: pedido {pedido} recebido com sucesso!")
        elif topico == "PagamentoAprovado":
            print(f"[{self.nome}] SMS enviado: pagamento do pedido {pedido} aprovado!")
        elif topico == "EnvioRealizado":
            codigo = mensagem.get("codigo_rastreio")
            print(f"[{self.nome}] E-mail enviado: pedido {pedido} enviado (rastreio {codigo})")
        elif topico == "PedidoEntregue":
            print(f"[{self.nome}] SMS enviado: pedido {pedido} foi entregue. Aproveite!")


class SetorEstoque:
    """
    Simula o setor de estoque, que precisa dar baixa nos itens quando
    o pagamento eh aprovado e liberar a reserva quando o pedido eh enviado.
    """

    def __init__(self, nome="SetorEstoque"):
        self.nome = nome

    def notificar(self, topico, mensagem):
        pedido = mensagem.get("id_pedido")

        if topico == "PagamentoAprovado":
            print(f"[{self.nome}] Baixa de estoque efetuada para o pedido {pedido}")
        elif topico == "EnvioRealizado":
            print(f"[{self.nome}] Reserva de estoque liberada para o pedido {pedido}")


class SetorFiscal:
    """
    Simula o setor fiscal, responsavel por emitir a nota fiscal assim
    que o pagamento do pedido eh aprovado.
    """

    def __init__(self, nome="SetorFiscal"):
        self.nome = nome

    def notificar(self, topico, mensagem):
        pedido = mensagem.get("id_pedido")

        if topico == "PagamentoAprovado":
            valor = mensagem.get("valor")
            print(f"[{self.nome}] Nota fiscal emitida para o pedido {pedido} (R$ {valor:.2f})")
