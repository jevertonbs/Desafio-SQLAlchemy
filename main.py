from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import select

Base = declarative_base()


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String(9), unique=True, autoincrement=True)
    address = Column(String(100))

    def __repr__(self) -> str:
        return f"""
                    Cliente
        
        Nome: {self.name} - ID: {self.id}
        CPF: {self.cpf}
        ENDEREÇO(s): {self.address}

        """


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    acc_type = Column(String, autoincrement=True)
    agency = Column(String, default="0001")
    acc_num = Column(Integer, unique=True)
    credit = Column(Float)
    id_client = Column(Integer, ForeignKey("client.id"), nullable=False)

    def __repr__(self) -> str:
        return f"""
                    Conta
        
        TIPO DA CONTA: {self.acc_type} - ID: {self.id}
        AGÊNCIA: {self.agency} - NUM. DA CONTA: {self.acc_num}

        SALDO: {self.credit}    ID DO CLIENTE: {self.id_client}

        """


engine = create_engine("sqlite://")
Base.metadata.create_all(engine)


with Session(engine) as session:
    joao = Client(
        name="João Silva",
        cpf="123456789",
        address="Rua blá blá Joao Silva",
    )

    marcos = Client(
        name="Marcos Filho",
        cpf="963521487",
        address="Rua blá blá Marcos Filho",
    )

    joao_acc = Account(
        acc_type="conta corrente",
        agency="0001",
        acc_num=7415876329,
        credit=500.0,
        id_client=1,
    )

    marcos_acc = Account(
        acc_type="conta poupanca",
        agency="0001",
        acc_num=4075215368,
        credit=70.0,
        id_client=2,
    )

    session.add_all([joao, joao_acc, marcos, marcos_acc])
    session.commit()


def consultas():
    """
    Lista de consultados no banco de dados usando as Querys.
    """

    print("==========================================================")
    print("\n       Retornar os dados do primeiro cliente do DB (ID 1)\n")
    client_id_statement = select(Client).where(Client.id.in_([1]))
    for c in session.scalars(client_id_statement):
        print(c)

    print("==========================================================")
    print(
        "\n     Retorna a inforamção da conta com relação ao primeiro cliente do DB (com o ID 1)\n"
    )
    acc_id_statement = select(Account).where(Account.id_client.in_([1]))
    for a in session.scalars(acc_id_statement):
        print(a)

    print("==========================================================")
    print("\n       Retorna somente as contas poupanças\n")
    acc_poupanca_statement = select(Account).where(
        Account.acc_type.in_(["conta poupanca"])
    )
    for p in session.scalars(acc_poupanca_statement):
        print(p)


consultas()
