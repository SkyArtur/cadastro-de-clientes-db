import re
from hashlib import sha256

from pycep_correios import get_address_from_cep, WebService, exceptions

from modulos.mensagens import *


# ----------------------------------------------------------------------------------------------------------------------
#              Classe InputPadrao
# ----------------------------------------------------------------------------------------------------------------------
class InputPadrao:
    def __init__(self, input_usuario="=> ", tipo_input=None, minn=None, maxx=None):
        """Entrada de dados do programa. Construtor da classe, disponibiliza o
        input para o usuário, pode controlar o tipo de input desejado (int, float, str),
        pode controlar a dimensão numérica dos menus (minn, maxx).

        Constructors:
            - __init__()

        Privates:
            - __meu_input()

        Operators:
            - __repr__(), __str__(), __len__(), __iter__(), __eq__(), __le__(), __lt__(), __ge__(), __gt__().

        Methods:
            - menu_input()
            - cep_input()

        Properties:
            - conteudo

        :param input_usuario: Any
        :param tipo_input: int: int | float: float | str: None
        :param minn: int - menor opção de um menu.
        :param maxx: int - maior opção do menu.
        """
        self.__input_do_usuario = self.__meu_input(input_usuario, tipo_input)
        self.__min = minn
        self.__max = maxx
        self.__padrao_data = "([0-3][0-9])([0-1][0-9])([0-9]{4})"
        self.__padrao_tel = "([0-9]{2})([0-9]{4,5})([0-9]{4})"

    def __repr__(self):
        return self.__input_do_usuario

    def __str__(self):
        return self.__input_do_usuario

    def __iter__(self):
        return iter(self.__input_do_usuario)

    def __len__(self):
        return len(self.__input_do_usuario)

    def __eq__(self, other):
        return self.__input_do_usuario == other

    def __ne__(self, other):
        return self.__input_do_usuario != other

    def __lt__(self, other):
        return self.__input_do_usuario < other

    def __le__(self, other):
        return self.__input_do_usuario <= other

    def __gt__(self, other):
        return self.__input_do_usuario > other

    def __ge__(self, other):
        return self.__input_do_usuario >= other

    @property
    def conteudo(self):
        """Getter da classe InputPadrao.

        :return: input do usuário -> int | float | str
        """
        return self.__input_do_usuario

    def __meu_input(self, input_usuario, tipo_input=None):
        """Função privada da classe InputPadrao. Faz o tratamento dos inputs do programa.

        :param input_usuario: Any
        :param tipo_input: int | float | str
        :return: input_usuario -> int | float | str
        """
        if tipo_input == int:
            while True:
                try:
                    self.__input_do_usuario = int(input(input_usuario))
                except ValueError:
                    print(digite_apenas_int)
                else:
                    return int(self.__input_do_usuario)
        elif tipo_input == float:
            while True:
                try:
                    self.__input_do_usuario = float(input(input_usuario))
                except ValueError:
                    print(digite_apenas_float)
                else:
                    return float(self.__input_do_usuario)
        else:
            while True:
                try:
                    self.__input_do_usuario = input(input_usuario)
                except ValueError:
                    print(algo_errado_aconteceu)
                else:
                    return self.__input_do_usuario

    def num_conta_input(self):
        self.__input_do_usuario = f'{self.__input_do_usuario:0>5}-2'
        return  self.__input_do_usuario

    def senha_input(self):
        self.__input_do_usuario = sha256(bytes(self.__input_do_usuario, 'utf-8')).hexdigest()
        return self.__input_do_usuario

    def menu_input(self):
        """Método para tratamento da entrada de opções em menus.

        :return: input_do_usuario -> int
        """
        while self.__input_do_usuario < self.__min or self.__input_do_usuario > self.__max:
            print(opcao_invalida)
            self.__input_do_usuario = self.__meu_input('=> ', int)
        else:
            return int(self.__input_do_usuario)

    def tel_input(self):
        while True:
            try:
                tel = re.search(self.__padrao_tel, str(self.__input_do_usuario))
                ddd, pref, suf = tel.group(1), tel.group(2), tel.group(3)
                return f"({tel.group(1)}){tel.group(2)}-{tel.group(3)}"
            except AttributeError:
                print(opcao_invalida)
                self.__input_do_usuario = self.__meu_input('DIGITE O TELEFONE: ')
                continue

    def cep_input(self):
        """Método para tratamento da entrada do CEP.

        :return: input_do_usuario -> str
        """
        while True:
            try:
                cep = get_address_from_cep(self.__input_do_usuario, webservice=WebService.VIACEP)
            except exceptions.BaseException:
                print(cep_invalido)
                self.__input_do_usuario = self.__meu_input('DIGITE O CEP:  ')
                continue
            else:
                numero = self.__meu_input('DIGITE O NÚMERO DA RESIDÊNCIA:  ')
                endereco = [cep['logradouro'], numero, cep['cep'],
                            cep['bairro'], cep['cidade'], cep['uf']]
                del cep
                return endereco

    def cpf_input(self):
        while not validador_cpf(self.__input_do_usuario).confirmar_cpf:
            print(cpf_invalido)
            self.__input_do_usuario = self.__meu_input('=>')
        else:
            return validador_cpf(self.__input_do_usuario).confirmar_cpf

    def data_input(self):
        while True:
            try:
                data = re.search(self.__padrao_data, str(self.__input_do_usuario))
                dia, mes, ano = data.group(1), data.group(2), data.group(3)
                if not len(self.__input_do_usuario) == 8 or not self.__input_do_usuario.isnumeric():
                    raise AttributeError
                if (int(dia) < 1) or (int(dia) > 31):
                    raise AttributeError
                if (int(mes) < 1) or (int(mes) > 12):
                    raise AttributeError
                if (int(ano) < 1900) or (int(ano) > 2100):
                    raise AttributeError
            except AttributeError:
                print(opcao_invalida)
                self.__input_do_usuario = self.__meu_input('DATA A DATA DE NASCIMENTO:  ')
                continue
            else:
                return f"{dia}/{mes}/{ano}"


