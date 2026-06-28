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
    ultimos = [int(c["id"].replace(prefixo, "")) for c in lista if c["id"].startswith(prefixo)]
    return f"{prefixo}{(max(ultimos) + 1):03d}"

def validar_data(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validar_hora(hora):
    return bool(re.match(r"^([01]\d|2[0-3]):[0-5]\d$", hora))

def buscar_paciente_por_cpf(dados, cpf):
    for p in dados["pacientes"]:
        if p["cpf"] == cpf:
            return p
    return None

def buscar_profissional_por_cpf(dados, cpf):
    for p in dados["profissionais"]:
        if p["cpf"] == cpf:
            return p
    return None

def buscar_consulta_por_id(dados, id_consulta):
    for c in dados["consultas"]:
        if c["id"] == id_consulta:
            return c
    return None

def nome_paciente(dados, id_pac):
    p = next((p for p in dados["pacientes"] if p["id"] == id_pac), None)
    return p["nome"] if p else "Desconhecido"

def nome_profissional(dados, id_pro):
    p = next((p for p in dados["profissionais"] if p["id"] == id_pro), None)
    return p["nome"] if p else "Desconhecido"

def imprimir_consulta(c, dados):
    status_icon = {"Realizada": "✓", "Agendada": "◷", "Cancelada": "✗"}.get(c["status"], "•")
    print(f"""
  ┌─────────────────────────────────────────────
  │ ID:           {c['id']}  [{status_icon} {c['status']}]
  │ Data/Hora:    {c['data']} às {c['hora']}
  │ Tipo:         {c['tipo']}
  │ Especialidade:{c['especialidade']}
  │ Paciente:     {nome_paciente(dados, c['id_paciente'])} ({c['id_paciente']})
  │ Profissional: {nome_profissional(dados, c['id_profissional'])} ({c['id_profissional']})
  │ Queixa:       {c.get('queixa_principal') or '-'}
  │ Diagnóstico:  {c.get('diagnostico') or '-'}
  │ Prescrição:   {c.get('prescricao') or '-'}
  │ Observações:  {c.get('observacoes') or '-'}
  └─────────────────────────────────────────────""")

def selecionar_paciente(dados):
    while True:
        cpf = input("  CPF do paciente (000.000.000-00): ").strip()
        if not re.match(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", cpf):
            print("  ⚠  CPF inválido. Use o formato: 000.000.000-00")
            continue
        p = buscar_paciente_por_cpf(dados, cpf)
        if p:
            print(f"  ✓ Paciente: {p['nome']}")
            return p
        print("  ✗ Paciente não encontrado. Cadastre o paciente primeiro.")
        return None

def selecionar_profissional(dados):
    # Mostra apenas profissionais ativos
    ativos = [p for p in dados["profissionais"] if p.get("status") == "Ativo"]
    if not ativos:
        print("  ✗ Nenhum profissional ativo cadastrado.")
        return None

    print("\n  Profissionais disponíveis:")
    for i, p in enumerate(ativos, 1):
        crm = p.get("crm") or p.get("registro") or "-"
        print(f"  {i}. {p['nome']} - {p.get('especialidade','-')} ({crm})")

    while True:
        try:
            idx = int(input("  Número do profissional: ")) - 1
            if 0 <= idx < len(ativos):
                p = ativos[idx]
                print(f"  ✓ Profissional: {p['nome']}")
                return p
            print("  ⚠  Número inválido.")
        except ValueError:
            print("  ⚠  Digite um número.")

def agendar_consulta():
    dados = carregar_dados()
    print("\n  ── AGENDAR CONSULTA ──")

    paciente = selecionar_paciente(dados)
    if not paciente:
        return

    profissional = selecionar_profissional(dados)
    if not profissional:
        return

    # Data
    while True:
        data = input("  Data da consulta (DD/MM/AAAA): ").strip()
        if validar_data(data):
            break
        print("  ⚠  Data inválida.")

    # Hora
    while True:
        hora = input("  Hora (HH:MM): ").strip()
        if validar_hora(hora):
            break
        print("  ⚠  Hora inválida. Use o formato HH:MM.")

    # Verifica conflito de horário
    conflito = [c for c in dados["consultas"]
                if c["id_profissional"] == profissional["id"]
                and c["data"] == data
                and c["hora"] == hora
                and c["status"] != "Cancelada"]
    if conflito:
        print(f"  ⚠  Conflito! {profissional['nome']} já tem consulta neste horário.")
        confirmar = input("  Deseja agendar mesmo assim? (s/N): ").strip().lower()
        if confirmar != "s":
            return

    print("  Tipo: 1-Consulta  2-Retorno  3-Exame  4-Procedimento")
    tipo_map = {"1": "Consulta", "2": "Retorno", "3": "Exame", "4": "Procedimento"}
    tipo = tipo_map.get(input("  Opção: ").strip(), "Consulta")

    especialidade = profissional.get("especialidade", "")
    esp_input = input(f"  Especialidade [{especialidade}]: ").strip()
    if esp_input:
        especialidade = esp_input

    queixa = input("  Queixa principal (Enter para pular): ").strip()
    observacoes = input("  Observações (Enter para pular): ").strip()

    consulta = {
        "id": gerar_id(dados["consultas"], "CON"),
        "id_paciente": paciente["id"],
        "id_profissional": profissional["id"],
        "data": data,
        "hora": hora,
        "tipo": tipo,
        "especialidade": especialidade,
        "status": "Agendada",
        "queixa_principal": queixa,
        "diagnostico": "",
        "prescricao": "",
        "observacoes": observacoes
    }

    dados["consultas"].append(consulta)
    salvar_dados(dados)
    print(f"\n  ✓ Consulta agendada! ID: {consulta['id']}")
    print(f"  {paciente['nome']} com {profissional['nome']} em {data} às {hora}")

def listar_consultas():
    dados = carregar_dados()
    consultas = dados["consultas"]
    print("\n  ── LISTA DE CONSULTAS ──")

    if not consultas:
        print("  Nenhuma consulta registrada.")
        return

    print("  Filtrar por: 1-Todas  2-Agendadas  3-Realizadas  4-Canceladas  5-Por data")
    filtro = input("  Opção: ").strip()

    if filtro == "2":
        resultado = [c for c in consultas if c["status"] == "Agendada"]
        titulo = "AGENDADAS"
    elif filtro == "3":
        resultado = [c for c in consultas if c["status"] == "Realizada"]
        titulo = "REALIZADAS"
    elif filtro == "4":
        resultado = [c for c in consultas if c["status"] == "Cancelada"]
        titulo = "CANCELADAS"
    elif filtro == "5":
        data = input("  Data (DD/MM/AAAA): ").strip()
        resultado = [c for c in consultas if c["data"] == data]
        titulo = f"DATA {data}"
    else:
        resultado = consultas
        titulo = "TODAS"

    # Ordena por data e hora
    def sort_key(c):
        try:
            return datetime.strptime(f"{c['data']} {c['hora']}", "%d/%m/%Y %H:%M")
        except:
            return datetime.min

    resultado.sort(key=sort_key)
    print(f"\n  [{titulo}] — {len(resultado)} consulta(s)")
    for c in resultado:
        imprimir_consulta(c, dados)

def editar_consulta():
    dados = carregar_dados()
    print("\n  ── EDITAR / ATENDER CONSULTA ──")
    id_consulta = input("  ID da consulta (ex: CON001): ").strip().upper()

    consulta = buscar_consulta_por_id(dados, id_consulta)
    if not consulta:
        print("  ✗ Consulta não encontrada.")
        return

    imprimir_consulta(consulta, dados)

    print("\n  O que deseja fazer?")
    print("  1 - Registrar atendimento (diagnóstico e prescrição)")
    print("  2 - Alterar data/hora")
    print("  3 - Alterar status")
    print("  4 - Editar observações")

    op = input("  Opção: ").strip()

    if op == "1":
        print("  ── Registrar Atendimento ──")
        queixa = input(f"  Queixa [{consulta.get('queixa_principal','')}]: ").strip()
        if queixa: consulta["queixa_principal"] = queixa

        diagnostico = input(f"  Diagnóstico [{consulta.get('diagnostico','')}]: ").strip()
        if diagnostico: consulta["diagnostico"] = diagnostico

        prescricao = input(f"  Prescrição [{consulta.get('prescricao','')}]: ").strip()
        if prescricao: consulta["prescricao"] = prescricao

        obs = input(f"  Observações [{consulta.get('observacoes','')}]: ").strip()
        if obs: consulta["observacoes"] = obs

        consulta["status"] = "Realizada"
        print("  ✓ Status atualizado para: Realizada")

    elif op == "2":
        nova_data = input(f"  Data [{consulta['data']}]: ").strip()
        if nova_data:
            if validar_data(nova_data):
                consulta["data"] = nova_data
            else:
                print("  ⚠  Data inválida, mantida a anterior.")
        nova_hora = input(f"  Hora [{consulta['hora']}]: ").strip()
        if nova_hora:
            if validar_hora(nova_hora):
                consulta["hora"] = nova_hora
            else:
                print("  ⚠  Hora inválida, mantida a anterior.")

    elif op == "3":
        print("  Status: 1-Agendada  2-Realizada  3-Cancelada")
        status_map = {"1": "Agendada", "2": "Realizada", "3": "Cancelada"}
        novo_status = status_map.get(input("  Opção: ").strip())
        if novo_status:
            consulta["status"] = novo_status
            if novo_status == "Cancelada":
                motivo = input("  Motivo do cancelamento (opcional): ").strip()
                if motivo:
                    consulta["observacoes"] = f"Cancelado: {motivo}"

    elif op == "4":
        nova_obs = input(f"  Observações [{consulta.get('observacoes','')}]: ").strip()
        if nova_obs: consulta["observacoes"] = nova_obs

    salvar_dados(dados)
    print("  ✓ Consulta atualizada com sucesso!")

def pesquisar_consulta():
    dados = carregar_dados()
    print("\n  ── PESQUISAR CONSULTA ──")
    print("  1 - Por ID   2 - Por CPF do paciente   3 - Por CPF do profissional")
    op = input("  Opção: ").strip()

    resultado = []
    if op == "1":
        id_c = input("  ID (ex: CON001): ").strip().upper()
        resultado = [c for c in dados["consultas"] if c["id"] == id_c]
    elif op == "2":
        cpf = input("  CPF do paciente: ").strip()
        pac = buscar_paciente_por_cpf(dados, cpf)
        if pac:
            resultado = [c for c in dados["consultas"] if c["id_paciente"] == pac["id"]]
            print(f"  Histórico de {pac['nome']}:")
        else:
            print("  ✗ Paciente não encontrado.")
            return
    elif op == "3":
        cpf = input("  CPF do profissional: ").strip()
        pro = buscar_profissional_por_cpf(dados, cpf)
        if pro:
            resultado = [c for c in dados["consultas"] if c["id_profissional"] == pro["id"]]
            print(f"  Agenda de {pro['nome']}:")
        else:
            print("  ✗ Profissional não encontrado.")
            return
    else:
        print("  Opção inválida.")
        return

    if not resultado:
        print("  Nenhuma consulta encontrada.")
    else:
        print(f"\n  {len(resultado)} consulta(s) encontrada(s):")
        for c in resultado:
            imprimir_consulta(c, dados)

def cancelar_consulta():
    dados = carregar_dados()
    print("\n  ── CANCELAR / EXCLUIR CONSULTA ──")
    id_consulta = input("  ID da consulta (ex: CON001): ").strip().upper()

    consulta = buscar_consulta_por_id(dados, id_consulta)
    if not consulta:
        print("  ✗ Consulta não encontrada.")
        return

    imprimir_consulta(consulta, dados)

    print("\n  1 - Cancelar consulta (mantém registro)")
    print("  2 - Excluir consulta (remove permanentemente)")
    op = input("  Opção: ").strip()

    if op == "1":
        motivo = input("  Motivo do cancelamento: ").strip()
        consulta["status"] = "Cancelada"
        if motivo:
            consulta["observacoes"] = f"Cancelado: {motivo}"
        salvar_dados(dados)
        print("  ✓ Consulta cancelada.")
    elif op == "2":
        confirmar = input(f"  Confirma exclusão permanente? (s/N): ").strip().lower()
        if confirmar == "s":
            dados["consultas"].remove(consulta)
            salvar_dados(dados)
            print("  ✓ Consulta excluída permanentemente.")
        else:
            print("  Exclusão cancelada.")

def menu_consultas():
    while True:
        print("""
╔══════════════════════════════════╗
║       MÓDULO DE CONSULTAS        ║
╠══════════════════════════════════╣
║  1 - Agendar consulta            ║
║  2 - Listar consultas            ║
║  3 - Editar / Atender consulta   ║
║  4 - Pesquisar consulta          ║
║  5 - Cancelar / Excluir          ║
║  0 - Voltar ao menu principal    ║
╚══════════════════════════════════╝""")
        op = input("  Opção: ").strip()
        match op:
            case "1": agendar_consulta()
            case "2": listar_consultas()
            case "3": editar_consulta()
            case "4": pesquisar_consulta()
            case "5": cancelar_consulta()
            case "0": break
            case _: print("  ⚠  Opção inválida.")

if __name__ == "__main__":
    menu_consultas()
