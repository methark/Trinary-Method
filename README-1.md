# IA Trinária — MVP 0.1

Protótipo local, auditável e sem dependências externas para experimentar uma arquitetura de IA baseada no Método Trinário.

## O que já existe

- núcleo matemático com canais positivos/negativos, cobertura, conflito, teto ±0,95 e diagnósticos D1–D5;
- memória adaptativa inicial em XML, com escrita atômica;
- identidade persistente;
- aprendizagem explícita de proposições e evidências;
- autocrítica baseada em cobertura, conflito e estado da conclusão;
- chat textual por terminal;
- monitoramento somente-leitura de disco, carga e bateria quando disponível;
- testes unitários.

## Limites deliberados

Este MVP não é consciente, não possui vontade própria e ainda não contém um modelo de linguagem. “Identidade” significa um perfil persistente; “autocrítica” significa auditoria computável da própria conclusão. A proteção de energia/hardware se limita a observar, registrar e recomendar ações seguras. O agente não desativa proteções, não amplia permissões e não executa alterações autônomas no sistema.

## Executar

```bash
python main.py
```

Comandos no chat:

```text
ajuda
identidade
status
aprender :: o céu está nublado :: 0.70 :: observação direta
avaliar :: o céu está nublado
sair
```

## Testes

```bash
python -m unittest discover -s tests -v
```

## Próximas camadas

1. `InputAdapter` para texto, imagem, áudio, mouse e sensores.
2. Banco de eventos e memória semântica adicional, mantendo XML como trilha de auditoria.
3. Modelo de linguagem local ou remoto atrás de uma interface, sem misturar geração textual com avaliação lógica.
4. Aprendizado supervisionado pelo criador: propostas de memória precisam ser aceitas, corrigidas ou rejeitadas.
5. Políticas de hardware com lista explícita de ações permitidas, confirmação humana e desligamento seguro.
