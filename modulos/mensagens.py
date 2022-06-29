from time import strftime


# ----------------------------------------------------------------------------------------------------------------------
#              EXIBIÇÕES DO PROGRAMA
# ----------------------------------------------------------------------------------------------------------------------
class Relatorios:
    def __init__(self, dados):
        self.__dados = dados
        self.__data = strftime('%d/%m/%Y - %H:%M')

    def _ralatorio_cliente(self):
        relatorio = f"""
{'-' * 70}
CONTA: {self.__dados['numero_conta']:<15}   DATA: {self.__data[:10]:<15} HORA: {self.__data[12:]} 
CLIENTE: {self.__dados['nome'].upper()} 
    | DATA NASC.: {self.__dados['data_nascimento']}  
    | CPF: {self.__dados['cpf']}
    | TELEFONE: {self.__dados['telefone']}
    | ENDEREÇO: {self.__dados['logradouro']} nº{self.__dados['numero_casa']}
        -> {self.__dados['bairro']} | {self.__dados['cidade']}/{self.__dados['uf']} | CEP: {self.__dados['cep']}
    | DATA DE ABERTURA: {self.__dados['data_abertura']}    
    | SALDO: ----------------------  R${self.__dados['saldo']:.2f}      
    | LIMITE: ---------------------  R${self.__dados['limite']:.2f}
    | DISPONÍVEL: -----------------  R${self.__dados['disponivel']:.2f}
{'-' * 70}"""
        return relatorio

    def _relatorio_de_busca(self):
        relatorio = f"""DATA: {self.__data[:10]:<15} HORA: {self.__data[12:]} 
{'CONTA':^15} | {'CLIENTE':^25} | {'CPF':^20}
{self.__dados['numero_conta']:^15}   | {self.__dados['nome'].upper():^25}  | {self.__dados['cpf']:^20}"""
        return relatorio

    def _relatorio_extrato(self):
        relatorio = f"""{self.__dados['op']:^15} | {self.__dados['data']:^20} | {self.__dados['valor']:^15}"""
        return relatorio


# ----------------------------------------------------------------------------------------------------------------------
#              MÓDULO BANCO DE DADOS
# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------- COMANDOS TABELA CLIENTES -----------------------------------------------------
criar_tabela_clientes = '''CREATE TABLE clientes 
(numero_conta text, nome text, data_nascimento text, cpf text, 
telefone text, logradouro text, numero_casa text, cep text, 
bairro text, cidade text, uf text, senha text, data_abertura text,
saldo real, limite real, disponivel real)'''

