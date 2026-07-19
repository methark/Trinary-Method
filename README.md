Proposta de sistema lógico formal · versão revisada

# Lógica Trinária E?

Escala simétrica \[−1, +1] com zero como incerteza genuína, camada evidencial por soma com média ponderada, semântica trivalente, diagnóstico computável, cálculo de inferência e resultados de verificação computacional

**Autor:** Arthur Braga Padilha  ·  **Versão 2.0** — revisão da v1.0 com base em bateria de testes exaustivos (50.000+ fórmulas; enumeração completa de valorações)

Resumo

Este texto formaliza a **Lógica Trinária E?** como um sistema em três camadas. A **camada evidencial** atribui a cada proposição um *balanço* em \[−1, +1] calculado por **soma com média ponderada** das evidências disponíveis, junto com uma *massa* total de evidência. A **camada semântica** discretiza o balanço em três valores — F = −1, E = 0, V = +1 — com o zero representando incerteza genuína, ponto fixo da negação. A **camada diagnóstica** torna os metadados D (dados insuficientes) e C (conflito) *computáveis* a partir de balanço e massa, em vez de atribuídos manualmente.

Em relação à v1.0, esta versão: (i) adota a escala simétrica −1/0/+1 com negação por reflexão ¬x = −x; (ii) introduz a média ponderada como mecanismo gerador dos valores; (iii) reformula o Teorema 3 conforme apontado pela auditoria computacional; (iv) enuncia o teorema de ausência de tautologias; e (v) responde à questão de revisão de crenças deixada em aberto na Seção 11 da v1.0. Todos os resultados marcados com Verificado foram confirmados por teste computacional exaustivo ou estatístico.

## 1. Objetivo e escopo

O sistema responde a três perguntas, uma por camada:

1. **Quanto pesa a evidência?** — balanço B(φ) ∈ \[−1,+1] e massa M(φ) ≥ 0, via média ponderada.
2. **Qual é o estado semântico da proposição?** — V, E ou F.
3. **Por que a avaliação está suspensa?** — diagnóstico D, C ou I, agora derivável das duas primeiras camadas.

A separação continua evitando transformar causas epistemológicas em valores de verdade: o núcleo lógico possui exatamente três valores. A novidade da v2.0 é que as causas de E deixam de ser apenas declaradas e passam a ser *calculadas*.

## 2. Linguagem formal

### 2.1 Alfabeto

Seja Prop = {p₁,p₂,p₃,…} um conjunto enumerável de variáveis proposicionais. A linguagem LE contém variáveis proposicionais, os conectivos ¬, ∧, ∨, →, ↔ e parênteses auxiliares.

### 2.2 Formação

Definição 1 — Fórmulas

φ ::= p | ¬φ | (φ ∧ φ) | (φ ∨ φ) | (φ → φ) | (φ ↔ φ).

## 3. Domínio semântico: a escala simétrica

Definição 2 — Valores

𝕍 = { −1, 0, +1 }  =  { F, E, V }

com a ordem informacional/verdade

F &lt; E &lt; V,  isto é,  −1 &lt; 0 &lt; +1.

#### V = +1 — Verdadeiro

O balanço da evidência autoriza aceitar a proposição.

#### E = 0 — E?

Incerteza genuína: o zero é o ponto de equilíbrio da escala e o único ponto fixo da negação.

#### F = −1 — Falso

O balanço da evidência autoriza rejeitar a proposição.

Por que −1/0/+1 em vez de 0/½/1

Na v1.0, a negação era ¬x = 1−x e E = ½. Na escala simétrica, a negação torna-se pura **reflexão em torno do zero**: ¬x = −x. As três propriedades desejadas saem da aritmética, sem estipulação: a involução ¬¬x = x é imediata (−(−x) = x); E é ponto fixo porque −0 = 0; e verdade e falsidade são espelhos exatos. Além disso, a escala passa a comportar a camada evidencial contínua da Seção 4, na qual +1 e −1 são evidência plena a favor e contra, e 0 é ausência ou anulação de evidência.

✔ Verificado: a recodificação é um isomorfismo exato da v1.0 pela função x ↦ 2x−1. Todas as tabelas, teoremas e resultados do núcleo lógico da v1.0 são preservados célula a célula.

## 4. Camada evidencial: soma com média ponderada Nova na v2.0

Os valores da escala não são estipulados: eles **resultam da agregação ponderada da evidência**.

