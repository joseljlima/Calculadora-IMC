# Calculadora de IMC

Aplicativo desktop para calcular o Índice de Massa Corporal (IMC), salvar os cálculos em um banco de dados local e consultar o histórico. Feito em Python com [Flet](https://flet.dev) e [SQLAlchemy](https://www.sqlalchemy.org).

## Funcionalidades

- Cadastro de nome, idade, altura e peso
- Cálculo do IMC e classificação segundo a OMS
- Cards coloridos por faixa de resultado
- Mensagens de sucesso e erro temporárias
- Histórico de todos os cálculos salvos, em tela separada
- Banco de dados SQLite criado automaticamente

## Classificação do IMC

| IMC              | Classificação       |
|------------------|---------------------|
| Abaixo de 18,5   | Abaixo do peso      |
| 18,5 a 24,9      | Peso normal         |
| 25 a 29,9        | Sobrepeso           |
| 30 a 34,9        | Obesidade grau 1    |
| 35 a 39,9        | Obesidade grau 2    |
| 40 ou mais       | Obesidade grau 3    |

## Tecnologias

- Python 3.10 ou superior
- Flet 1.x (interface)
- SQLAlchemy (banco de dados)

## Estrutura do projeto

```text
Calculadora IMC/
├── main.py
├── models.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Instalação

1. Clone o repositório:

```bash
   git clone https://github.com/joseljlima/calculadora-imc.git
   cd calculadora-imc
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):

```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Linux/macOS
```

3. Instale as dependências:

```bash
   pip install -r requirements.txt
```

## Como executar

```bash
flet run main.py
```

Ou, se preferir, `python main.py`.

## Onde os dados são salvos

O banco de dados é o arquivo `bancoDados.db`, criado automaticamente na pasta do projeto na primeira execução.

- Rodando pelo código-fonte, o arquivo fica ao lado do `models.py`.
- No executável gerado pelo `flet build`, o arquivo fica junto aos arquivos do programa, dentro da pasta `build\windows\`.

Se o banco for apagado, o programa cria um novo vazio na próxima abertura.

## Gerar o executável (Windows)

```bash
flet build windows
```

O resultado fica em `build\windows\`. Para distribuir, copie a pasta inteira, porque o `.exe` depende dos arquivos ao lado dele.

Antes de rodar o build, é necessário:

- Ter o **Git** instalado e no PATH
- Ter o **Modo de Desenvolvedor** do Windows ativado (necessário para links simbólicos do Flutter)
- Ter o Visual Studio com as ferramentas de desenvolvimento para desktop C++

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.