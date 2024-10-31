from app.config.connection import engine
from asyncio import run
from app.utils.models import Base
from app.models.passagem_model import PassagemModel  # Importe seus modelos
from app.models.voo_model import VooModel  # Importe seus modelos
from app.models.user_model import UserModel  # Importe seus modelos
from datetime import datetime
from app.security.security import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
import logging

# Configuração de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Criando uma fábrica de sessões assíncronas
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def create_database():
    try:
        async with engine.begin() as conn:
            logging.info("Iniciando a recriação do banco de dados...")
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            logging.info("Banco de dados recriado com sucesso!")
    except Exception as e:
        logging.error(f"Erro ao recriar o banco de dados: {e}")

async def popular_banco():
    try:
        async with AsyncSessionLocal() as session:  # Usando a sessão assíncrona
            logging.info("Populando o banco de dados com dados iniciais...")

            # Criando 10 voos
            voos = [
                VooModel(origem="São Paulo", destino="Rio de Janeiro", capacidade_voo=2, companhia_aerea="Azul"),
                VooModel(origem="Belo Horizonte", destino="Brasília", capacidade_voo=2, companhia_aerea="Gol"),
                VooModel(origem="Curitiba", destino="Porto Alegre", capacidade_voo=2, companhia_aerea="Latam"),
                VooModel(origem="Fortaleza", destino="Recife", capacidade_voo=2, companhia_aerea="Gol"),
                VooModel(origem="Salvador", destino="Manaus", capacidade_voo=2, companhia_aerea="Azul"),
                VooModel(origem="Recife", destino="São Paulo", capacidade_voo=2, companhia_aerea="Latam"),
                VooModel(origem="Manaus", destino="Fortaleza", capacidade_voo=2, companhia_aerea="Azul"),
                VooModel(origem="Porto Alegre", destino="Curitiba", capacidade_voo=2, companhia_aerea="Gol"),
                VooModel(origem="Brasília", destino="Salvador", capacidade_voo=2, companhia_aerea="Azul"),
                VooModel(origem="Rio de Janeiro", destino="Fortaleza", capacidade_voo=2, companhia_aerea="Latam"),
            ]

            # Criando 10 usuários
            usuarios = [
                UserModel(nome="João Silva", username="joao_silva", password="senha123", cpf="123.456.789-00"),
                UserModel(nome="Maria Souza", username="maria_souza", password="senha456", cpf="987.654.301-00"),
                UserModel(nome="Carlos Pereira", username="carlos_pereira", password="senha789", cpf="456.789.123-00"),
                UserModel(nome="Ana Lima", username="ana_lima", password="senha101", cpf="789.123.456-00"),
                UserModel(nome="Pedro Rocha", username="pedro_rocha", password="senha202", cpf="321.654.987-00"),
                UserModel(nome="Mariana Alves", username="mariana_alves", password="senha303", cpf="654.321.987-00"),
                UserModel(nome="Luis Martins", username="luis_martins", password="senha404", cpf="987.654.321-00"),
                UserModel(nome="Carla Torres", username="carla_torres", password="senha505", cpf="147.258.369-00"),
                UserModel(nome="Bruno Costa", username="bruno_costa", password="senha606", cpf="258.369.147-00"),
                UserModel(nome="Fernanda Dias", username="fernanda_dias", password="senha707", cpf="369.147.258-00"),
            ]

            # Inserindo voos no banco
            for voo in voos:
                session.add(voo)

            # Inserindo usuários no banco
            for usuario in usuarios:
                usuario.password = get_password_hash( usuario.password)
                session.add(usuario)

            await session.commit()  # Commit para salvar as alterações no banco
            logging.info("Dados iniciais inseridos com sucesso!")
    except Exception as e:
        logging.error(f"Erro ao popular o banco de dados: {e}")

async def main():
    await create_database()
    await popular_banco()

if __name__ == "__main__":
    run(main())
