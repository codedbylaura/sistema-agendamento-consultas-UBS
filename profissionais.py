import json
import os

profissionais = []

def salvar_json():
    with open("profissionais.json", "w") as f:
        json.dump(profissionais, f, indent=4, ensure_ascii=False)

def carregar_json():
    global profissionais
    if os.path.exists("profissionais.json"):
        with open("profissionais.json", "r") as f:
            profissionais = json.load(f)

carregar_json()

while True:
    opcao = int(input("Digite uma opção: \n 1- Cadastrar profissional \n 2- Listar profissionais \n 3- Editar profissional \n 4- Pesquisar profissional \n 5- Excluir profissional \n 6- Relatório \n 7- Sair\n"))
    match(opcao):
        case 1:
            nome = input("Digite o nome do profissional: ")
            cpf = input("Digite o CPF do profissional: ")
            registro = input("Digite o registro no conselho: ")
            especialidade = input("Digite a especialidade: ")
            telefone = input("Digite o telefone: ")
            email = input("Digite o e-mail: ")
            rua = input("Digite a rua: ")
            bairro = input("Digite o bairro: ")
            numero = input("Digite o número: ")
            profissional = {
                "nome": nome,
                "cpf": cpf,
                "registro": registro,
                "especialidade": especialidade,
                "telefone": telefone,
                "email": email,
                "endereco": {
                    "rua": rua,
                    "bairro": bairro,
                    "numero": numero
                }
            }
            profissionais.append(profissional)
            salvar_json()
            print("Profissional cadastrado com sucesso! É só colocar a mão na massa agora!")
        case 2:
            if len(profissionais) == 0:
                print("Não existem profissionais cadastrados! Equipe está vazia T-T")
            else:
                for p in profissionais:
                    print("Nome:", p["nome"], "\n CPF:", p["cpf"], "\n Registro:", p["registro"], "\n Especialidade:", p["especialidade"], "\n Telefone:", p["telefone"], "\n E-mail:", p["email"], "\n Endereço:", p["endereco"]["rua"], "-", p["endereco"]["bairro"], "-", p["endereco"]["numero"])
        case 3:
            cpf_busca = input("Digite o CPF do profissional que deseja editar: ")
            encontrado = False
            for p in profissionais:
                if p["cpf"] == cpf_busca:
                    p["nome"] = input("Novo nome: ")
                    p["registro"] = input("Novo registro: ")
                    p["especialidade"] = input("Nova especialidade: ")
                    p["telefone"] = input("Novo telefone: ")
                    p["email"] = input("Novo e-mail: ")
                    p["endereco"]["rua"] = input("Nova rua: ")
                    p["endereco"]["bairro"] = input("Novo bairro: ")
                    p["endereco"]["numero"] = input("Novo número: ")
                    salvar_json()
                    print("Profissional atualizado com sucesso! Dados tão novos como o sistema")
                    encontrado = True
            if not encontrado:
                print("Profissional não encontrado!")
        case 4:
            cpf_busca = input("Digite o CPF do profissional que deseja pesquisar: ")
            encontrado = False
            for p in profissionais:
                if p["cpf"] == cpf_busca:
                    print("Nome:", p["nome"], "\n CPF:", p["cpf"], "\n Registro:", p["registro"], "\n Especialidade:", p["especialidade"], "\n Telefone:", p["telefone"], "\n E-mail:", p["email"], "\n Endereço:", p["endereco"]["rua"], "-", p["endereco"]["bairro"], "-", p["endereco"]["numero"])
                    encontrado = True
            if not encontrado:
                print("Profissional não encontrado! Fantasma? Nem, provavel os dados forem inseridos errados.")
        case 5:
            cpf_busca = input("Digite o CPF do profissional que deseja excluir: ")
            encontrado = False
            for p in profissionais:
                if p["cpf"] == cpf_busca:
                    profissionais.remove(p)
                    salvar_json()
                    print("Profissional excluído com sucesso! -1 Na equipe :(")
                    encontrado = True
                    break
            if not encontrado:
                print("Profissional não encontrado!")
        case 6:
            print("\n=== Relatório de Profissionais ===")
            print("Total de profissionais cadastrados:", len(profissionais))
            for p in profissionais:
                print("-", p["nome"], "|", p["especialidade"])
        case 7:
            print("Saindo... Calma lá")
            break
        case _:
            print("Opção inválida! Tente novamente por favor.")