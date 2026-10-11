import os
from sqlalchemy import create_engine, Column, Integer, String,Float
from sqlalchemy.orm import sessionmaker, declarative_base

# Descobre a pasta onde este arquivo (models.py) está salvo
pasta_do_projeto = os.path.dirname(os.path.abspath(__file__))

# Monta o caminho completo do arquivo do banco dentro dessa pasta
caminho_banco = os.path.join(pasta_do_projeto, "bancoDados.db")

# O engine é a conexão principal com o banco. "sqlite:///bancoDados.db" indica
# que usaremos SQLite e que o arquivo do banco se chamará bancoDados.db,
# criado na mesma pasta do projeto.
engine = create_engine(f"sqlite:///{caminho_banco}")

# Base é a classe da qual todos os modelos (tabelas) herdam.
# O SQLAlchemy usa ela para saber quais tabelas existem.
Base = declarative_base()

# SessionLocal é uma "fábrica" de sessões. Cada sessão representa
# uma sequência de operações com o banco (adicionar, consultar, salvar).
SessionLocal = sessionmaker(bind=engine)

# Define a tabela "usuarios". Cada atributo da classe vira uma coluna.
class Usuario(Base):
    __tablename__ = "usuarios"  # nome da tabela no banco

    id = Column(Integer, primary_key=True)  # número único, gerado automaticamente
    nome = Column(String(50), nullable=False)  # texto de até 50 caracteres, obrigatório
    idade = Column(Integer, nullable=False)
    peso = Column(Float, nullable=False)
    altura = Column(Float, nullable=False)
    imc = Column(Float, nullable=False)            # resultado do cálculo
    classificacao = Column(String(50), nullable=False)

# Cria no banco todas as tabelas definidas a partir de Base.
# Se a tabela já existir, ela não é alterada nem apagada.
def criar_tabelas():
    Base.metadata.create_all(engine)

# Faixas do IMC segundo a OMS para adultos
def classificar_imc(valor):
    if valor < 18.5:
        return "Abaixo do peso"
    elif valor < 25:
        return "Peso normal"
    elif valor < 30:
        return "Sobrepeso"
    elif valor < 35:
        return "Obesidade grau 1"
    elif valor < 40:
        return "Obesidade grau 2"
    else:
        return "Obesidade grau 3"
    
# Recebe os dados já convertidos para número, calcula o IMC,
# salva no banco e devolve o id, o valor e a classificação.
def salvar_usuario(nome,idade,peso,altura):
    imc = peso/(altura ** 2)
    classificacao = classificar_imc(imc)
    
    # "with" abre a sessão e a fecha automaticamente ao final do bloco,
    # mesmo que ocorra algum erro.
    with SessionLocal() as session:
        # cria o objeto em memória
        novo_usuario = Usuario(nome=nome,
                               idade=idade,
                               peso=peso,
                               altura=altura,
                               imc=imc,
                               classificacao=classificacao)  
        
        session.add(novo_usuario)     # marca o objeto para ser salvo
        session.commit()              # grava de fato no banco de dados
        novo_id = novo_usuario.id
        return novo_id, imc, classificacao

# Retorna todos os cálculos salvos, do mais recente para o mais antigo.
# Cada item é uma tupla simples, para a interface não precisar conhecer o SQLAlchemy.
def listar_usuarios():
    with SessionLocal() as session:
        # order_by(...desc()) ordena do id maior (mais recente) para o menor
        usuarios = session.query(Usuario).order_by(Usuario.id.desc()).all()
        return [(u.nome, u.imc, u.classificacao) for u in usuarios]