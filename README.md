# RocketSeat - Desafio 01 - Agenda

Projeto criado como forma de fixar e avaliar os conhecimentos obtidos no módulo 3: "Comunicação em Tempo Real com Flask".
O [Desafio proposto](Desafio03.txt).

### Funcionalidades

Sample: Projeto de teste criado em aula simulando pagament com pix via api.


## Requisitos

- [Python 3.13](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [Docker Desktop](https://docs.docker.com/desktop/)

#### VSCode Extensions recomendadas:
- SQLite Viewer
- MySQL (database-client.com)

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/ShiniAkaiUsagi/rocketseat_python_flask_realtime_api.git

# 2. Acesse a pasta do projeto
cd rocketseat_python_python_flask_realtime_api

# 3. Execute o script de build para preparar as ferramentas e ambiente
sh scripts/build.sh

# O script executa:
# python.exe -m pip install --upgrade pip
# pip install -U poetry
# poetry self update
# poetry update
# poetry run pre-commit install

```

### Para executar os testes unitários de todos os projetos (aulas e desafio):
```bash
PYTHONPATH=. poetry run pytest
```
Observação: Os testes unitários dos projetos sql_alchemy_api e do desafio02
    estão utilizando um banco de dados na memória, não impactando a aplicação.

## Executando sample - Payments
PYTHONPATH=. poetry run python sample/payment/src/app.py

PYTHONPATH=. FLASK_APP=sample.payment.src.app poetry run flask shell
db.create_all()

