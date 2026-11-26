from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


#CONFIGURAÇÕES DO EXPERIMENTO

pasta_projeto = Path(__file__).resolve().parent

caminho_imagem = pasta_projeto / "imagens" / "01_original_cinza.png"
pasta_saida = pasta_projeto / "imagens_saida"

#valores considerados para imagens na escala de 0 a 255
k = 20.0
passo = 0.1

quantidades_iteracoes = [5, 15, 30]

media_ruido = 0.0
desvio_padrao_ruido = 5.0
semente = 42


#FUNÇÃO PARA ADICIONAR RUÍDO GAUSSIANO

def adicionar_ruido(imagem, media, desvio_padrao, semente):
    """Adiciona ruído gaussiano de maneira reproduzível."""

    gerador = np.random.default_rng(semente)

    ruido = gerador.normal(
        loc=media,
        scale=desvio_padrao,
        size=imagem.shape
    )

    imagem_com_ruido = imagem + ruido

    # Mantém as intensidades dentro da escala de 0 a 255
    return np.clip(imagem_com_ruido, 0, 255)


#FILTRO DE DIFUSÃO ANISOTRÓPICA

def difusao_anisotropica(imagem, iteracoes, k, passo):
    """
    Aplica uma versão discreta do modelo de Perona-Malik.

    Utiliza quatro vizinhos e a função de condução exponencial.
    """

    if k <= 0:
        raise ValueError("O parâmetro k deve ser maior que zero.")

    #limite para este esquema de quatro vizinhos, sem divisão adicional da soma por quatro
    if not 0 < passo <= 0.25:
        raise ValueError("O passo deve estar entre 0 e 0.25.")

    #cálculo usa ponto flutuante para preservar valores negativos nas diferenças e casas decimais nas atualizações
    resultado = imagem.astype(np.float64).copy()

    for _ in range(iteracoes):

        #repete os pixels das bordas para criar uma margem, dessa forma, não conectamos lados opostos da imagem
        imagem_expandida = np.pad(
            resultado,
            pad_width=1,
            mode="edge"
        )

        #diferenças entre cada vizinho e o pixel central
        diferenca_norte = imagem_expandida[:-2, 1:-1] - resultado
        diferenca_sul = imagem_expandida[2:, 1:-1] - resultado
        diferenca_leste = imagem_expandida[1:-1, 2:] - resultado
        diferenca_oeste = imagem_expandida[1:-1, :-2] - resultado

        #função de condução: c = exp[-(diferença / k)²]
        conducao_norte = np.exp(-(diferenca_norte / k) ** 2)
        conducao_sul = np.exp(-(diferenca_sul / k) ** 2)
        conducao_leste = np.exp(-(diferenca_leste / k) ** 2)
        conducao_oeste = np.exp(-(diferenca_oeste / k) ** 2)

        #soma das contribuições dos quatro vizinhos
        atualizacao = (
            conducao_norte * diferenca_norte
            + conducao_sul * diferenca_sul
            + conducao_leste * diferenca_leste
            + conducao_oeste * diferenca_oeste
        )

        #todos os pixels são atualizados a partir dos valores da mesma iteração anterior
        resultado = resultado + passo * atualizacao

    return resultado


#FUNÇÃO PARA SALVAR AS IMAGENS

def salvar_imagem(imagem, caminho):
    """Arredonda e converte para 8 bits somente ao salvar."""

    imagem_8bits = np.clip(
        np.rint(imagem),
        0,
        255
    ).astype(np.uint8)

    Image.fromarray(imagem_8bits).save(caminho)


#EXECUÇÃO DO EXPERIMENTO

def main():
    pasta_saida.mkdir(parents=True, exist_ok=True)

    # Abre a imagem, que já está em tons de cinza
    with Image.open(caminho_imagem) as foto:
        pixels = np.array(foto, dtype=np.float64)

    #os canais de cor são iguais, utiliza apenas o primeiro
    imagem_original = pixels[:, :, 0]

    #cria uma única versão com ruído para todos os testes
    imagem_com_ruido = adicionar_ruido(
        imagem_original,
        media_ruido,
        desvio_padrao_ruido,
        semente
    )

    salvar_imagem(
        imagem_original,
        pasta_saida / "01_original_cinza.png"
    )

    salvar_imagem(
        imagem_com_ruido,
        pasta_saida / "02_com_ruido.png"
    )

    imagens_comparacao = [
        ("Original em cinza", imagem_original),
        ("Com ruído gaussiano", imagem_com_ruido)
    ]

    #cada teste começa na mesma imagem com ruído
    for iteracoes in quantidades_iteracoes:
        imagem_filtrada = difusao_anisotropica(
            imagem_com_ruido,
            iteracoes,
            k,
            passo
        )

        salvar_imagem(
            imagem_filtrada,
            pasta_saida / f"difusao_{iteracoes:02d}_iteracoes.png"
        )

        imagens_comparacao.append(
            (f"Difusão: {iteracoes} iterações", imagem_filtrada)
        )

        print(f"Filtro aplicado com {iteracoes} iterações.")

    #apresenta todas as versões na mesma escala de intensidade
    figura, eixos = plt.subplots(
        1,
        len(imagens_comparacao),
        figsize=(16, 7)
    )

    for eixo, (titulo, imagem) in zip(eixos, imagens_comparacao):
        eixo.imshow(
            imagem,
            cmap="gray",
            vmin=0,
            vmax=255
        )

        eixo.set_title(titulo)
        eixo.axis("off")

    figura.suptitle(
        f"Difusão anisotrópica — K={k:g} | passo={passo:g}"
    )

    figura.tight_layout()

    figura.savefig(
        pasta_saida / "comparacao.png",
        dpi=150,
        bbox_inches="tight"
    )

    print(f"\nImagens salvas em: {pasta_saida}")

    plt.show()
    plt.close(figura)


if __name__ == "__main__":
    main()