import os
import re
import urllib.request

# URLs bloqueadas vs novos caminhos locais relativos
SUBSTITUICOES = {
    r'https://storage\.googleapis\.com/claat-public/codelab-elements\.css': './codelab-elements.css',
    r'https://storage\.googleapis\.com/claat-public/native-shim\.js': './native-shim.js',
    r'https://storage\.googleapis\.com/claat-public/custom-elements\.min\.js': './custom-elements.min.js',
    r'https://storage\.googleapis\.com/claat-public/prettify\.js': './prettify.js',
    r'https://storage\.googleapis\.com/claat-public/codelab-elements\.js': './codelab-elements.js'
}

# Fontes oficiais para baixar os arquivos originais
ARQUIVOS_DOWNLOAD = {
    'codelab-elements.css': 'https://githubusercontent.com',
    'codelab-elements.js': 'https://githubusercontent.com',
    'native-shim.js': 'https://githubusercontent.com',
    'custom-elements.min.js': 'https://githubusercontent.com',
    'prettify.js': 'https://githubusercontent.com'
}

def garantir_arquivos_locais():
    """Baixa os arquivos de dependência se eles não existirem no diretório do script."""
    print("Verificando se as dependências existem localmente...")
    for nome, url in ARQUIVOS_DOWNLOAD.items():
        if not os.path.exists(nome):
            print(f"Baixando {nome}...")
            try:
                urllib.request.urlretrieve(url, nome)
            except Exception as e:
                print(f"Erro ao baixar {nome}: {e}. Crie o arquivo manualmente.")

def corrigir_arquivos():
    diretorio_atual = os.getcwd()
    
    # 1. Baixa os arquivos necessários para a pasta raiz onde o script roda
    garantir_arquivos_locais()
    
    print(f"\nBuscando arquivos index.html em: {diretorio_atual}\n")
    contador = 0

    # 2. Varre recursivamente todas as pastas
    for raiz, _, arquivos in os.walk(diretorio_atual):
        for arquivo in arquivos:
            if arquivo == "index.html":
                caminho_completo = os.path.join(raiz, arquivo)
                
                # Lê o conteúdo do index.html
                with open(caminho_completo, 'r', encoding='utf-8', errors='ignore') as f:
                    conteudo = f.read()
                
                # Aplica as substituições no HTML
                alterado = False
                novo_conteudo = conteudo
                for url_antiga, caminho_novo in SUBSTITUICOES.items():
                    if re.search(url_antiga, novo_conteudo):
                        novo_conteudo = re.sub(url_antiga, caminho_novo, novo_conteudo)
                        alterado = True
                
                # Se alterou o HTML, atualiza e copia os arquivos dependentes para o lado dele
                if alterado:
                    # Salva o arquivo HTML atualizado
                    with open(caminho_completo, 'w', encoding='utf-8') as f:
                        f.write(novo_conteudo)
                    
                    # Copia as dependências baixadas para a pasta desse codelab específico
                    for nome_arquivo in ARQUIVOS_DOWNLOAD.keys():
                        origem = os.path.join(diretorio_atual, nome_arquivo)
                        destino = os.path.join(raiz, nome_arquivo)
                        if os.path.exists(origem):
                            # Lê da raiz e escreve na subpasta
                            with open(origem, 'rb') as f_origem:
                                dados = f_origem.read()
                            with open(destino, 'wb') as f_destino:
                                f_destino.write(dados)
                                
                    print(f"[CORRIGIDO + INJETADO] {os.path.relpath(raiz, diretorio_atual)}")
                    contador += 1

    print(f"\nPronto! {contador} codelabs foram reparados com sucesso.")

if __name__ == "__main__":
    corrigir_arquivos()
