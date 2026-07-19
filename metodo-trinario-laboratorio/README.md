# Laboratório do Método Trinário

Aplicação web interativa para demonstrar o Método Trinário por meio de evidências positivas e negativas, pesos, cobertura, conflito, suficiência e resultado final.

## Demonstração

Abra o arquivo `index.html` diretamente no navegador.

Não é necessário instalar dependências, executar servidor ou compilar o projeto.

## Recursos

- Escala contínua entre `-0,95` e `+0,95`
- Canais separados de evidências positivas e negativas
- Médias ponderadas
- Cobertura saturante
- Suportes efetivos
- Resultante e valor final
- Medição de conflito
- Diagnósticos automáticos
- Cenários prontos
- Histórico local
- Importação e exportação em JSON
- Persistência com `localStorage`
- Funcionamento offline

## Fórmulas centrais

A cobertura é calculada por:

```text
C(m) = m / (m + 1)
```

Os suportes efetivos são:

```text
E+ = M+ × C+
E- = M- × C-
```

A resultante é:

```text
R = E+ - E-
```

O valor final permanece limitado ao intervalo:

```text
-0,95 ≤ v ≤ +0,95
```

## Publicação no GitHub Pages

1. Crie um repositório no GitHub.
2. Envie os arquivos deste projeto para a branch principal.
3. Abra **Settings → Pages**.
4. Em **Build and deployment**, selecione **Deploy from a branch**.
5. Escolha a branch principal e a pasta `/root`.
6. Salve.

O GitHub publicará a aplicação usando o arquivo `index.html`.

## Estrutura

```text
metodo-trinario-laboratorio/
├── index.html
├── README.md
├── LICENSE
├── .gitignore
├── assets/
└── docs/
```

## Armazenamento

Os dados são guardados no navegador do usuário usando `localStorage`. Eles não são enviados para servidores externos.

## Autoria

Método Trinário — Arthur Braga Padilha.

## Estado do projeto

Esta versão é uma demonstração interativa e educacional. Ela pode servir como base para aplicações futuras em análise de decisões, avaliação de hipóteses, sistemas especialistas e inteligência artificial.
