pacientes = []

while True:

    opcao = int (input ("Digite uma opção: \n 1- Cadastrar paciente \n 2- Listar pacientes \n 3- Editar paciente \n 4- Pesquisar paciente \n 5- Excluir paciente \n 6- Sair"))

    match (opcao):
        case 1:
            nome = input ("Digite o nome do paciente: ")
            cpf = input ("Digite o CPF do paciente: ")
            data_nasc = input ("Digite a data de nascimento do paciente (dd/mm/aaaa): ")
            nome_pai = input ("Digite o nome do pai do paciente: ")
            nome_mae = input ("Digite o nome da mãe do paciente: ")
            cidade = input ("Digite a cidade que reside: ")
            sexoopc = int (input ("Digite um valor para o sexo do paciente: \n 1- Feminino \n 2- Masculino \n 3- Outro"))
            match (sexoopc):
                case 1:
                    sexo = "Feminino"
                
                case 2:
                    sexo = "Masculino"

                case 3: 
                    sexo = "Outro"

                case _:
                    print ("Valor inválido!")

            racaopc = int (input ("Digite um valor para a raça do paciente: \n 1- Branca \n 2- Preta \n 3- Parda \n 4- Amarela \n 5- Indígena \n 6- Quilombola \n 7- Outra"))
            match (racaopc):
                case 1:
                    raca = "Branca"

                case 2:
                    raca = "Preta"

                case 3:
                    raca = "Parda" 

                case 4:
                    raca = "Amarela"

                case 5:
                    raca = "Indígena"

                case 6:
                    raca = "Quilombola"

                case 7:
                    raca = "Outra"

                case _:
                    print ("Valor inválido!")

            telefone = input ("Digite o telefone do paciente: ")

            paciente = {
            "nome" : nome,
            "cpf" : cpf,
            "data_nasc" : data_nasc,
            "nome_pai" : nome_pai,
            "nome_mae" : nome_mae,
            "cidade" : cidade,
            "sexo" : sexo,
            "raca" : raca,
            "telefone" : telefone
        }

            pacientes.append(paciente)

            print ("Paciente cadastrado com sucesso!")

        case 2:
            if (len(pacientes) == 0):
                print ("Não existem pacientes cadastrados!")

            else:
                for paciente in pacientes:
                    print ("Nome: ", paciente["nome"] ,"\n CPF: ", paciente["cpf"] ,"\n Data de nascimento: ", paciente["data_nasc"] ,"\n Nome do pai: ", paciente["nome_pai"],"\n Nome da mãe: ", paciente["nome_mae"] ,"\n Cidade que reside: ", paciente["cidade"] ,"\n Sexo: ", paciente["sexo"] ,"\n Raça: ", paciente["raca"], "\n Telefone: ", paciente["telefone"])
