from modulos.gerenciador import *

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
