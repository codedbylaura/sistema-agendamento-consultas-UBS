import sqlite3

def conectar():
    return sqlite3.connect("ubs.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profissionais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            especialidade TEXT NOT NULL,
            telefone TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def cadastrar_profissional():
    nome = input("Nome completo: ")
    cpf = input("CPF: ")
    especialidade = input("Especialidade: ")
    telefone = input("Telefone: ")
        
#é especialidade mesmo? agora vai ser

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO profissionais (nome, cpf, especialidade, telefone)
        VALUES (?, ?, ?, ?)
    """, (nome, cpf, especialidade, telefone))
    conn.commit()
    conn.close()
    print("Profissional cadastrado com sucesso!")

def listar_profissionais():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profissionais")
    profissionais = cursor.fetchall()
    conn.close()

    if not profissionais:
        print("Nenhum profissional cadastrado.")
    else:
        for p in profissionais:
            print(f"ID: {p[0]} | Nome: {p[1]} | CPF: {p[2]} | Especialidade: {p[3]} | Telefone: {p[4]}")

def editar_profissional():
    listar_profissionais()
    id_prof = input("Digite o ID do profissional que deseja editar: ")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profissionais WHERE id = ?", (id_prof,))
    prof = cursor.fetchone()

    if not prof:
        print("Profissional não encontrado.")
        conn.close()
        return

    nome = input(f"Novo nome [{prof[1]}]: ") or prof[1]
    cpf = input(f"Novo CPF [{prof[2]}]: ") or prof[2]
    especialidade = input(f"Nova especialidade [{prof[3]}]: ") or prof[3]
    telefone = input(f"Novo telefone [{prof[4]}]: ") or prof[4]

#mesmo pesquisando eu estou pensando se não tem nada melhor para definir
#vou deixar assim, vou trocar mais não homi

    cursor.execute("""
        UPDATE profissionais
        SET nome=?, cpf=?, especialidade=?, telefone=?
        WHERE id=?
    """, (nome, cpf, especialidade, telefone, id_prof))
    conn.commit()
    conn.close()
    print("Profissional atualizado com sucesso! Pronto para atuar")

def excluir_profissional():
    listar_profissionais()
    id_prof = input("Digite o ID do profissional que deseja excluir: ")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profissionais WHERE id = ?", (id_prof,))
    prof = cursor.fetchone()

    if not prof:
        print("Profissional não encontrado.")
        conn.close()
        return

    confirmar = input(f"Tem certeza que deseja excluir {prof[1]}? (s/n): ")
    if confirmar.lower() == 's':
        cursor.execute("DELETE FROM profissionais WHERE id = ?", (id_prof,))
        conn.commit()
        print("Profissional excluido com sucesso!")
    else:
        print("Operação cancelada.")
    conn.close()

def menu():
    criar_tabela()
    while True:
        print("\n=== CRUD Profissionais - UBS ===")
        print("1 - Cadastrar profissional")
        print("2 - Listar profissionais")
        print("3 - Editar profissional")
        print("4 - Excluir profissional")
        print("5 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            cadastrar_profissional()
        elif opcao == "2":
            listar_profissionais()
        elif opcao == "3":
            editar_profissional()
        elif opcao == "4":
            excluir_profissional()
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida, escolha outra.")

menu()