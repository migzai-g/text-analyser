# 📝 Analisador de Texto

Programa didático em Python que lê um texto e mostra estatísticas sobre ele: quantas palavras, quantas frases, tempo de leitura, palavras mais usadas e mais.

Funciona com arquivos `.txt`, `.md` e `.html` (inclusive **páginas de sites**, ignorando menu, rodapé e scripts) ou com uma **pasta inteira** de uma vez.

Não precisa instalar nada: usa só a biblioteca padrão do Python.

---

## Requisitos

- Python 3.8 ou superior

---

## Como usar

### 1. Analisar um arquivo

```bash
python analisador.py exemplo.txt
```

### 2. Analisar uma página HTML

```bash
python analisador.py minha-pagina.html
```

### 3. Analisar uma pasta inteira

```bash
python analisador.py minha_pasta/
```

Mostra um resumo de cada arquivo e, no final, o total de todos juntos. É ótimo para analisar todos os textos de um site estático (por exemplo, a pasta `projetos/` de um site do Neocities).

### 4. Sem nenhuma opção

Se você rodar só `python analisador.py` (ou clicar em "Run" no VS Code), o programa pergunta o caminho. Apertando `Enter`, ele usa o `exemplo.txt`.

### Opções

| Opção | Descrição |
|-------|-----------|
| `--top N` | Quantas palavras mostrar no ranking (padrão: `10`) |
| `--min-letras N` | Tamanho mínimo das palavras no ranking (padrão: `3`) |
| `--todas` | Inclui palavras "vazias" (de, a, o, que...) no ranking |

---

## Exemplo de saída

```
========================================================
 exemplo.txt
========================================================
 Palavras          : 91
 Palavras únicas   : 65
 Frases            : 9
 Média/frase       : 10.1 palavras
 Diversidade       : 71%  (únicas ÷ total)
 Tempo de leitura  : 27 seg
 Maior palavra     : equilíbrio

 Top 6 palavras:
  aprender            2  ████████████████████
  programar           2  ████████████████████
  parece              2  ████████████████████
  pista               2  ████████████████████
  projeto             2  ████████████████████
  andar               1  ██████████
```

---

## Exemplo real: analisando um site

O analisador também funciona em páginas HTML. Aqui, ele foi usado na pasta `projetos/` do meu site no Neocities ([migzai.neocities.org](https://migzai.neocities.org)), que tem 8 textos:

```bash
python analisador.py neocities-migzai/projetos
```

Para pastas, o programa mostra primeiro um resumo de cada página e, no fim, o total de todas juntas:

```
========================================================
 TOTAL (8 arquivos)
========================================================
 Palavras          : 5851
 Palavras únicas   : 1891
 Frases            : 388
 Média/frase       : 15.1 palavras
 Diversidade       : 32%  (únicas ÷ total)
 Tempo de leitura  : 29.3 min
 Maior palavra     : inconscientemente

 Top 10 palavras:
  jogo               29  ████████████████████
  sociedade          21  ██████████████
  cidade             20  ██████████████
  mundo              17  ████████████
  han                14  ██████████
  algo               14  ██████████
  axel               14  ██████████
  coisa              13  █████████
  ponto              12  ████████
  apenas             12  ████████
```

Dá para ver que os textos giram em torno de temas como jogos, sociedade e cidade. Os nomes próprios (`han`, `axel`) aparecem no ranking porque são citados várias vezes.

---

## O que cada número significa

| Estatística | Como é calculada |
|-------------|------------------|
| **Palavras** | Total de palavras (números ficam de fora) |
| **Únicas** | Quantas palavras diferentes existem |
| **Frases** | Trechos terminados em `.` `!` `?` ou `…` |
| **Média/frase** | Palavras ÷ frases |
| **Diversidade** | Únicas ÷ total. Quanto maior, mais variado é o vocabulário |
| **Tempo de leitura** | Palavras ÷ 200 (média de leitura de um adulto, em palavras por minuto) |

---

## Como funciona

O código tem 4 etapas simples:

1. **Ler** (`ler_texto`): abre o arquivo. Se for HTML, a classe `ExtratorHTML` remove as tags e descarta `nav`, `footer`, `script` e `style`, ficando só com o texto.
2. **Separar palavras** (`REGEX_PALAVRA`): uma expressão regular encontra as palavras, aceitando acentos e hífen (`guarda-chuva`).
3. **Contar** (`analisar`): usa `Counter`, do módulo `collections`, para contar quantas vezes cada palavra aparece. Palavras muito comuns (as *stopwords*, como "de", "que", "para") são ignoradas no ranking, porque não dizem nada sobre o assunto.
4. **Mostrar** (`mostrar`): imprime tudo formatado, com barrinhas proporcionais no ranking.

### Personalizando

- Quer ignorar mais palavras no ranking? Adicione-as à lista `STOPWORDS` no topo do `analisador.py`.
- Quer outra velocidade de leitura? Troque o `200` em `minutos_leitura`.

---

## Ideias para evoluir

- Exportar o resultado para CSV ou JSON
- Gerar uma nuvem de palavras com a biblioteca `wordcloud`
- Fazer um gráfico das palavras mais usadas com `matplotlib`
- Comparar dois textos lado a lado
- Detectar palavras repetidas muito perto uma da outra (vício de escrita)
- Medir a legibilidade do texto (índice Flesch adaptado ao português)

---

## Licença

Livre para estudar, usar e modificar.