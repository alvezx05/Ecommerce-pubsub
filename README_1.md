# Pub/Sub - Plataforma de E-commerce / Gestão de Pedidos

**Disciplina:** Sistemas Computacionais Distribuídos e Computação em Nuvem
**Professor:** Ana Paula Rezende Dos Santos
**Integrantes do grupo:**
- Adriano Alves
- 
- 
- 

## 📖 Sobre o projeto

Este trabalho implementa o padrão arquitetural **Publish-Subscribe (Pub/Sub)** aplicado a uma **plataforma de e-commerce**, simulando o fluxo de status de um pedido em um sistema distribuído e desacoplado.

Em vez dos componentes se comunicarem diretamente, todos publicam e recebem eventos através de um **Broker central**, o que reduz o acoplamento entre as partes do sistema.

### Tópicos (eventos do pedido)
- `PedidoCriado`
- `PagamentoAprovado`
- `EnvioRealizado`
- `PedidoEntregue`

### Publishers (quem gera os eventos)
- **Loja** → publica `PedidoCriado`
- **Gateway de Pagamento** → publica `PagamentoAprovado`
- **Centro de Distribuição** → publica `EnvioRealizado` e `PedidoEntregue`

### Subscribers (quem consome os eventos)
- **Serviço de Notificação ao Cliente** (E-mail/SMS) → escuta todos os tópicos
- **Setor de Estoque** → escuta `PagamentoAprovado` (baixa) e `EnvioRealizado` (libera reserva)
- **Setor Fiscal** → escuta `PagamentoAprovado` (emite nota fiscal)

## 🗂️ Estrutura do repositório

```
ecommerce-pubsub/
├── pubsub.py        # Classe PubSubBroker (subscribe, unsubscribe, publish)
├── publishers.py     # Loja, GatewayPagamento, CentroDistribuicao
├── subscribers.py    # ServicoNotificacaoCliente, SetorEstoque, SetorFiscal
├── main.py           # Script de simulação do fluxo completo
└── README.md
```

## ▶️ Como executar

Pré-requisito: Python 3.8+ instalado.

```bash
git clone <link-do-repositorio>
cd ecommerce-pubsub
python3 main.py
```

O script simula dois pedidos completos (criação → pagamento → envio → entrega) e demonstra o `unsubscribe`: o Setor Fiscal se desinscreve do tópico `PagamentoAprovado` após o primeiro pedido e deixa de receber notificações no segundo.

## 🧠 Conceitos demonstrados

- **Broker/Gerenciador de Tópicos:** classe `PubSubBroker`, ponto central que conhece publishers e subscribers.
- **subscribe(topico, assinante):** inscreve um assinante em um tópico.
- **unsubscribe(topico, assinante):** remove um assinante, interrompendo o recebimento de eventos.
- **publish(topico, mensagem):** notifica todos os assinantes ativos daquele tópico.
- **Desacoplamento:** publishers não conhecem subscribers (e vice-versa) — toda comunicação passa pelo Broker.
