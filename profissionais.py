import json
import os
import re

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

def validar_email(email):
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))

def validar_telefone(telefone):
    return bool(re.match(r"^\(\d{2}\) \d{4,5}-\d{4}$", telefone))

def input_obrigatorio(prompt):
    while True:
        valor = input(prompt).strip()
        if valor:
            return valor
        print("  ⚠  Campo obrigatório.")

def input_cpf(prompt):
    while True:
        cpf = input(prompt).strip()
        if validar_cpf(cpf):
            return cpf
        print("  ⚠  CPF inválido. Use: 000.000.000-00")

def imprimir_profissional(p):
    status = p.get("status", "Ativo")
    icon = "✓" if status == "Ativo" else "✗"
    crm = p.get("crm") or p.get("registro") or "-"
    print(f"""
  ┌─────────────────────────────────────────────
  │ ID:           {p['id']}  [{icon} {status}]
  │ Nome:         {p['nome']}
  │ CPF:          {p['cpf']}
  │ CRM/Registro: {crm}
  │ Especialidade:{p.get('especialidade', '-')}
  │ Telefone:     {p.get('telefone', '-')}
  │ E-mail:       {p.get('email', '-')}
  └─────────────────────────────────────────────""")

def cadastrar_profissional():
    dados = carregar_dados()
    print("\n  ── CADASTRAR PROFISSIONAL ──")

    cpf = input_cpf("  CPF (000.000.000-00): ")
    if any(p["cpf"] == cpf for p in dados["profissionais"]):
        print("  ✗ CPF já cadastrado!")
        return

    nome = input_obrigatorio("  Nome completo: ")
    crm = input_obrigatorio("  CRM / Registro no conselho: ")
    especialidade = input_obrigatorio("  Especialidade: ")

    telefone = input("  Telefone ((00) 00000-0000): ").strip()
    if telefone and not validar_telefone(telefone):
        print("  ⚠  Telefone inválido, salvo sem formatação.")

    email = input("  E-mail: ").strip()
    if email and not validar_email(email):
        print("  ⚠  E-mail inválido, salvo assim mesmo.")

    rua = input("  Rua: ").strip()
    bairro = input("  Bairro: ").strip()
    numero = input("  Número: ").strip()

    profissional = {
        "id": gerar_id(dados["profissionais"], "PRO"),
        "nome": nome,
        "cpf": cpf,
        "crm": crm,
        "especialidade": especialidade,
        "telefone": telefone,
        "email": email,
        "status": "Ativo",
        "endereco": {
            "rua": rua,
            "bairro": bairro,
            "numero": numero
        }
    }

    dados["profissionais"].append(profissional)
    salvar_dados(dados)
    print(f"\n  ✓ Profissional {nome} cadastrado! ID: {profissional['id']}")

def listar_profissionais():
    dados = carregar_dados()
    profissionais = dados["profissionais"]
    print("\n  ── LISTA DE PROFISSIONAIS ──")

    if not profissionais:
        print("  Nenhum profissional cadastrado.")
        return

    print("  Filtrar: 1-Todos  2-Ativos  3-Inativos")
    filtro = input("  Opção: ").strip()

    if filtro == "2":
        lista = [p for p in profissionais if p.get("status") == "Ativo"]
    elif filtro == "3":
        lista = [p for p in profissionais if p.get("status") != "Ativo"]
    else:
        lista = profissionais

    print(f"\n  Total: {len(lista)} profissional(is)")
    for p in lista:
        imprimir_profissional(p)

def editar_profissional():
    dados = carregar_dados()
    print("\n  ── EDITAR PROFISSIONAL ──")
    cpf_busca = input_cpf("  CPF do profissional: ")

    for p in dados["profissionais"]:
        if p["cpf"] == cpf_busca:
            imprimir_profissional(p)
            print("\n  Preencha os novos dados (Enter mantém o valor atual):\n")

            novo_nome = input(f"  Nome [{p['nome']}]: ").strip()
            if novo_nome: p["nome"] = novo_nome

            crm_atual = p.get("crm") or p.get("registro") or ""
            novo_crm = input(f"  CRM/Registro [{crm_atual}]: ").strip()
            if novo_crm: p["crm"] = novo_crm

            nova_esp = input(f"  Especialidade [{p.get('especialidade','')}]: ").strip()
            if nova_esp: p["especialidade"] = nova_esp

            novo_tel = input(f"  Telefone [{p.get('telefone','')}]: ").strip()
            if novo_tel: p["telefone"] = novo_tel

            novo_email = input(f"  E-mail [{p.get('email','')}]: ").strip()
            if novo_email: p["email"] = novo_email

            print(f"  Status atual: {p.get('status','Ativo')}")
            print("  Alterar status? 1-Ativo  2-Inativo  (Enter mantém)")
            status_op = input("  Opção: ").strip()
            if status_op == "1": p["status"] = "Ativo"
            elif status_op == "2": p["status"] = "Inativo"

            if "endereco" not in p:
                p["endereco"] = {}
            nova_rua = input(f"  Rua [{p['endereco'].get('rua','')}]: ").strip()
            if nova_rua: p["endereco"]["rua"] = nova_rua

            novo_bairro = input(f"  Bairro [{p['endereco'].get('bairro','')}]: ").strip()
            if novo_bairro: p["endereco"]["bairro"] = novo_bairro

            novo_num = input(f"  Número [{p['endereco'].get('numero','')}]: ").strip()
            if novo_num: p["endereco"]["numero"] = novo_num

            salvar_dados(dados)
            print("\n  ✓ Profissional atualizado com sucesso!")
            return

    print("  ✗ Profissional não encontrado.")

