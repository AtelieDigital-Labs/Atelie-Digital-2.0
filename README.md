# 🏗️ Infraestrutura Global, Gateway e Bancos — Ateliê Digital 2.0

## 📖 Sobre o Projeto
O **Ateliê Digital 2.0** é um ecossistema distribuído baseado em microsserviços criado para operar como um marketplace completo de produtos artesanais. O objetivo do ecossistema é interconectar artesãos e consumidores finais de forma altamente escalável, tolerante a falhas e auditável.

Neste repositório encontra-se a **camada de infraestrutura central, roteamento e persistência global** do projeto. Esta camada unifica a malha de comunicação, servidores de proxy reverso, bancos de dados relacionais e em memória, corretores de mensagens assíncronas, provedores de armazenamento de objetos e coletores de telemetria que servem como fundação imutável para a execução de todos os microsserviços do core (*Catalog*, *Accounts*, *Orders* e *Auditoria de Logs*).

---

## 🚀 Componentes de Infraestrutura e Stack

A topologia arquitetural da infraestrutura do Ateliê Digital 2.0 é composta pelas seguintes soluções conteinerizadas:

* **Nginx:** Atua como Proxy Reverso e API Gateway central da aplicação. É responsável pelo roteamento inteligente de requisições externas para seus respectivos microsserviços, terminação TLS/SSL, limitação de taxa (*rate limiting*) e centralização de logs de acesso.
* **PostgreSQL (Multi-tenant por Esquema):** Banco de dados relacional unificado para persistência de dados estruturados e de auditoria. Para otimizar recursos sem perder o isolamento, utiliza-se uma abordagem multilocatária (*multi-tenant*) dividida em **schemas lógicos isolados**:
  * `accounts`: Dados cadastrais, perfis e carteiras financeiras.
  * `catalog`: Cadastro de produtos, variações, lojas e categorias.
  * `orders`: Pedidos.
  * `logs`: Registros imutáveis de auditoria de eventos e trilhas de compliance.
* **Redis:** Banco de dados chave-valor em memória de altíssima velocidade. É utilizado exclusivamente pelo microsserviço de *Orders* para o gerenciamento volátil de **carrinhos de compras ativos** e cache temporário de **cálculos de frete**.
* **RabbitMQ:** Message Broker (corretor de mensagens) oficial do ecossistema, encarregado de gerenciar as filas e exchanges para toda a comunicação assíncrona orientada a eventos entre os serviços.
* **MinIO:** Servidor de armazenamento de objetos de alta performance e totalmente compatível com a API do Amazon S3. Utilizado para armazenar mídias estáticas do sistema, tais como fotos de perfis de usuários e imagens em alta resolução do catálogo de produtos.
* **OpenTelemetry (Otel) + GLMT Stack:** Infraestrutura completa de observabilidade distribuída. Utiliza coletores OpenTelemetry integrados à stack Grafana, Loki, Mimir e Tempo (GLMT) para capturar de forma centralizada métricas, traces distribuídos (APM) e logs agregados de toda a malha de microsserviços.
* **Docker & Docker Compose:** Tecnologia de conteinerização utilizada para empacotar, isolar e orquestrar de forma imutável cada um dos componentes descritos na mesma malha de rede.

---
## 🛠️ Pipeline de CI/CD (GitHub Actions)

A infraestrutura e a validação do código contam com automações rigorosas integradas via GitHub Actions através do workflow **Python CI**. O pipeline é disparado automaticamente a cada **Pull Request** destinado às branches `main` e `develop`.

A execução do pipeline roda de forma paralela em ambientes isolados (`ubuntu-latest`) utilizando uma estratégia de matriz para garantir a compatibilidade do ecossistema nas versões **Python 3.12** e **Python 3.13**, executando sequencialmente as seguintes etapas:

1. **Setup do Ambiente e Instalação Otimizada:**
   * Realiza o checkout do código fonte.
   * Configura a versão correspondente do Python.
   * Instala o gerenciador de pacotes **uv** de forma automatizada.
2. **Gerenciamento de Cache:**
   * Utiliza uma camada de cache inteligente para o diretório `~/.cache/uv` baseada no hash do arquivo `uv.lock`. Isso acelera drasticamente o tempo de execução dos próximos builds evitando downloads redundantes.
