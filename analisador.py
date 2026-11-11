import argparse
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path


STOPWORDS = set("""
a à ao aos as às até com como da das de dela delas dele deles depois do dos e é
ela elas ele eles em entre era eram essa essas esse esses esta estas este estes
eu foi for foram há isso isto já lhe lhes mais mas me mesmo meu meus minha minhas
muito na nas nem no nos nós não num numa o os ou para pela pelas pelo pelos por
qual quando que quem se sem ser seu seus só sua suas também te tem têm teu tua
tudo um uma uns umas você vocês vai vão vou são sou está estou estava
ter tinha foi sido ainda aqui ali então assim onde porque pois cada outro outra
outros outras todo toda todos todas isso nesse nessa neste nesta dele dela
pra pro pras pros né tá tô
""".split())



class ExtratorHTML(HTMLParser):
    """
    Pega só o texto visível de uma página HTML, ignorando o que não é
    conteúdo (menu, rodapé, scripts e estilos).
    """
    IGNORAR = {"script", "style", "nav", "footer", "head", "noscript"}

    def __init__(self):
        super().__init__()
        self.partes = []
        self.nivel_ignorado = 0  

    def handle_starttag(self, tag, attrs):
        if tag in self.IGNORAR:
            self.nivel_ignorado += 1
        elif tag in ("p", "br", "h1", "h2", "h3", "li", "blockquote"):
            self.partes.append("\n")  
    def handle_endtag(self, tag):
        if tag in self.IGNORAR and self.nivel_ignorado > 0:
            self.nivel_ignorado -= 1

    def handle_data(self, data):
        if self.nivel_ignorado == 0:
            self.partes.append(data)


def ler_texto(caminho: Path) -> str:
    """Lê o arquivo e devolve só o texto. Se for HTML, remove as tags."""
    bruto = caminho.read_text(encoding="utf-8", errors="ignore")
    if caminho.suffix.lower() in (".html", ".htm"):
        extrator = ExtratorHTML()
        extrator.feed(bruto)
        return "".join(extrator.partes)
    return bruto



REGEX_PALAVRA = re.compile(r"[^\W\d_]+(?:[-'’][^\W\d_]+)*", re.UNICODE)


REGEX_FRASE = re.compile(r"[^.!?…]+[.!?…]*")


def analisar(texto: str, incluir_stopwords: bool = False, min_letras: int = 3) -> dict:
    """Recebe um texto e devolve um dicionário com todas as estatísticas."""
    palavras = [p.lower() for p in REGEX_PALAVRA.findall(texto)]
    frases = [f for f in REGEX_FRASE.findall(texto) if REGEX_PALAVRA.search(f)]

    
    relevantes = [
        p for p in palavras
        if len(p) >= min_letras and (incluir_stopwords or p not in STOPWORDS)
    ]

    total = len(palavras)
    unicas = len(set(palavras))

    return {
        "palavras": total,
        "unicas": unicas,
        "frases": len(frases),
        "caracteres": len(texto.strip()),
        "media_por_frase": total / len(frases) if frases else 0,
        "diversidade": unicas / total if total else 0,
        "minutos_leitura": total / 200,  # ~200 palavras por minuto
        "maior_palavra": max(palavras, key=len) if palavras else "",
        "ranking": Counter(relevantes),
    }



def mostrar(titulo: str, r: dict, top: int):
    print("=" * 56)
    print(f" {titulo}")
    print("=" * 56)
    if r["palavras"] == 0:
        print(" (nenhuma palavra encontrada)\n")
        return

    minutos = r["minutos_leitura"]
    leitura = f"{minutos:.1f} min" if minutos >= 1 else f"{minutos * 60:.0f} seg"

    print(f" Palavras          : {r['palavras']}")
    print(f" Palavras únicas   : {r['unicas']}")
    print(f" Frases            : {r['frases']}")
    print(f" Média/frase       : {r['media_por_frase']:.1f} palavras")
    print(f" Diversidade       : {r['diversidade']:.0%}  (únicas ÷ total)")
    print(f" Tempo de leitura  : {leitura}")
    print(f" Maior palavra     : {r['maior_palavra']}")

    if r["ranking"]:
        print(f"\n Top {top} palavras:")
        mais_comuns = r["ranking"].most_common(top)
        maior = mais_comuns[0][1]
        for palavra, qtd in mais_comuns:
            barra = "█" * max(1, round(qtd / maior * 20))
            print(f"  {palavra:<16} {qtd:>4}  {barra}")
    print()



def coletar_arquivos(caminho: Path):
    """Se for um arquivo, devolve ele. Se for pasta, devolve todos os textos dentro."""
    extensoes = {".txt", ".md", ".html", ".htm"}
    if caminho.is_file():
        return [caminho]
    return sorted(p for p in caminho.rglob("*") if p.suffix.lower() in extensoes)


def main():
    parser = argparse.ArgumentParser(description="Analisador de texto simples.")
    parser.add_argument("caminho", nargs="?", help="arquivo (.txt .md .html) ou pasta")
    parser.add_argument("--top", type=int, default=10, help="quantas palavras mostrar (padrão 10)")
    parser.add_argument("--min-letras", type=int, default=3, help="tamanho mínimo das palavras no ranking (padrão 3)")
    parser.add_argument("--todas", action="store_true", help="incluir palavras vazias (de, a, o, que...) no ranking")
    args = parser.parse_args()


    if not args.caminho:
        args.caminho = input("Arquivo ou pasta [exemplo.txt]: ").strip() or "exemplo.txt"
        print()

    caminho = Path(args.caminho.strip('"'))
    if not caminho.exists():
        sys.exit(f"Não encontrei: {caminho}")

    arquivos = coletar_arquivos(caminho)
    if not arquivos:
        sys.exit("Nenhum arquivo .txt, .md ou .html encontrado.")

    textos = []
    for arquivo in arquivos:
        texto = ler_texto(arquivo)
        textos.append(texto)
        if len(arquivos) > 1:
            r = analisar(texto, args.todas, args.min_letras)
            mostrar(arquivo.name, r, top=5)

    geral = analisar("\n".join(textos), args.todas, args.min_letras)
    nome = arquivos[0].name if len(arquivos) == 1 else f"TOTAL ({len(arquivos)} arquivos)"
    mostrar(nome, geral, args.top)


if __name__ == "__main__":
    main()