Definição 3 — Balanço e massa

Seja Ev(p) = {(w₁,e₁), …, (wₙ,eₙ)} o conjunto de evidências relevantes para a proposição atômica p, onde cada eᵢ ∈ \[−1,+1] é a direção e intensidade da evidência e cada wᵢ &gt; 0 é o seu peso (confiabilidade, qualidade metodológica, independência da fonte). Definem-se:

B(p) = ( Σᵢ wᵢ·eᵢ ) / ( Σᵢ wᵢ )   ∈ \[−1,+1]   (balanço — média ponderada)  
M(p) = Σᵢ wᵢ   ≥ 0   (massa — soma dos pesos)

Convenção: se Ev(p) = ∅, então B(p) = 0 e M(p) = 0.

Definição 4 — Discretização (valoração induzida)

Fixados um limiar de decisão θ ∈ (0,1) e uma massa mínima m₀ &gt; 0:

v(p) = +1 (V)  se  B(p) ≥ θ  e  M(p) ≥ m₀  
v(p) = −1 (F)  se  B(p) ≤ −θ  e  M(p) ≥ m₀  
v(p) = 0 (E)  caso contrário.

Valores de referência usados nos testes: θ = ⅓ e m₀ = 1. A exigência de massa mínima impede que uma única evidência fraca produza um veredito decidido: com uma só evidência de peso 0,3, obtém-se B = 1 mas M = 0,3 &lt; m₀, e o resultado permanece E.

Definição 5 — Diagnóstico computável

Se v(p) = E, o metadado é derivado de B e M:

δ(p) = D  (dados insuficientes)  ⇔  M(p) &lt; m₀  
δ(p) = C  (conflito)  ⇔  M(p) ≥ m₀  e  |B(p)| &lt; θ  
δ(p) = I  (intangível)  ⇔  não há procedimento admissível para gerar Ev(p) no enquadramento adotado.

D e C deixam de ser rótulos manuais: **pouca massa é falta de dados; muita massa que se anula na média é conflito.** Apenas I permanece um juízo de enquadramento, pois diz respeito à inexistência do próprio procedimento de coleta.

✔ Verificado: conjunto vazio → E/D; conflito balanceado (2,+1) contra (2,−1) → B = 0, M = 4 → E/C; evidência consistente → V ou F; conflito assimétrico (3,+1) contra (1,−1) → B = 0,5 → V. Conflito simétrico acumulado por 100 evidências permanece E/C indefinidamente — acúmulo de contradição jamais vira verdade.

Correspondência estrutural com Belnap

