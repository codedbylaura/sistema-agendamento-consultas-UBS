import json
import os

ARQUIVO = "clinica.json"

# ── Importa os módulos ──────────────────────────────────────
from profissionais import menu_profissionais
from pacientes import menu_pacientes
from consultas import menu_consultas
from relatorios import menu_relatorios

def inicializar_dados():
    """Cria o arquivo clinica.json se não existir."""
    if not os.path.exists(ARQUIVO):
        dados_iniciais = {"pacientes": [], "profissionais": [], "consultas": []}
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(dados_iniciais, f, indent=4, ensure_ascii=False)
        print("  ✓ Banco de dados inicializado.")

def resumo_rapido():
    """Mostra contadores rápidos no menu principal."""
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            d = json.load(f)
        pac = len(d.get("pacientes", []))
        pro = len(d.get("profissionais", []))
        agendadas = sum(1 for c in d.get("consultas", []) if c.get("status") == "Agendada")
        return f"  Pacientes: {pac}  |  Profissionais: {pro}  |  Agendadas: {agendadas}"
    except:
        return ""

def main():
    inicializar_dados()

    while True:
        status = resumo_rapido()
        print(f"""
╔══════════════════════════════════════════════╗
║        SISTEMA DE GESTÃO DE CLÍNICA          ║
╠══════════════════════════════════════════════╣
║  1 - 👤  Profissionais                       ║
║  2 - 🏥  Pacientes                           ║
║  3 - 📅  Consultas                           ║
║  4 - 📊  Relatórios                          ║
║  0 - 🚪  Sair                                ║
╚══════════════════════════════════════════════╝
{status}""")

        op = input("\n  Opção: ").strip()
        match op:
            case "1": menu_profissionais()
            case "2": menu_pacientes()
            case "3": menu_consultas()
            case "4": menu_relatorios()
            case "0":
                print("\n  Encerrando o sistema. Até logo!\n")
                break
            case _:
                print("  ⚠  Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
