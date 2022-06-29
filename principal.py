import os
from time import sleep as espere

from modulos.bancodados import BancoDeDados, AuxTabExtratos
from modulos.inputpadrao import InputPadrao, Menu
from modulos.mensagens import *


class Gerenciador:
    def __init__(self):
        BancoDeDados(), AuxTabExtratos()
        self.__dados = list()
        self.__data_hora = strftime('%d/%m/%Y - %H:%M')
        self.__data_abertura = strftime('%d/%m/%Y')

    def abrir_nova_conta(self):
        print(cadastro_do_cliente)
        while True:
            try:
                self.__dados.append(BancoDeDados().gerar_numero_de_conta())
                nome = InputPadrao('DIGITE O NOME DO CLIENTE: ').conteudo.lower()
                if not BancoDeDados().validar_nome_cliente(nome):
                    self.__dados.append(nome)
                else:
                    print(cliente_ja_cadastrado)
                    self.__dados.clear()
                    raise ValueError
                self.__dados.append(InputPadrao('DIGITE A DATA DE NASCIMENTO: ').data_input())
                cpf = InputPadrao('DIGITE O CPF: ').cpf_input()
                if not BancoDeDados().validar_cpf_cliente(cpf):
                    self.__dados.append(cpf)
                else:
                    print(cpf_ja_cadastrado)
                    self.__dados.clear()
                    raise ValueError
                self.__dados.append(InputPadrao('DIGITE O NÚMERO DE TELEFONE: ').tel_input())
                self.__dados += InputPadrao('DIGITE O CEP: ').cep_input()
                self.__dados.append(InputPadrao('DIGITE A SENHA DO CLIENTE: ').senha_input())
                self.__dados.append(self.__data_abertura)
                self.__dados.append(InputPadrao('DIGITE O DEPÓSITO INICIAL: ', float).conteudo)
                limite = Menu().menu_creditos
                if limite == 1:
                    self.__dados.append(InputPadrao('DIGITE O LIMITE INICIAL: ', float).conteudo)
                else:
                    self.__dados.append(0)
                self.__dados.append(self.__dados[-2] + self.__dados[-1])
            except ValueError:
                self.limpe_a_tela()
                continue
            else:
                self.limpe_a_tela()
                __dados = tuple(self.__dados)
                BancoDeDados().inserir_dados_do_cliente(self.__dados)
                AuxTabExtratos().inserir_dados_extrato(
                    (self.__dados[0], 'Abertura', self.__data_hora, self.__dados[-3]))
                self.limpe_a_tela()
                return

    def operacao_conta(self):
        self.limpe_a_tela()
        print(operacoes_em_conta)
        numero_conta = self.buscar_cliente()
        if not numero_conta:
            self.limpe_a_tela()
            return False
        while True:
            print(operacoes_em_conta)
            operacoes = Menu().menu_operacoes
            if operacoes == 1:
                valor = InputPadrao('DIGITE O VALOR DO SAQUE: ', float).conteudo
                BancoDeDados().altera_saldo_limite((valor, numero_conta))
                AuxTabExtratos().inserir_dados_extrato((numero_conta, 'Saque', self.__data_hora, -valor))
                self.limpe_a_tela()
                BancoDeDados().acessar_dados_do_cliente(numero_conta)
                print(msg_gerenciador_saque, f"R${valor:.2f}")
            elif operacoes == 2:
                valor = InputPadrao('DIGITE O VALOR DO DEPÓSITO: ', float).conteudo
                BancoDeDados().altera_saldo_limite((valor, numero_conta), 'deposito')
                AuxTabExtratos().inserir_dados_extrato((numero_conta, 'Depósito', self.__data_hora, +valor))
                self.limpe_a_tela()
                BancoDeDados().acessar_dados_do_cliente(numero_conta)
                print(msg_gerenciador_deposito, f"R${valor:.2f}")
            elif operacoes == 3:
                valor = InputPadrao('DIGITE O NOVO LIMITE: ', float).conteudo
                BancoDeDados().altera_saldo_limite((valor, numero_conta), 'limite')
                AuxTabExtratos().inserir_dados_extrato((numero_conta, 'Novo Limite', self.__data_hora, valor))
                self.limpe_a_tela()
                BancoDeDados().acessar_dados_do_cliente(numero_conta)
                print(msg_gerenciador_limite, f"R${valor:.2f}")
            elif operacoes == 4:
                self.limpe_a_tela()
                BancoDeDados().acessar_dados_do_cliente(numero_conta)
                AuxTabExtratos().trazer_extrato(numero_conta)
            else:
                self.limpe_a_tela()
                break

    @staticmethod
    def limpe_a_tela():
        """Função que realiza a limpeza do console em tempo de execução.

        :return: command(clear | cls)
        """
        os.system(command='cls') if os.name in ['nt', 'dos'] else os.system(command='clear')

    @staticmethod
    def encerre_o_programa():
        """Função para encerramento do programa.

        :return: function(exit())
        """
        print('Encerrando.......')
        espere(1)
        return exit()

    @staticmethod
    def buscar_cliente():
        buscar = Menu().menu_busca
        if buscar == 1:
            numero_conta = InputPadrao('Digite o número da conta sem o digito: ').num_conta_input()
            return BancoDeDados().acessar_dados_do_cliente(numero_conta)
        elif buscar == 2:
            numero_cpf = InputPadrao('Digite o número de CPF: ').cpf_input()
            return BancoDeDados().acessar_dados_do_cliente(numero_cpf, 'cpf')
        elif buscar == 3:
            nome = InputPadrao('Digite o nome do Cliente: ').conteudo.lower()
            return BancoDeDados().acessar_dados_do_cliente(nome, 'nome')
        else:
            return False


# ----------------------------------------------------------------------------------------------------------------------
#                       Execução do Programa
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    Gerenciador().limpe_a_tela()
    print(abertura_do_programa)
    while True:
        print(sistema_de_cadastro_de_clientes)
        opcao = Menu().menu_inicial
        # Cadastrar Cliente
        if opcao == 1:
            Gerenciador().abrir_nova_conta()
        # Operações em Conta
        elif opcao == 2:
            Gerenciador().operacao_conta()
        # Encerrar Programa
        else:
            Gerenciador().encerre_o_programa()
