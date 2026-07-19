from pathlib import Path

from trinary_ai import TrinaryAgent, XMLMemory


def main() -> None:
    memory_path = Path(__file__).parent / "data" / "memory.xml"
    agent = TrinaryAgent(XMLMemory(memory_path))
    print("IA Trinária MVP iniciada. Digite 'ajuda' ou 'sair'.")
    while True:
        try:
            text = input("Você> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerramento seguro.")
            break
        if text.lower() in {"sair", "exit", "quit"}:
            print("IA> Memória salva. Encerramento seguro.")
            break
        if text:
            print("IA>", agent.respond(text))


if __name__ == "__main__":
    main()
