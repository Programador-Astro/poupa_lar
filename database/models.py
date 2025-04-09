from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import date

Base = declarative_base()

class Casa(Base):
    __tablename__ = 'casas'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), unique=True)
    nome = Column(String(100))
    uf = Column(String(50), nullable=False)
    cidade = Column(String(50), nullable=False)
    cep = Column(String(50), nullable=False)
    endereco = Column(String(50), nullable=False)
    numero = Column(String(50), nullable=False)
    complemento = Column(String(200), nullable=False)

    usuarios = relationship("Usuario", back_populates="casa")
    itens = relationship("ItemEstoque", back_populates="casa")

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    usuario = Column(String(50), unique=True, nullable=False)
    nome = Column(String(100))
    email = Column(String(120), unique=True)
    senha_hash = Column(Text)
    casa_id = Column(Integer, ForeignKey('casas.id'))

    casa = relationship("Casa", back_populates="usuarios")

class ItemEstoque(Base):
    __tablename__ = 'itens_estoque'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    categoria = Column(String(50))
    quantidade = Column(Integer)
    minimo = Column(Integer)
    casa_id = Column(Integer, ForeignKey('casas.id'))

    casa = relationship("Casa", back_populates="itens")
    precos = relationship("Preco", back_populates="item")

class Preco(Base):
    __tablename__ = 'precos'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('itens_estoque.id'))
    mercado = Column(String(100))
    preco = Column(Float)
    data = Column(Date, default=date.today)

    item = relationship("ItemEstoque", back_populates="precos")