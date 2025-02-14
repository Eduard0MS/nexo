import pandas as pd

def processa_planilhas(file_hierarquia, file_estrutura_viva):
    # Leitura da planilha de hierarquia
    if file_hierarquia.name.endswith('.csv'):
        df_hierarquia = pd.read_csv(file_hierarquia, encoding="utf-8")
    else:
        df_hierarquia = pd.read_excel(file_hierarquia)

    # Leitura da planilha de estrutura viva
    if file_estrutura_viva.name.endswith('.csv'):
        df_estrutura_viva = pd.read_csv(file_estrutura_viva, encoding="utf-8")
    else:
        df_estrutura_viva = pd.read_excel(file_estrutura_viva)

    # Processar a planilha de hierarquia: remover metadados e renomear colunas
    df_hierarquia = df_hierarquia.iloc[3:].reset_index(drop=True)
    df_hierarquia.columns = ["Código", "Unidade Organizacional - Sigla"]
    df_hierarquia.dropna(inplace=True)
    df_hierarquia["Código"] = df_hierarquia["Código"].astype(str).str.strip()

    # Processar a planilha de estrutura viva sem alterar os demais dados
    if "Código Unidade" not in df_estrutura_viva.columns:
        raise KeyError("A coluna 'Código Unidade' não foi encontrada na planilha de estrutura viva.")
    df_estrutura_viva["Código Unidade"] = df_estrutura_viva["Código Unidade"].astype(str).str.strip()
    if "Categoria" in df_estrutura_viva.columns:
        df_estrutura_viva["Categoria"] = df_estrutura_viva["Categoria"].fillna(0).astype(int)
    if "Nível" in df_estrutura_viva.columns:
        df_estrutura_viva["Nível"] = df_estrutura_viva["Nível"].fillna(0).astype(int)

    # -------------------------------
    # Apenas para construir o campo "Grafo"
    # -------------------------------
    hierarquia_info = {}
    stack = []
    for _, row in df_hierarquia.iterrows():
        codigo = row["Código"]
        unidade = row["Unidade Organizacional - Sigla"]
        # Aqui a lógica calcula o nível para construir o grafo a partir da indentação;
        # ela não altera nenhum dado que será carregado no BD.
        nivel_hierarquico = (len(unidade) - len(unidade.lstrip())) // 5
        while len(stack) > nivel_hierarquico:
            stack.pop()
        if stack:
            grafo_val = f"{hierarquia_info[stack[-1]]['grafo']}-{codigo}"
        else:
            grafo_val = codigo
        stack.append(codigo)
        hierarquia_info[codigo] = {
            "grafo": grafo_val,
            "nivel_hierarquico": nivel_hierarquico,
            "deno_unidade": unidade.strip()
        }

    # Cria uma cópia dos dados originais da planilha de estrutura viva
    df_resultado = df_estrutura_viva.copy()

    # Atualiza (ou adiciona) apenas as colunas "Grafo" e "Sigla"
    df_resultado["Grafo"] = df_resultado["Código Unidade"].map(
        lambda code: hierarquia_info.get(code, {}).get("grafo", "")
    )
    # Se "Nível Hierárquico" não existir na planilha original, o adiciona
    if "Nível Hierárquico" not in df_resultado.columns:
        df_resultado["Nível Hierárquico"] = df_resultado["Código Unidade"].map(
            lambda code: hierarquia_info.get(code, {}).get("nivel_hierarquico", 0)
        )
    # Se "Deno Unidade" não existir na planilha original, o adiciona
    if "Deno Unidade" not in df_resultado.columns:
        df_resultado["Deno Unidade"] = df_resultado["Código Unidade"].map(
            lambda code: hierarquia_info.get(code, {}).get("deno_unidade", "")
        )

    # Criação da coluna "Sigla" com o formato "Tipo do Cargo-Categoria-Nível"
    def format_sigla(row):
        if pd.notna(row["Tipo do Cargo"]) and pd.notna(row["Categoria"]) and pd.notna(row["Nível"]):
            return f"{row['Tipo do Cargo']}-{row['Categoria']}.{row['Nível']:02d}"
        return ""
    df_resultado["Sigla"] = df_resultado.apply(format_sigla, axis=1)

    return df_resultado
