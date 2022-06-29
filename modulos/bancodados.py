import sqlite3
from os import mkdir

from modulos.mensagens import *


# ----------------------------------------------------------------------------------------------------------------------
#       CLASSE AUXILIAR DO ARQUIVO DO BANCO DE DADOS
# ----------------------------------------------------------------------------------------------------------------------
class AuxiliarArquivo:

    # ----------------------------------------------------------------------------
    #  PROCURAR ARQUIVO
    # ----------------------------------------------------------------------------
    @staticmethod
    def _procura_banco():
        try:
            arquivo_banco = open('./banco/banco.db')
            arquivo_banco.close()
        except FileNotFoundError:
            return False
        else:
            return True

    # ----------------------------------------------------------------------------
    #  PROCURAR ARQUIVO
    # ----------------------------------------------------------------------------
    @staticmethod
    def _procura_extrato():
        try:
            arquivo_extrato = open('./banco/extratos.db')
            arquivo_extrato.close()
        except FileNotFoundError:
            return False
        else:
            return True


# ----------------------------------------------------------------------------------------------------------------------
#       CLASSE AUXILIAR DA TABELA DE EXTRATOS
# ----------------------------------------------------------------------------------------------------------------------
class AuxTabExtratos(AuxiliarArquivo, Relatorios):
    def __init__(self):
        if self._procura_extrato():
            self.__tabela_extrato = sqlite3.connect('./banco/extratos.db')
            self.__cursor = self.__tabela_extrato.cursor()
        else:
            self.__tabela_extrato = sqlite3.connect('./banco/extratos.db')
            self.__cursor = self.__tabela_extrato.cursor()
            self.__cursor.execute(criar_tabela_extratos)
            self.__tabela_extrato.commit()

    # ----------------------------------------------------------------------------
    #  INSERIR DADOS DO EXTRATO
    # ----------------------------------------------------------------------------
    def inserir_dados_extrato(self, dados):
        try:
            self.__cursor.execute(inserir_dados_extrato, dados)
            self.__tabela_extrato.commit()

        except sqlite3.Error:
            print(msg_erro_inserir_dados_extrato)
        else:
            print(msg_inserir_dados_extrato, f"R${dados[3]:.2f}")
            return self.__tabela_extrato.close()

    # ----------------------------------------------------------------------------
    #  TRAZER EXTRATO
    # ----------------------------------------------------------------------------
    def trazer_extrato(self, numero_conta):
        chaves = ['numero_conta', 'op', 'data', 'valor']
        try:
            self.__cursor.execute(trazer_extrato, (numero_conta,))
            extrato = self.__cursor.fetchall()
            self.__tabela_extrato.close()
        except IndexError:
            self.__tabela_extrato.close()
            print(msg_erro_trazer_extrato)
        else:
            print(f'{"OPERAÇÃO":^15} {"DATA":^25} {"SALDO":^20}')
            for operacao in extrato:
                lista = {(chaves[item], operacao[item]) for item in range(len(operacao))}
                print(Relatorios(dict(lista))._relatorio_extrato())


