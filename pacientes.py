import json
import os
import re
from datetime import datetime

ARQUIVO = "clinica.json"

def carregar_dados():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"pacientes": [], "profissionais": [], "consultas": []}

def salvar_dados(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def gerar_id(lista, prefixo):
    if not lista:
        return f"{prefixo}001"
    ultimos = [int(p["id"].replace(prefixo, "")) for p in lista if p["id"].startswith(prefixo)]
    return f"{prefixo}{(max(ultimos) + 1):03d}"

def validar_cpf(cpf):
    return bool(re.match(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", cpf))

def validar_data(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validar_telefone(telefone):
    return bool(re.match(r"^\(\d{2}\) \d{4,5}-\d{4}$", telefone))

def input_obrigatorio(prompt):
    while True:
        valor = input(prompt).strip()
        if valor:
            return valor
        print("  ⚠  Campo obrigatório. Tente novamente.")

def input_cpf(prompt):
    while True:
        cpf = input(prompt).strip()
        if validar_cpf(cpf):
            return cpf
        print("  ⚠  CPF inválido. Use o formato: 000.000.000-00")

def input_data(prompt):
    while True:
        data = input(prompt).strip()
        if validar_data(data):
            return data
        print("  ⚠  Data inválida. Use o formato: DD/MM/AAAA")

def input_telefone(prompt):
    while True:
        tel = input(prompt).strip()
        if validar_telefone(tel):
            return tel
        print("  ⚠  Telefone inválido. Use: (00) 00000-0000")

def imprimir_paciente(p):
    print(f"""
  ┌─────────────────────────────────────────────
  │ ID:          {p['id']}
  │ Nome:        {p['nome']}
  │ CPF:         {p['cpf']}
  │ Nascimento:  {p['data_nasc']}
  │ Sexo:        {p['sexo']}
  │ Raça:        {p['raca']}
  │ Cidade:      {p['cidade']}
  │ Telefone:    {p['telefone']}
  │ Pai:         {p.get('nome_pai', '-')}
  │ Mãe:         {p.get('nome_mae', '-')}
  └─────────────────────────────────────────────""")

def cadastrar_paciente():
    dados = carregar_dados()
    print("\n  ── CADASTRAR PACIENTE ──")

    # Verifica CPF duplicado
    cpf = input_cpf("  CPF (000.000.000-00): ")
    if any(p["cpf"] == cpf for p in dados["pacientes"]):
        print("  ✗ CPF já cadastrado!")
        return

    nome = input_obrigatorio("  Nome completo: ")
    data_nasc = input_data("  Data de nascimento (DD/MM/AAAA): ")

    print("  Sexo: 1-Feminino  2-Masculino  3-Outro")
    sexo_map = {"1": "Feminino", "2": "Masculino", "3": "Outro"}
    sexo_op = input("  Opção: ").strip()
    sexo = sexo_map.get(sexo_op, "Não informado")

    print("  Raça: 1-Branca  2-Preta  3-Parda  4-Amarela  5-Indígena  6-Não declarada")
    raca_map = {"1": "Branca", "2": "Preta", "3": "Parda", "4": "Amarela", "5": "Indígena", "6": "Não declarada"}
    raca_op = input("  Opção: ").strip()
    raca = raca_map.get(raca_op, "Não declarada")

    cidade = input_obrigatorio("  Cidade: ")
    telefone = input_telefone("  Telefone ((00) 00000-0000): ")
    nome_pai = input("  Nome do pai (Enter para pular): ").strip() or "Não informado"
    nome_mae = input("  Nome da mãe (Enter para pular): ").strip() or "Não informado"

    paciente = {
        "id": gerar_id(dados["pacientes"], "PAC"),
        "nome": nome,
        "cpf": cpf,
        "data_nasc": data_nasc,
        "nome_pai": nome_pai,
        "nome_mae": nome_mae,
        "cidade": cidade,
        "sexo": sexo,
        "raca": raca,
        "telefone": telefone
    }

    dados["pacientes"].append(paciente)
    salvar_dados(dados)
    print(f"\n  ✓ Paciente {nome} cadastrado com sucesso! ID: {paciente['id']}")

def listar_pacientes():
    dados = carregar_dados()
    pacientes = dados["pacientes"]
    print("\n  ── LISTA DE PACIENTES ──")
    if not pacientes:
        print("  Nenhum paciente cadastrado.")
        return
    print(f"  Total: {len(pacientes)} paciente(s)\n")
    for p in pacientes:
        imprimir_paciente(p)

def editar_paciente():
    dados = carregar_dados()
    print("\n  ── EDITAR PACIENTE ──")
    cpf_busca = input_cpf("  CPF do paciente: ")

    for p in dados["pacientes"]:
        if p["cpf"] == cpf_busca:
            print("  Paciente encontrado:")
            imprimir_paciente(p)
            print("\n  Preencha os novos dados (Enter mantém o valor atual):\n")

            novo_nome = input(f"  Nome [{p['nome']}]: ").strip()
            if novo_nome: p["nome"] = novo_nome

            nova_data = input(f"  Nascimento [{p['data_nasc']}]: ").strip()
            if nova_data:
                if validar_data(nova_data):
                    p["data_nasc"] = nova_data
                else:
                    print("  ⚠  Data inválida, mantendo o valor anterior.")

            nova_cidade = input(f"  Cidade [{p['cidade']}]: ").strip()
            if nova_cidade: p["cidade"] = nova_cidade

            novo_tel = input(f"  Telefone [{p['telefone']}]: ").strip()
            if novo_tel:
                if validar_telefone(novo_tel):
                    p["telefone"] = novo_tel
                else:
                    print("  ⚠  Telefone inválido, mantendo o valor anterior.")

            novo_pai = input(f"  Nome do pai [{p.get('nome_pai','-')}]: ").strip()
            if novo_pai: p["nome_pai"] = novo_pai

            novo_mae = input(f"  Nome da mãe [{p.get('nome_mae','-')}]: ").strip()
            if novo_mae: p["nome_mae"] = novo_mae

            salvar_dados(dados)
            print("\n  ✓ Paciente atualizado com sucesso!")
            return

    print("  ✗ Paciente não encontrado.")

def pesquisar_paciente():
    dados = carregar_dados()
    print("\n  ── PESQUISAR PACIENTE ──")
    print("  1- Por CPF   2- Por nome   3- Por cidade")
    op = input("  Opção: ").strip()

    resultados = []
    if op == "1":
        cpf = input_cpf("  CPF: ")
        resultados = [p for p in dados["pacientes"] if p["cpf"] == cpf]
    elif op == "2":
        nome = input("  Nome (parcial): ").strip().lower()
        resultados = [p for p in dados["pacientes"] if nome in p["nome"].lower()]
    elif op == "3":
        cidade = input("  Cidade: ").strip().lower()
        resultados = [p for p in dados["pacientes"] if cidade in p["cidade"].lower()]
    else:
        print("  Opção inválida.")
        return

    if not resultados:
        print("  ✗ Nenhum paciente encontrado.")
    else:
        print(f"\n  {len(resultados)} resultado(s) encontrado(s):")
        for p in resultados:
            imprimir_paciente(p)

def excluir_paciente():
    dados = carregar_dados()
    print("\n  ── EXCLUIR PACIENTE ──")
    cpf_busca = input_cpf("  CPF do paciente: ")

    for p in dados["pacientes"]:
        if p["cpf"] == cpf_busca:
            imprimir_paciente(p)

            # Verifica consultas vinculadas
            consultas_vinculadas = [c for c in dados["consultas"] if c["id_paciente"] == p["id"]]
            if consultas_vinculadas:
                print(f"\n  ⚠  Este paciente possui {len(consultas_vinculadas)} consulta(s) registrada(s).")
                print("  A exclusão removerá também essas consultas.")

            confirmar = input(f"\n  Confirma exclusão de {p['nome']}? (s/N): ").strip().lower()
            if confirmar == "s":
                dados["pacientes"].remove(p)
                dados["consultas"] = [c for c in dados["consultas"] if c["id_paciente"] != p["id"]]
                salvar_dados(dados)
                print(f"  ✓ Paciente {p['nome']} excluído com sucesso.")
            else:
                print("  Exclusão cancelada.")
            return

    print("  ✗ Paciente não encontrado.")

def menu_pacientes():
    while True:
        print("""
╔══════════════════════════════════╗
║       MÓDULO DE PACIENTES        ║
╠══════════════════════════════════╣
║  1 - Cadastrar paciente          ║
║  2 - Listar pacientes            ║
║  3 - Editar paciente             ║
║  4 - Pesquisar paciente          ║
║  5 - Excluir paciente            ║
║  0 - Voltar ao menu principal    ║
╚══════════════════════════════════╝""")
        op = input("  Opção: ").strip()
        match op:
            case "1": cadastrar_paciente()
            case "2": listar_pacientes()
            case "3": editar_paciente()
            case "4": pesquisar_paciente()
            case "5": excluir_paciente()
            case "0": break
            case _: print("  ⚠  Opção inválida.")

if __name__ == "__main__":
    menu_pacientes()