# ----------------------------------------------------------------------------------------------------------------------
#              Classe menu
# ----------------------------------------------------------------------------------------------------------------------
class Menu:
    """Classe para construção dos menus do programa.

    Properties:
       - menu_inicial
       - menu_creditos
       - menu_operacoes
    """

    @property
    def menu_inicial(self):
        """Propriedade para construção do menu inicial do programa.

        :return: resposta_do_usuario -> int
        """
        resposta_do_usuario = InputPadrao(f'{montar_menu_inicial}\n=> ', int, 0, 2).menu_input()
        return resposta_do_usuario

    @property
    def menu_creditos(self):
        """Propriedade para construção do menu para definição dos créditos do usuário.

        :return: resposta_usuario -> int
        """
        resposta_usuario = InputPadrao(f'{montar_menu_creditos}\n=> ', int, 1, 2).menu_input()
        return resposta_usuario

    @property
    def menu_operacoes(self):
        """Propriedade para construção do menu para realização de operações em conta.

        :return: resposta_usuario -> int
        """
        resposta = InputPadrao(f'{montar_menu_operacoes}\n=> ', int, 0, 4).menu_input()
        return resposta

    @property
    def menu_busca(self):
        resposta = InputPadrao(f'{montar_menu_busca}\n=> ', int, 0, 3).menu_input()
        return resposta
# ----------------------------------------------------------------------------------------------------------------------
#                       Classe CPF
# --------------------------------------------------------------------------------------------------------------------
class validador_cpf:
    def __init__(self, documento):
        self.__cpf = documento
        self.__padrao_cpf = '([0-9]{3})([0-9]{3})([0-9]{3})([0-9]{2})'

    @property
    def confirmar_cpf(self):
        while True:
            try:
                cpf = re.search(self.__padrao_cpf, self.__cpf)
                if self.__validar():
                    return f'{cpf.group(1)}.{cpf.group(2)}.{cpf.group(3)}-{cpf.group(4)}'
                else:
                    print(cpf_invalido)
                    return False
            except AttributeError:
                return False

    def __validar(self):
        primeiro_digito, segundo_digito = 0, 0

        for i, j in enumerate(range(10, 1, -1)):
            primeiro_digito += int(self.__cpf[i]) * j
        primeiro_digito = 11 - (primeiro_digito % 11)
        primeiro_digito = 0 if primeiro_digito > 9 else primeiro_digito

        for i, j in enumerate(range(11, 1, -1)):
            segundo_digito += int(self.__cpf[i]) * j
        segundo_digito = 11 - (segundo_digito % 11)
        segundo_digito = 0 if segundo_digito > 9 else segundo_digito

        if f"{primeiro_digito}{segundo_digito}" in self.__cpf:
            return True
        else:
            raise AttributeError
