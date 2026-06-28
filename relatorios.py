import json
import os
from datetime import datetime
from collections import Counter

ARQUIVO = "clinica.json"

def carregar_dados():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"pacientes": [], "profissionais": [], "consultas": []}

def nome_paciente(dados, id_pac):
    p = next((p for p in dados["pacientes"] if p["id"] == id_pac), None)
    return p["nome"] if p else "Desconhecido"

def nome_profissional(dados, id_pro):
    p = next((p for p in dados["profissionais"] if p["id"] == id_pro), None)
    return p["nome"] if p else "Desconhecido"

def barra(valor, maximo, largura=30):
    if maximo == 0:
        return "░" * largura
    cheio = int((valor / maximo) * largura)
    return "█" * cheio + "░" * (largura - cheio)

def separador(titulo=""):
    if titulo:
        pad = (60 - len(titulo) - 2) // 2
        print(f"\n  {'─' * pad} {titulo} {'─' * pad}")
    else:
        print("  " + "─" * 62)

def relatorio_geral():
    dados = carregar_dados()
    pacientes = dados["pacientes"]
    profissionais = dados["profissionais"]
    consultas = dados["consultas"]

    realizadas = sum(1 for c in consultas if c["status"] == "Realizada")
    agendadas = sum(1 for c in consultas if c["status"] == "Agendada")
    canceladas = sum(1 for c in consultas if c["status"] == "Cancelada")
    ativos = sum(1 for p in profissionais if p.get("status") == "Ativo")

    print("""
╔════════════════════════════════════════════════════════════╗
║                   RELATÓRIO GERAL DO SISTEMA               ║
╚════════════════════════════════════════════════════════════╝""")

    separador("VISÃO GERAL")
    print(f"""
  {'Pacientes cadastrados:':<35} {len(pacientes):>5}
  {'Profissionais cadastrados:':<35} {len(profissionais):>5}
  {'  └─ Ativos:':<35} {ativos:>5}
  {'  └─ Inativos:':<35} {len(profissionais) - ativos:>5}
  {'Total de consultas:':<35} {len(consultas):>5}
  {'  └─ Realizadas:':<35} {realizadas:>5}
  {'  └─ Agendadas:':<35} {agendadas:>5}
  {'  └─ Canceladas:':<35} {canceladas:>5}""")

    separador("CONSULTAS POR STATUS")
    maximo = max(realizadas, agendadas, canceladas, 1)
    print(f"\n  Realizadas  {barra(realizadas, maximo)} {realizadas}")
    print(f"  Agendadas   {barra(agendadas, maximo)} {agendadas}")
    print(f"  Canceladas  {barra(canceladas, maximo)} {canceladas}")

    separador("CONSULTAS POR ESPECIALIDADE")
    esp_counter = Counter(c["especialidade"] for c in consultas)
    maximo = max(esp_counter.values(), default=1)
    for esp, qtd in esp_counter.most_common():
        label = f"{esp[:18]:<18}"
        print(f"  {label}  {barra(qtd, maximo)} {qtd}")

    separador("PACIENTES POR SEXO")
    sexo_counter = Counter(p.get("sexo", "Não informado") for p in pacientes)
    maximo = max(sexo_counter.values(), default=1)
    for sexo, qtd in sexo_counter.most_common():
        print(f"  {sexo:<18}  {barra(qtd, maximo)} {qtd}")

    separador("PACIENTES POR RAÇA")
    raca_counter = Counter(p.get("raca", "Não informado") for p in pacientes)
    maximo = max(raca_counter.values(), default=1)
    for raca, qtd in raca_counter.most_common():
        print(f"  {raca:<18}  {barra(qtd, maximo)} {qtd}")

    print()