# ----------------------------------------------------------------------------------------------------------------------
#       CLASSE BANCO DE DADOS
# ----------------------------------------------------------------------------------------------------------------------
class BancoDeDados(AuxiliarArquivo, Relatorios):
    def __init__(self):
        if self._procura_banco():
            sqlite3.
            self.__cliente_db = sqlite3.connect('./banco/banco.db')
            self.__cursor = self.__cliente_db.cursor()
        else:
            self.__cliente_db = sqlite3.connect('./banco/banco.db')
            self.__cursor = self.__cliente_db.cursor()
            self.__cursor.execute(criar_tabela_clientes)
            self.__cliente_db.commit()

    # ----------------------------------------------------------------------------
    #  INSERIR DADOS DO CLIENTE
    # ----------------------------------------------------------------------------
    def inserir_dados_do_cliente(self, dados):
        conta = f'\n\tCONTA: {dados[0]}'
        cliente = f'\n\tCLIENTE: {dados[1].title()}'
        try:
            self.__cursor.execute(inserir_dados_do_cliente, dados)
            self.__cliente_db.commit()
            print(msg_inserir_dados_do_cliente + conta + cliente)
        except sqlite3.Error:
            print(msg_erro_inserir_dados_do_cliente)
        else:
            return self.__cliente_db.close()

    # ----------------------------------------------------------------------------
    #  BUSCAR TODOS OS CLIENTES
    # ----------------------------------------------------------------------------
    def buscar_todos_os_clientes(self):
        print('\tCONTA\t\t|\t\t\t\tNOME\t\t\t\t|\tCPF')
        for cliente in self.__cursor.execute(buscar_todos_os_clientes):
            print(f"{cliente[0]:^15} | {cliente[1]:^34}| {cliente[2]}".title())

    # ----------------------------------------------------------------------------
    #  VALIDAÇÕES PARA NÚMERO DE CONTA, NOME, CPF
    # ----------------------------------------------------------------------------
    def validar_numero_conta(self, numero_conta):
        for conta in self.__cursor.execute(validar_numero_conta, numero_conta):
            confirma = True if numero_conta == conta else False
            return confirma

    def validar_nome_cliente(self, nome_cliente):
        for nome in self.__cursor.execute(validar_nome_cliente):
            if nome_cliente in nome[0]:
                return True
        else:
            return False

    def validar_cpf_cliente(self, cpf_cliente):
        for cpf in self.__cursor.execute(validar_cpf_cliente):
            if cpf_cliente in cpf[0]:
                return True
        else:
            return False

    # ----------------------------------------------------------------------------
    #  GERAR NUMERO DE CONTA
    # ----------------------------------------------------------------------------
    def gerar_numero_de_conta(self):
        try:
            self.__cursor.execute(gerar_numero_de_conta)
            numero = list(self.__cursor.fetchall()[-1])
            numero = int(numero[0][:-2]) + 1
            self.__cliente_db.close()
        except IndexError:
            return '00001-2'
        else:
            return f"{numero:0>5}-2"

    # ----------------------------------------------------------------------------
    #  ACESSAR POR NUMERO DA CONTA
    # ----------------------------------------------------------------------------
    def acessar_dados_do_cliente(self, busca, ident='numero_conta'):
        chaves = ['numero_conta', 'nome', 'data_nascimento', 'cpf', 'telefone',
                  'logradouro', 'numero_casa', 'cep', 'bairro', 'cidade', 'uf',
                  'senha', 'data_abertura', 'saldo', 'limite', 'disponivel']
        if ident == 'nome':
            self.__cursor.execute(acessar_por_nome, (busca,))
        elif ident == 'cpf':
            self.__cursor.execute(acessar_por_cpf, (busca,))
        else:
            self.__cursor.execute(acessar_por_numero_conta, (busca,))
        try:
            conta = self.__cursor.fetchall()[0]
            self.__cliente_db.close()
        except IndexError:
            self.__cliente_db.close()
            print(msg_erro_buscar + busca)
        else:
            dados_da_conta = {chaves[x]: conta[x] for x in range(len(conta))}
            del dados_da_conta['senha']
            print(Relatorios(dados_da_conta)._ralatorio_cliente())
            return conta[0]

    # ----------------------------------------------------------------------------
    #  PROCURAR CLIENTE
    # ----------------------------------------------------------------------------
    def procurar_por_cpf_nome(self, item, ident=None):
        chaves = ['numero_conta', 'nome', 'cpf']
        if ident == 'nome':
            self.__cursor.execute(procurar_por_nome, (item,))
        else:
            self.__cursor.execute(procurar_por_cpf, (item,))
        try:
            cliente = self.__cursor.fetchall()[0]
            self.__cliente_db.close()
        except IndexError:
            self.__cliente_db.close()
            print(msg_erro_buscar + item)
        else:
            dados_cliente = {chaves[x]: cliente[x] for x in range(len(cliente))}
            print(Relatorios(dados_cliente)._relatorio_de_busca())

    # ----------------------------------------------------------------------------
    #  ALTERAR SALDO
    # ----------------------------------------------------------------------------
    def altera_saldo_limite(self, dados_de_saque: tuple, ident='saldo'):
        self.__cursor.execute(alterar_saldo_select, (dados_de_saque[1],))
        valores = self.__cursor.fetchall()[0]
        saldo, limite, disponivel = valores[0], valores[1], valores[2]
        if ident == 'limite':
            limite = dados_de_saque[0]
        elif ident == 'deposito':
            saldo = valores[0] + dados_de_saque[0]
        else:
            if disponivel >= dados_de_saque[0]:
                saldo = valores[0] - dados_de_saque[0]
            else:
                print(valor_excedeu_limite)
        disponivel = saldo + limite
        valores = tuple([saldo, limite, disponivel, dados_de_saque[1]])
        self.__cursor.execute(alterar_saldo_update, valores)
        self.__cliente_db.commit()
        self.__cliente_db.close()
