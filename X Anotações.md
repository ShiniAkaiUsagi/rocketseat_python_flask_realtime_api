
## Conceitos

### WebSocket
Um Protocolo de comunicação bidirecional que permite uma comunicação eficiente em tempo real entre o servidor e o cliente.

Exemplos
- Aplicações de Chat em Tempo Real
- Rastreamento de Atividades
- Ferramentas de Colaboração em Tempo Real

#### Long Polling x WebSockets
Ao invés de, por exemplo, a cada 30s enviarmos um GET para obter determinada informação, o WebSocket está a todo o tempo ativo e se comunicando, são diversas atualizações para que tenhamos um retorno o mais rápido possível.

Exemplo:

LongPolling
2 requisições por segundo
120 por minuto
720 por hora

WebSocket
1 requisição única, com mínimo de latência e bilateral

#### Conclusão
O uso de websockets proporciona uma experiência mais fuida e eficiente em notificações em tempo real.