def relatorio_profissional():
    dados = carregar_dados()
    consultas = dados["consultas"]
    profissionais = dados["profissionais"]

    print("""
╔════════════════════════════════════════════════════════════╗
║              RELATÓRIO POR PROFISSIONAL                    ║
╚════════════════════════════════════════════════════════════╝""")

    if not profissionais:
        print("  Nenhum profissional cadastrado.")
        return

    for pro in profissionais:
        cons_pro = [c for c in consultas if c["id_profissional"] == pro["id"]]
        realizadas = sum(1 for c in cons_pro if c["status"] == "Realizada")
        agendadas = sum(1 for c in cons_pro if c["status"] == "Agendada")
        canceladas = sum(1 for c in cons_pro if c["status"] == "Cancelada")

        taxa_cancel = (canceladas / len(cons_pro) * 100) if cons_pro else 0
        status_icon = "✓" if pro.get("status") == "Ativo" else "✗"
        crm = pro.get("crm") or pro.get("registro") or "-"

        print(f"""
  [{status_icon}] {pro['nome']}
      {crm} — {pro.get('especialidade', '-')}
      Total de consultas: {len(cons_pro)}  |  Realizadas: {realizadas}  |  Agendadas: {agendadas}  |  Canceladas: {canceladas}
      Taxa de cancelamento: {taxa_cancel:.1f}%""")

        # Lista próximas consultas agendadas
        agendadas_list = sorted(
            [c for c in cons_pro if c["status"] == "Agendada"],
            key=lambda c: datetime.strptime(f"{c['data']} {c['hora']}", "%d/%m/%Y %H:%M")
            if all(c.get(k) for k in ["data", "hora"]) else datetime.min
        )
        if agendadas_list:
            print(f"      Próximas consultas ({len(agendadas_list)}):")
            for c in agendadas_list[:3]:
                pac_nome = nome_paciente(dados, c["id_paciente"])
                print(f"        • {c['data']} {c['hora']} — {pac_nome}")
            if len(agendadas_list) > 3:
                print(f"        ... e mais {len(agendadas_list)-3}")

    separador()
    print()

def relatorio_paciente():
    dados = carregar_dados()
    consultas = dados["consultas"]
    pacientes = dados["pacientes"]

    print("""
╔════════════════════════════════════════════════════════════╗
║               RELATÓRIO POR PACIENTE                       ║
╚════════════════════════════════════════════════════════════╝""")

    if not pacientes:
        print("  Nenhum paciente cadastrado.")
        return

    for pac in pacientes:
        cons_pac = [c for c in consultas if c["id_paciente"] == pac["id"]]
        realizadas = [c for c in cons_pac if c["status"] == "Realizada"]
        agendadas = [c for c in cons_pac if c["status"] == "Agendada"]

        # Calcula idade
        try:
            nasc = datetime.strptime(pac["data_nasc"], "%d/%m/%Y")
            idade = (datetime.now() - nasc).days // 365
        except:
            idade = "?"

        print(f"""
  {pac['nome']} ({pac['id']})
  CPF: {pac['cpf']}  |  {idade} anos  |  {pac.get('cidade', '-')}  |  Tel: {pac['telefone']}
  Total de consultas: {len(cons_pac)}  |  Realizadas: {len(realizadas)}  |  Agendadas: {len(agendadas)}""")

        if realizadas:
            # Última consulta
            ultima = sorted(realizadas, key=lambda c: datetime.strptime(
                f"{c['data']} {c['hora']}", "%d/%m/%Y %H:%M")
                if all(c.get(k) for k in ["data","hora"]) else datetime.min)[-1]
            pro_nome = nome_profissional(dados, ultima["id_profissional"])
            print(f"  Última visita: {ultima['data']} com {pro_nome} ({ultima['especialidade']})")
            if ultima.get("diagnostico"):
                print(f"  Diagnóstico: {ultima['diagnostico']}")

        if agendadas:
            proxima = sorted(agendadas, key=lambda c: datetime.strptime(
                f"{c['data']} {c['hora']}", "%d/%m/%Y %H:%M")
                if all(c.get(k) for k in ["data","hora"]) else datetime.min)[0]
            pro_nome = nome_profissional(dados, proxima["id_profissional"])
            print(f"  Próxima consulta: {proxima['data']} {proxima['hora']} com {pro_nome}")

    separador()
    print()