3. **Sincronização de Dependências:**
   * Instala e sincroniza todas as dependências de produção e desenvolvimento do projeto utilizando o comando de alta performance `uv sync --dev`.
4. **Análise Estática e Qualidade (Lint):**
   * Executa a checagem de erros de sintaxe, boas práticas e PEP 8 através do comando `uv run ruff check .`.
   * Valida se a formatação do código cumpre os padrões estabelecidos utilizando `uv run ruff format --check .`.
5. **Testes Automatizados:**
   * Executa toda a suíte de testes unitários e de integração do projeto utilizando o comando `uv run pytest`, garantindo que nenhuma alteração quebre as regras de negócio antes de permitir o merge.
---

## ⚙️ Configuração do Ambiente

Para implantar a infraestrutura em seu ambiente local ou de homologação, certifique-se de possuir o **Docker** e o **Docker Compose** instalados.

### 1. Clonar e Configurar Variáveis de Ambiente
Na raiz do repositório de infraestrutura, configure as credenciais globais copiando o arquivo de exemplo:
```bash
cp .env.example .env
```
*(Preencha as senhas mestras do PostgreSQL, usuários do RabbitMQ, chaves de acesso do MinIO e tokens de autenticação do OpenTelemetry no arquivo `.env` gerado).*

### 2. Criação da Rede Global do Projeto
Para que os microsserviços do core consigam se conectar a estes bancos e componentes de forma isolada e segura, é **obrigatório** que todos façam parte da mesma rede virtual estável do Docker. Caso ainda não tenha criado, execute:

```bash
docker network create atelie-network
```

---

## ▶️ Como Executar a Infraestrutura

Com a rede criada e o arquivo `.env` preenchido, você pode gerenciar o ciclo de vida de toda a base do projeto através do Docker Compose.

### Passo 1: Construir e Iniciar os Containers
Para realizar o download das imagens oficiais, construir as customizações e iniciar os serviços em segundo plano (*detached mode*), execute:

```bash
docker compose up -build -d
```

### Passo 2: Verificar a Saúde dos Serviços
Após a execução do comando, os componentes começarão a se inicializar na malha de rede `atelie-network`. Você pode validar se todos os containers estão saudáveis executando:

```bash
docker compose ps
```

---

## 🎛️ Portas e Serviços Expostos

Por padrão, a configuração do Nginx e do compose expõe os seguintes pontos de acesso locais para desenvolvimento e administração:

| Componente | Porta Exposta | Descrição / Painel de Controle |
| :--- | :--- | :--- |
| **Nginx (Gateway)** | `80` / `443` | Ponto de entrada unificado para todas as requisições HTTP/HTTPS da API. |
| **PostgreSQL** | `5432` | Conexão externa com o banco de dados principal (multi-schema). |
| **Redis** | `6379` | Banco em memória para gerenciamento de sessões de carrinhos e fretes. |
| **RabbitMQ Admin** | `15672` | Painel Web de gerenciamento de filas, exchanges e conexões de mensageria. |
| **MinIO Console** | `9001` | Interface Web para administração de buckets de arquivos e permissões S3. |
| **Grafana (GLMT)** | `3000` | Painel centralizado para visualização das métricas, traces e logs do OpenTelemetry. |

---

## 🐋 Comandos Úteis de Operação (CLI)

Abaixo estão listados os comandos mais utilizados para gerenciar e monitorar a infraestrutura global:

* **Visualizar logs em tempo real:**
  ```bash
  docker compose logs -f
  ```
* **Visualizar logs de um serviço específico (ex: Nginx):**
  ```bash
  docker compose logs -f nginx
  ```
* **Reiniciar um componente específico (ex: Broker de Mensagens):**
  ```bash
  docker compose restart rabbitmq
  ```
* **Derrubar a infraestrutura mantendo os volumes de dados salvos:**
  ```bash
  docker compose down
  ```
* **Derrubar a infraestrutura limpando todos os volumes e dados persistidos (Reset Geral):**
  ```bash
  docker compose down -v
  ```