def pesquisar_profissional():
    dados = carregar_dados()
    print("\n  ── PESQUISAR PROFISSIONAL ──")
    print("  1 - Por CPF   2 - Por nome   3 - Por especialidade")
    op = input("  Opção: ").strip()

    resultado = []
    if op == "1":
        cpf = input_cpf("  CPF: ")
        resultado = [p for p in dados["profissionais"] if p["cpf"] == cpf]
    elif op == "2":
        nome = input("  Nome (parcial): ").strip().lower()
        resultado = [p for p in dados["profissionais"] if nome in p["nome"].lower()]
    elif op == "3":
        esp = input("  Especialidade: ").strip().lower()
        resultado = [p for p in dados["profissionais"] if esp in p.get("especialidade","").lower()]
    else:
        print("  Opção inválida.")
        return

    if not resultado:
        print("  ✗ Nenhum profissional encontrado.")
    else:
        print(f"\n  {len(resultado)} resultado(s):")
        for p in resultado:
            imprimir_profissional(p)

def excluir_profissional():
    dados = carregar_dados()
    print("\n  ── EXCLUIR PROFISSIONAL ──")
    cpf_busca = input_cpf("  CPF do profissional: ")

    for p in dados["profissionais"]:
        if p["cpf"] == cpf_busca:
            imprimir_profissional(p)

            cons_vinculadas = [c for c in dados["consultas"] if c["id_profissional"] == p["id"]]
            if cons_vinculadas:
                print(f"\n  ⚠  Este profissional possui {len(cons_vinculadas)} consulta(s) registrada(s).")
                print("  Sugestão: desative-o em vez de excluir (opção Editar → Status: Inativo).")
                confirmar = input("  Confirma exclusão mesmo assim? (s/N): ").strip().lower()
            else:
                confirmar = input(f"\n  Confirma exclusão de {p['nome']}? (s/N): ").strip().lower()

            if confirmar == "s":
                dados["profissionais"].remove(p)
                salvar_dados(dados)
                print(f"  ✓ Profissional {p['nome']} excluído.")
            else:
                print("  Exclusão cancelada.")
            return

    print("  ✗ Profissional não encontrado.")

def relatorio_profissionais():
    dados = carregar_dados()
    profissionais = dados["profissionais"]
    consultas = dados["consultas"]

    print("\n  ── RELATÓRIO DE PROFISSIONAIS ──")
    ativos = [p for p in profissionais if p.get("status") == "Ativo"]
    inativos = [p for p in profissionais if p.get("status") != "Ativo"]

    print(f"\n  Total cadastrados: {len(profissionais)}")
    print(f"  Ativos: {len(ativos)}  |  Inativos: {len(inativos)}\n")

    for p in profissionais:
        total = sum(1 for c in consultas if c["id_profissional"] == p["id"])
        crm = p.get("crm") or p.get("registro") or "-"
        icon = "✓" if p.get("status") == "Ativo" else "✗"
        print(f"  [{icon}] {p['nome']:<30} {p.get('especialidade','-'):<20} {crm:<18} {total:>3} consulta(s)")

def menu_profissionais():
    while True:
        print("""
╔══════════════════════════════════╗
║      MÓDULO DE PROFISSIONAIS     ║
╠══════════════════════════════════╣
║  1 - Cadastrar profissional      ║
║  2 - Listar profissionais        ║
║  3 - Editar profissional         ║
║  4 - Pesquisar profissional      ║
║  5 - Excluir profissional        ║
║  6 - Relatório                   ║
║  0 - Voltar ao menu principal    ║
╚══════════════════════════════════╝""")
        op = input("  Opção: ").strip()
        match op:
            case "1": cadastrar_profissional()
            case "2": listar_profissionais()
            case "3": editar_profissional()
            case "4": pesquisar_profissional()
            case "5": excluir_profissional()
            case "6": relatorio_profissionais()
            case "0": break
            case _: print("  ⚠  Opção inválida.")

if __name__ == "__main__":
    menu_profissionais()