def relatorio_periodo():
    dados = carregar_dados()
    consultas = dados["consultas"]

    print("""
╔════════════════════════════════════════════════════════════╗
║                  RELATÓRIO POR PERÍODO                     ║
╚════════════════════════════════════════════════════════════╝""")

    data_ini_str = input("  Data inicial (DD/MM/AAAA): ").strip()
    data_fim_str = input("  Data final   (DD/MM/AAAA): ").strip()

    try:
        data_ini = datetime.strptime(data_ini_str, "%d/%m/%Y")
        data_fim = datetime.strptime(data_fim_str, "%d/%m/%Y")
    except ValueError:
        print("  ✗ Data inválida.")
        return

    def dentro_periodo(c):
        try:
            data_c = datetime.strptime(c["data"], "%d/%m/%Y")
            return data_ini <= data_c <= data_fim
        except:
            return False

    filtradas = [c for c in consultas if dentro_periodo(c)]

    print(f"\n  Período: {data_ini_str} a {data_fim_str}")
    print(f"  Total de consultas no período: {len(filtradas)}")

    if not filtradas:
        print("  Nenhuma consulta no período informado.")
        return

    realizadas = sum(1 for c in filtradas if c["status"] == "Realizada")
    agendadas = sum(1 for c in filtradas if c["status"] == "Agendada")
    canceladas = sum(1 for c in filtradas if c["status"] == "Cancelada")

    separador("RESUMO DO PERÍODO")
    print(f"\n  Realizadas: {realizadas}  |  Agendadas: {agendadas}  |  Canceladas: {canceladas}")

    separador("CONSULTAS POR ESPECIALIDADE")
    esp_counter = Counter(c["especialidade"] for c in filtradas)
    maximo = max(esp_counter.values(), default=1)
    for esp, qtd in esp_counter.most_common():
        print(f"  {esp:<20}  {barra(qtd, maximo, 20)} {qtd}")

    separador("PROFISSIONAIS MAIS ATIVOS")
    pro_counter = Counter(c["id_profissional"] for c in filtradas if c["status"] == "Realizada")
    for id_pro, qtd in pro_counter.most_common(5):
        pro_nome = nome_profissional(dados, id_pro)
        print(f"  {pro_nome:<30} {qtd:>3} consulta(s)")

    separador("LISTA DE CONSULTAS")
    filtradas_ord = sorted(filtradas, key=lambda c: datetime.strptime(
        f"{c['data']} {c['hora']}", "%d/%m/%Y %H:%M")
        if all(c.get(k) for k in ["data","hora"]) else datetime.min)

    for c in filtradas_ord:
        status_icon = {"Realizada": "✓", "Agendada": "◷", "Cancelada": "✗"}.get(c["status"], "•")
        pac_nome = nome_paciente(dados, c["id_paciente"])
        pro_nome = nome_profissional(dados, c["id_profissional"])
        print(f"  {status_icon} {c['data']} {c['hora']}  {pac_nome:<22} → {pro_nome:<25} [{c['especialidade']}]")

    print()

def relatorio_diagnosticos():
    dados = carregar_dados()
    consultas = dados["consultas"]

    print("""
╔════════════════════════════════════════════════════════════╗
║              RELATÓRIO DE DIAGNÓSTICOS                     ║
╚════════════════════════════════════════════════════════════╝""")

    realizadas = [c for c in consultas if c["status"] == "Realizada" and c.get("diagnostico")]

    if not realizadas:
        print("  Nenhuma consulta realizada com diagnóstico registrado.")
        return

    separador("DIAGNÓSTICOS REGISTRADOS")
    diag_counter = Counter(c["diagnostico"] for c in realizadas if c["diagnostico"])

    print(f"\n  Total de atendimentos com diagnóstico: {len(realizadas)}")
    print(f"  Diagnósticos distintos: {len(diag_counter)}\n")

    for diag, qtd in diag_counter.most_common(10):
        print(f"  {qtd:>3}×  {diag}")

    separador("DETALHES DOS ATENDIMENTOS")
    for c in realizadas:
        pac_nome = nome_paciente(dados, c["id_paciente"])
        pro_nome = nome_profissional(dados, c["id_profissional"])
        print(f"""
  {c['data']} | {pac_nome} → {pro_nome}
  Queixa:      {c.get('queixa_principal','-')}
  Diagnóstico: {c.get('diagnostico','-')}
  Prescrição:  {c.get('prescricao','-')}""")

    print()

def menu_relatorios():
    while True:
        print("""
╔══════════════════════════════════╗
║         MÓDULO DE RELATÓRIOS     ║
╠══════════════════════════════════╣
║  1 - Relatório geral             ║
║  2 - Por profissional            ║
║  3 - Por paciente                ║
║  4 - Por período                 ║
║  5 - Diagnósticos                ║
║  0 - Voltar ao menu principal    ║
╚══════════════════════════════════╝""")
        op = input("  Opção: ").strip()
        match op:
            case "1": relatorio_geral()
            case "2": relatorio_profissional()
            case "3": relatorio_paciente()
            case "4": relatorio_periodo()
            case "5": relatorio_diagnosticos()
            case "0": break
            case _: print("  ⚠  Opção inválida.")

if __name__ == "__main__":
    menu_relatorios()