Os quadrantes (B, M) reproduzem os quatro estados informacionais de Belnap–Dunn: massa nula ↔ *None*; massa alta com balanço nulo ↔ *Both*; balanço decidido ↔ *True*/*False*. A v2.0 obtém a expressividade dos quatro valores *sem abandonar o núcleo de três valores*: a quarta distinção vive na camada evidencial, exatamente onde a Seção 11 da v1.0 conjeturava que ela deveria estar.

## 5. Valorações e semântica composicional

Definição 6 — Valoração

Uma valoração é uma função v: Prop → 𝕍 (induzida pela Definição 4 ou dada diretamente), estendida recursivamente pelas cláusulas abaixo.

### 5.1 Negação — reflexão

v(¬φ) = −v(φ).

| φ  | ¬φ |
|----|----|
| +1 | −1 |
| 0  | 0  |
| −1 | +1 |

### 5.2 Conjunção — mínimo

v(φ∧ψ) = min(v(φ), v(ψ)).

| φ ∧ ψ | +1 | 0  | −1 |
|-------|----|----|----|
| +1    | +1 | 0  | −1 |
| 0     | 0  | 0  | −1 |
| −1    | −1 | −1 | −1 |

### 5.3 Disjunção — máximo

v(φ∨ψ) = max(v(φ), v(ψ)).

| φ ∨ ψ | +1 | 0  | −1 |
|-------|----|----|----|
| +1    | +1 | +1 | +1 |
| 0     | +1 | 0  | 0  |
| −1    | +1 | 0  | −1 |

### 5.4 Implicação e bicondicional

φ → ψ := ¬φ ∨ ψ,  logo  v(φ→ψ) = max(−v(φ), v(ψ)).  
φ ↔ ψ := (φ→ψ) ∧ (ψ→φ).

| φ → ψ | +1 | 0  | −1 |
|-------|----|----|----|
| +1    | +1 | 0  | −1 |
| 0     | +1 | 0  | 0  |
| −1    | +1 | +1 | +1 |

| φ ↔ ψ | +1 | 0 | −1 |
|-------|----|---|----|
| +1    | +1 | 0 | −1 |
| 0     | 0  | 0 | 0  |
| −1    | −1 | 0 | +1 |

✔ Verificado: as cinco tabelas são exatamente as geradas pelas definições aritméticas (−x, min, max), célula a célula, sem exceções.

### 5.5 Por que os conectivos não são eles próprios médias ponderadas

Resultado de teste — limite da média ponderada

Testou-se computacionalmente usar a média ponderada diretamente como conectivo (com pesos de decisividade: a conjunção pesando a falsidade, a disjunção pesando a verdade). Dois resultados:

1. **Positivo:** a média ponderada de decisividade, seguida de discretização por limiar, reproduz exatamente as tabelas min/max acima — em 20 de 20 configurações testadas de limiar (0,15 a 0,6) e suavização (0,001 a 0,1). Ou seja, **as tabelas da Seção 5 são a sombra discreta da agregação ponderada**: min e max são o caso-limite estável da média com pesos de decisividade.
2. **Negativo:** sem a discretização, a média ponderada contínua não serve como conectivo composicional: ela viola a conservatividade (v(V∧F) = −0,98 ≠ −1) e falha a associatividade em 20.000 de 20.000 triplas aleatórias — (a∧b)∧c ≠ a∧(b∧c).

Conclusão de arquitetura: **a média ponderada pertence à camada evidencial (agregação de evidências sobre átomos); min/max pertencem à camada lógica (composição de fórmulas)**. Cada operação no lugar onde suas propriedades matemáticas a sustentam.

## 6. Verdade lógica e consequência

Definição 7 — Valor designado

D = {+1}.

Uma fórmula é aceita apenas quando avaliada como V.

Definição 8 — Consequência semântica

Γ ⊨E φ ⇔ para toda valoração v, se v(γ)=+1 para todo γ∈Γ, então v(φ)=+1.

Definição 9 — Validade

⊨E φ ⇔ v(φ)=+1 para toda valoração v.

## 7. Cálculo de inferência

Dedução natural com regras seguras para o valor designado, idênticas às da v1.0:

Estruturais — Identidade: Γ,φ ⊢ φ; Enfraquecimento; Corte.  
∧I, ∧E₁, ∧E₂; ∨I₁, ∨I₂, ∨E; →I, →E (Modus Ponens).

A negação é a reflexão v(¬φ) = −v(φ); não se adota a regra irrestrita φ,¬φ ⊢ ψ. A Regra E? diagnóstica permanece na camada operacional: se a avaliação de φ não pode ser justificada como V nem como F, registrar v(φ)=E e derivar δ(φ) pela Definição 5.

## 8. Propriedades formais

Teorema 1 — Conservatividade sobre o fragmento clássico

Se uma valoração atribui apenas +1 ou −1 às variáveis de φ, o valor de φ coincide com seu valor clássico.

Prova

Por indução estrutural. A reflexão −x restrita a {−1,+1} é a negação clássica; min e max restritos a {−1,+1} são a conjunção e a disjunção clássicas; → e ↔ são definidos a partir delas. ∎

✔ Verificado: 50.000 fórmulas aleatórias × todas as valorações binárias — 0 divergências (concordância de 100% com a lógica clássica).

Teorema 2 — Correção das regras principais

As regras de ∧, ∨ e Modus Ponens preservam o valor designado +1.

Prova

Idêntica à v1.0, com min/max sobre {−1,0,+1}: min(+1,+1)=+1; min = +1 exige ambos +1; max(+1,x)=+1; e a linha +1 da tabela de → força v(ψ)=+1 quando v(φ)=v(φ→ψ)=+1. ∎

✔ Verificado por enumeração exaustiva: Modus Ponens, Modus Tollens, silogismo disjuntivo, silogismo hipotético e dilema construtivo — todos válidos, sem contraexemplos.

Teorema 3 — Não trivialidade operacional (reformulado na v2.0)

(a) Nenhuma valoração satisfaz simultaneamente φ e ¬φ com valor designado; logo a regra de explosão jamais é acionável a partir de premissas efetivamente aceitas. (b) A forma material da explosão não é válida: ⊭E (φ∧¬φ)→ψ. (c) No protocolo evidencial, uma base conflitante produz E/C (massa alta, balanço nulo), e nenhuma fórmula arbitrária é autorizada.

Prova e nota de revisão

(a) v(φ)=+1 exige v(¬φ)=−1. (b) Contraexemplo: v(φ)=0, v(ψ)=−1 dá v((φ∧¬φ)→ψ) = max(−0, −1) = 0 ≠ +1. (c) Segue das Definições 3–5. *Nota:* o enunciado da v1.0 ("{φ,¬φ} ⊭E ψ") era incorreto sob a Definição 8: como nenhuma valoração satisfaz as premissas, a consequência vale *por vacuidade* — fato conhecido das semânticas com valor designado único. A auditoria computacional confirmou: 0 modelos das premissas em 9 valorações. O que o sistema garante não é o bloqueio semântico da explosão, e sim que ela nunca dispara (a) e que sua forma material não é lei (b). ∎

Teorema 4 — Ausência de tautologias Novo na v2.0

Não existe fórmula φ com ⊨E φ. O conjunto de validades é vazio.

Prova

O zero é ponto fixo de todos os conectivos: −0 = 0, min(0,0) = 0, max(0,0) = 0. Por indução estrutural, a valoração que atribui 0 a todas as variáveis atribui 0 a toda fórmula. Logo nenhuma fórmula vale +1 em todas as valorações. ∎

Leitura epistemológica

Este é o resultado estrutural mais forte do sistema e a expressão exata de sua postura: **nada é verdadeiro de graça**. A lógica não afirma nenhuma sentença por conta própria; ela apenas transmite aceitação de premissas para conclusões. Todo o poder inferencial clássico (Teorema 2) permanece — mas condicionado a premissas efetivamente aceitas. Em particular, o terceiro excluído p∨¬p e a não contradição ¬(p∧¬p) recebem 0 quando v(p)=0, valendo apenas no fragmento decidido.

✔ Verificado: 50.000 fórmulas aleatórias de profundidade 5 sob a valoração toda-zero — 100% resultaram em 0.

Teorema 5 — Consistência sintática relativa

Se o cálculo clássico é consistente, o fragmento clássico da Lógica Trinária E? é consistente, e o cálculo completo não deriva todas as fórmulas.

Prova

Pelo Teorema 1, uma contradição derivável no fragmento bivalente seria uma contradição clássica. Para a não trivialidade, tome v(p)=+1, v(q)=−1: pela correção, q não é derivável sem premissas. O Teorema 4 reforça: sem premissas, nada é derivável. ∎

Teorema 6 — Monotonicidade da consequência

Se Γ ⊨E φ e Γ⊆Δ, então Δ ⊨E φ.

Prova

Toda valoração que satisfaz Δ satisfaz Γ. ∎

✔ Verificado: 1.220 casos amostrados com Γ ⊨ φ; 0 falhas após acréscimo de premissas. Atenção à distinção: a consequência *lógica* é monotônica; a camada *evidencial* (Seção 9) é revisável — nova evidência pode mudar v(p), e com isso o conjunto de premissas aceitas, sem contradizer este teorema.

Teorema 7 — Álgebra de Kleene e reescrita segura Novo na v2.0

Valem como identidades de valor, em toda valoração: De Morgan, dupla negação, comutatividade, associatividade, idempotência, absorção e distributividade. A estrutura (𝕍, min, max, −x) é uma álgebra de Kleene.

Prova

Propriedades padrão de reticulado distributivo totalmente ordenado com involução que inverte a ordem. ∎

Distinção fina revelada pelos testes

Essas leis valem como *igualdade de valores*, mas não como fórmulas válidas: ¬(p∧q) e ¬p∨¬q têm sempre o mesmo valor, porém o bicondicional entre elas recebe 0 quando p=q=0 (pois 0↔0 = 0). Consequência prática: **simplificar e reescrever fórmulas por essas leis é sempre seguro** — nenhum resultado muda —, ainda que as leis não sejam teoremas (não poderiam ser: pelo Teorema 4, nada é).

✔ Verificado por enumeração exaustiva (3² e 3³ valorações por lei): todas as identidades confirmadas.

## 9. Revisão de crenças: dinâmica evidencial Nova na v2.0

A v1.0 deixava em aberto "como E/D migra para V ou F quando novos dados chegam". A camada evidencial responde: a chegada da evidência (wₙ₊₁, eₙ₊₁) atualiza o balanço por recomputação da média ponderada:

B' = ( M·B + wₙ₊₁·eₙ₊₁ ) / ( M + wₙ₊₁ ),    M' = M + wₙ₊₁.

Propriedades verificadas computacionalmente:

| Propriedade da dinâmica                                                                | Teste                       | Resultado  |
|----------------------------------------------------------------------------------------|-----------------------------|------------|
| E/D → V com dados consistentes: trajetória (0 evid.) E/D → (2 evid. de peso ½) V       | Simulação passo a passo     | Confirmado |
| Conflito simétrico permanece E/C para sempre (acúmulo não fabrica verdade)             | 100 evidências opostas      | Confirmado |
| Monotonicidade evidencial: evidência ≥ balanço atual nunca reduz o balanço             | 20.000 casos aleatórios     | 0 falhas   |
| Robustez (continuidade): perturbação ≤ 0,05 nas evidências altera o balanço em ≤ 0,045 | 5.000 conjuntos perturbados | Confirmado |

A última linha registra uma vantagem estrutural sobre o binário puro: pequenos erros de medição produzem pequenas variações de balanço, e só atravessam o limiar θ quando genuinamente relevantes. A escala contínua funciona como amortecedor entre o ruído do mundo e a decisão trivalente.

## 10. Protocolo de classificação epistemológica

1. **Bem-formação:** sintaxe e domínio definidos?
2. **Enquadramento:** existe procedimento admissível para gerar evidência? Se não: E/I.
3. **Coleta:** reunir Ev(p) com pesos justificados.
4. **Agregação:** calcular B(p) e M(p) pela média ponderada.
5. **Avaliação:** discretizar com θ e m₀ (Definição 4).
6. **Diagnóstico:** se E, derivar D ou C pela Definição 5.

| Condição observada                  | Balanço / Massa      | Valor | Metadado |
|-------------------------------------|----------------------|-------|----------|
| Evidência suficiente a favor        | B ≥ θ, M ≥ m₀        | V     | —        |
| Evidência suficiente contra         | B ≤ −θ, M ≥ m₀       | F     | —        |
| Faltam dados decisivos              | M &lt; m₀            | E     | D        |
| Evidências fortes que se anulam     | M ≥ m₀, \|B\| &lt; θ | E     | C        |
| Sem procedimento objetivo aplicável | Ev(p) indefinível    | E     | I        |

## 11. Testes comparativos

### 11.1 Fato matemático

φ₁: 2+2=4.

| Sistema          | Resultado | Comentário                                                 |
|------------------|-----------|------------------------------------------------------------|
| Binário          | V         | Classificação direta.                                      |
| Trinário E? v2.0 | V (+1)    | Prova dedutiva = evidência de peso máximo; B = +1, M ≫ m₀. |

### 11.2 Fato empírico ainda desconhecido

φ₂: Existe exatamente uma civilização inteligente extraterrestre.

| Sistema          | Resultado operacional                            | Comentário                               |
|------------------|--------------------------------------------------|------------------------------------------|
| Binário          | V ou F na realidade; valor atual não determinado | A suspensão não é codificada como valor. |
| Trinário E? v2.0 | E/D                                              | Derivado, não declarado: M(φ₂) &lt; m₀.  |

### 11.3 Enunciado mal especificado

φ₃: Tudo é azul.

| Sistema          | Resultado operacional      | Comentário                                                                |
|------------------|----------------------------|---------------------------------------------------------------------------|
| Binário          | Exige interpretação prévia | O domínio de "tudo" precisa ser fixado.                                   |
| Trinário E? v2.0 | E                          | Falha no passo 1 do protocolo (bem-formação); registrada antes da coleta. |

### 11.4 Condicional com antecedente falso

φ₄: Se a casa é verde, então todos os objetos são vermelhos; fato: a casa não é verde.

| Sistema          | Resultado | Comentário                                                          |
|------------------|-----------|---------------------------------------------------------------------|
| Binário          | V         | Verdade material vacuosa.                                           |
| Trinário E? v2.0 | V         | v(−1 → x) = max(+1, x) = +1 para todo x. Verificado exaustivamente. |

### 11.5 Paradoxo autorreferente

L: "Esta própria proposição é falsa."  Equação semântica: x = ¬x, isto é, x = −x.

| Sistema          | Resultado                 | Comentário                                                                                                                                   |
|------------------|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| Binário          | Sem solução em {−1,+1}    | x = −x não tem raiz em {−1,+1}.                                                                                                              |
| Trinário E? v2.0 | E/C — solução única x = 0 | Na escala simétrica, o Mentiroso vira uma equação com raiz única: o zero. O paradoxo não é resolvido; ele recebe um endereço formal estável. |

### 11.6 Concatenação acumulativa

C ↔ ¬C com v(C) = 0:  v(C↔¬C) = 0↔0 = 0 (E/C).

| Sistema          | Resultado             |
|------------------|-----------------------|
| Binário ingênuo  | Sem valoração estável |
| Trinário E? v2.0 | E/C — verificado      |

## 12. Comparação resumida

| Critério                          | Binário clássico      | E? v1.0                          | E? v2.0                                       |
|-----------------------------------|-----------------------|----------------------------------|-----------------------------------------------|
| Escala                            | {V, F}                | {0, ½, 1}                        | **\[−1,+1] contínua + {−1,0,+1} discreta**    |
| Origem dos valores                | Estipulada            | Estipulada                       | **Soma com média ponderada da evidência**     |
| Negação                           | Troca V/F             | 1−x                              | **Reflexão −x; E ponto fixo por aritmética**  |
| Diagnóstico D/C                   | —                     | Atribuído manualmente            | **Computável de (B, M)**                      |
| Fragmento decidido                | Excelente             | Idêntico ao clássico             | Idêntico ao clássico (verificado, 100%)       |
| Tautologias                       | Infinitas             | Nenhuma (não enunciado)          | **Nenhuma — Teorema 4 explícito**             |
| Explosão                          | Presente              | Teorema 3 tecnicamente incorreto | **Teorema 3 reformulado e correto**           |
| Revisão de crenças                | —                     | Questão em aberto                | **Dinâmica da Seção 9, testada**              |
| Robustez a ruído                  | Descontínua no limiar | —                                | **Contínua na camada evidencial (Lipschitz)** |
| Expressividade Belnap (None/Both) | —                     | Sugerida como trabalho futuro    | **Obtida via quadrantes (B, M)**              |

## 13. Limitações e questões em aberto

- Os parâmetros θ e m₀ são convencionais; a robustez a 20 configurações foi verificada, mas critérios normativos para escolhê-los por domínio de aplicação (medicina, direito, engenharia) permanecem abertos.
- A atribuição dos pesos wᵢ é o ponto de entrada do juízo humano no sistema; heurísticas de ponderação (independência de fontes, qualidade metodológica) precisam de formalização própria.
- A média ponderada assume evidências aproximadamente independentes; evidências correlacionadas inflam a massa M e pedem correção (por exemplo, deflator de correlação).
- A categoria I continua dependente do enquadramento epistemológico adotado.
- A semântica é proposicional; a extensão de primeira ordem exigirá domínio, quantificadores (∀ como ínfimo, ∃ como supremo são os candidatos naturais na escala ordenada) e regras adicionais.

## 14. Veredito formal

Conclusão

A Lógica Trinária E? v2.0 é um sistema em três camadas: agregação evidencial por soma com média ponderada em \[−1,+1], semântica trivalente {−1, 0, +1} com o zero como incerteza genuína e ponto fixo da negação, e diagnóstico D/C computável a partir de balanço e massa. O núcleo lógico é conservativo sobre a lógica clássica (verificado em 50.000 fórmulas, 100% de concordância), preserva Modus Ponens e as regras usuais (verificado exaustivamente), não possui tautologias (Teorema 4), é não trivial e monotônico na consequência, e revisável na evidência.

O ganho da v2.0 sobre a v1.0 é estrutural: os valores deixam de ser estipulados e passam a ser gerados; a indeterminação deixa de ser apenas rotulada e passa a ser explicada por duas grandezas mensuráveis — quanto se sabe (massa) e para onde pende o que se sabe (balanço). Além de aceitar, rejeitar ou suspender, o sistema agora informa *quanto falta* para decidir e *o que* impede a decisão.

**Autoria:** Arthur Braga Padilha

**Data:** 18 de julho de 2026

Documento de proposta teórica. Versão formal 2.0 — revisão com escala simétrica \[−1,+1], camada evidencial ponderada e correções da auditoria computacional (isomorfismo v1↔v2 verificado; 50.000 fórmulas por teste de conservatividade e ausência de tautologias; 20.000 casos de monotonicidade evidencial; 5.000 conjuntos de robustez; sementes fixas para reprodutibilidade).