inserir_dados_do_cliente = '''
INSERT INTO clientes 
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

buscar_todos_os_clientes = '''
SELECT numero_conta, nome, cpf 
FROM clientes 
VALUE'''

acessar_por_numero_conta = '''
SELECT * 
FROM clientes 
WHERE numero_conta=?'''

acessar_por_nome = '''
SELECT * 
FROM clientes 
WHERE nome=?'''

acessar_por_cpf = '''
SELECT * 
FROM clientes 
WHERE cpf=?'''

procurar_por_nome = '''
SELECT numero_conta, nome, cpf 
FROM clientes 
WHERE nome=?'''

procurar_por_cpf = '''
SELECT numero_conta, nome, cpf 
FROM clientes 
WHERE cpf=?'''

gerar_numero_de_conta = '''
SELECT numero_conta 
FROM clientes'''

alterar_saldo_update = '''
UPDATE clientes 
SET saldo=?, limite=?, disponivel=? 
WHERE numero_conta=?'''

alterar_saldo_select = '''
SELECT saldo, limite, disponivel 
FROM clientes 
WHERE numero_conta=?'''

validar_numero_conta = '''
SELECT numero_conta 
FROM clientes 
WHERE numero_conta=?'''

validar_nome_cliente = '''
SELECT nome 
FROM clientes'''

validar_cpf_cliente = '''
SELECT cpf 
FROM clientes'''

# --------------------------------------- COMANDOS TABELA EXTRATOS -----------------------------------------------------
criar_tabela_extratos = '''
CREATE TABLE extratos 
(numero_conta text, operacao text, data text, valor real)'''

inserir_dados_extrato = '''
INSERT INTO extratos 
VALUES (?,?,?,?)'''

trazer_extrato = '''
SELECT * 
FROM extratos 
WHERE numero_conta=?'''

# --------------------------------------- MENSAGENS TABELA CLIENTES ----------------------------------------------------
msg_inserir_dados_do_cliente = """Sucesso ao ralizar o cadastro do cliente:"""
msg_erro_buscar = """Infelizmente não pude encontrar:"""
msg_erro_inserir_dados_do_cliente = """ErroBancoDeDados~INSERT:
Algo de errado ocorreu ao cadastar do cliente."""

# --------------------------------------- MENSAGENS TABELA EXTRATO -----------------------------------------------------
msg_inserir_dados_extrato = """Conta aberta saldo inicial: """

msg_erro_inserir_dados_extrato = """ErroAuxiliarTabelaExtrato~INSERT:
    Algo de errado ocorreu ao registrar dados do extrato."""

msg_erro_trazer_extrato = """ErroAuxTabExtrato~SELECT:
    Infelizmente não pude encontrar o extrato da conta."""

# ----------------------------------------------------------------------------------------------------------------------
#              MÓDULO GERENCIADOR
# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------- MENSAGENS --------------------------------------------------------------------

cliente_ja_cadastrado = '''ErroCadastro ~01:
    Cliente já cadastrado!'''
cpf_ja_cadastrado = '''ErroCadastro ~02:
    CPF já cadastrado!'''
cliente_nao_encontrado = '''ErroCadastro ~03:
    Cliente não encontrado!'''
valor_excedeu_limite = '''ErroLimite ~01:
    O valor de saque excede seu limite disponível'''
# ----------------------------------------------------------------------------------------------------------------------
#              Mensagens do módulo principal
# ----------------------------------------------------------------------------------------------------------------------
abertura_do_programa = '''Exercício prático no aprendizado em Python.
Copyright (c) 2022 - Ponta Grossa/PR. 
Projeto Cadastro de Cliente.
Artur dos Santos Shon - EAD - UNINTER - 2021.'''
sistema_de_cadastro_de_clientes = f'''{'-' * 70}
{"Sistema de Cadastro de Clientes":^70}
{'-' * 70}'''
cadastro_do_cliente = f'''{'-' * 70}
{"Cadastro do Cliente":^70}
{'-' * 70}'''
operacoes_em_conta = f'''{'-' * 70}
{"Operações em Conta":^70}
{'-' * 70}'''
# ----------------------------------------------------------------------------------------------------------------------
#              Mensagens do módulo registrador
# ----------------------------------------------------------------------------------------------------------------------
cpf_invalido = """ErroDocumento ~01:
    Número do CPF não é válido!
"""
cep_invalido = """ErroCep ~01:
    número de CEP inválido!
"""
endereco_encontrado = """MensagemCep ~01:
    Endereço encontrado!
"""

# ----------------------------------------------------------------------------------------------------------------------
#              Mensagens do módulo gerenciador
# ----------------------------------------------------------------------------------------------------------------------
msg_gerenciador_abertura_de_conta = """MensagemGerente ~01:
    Conta aberta com sucesso."""
msg_gerenciador_saque = """Saque realizado com sucesso:
    VALOR:"""
msg_gerenciador_deposito = """Deposit realizado com sucesso:
    VALOR:"""
msg_gerenciador_limite = """Novo Limite:
    VALOR:"""
msg_gerenciador_03 = f"""MensagemGerente ~03:
    Arquivo não encontrado."""

# ----------------------------------------------------------------------------------------------------------------------
#              Mensagens do módulo entrada
# ----------------------------------------------------------------------------------------------------------------------
digite_apenas_int = f'''ErroEntrada ~01:
    São aceitos apenas números inteiros.'''
digite_apenas_float = f'''ErroEntrada ~02:
    Não são aceitos letras ou caractéres especiais.
    Use o ponto(.) ao invés da vírgula(,) para separar
    casas decimais.'''
algo_errado_aconteceu = f'''ErroEntrada ~03:
    Parece que você digitou algo errado!'''
opcao_invalida = f'''InputMenuError ~01:
    Parece que você digitou uma opção inválida!!'''
entrada_invalida_cep = f'''InputCepError ~01:
    Parece que você digitou algo inválido.
    Por favor, digite apenas os números.'''
montar_menu_busca = """Buscar Cliente por:
    (1) Número da conta | (2) CPF do Titular | (3) Nome 
        [0] Retornar"""
montar_menu_inicial = """Menu Inicial:
    (1) Cadastrar Novo Cliente | (2) Operações em Conta 
        [0] Encerrar"""
montar_menu_creditos = """Deseja definir os créditos do cliente?
    (1) Sim | (2) Não"""
montar_menu_operacoes = """Qual operação deseja realizar?
    (1) Sacar | (2) Depositar | (3) Novo Crédito | (4) Consultar extrato
        [0] Retornar"""
