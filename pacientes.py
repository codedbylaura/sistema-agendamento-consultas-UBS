opcao = int (input ("Digite uma opção: \n 1- Cadastrar paciente \n 2- Listar pacientes \n 3- Editar paciente \n 4- Pesquisar paciente \n 5- Excluir paciente \n 6- Sair"))

match (opcao):
    case 1:
        nome = input ("Digite o nome do paciente: ")
        cpf = int (input ("Digite o CPF do paciente: "))
        data_nasc = date (input ("Digite a data de nascimento do paciente (dd/mm/aaaa): "))
        nome_pai = input ("Digite o nome do pai do paciente: ")
        nome_mae = input ("Digite o nome da mãe do paciente: ")
        cidade = input ("Digite a cidade que reside: ")
        sexo = int (input ("Digite um valor para o sexo do paciente: \n 1- Feminino \n 2- Masculino \n 3- Outro"))
        raca = int (input ("Digite um valor para a raça do paciente: \n 1- Branca \n 2- Preta \n 3- Parda \n 4- Amarela \n 5- Indígena \n 6- Quilombola \n 7- Outra"))
        telefone = int (input ("Digite o telefone do paciente: "))
        print ("Paciente cadastrado com sucesso!")

    case 2:
        


        