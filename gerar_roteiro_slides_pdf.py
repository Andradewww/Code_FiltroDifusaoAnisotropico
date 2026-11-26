from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4


RAIZ = Path(__file__).resolve().parent
SAIDA = RAIZ / 'output' / 'pdf' / 'Conteudo_Slides_Difusao_Anisotropica.pdf'
SAIDA.parent.mkdir(parents=True, exist_ok=True)
for nome, arquivo in [('Arial', 'arial.ttf'), ('ArialBold', 'arialbd.ttf'), ('Consolas', 'consola.ttf'), ('MathSymbols', 'seguisym.ttf')]:
    pdfmetrics.registerFont(TTFont(nome, str(Path('C:/Windows/Fonts') / arquivo)))
pdfmetrics.registerFontFamily('Arial', normal='Arial', bold='ArialBold', italic='Arial', boldItalic='ArialBold')

estilos = {
    'titulo': ParagraphStyle('titulo', fontName='ArialBold', fontSize=21, leading=26, spaceAfter=22, textColor=colors.HexColor('#17354b')),
    'corpo': ParagraphStyle('corpo', fontName='Arial', fontSize=11, leading=16, spaceAfter=11),
    'rotulo': ParagraphStyle('rotulo', fontName='ArialBold', fontSize=10, leading=14, spaceBefore=16, spaceAfter=9, textColor=colors.HexColor('#34566d')),
    'nota': ParagraphStyle('nota', fontName='Arial', fontSize=10, leading=15, spaceAfter=9),
    'codigo': ParagraphStyle('codigo', fontName='Consolas', fontSize=8.5, leading=12, spaceBefore=7, spaceAfter=12),
}
historia = []

def p(texto, estilo='corpo'):
    marcado = escape(texto).replace('\n', '<br/>').replace('∇', '<font name="MathSymbols">∇</font>')
    historia.append(Paragraph(marcado, estilos[estilo]))

def topicos(itens):
    for item in itens:
        marcado = escape(item).replace('∇', '<font name="MathSymbols">∇</font>')
        historia.append(Paragraph('• ' + marcado, estilos['corpo']))

def codigo(texto):
    historia.append(Preformatted(texto, estilos['codigo']))

def tabela(linhas):
    t = Table([[Paragraph(escape(str(c)), estilos['nota']) for c in linha] for linha in linhas], colWidths=[300, 175], hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#edf2f5')),
        ('LINEBELOW', (0, 0), (-1, 0), .8, colors.HexColor('#8b9ca8')),
        ('LINEBELOW', (0, 1), (-1, -1), .3, colors.HexColor('#d8e0e5')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    historia.append(t)
    historia.append(Spacer(1, 12))

def slide(n, titulo):
    if n > 1:
        historia.append(PageBreak())
    p(f'SLIDE {n:02d}', 'rotulo')
    p(titulo, 'titulo')
    p('CONTEÚDO PARA O SLIDE', 'rotulo')

def imagem(texto):
    p('ORIENTAÇÃO DE IMAGEM - NÃO COPIAR COMO CONTEÚDO', 'rotulo')
    p(texto, 'nota')

slide(1, 'Filtro de difusão anisotrópica')
p('Filtro de difusão anisotrópica no realce de imagens')
p('Suavização de regiões com preservação de contornos')
p('Josué Henrique Baade de Andrade\nLucas Miles')
p('Instituto Federal Catarinense - IFC\nProcessamento Digital de Imagens')
imagem('Use a imagem geométrica original ao lado do título, sem ocupar o fundo inteiro.')

slide(2, 'Realce e suavização de imagens')
p('O realce busca tornar informações da imagem mais perceptíveis. A suavização contribui para esse processo ao reduzir variações locais de intensidade, como aquelas provocadas pelo ruído.')
p('Entretanto, suavizar uma imagem também pode borrar contornos e apagar detalhes. Por isso, é necessário equilibrar a redução do ruído com a conservação das estruturas importantes.')
p('Objetivo do trabalho: demonstrar como a difusão anisotrópica realiza essa suavização de maneira controlada.')
imagem('Coloque lado a lado a imagem original e a imagem com ruído, com os títulos Referência e Com ruído. Arquivos: 01_original_cinza.png e 02_com_ruido.png, na pasta imagens_saida.')

slide(3, 'Autores e origem do modelo')
p('O modelo estudado foi desenvolvido por Pietro Perona e Jitendra Malik, sendo conhecido como difusão de Perona-Malik.')
p('Seu artigo de referência foi publicado em 1990, com o título:')
p('Scale-Space and Edge Detection Using Anisotropic Diffusion')
p('A proposta favorece a suavização dentro das regiões e restringe a mistura de intensidades através de suas fronteiras.')
imagem('Internet: utilize uma captura do título e dos autores na primeira página do artigo original. Rodapé: Fonte: Perona e Malik (1990).')
p('https://people.eecs.berkeley.edu/~malik/papers/MP-aniso.pdf', 'nota')

slide(4, 'Como a difusão anisotrópica funciona')
p('O filtro compara as intensidades de pixels próximos e utiliza essas diferenças para controlar a suavização.')
topicos(['Diferenças pequenas: maior condução.', 'Diferenças grandes: menor condução.', 'Iterações: repetição das atualizações.'])
p('Assim, regiões semelhantes tendem a ficar mais uniformes, enquanto a mistura entre regiões muito diferentes é reduzida.')
imagem('Monte no Canva um esquema com um pixel central e quatro vizinhos: norte, sul, leste e oeste. Esse esquema representa a vizinhança utilizada no código.')

slide(5, 'Gradiente e função de condução')
p('O gradiente descreve a variação de intensidade da imagem. Em áreas uniformes, sua magnitude tende a ser pequena. Em transições entre regiões claras e escuras, tende a ser maior.')
p('O modelo contínuo é representado por:')
p('∂I/∂t = div[c(‖∇I‖) ∇I]')
topicos(['I: imagem em processamento.', '∇I: gradiente da imagem.', 'c: função que controla a condução.', 't: evolução da filtragem.'])
p('Na implementação, foi utilizada a função exponencial:')
p('c(s) = exp[−(s/K)²]')
p('Quanto maior a variação considerada em relação a K, menor será a condução.')
imagem('Destaque as equações. Não é necessário acrescentar fotografia.')

slide(6, 'Principais aplicações')
topicos(['Redução de ruído com preservação de contornos.', 'Preparação para detecção de bordas.', 'Preparação para segmentação de regiões.', 'Processamento de imagens médicas.'])
p('Gerig e colaboradores (1992) estudaram a aplicação da filtragem anisotrópica em imagens de ressonância magnética, buscando reduzir ruído e preservar estruturas e limites anatômicos.')
imagem('Internet: pode utilizar uma figura de ressonância magnética do estudo de Gerig e colaboradores. Identifique-a como exemplo de aplicação da literatura, pois não faz parte do experimento de vocês. Rodapé: Fonte: Gerig et al. (1992).')
p('https://www.lpi.tel.uva.es/muitic/pim/docus/gerig.pdf', 'nota')

slide(7, 'Imagem utilizada no experimento')
p('Foi utilizada uma imagem geométrica em tons de cinza, com 740 × 431 pixels.')
p('A imagem apresenta:')
topicos(['Uma região central uniforme.', 'Contornos inclinados.', 'Degradês no fundo.'])
p('Essas características permitem observar a granulação acrescentada e as alterações produzidas nos contornos e nas transições suaves.')
imagem('Use a Figura 1 do artigo em tamanho grande, preferencialmente inserindo o PNG original. Rodapé: Imagem de referência obtida no Magnific.')

slide(8, 'Preparação da imagem e adição de ruído')
p('A implementação foi desenvolvida em Python, utilizando:')
topicos(['Pillow: leitura e gravação.', 'NumPy: cálculos sobre os pixels.', 'Matplotlib: comparação dos resultados.'])
p('A imagem já apresentava tons de cinza. Foi utilizada uma matriz de intensidades em ponto flutuante, à qual se acrescentou ruído gaussiano.')
codigo('gerador = np.random.default_rng(semente)\n\nruido = gerador.normal(\n    loc=media,\n    scale=desvio_padrao,\n    size=imagem.shape\n)\n\nimagem_com_ruido = imagem + ruido')
imagem('Use a Figura 2, mostrando a imagem com ruído. Se o slide ficar cheio, dê prioridade ao código e a um recorte da região central.')

slide(9, 'Parâmetros do experimento')
tabela([['Parâmetro', 'Valor utilizado'], ['Função de condução', 'Exponencial'], ['K', '20'], ['Passo λ', '0,1'], ['Iterações', '5, 15 e 30'], ['Média do ruído', '0'], ['Desvio padrão do ruído', '5'], ['Semente aleatória', '42']])
p('K controla a sensibilidade às diferenças de intensidade.\nO passo controla a intensidade de cada atualização.\nAs iterações definem quantas atualizações são realizadas.')
p('Todos os testes começaram na mesma imagem com ruído.')
imagem('Utilize a tabela e explicações curtas, sem imagem de fundo.')

slide(10, 'Código: diferenças entre vizinhos')
p('Para cada pixel, são calculadas as diferenças em relação aos quatro vizinhos diretos.')
codigo('diferenca_norte = imagem_expandida[:-2, 1:-1] - resultado\ndiferenca_sul = imagem_expandida[2:, 1:-1] - resultado\ndiferenca_leste = imagem_expandida[1:-1, 2:] - resultado\ndiferenca_oeste = imagem_expandida[1:-1, :-2] - resultado')
p('Essas diferenças indicam quanto as intensidades variam em cada direção.')
p('Nas extremidades, os pixels das bordas são repetidos para formar uma margem, evitando a conexão entre lados opostos da imagem.')
imagem('Use o código acompanhado de um pequeno esquema dos quatro vizinhos. Utilize fonte monoespaçada e evite uma captura do arquivo inteiro.')

slide(11, 'Código: condução e atualização')
p('A função exponencial atribui um coeficiente a cada diferença. Exemplo para a direção norte:')
codigo('conducao_norte = np.exp(-(diferenca_norte / k) ** 2)')
p('O mesmo cálculo é realizado nas outras direções. Depois, as contribuições são somadas:')
codigo('atualizacao = (\n    conducao_norte * diferenca_norte\n    + conducao_sul * diferenca_sul\n    + conducao_leste * diferenca_leste\n    + conducao_oeste * diferenca_oeste\n)\n\nresultado = resultado + passo * atualizacao')
p('Todos os novos valores são calculados a partir da mesma iteração anterior.')
imagem('Destaque a função exponencial e a última linha. O código pode ocupar a maior parte do slide.')

slide(12, 'Comparação das imagens completas')
p('Efeito do número de iterações')
topicos(['5 iterações: redução da granulação, com variações ainda presentes.', '15 iterações: região central mais uniforme e contorno principal bem definido.', '30 iterações: maior suavização, com borramento em algumas transições.'])
imagem('Use a organização da Figura 3 do artigo: Referência | Com ruído | 5 iterações | 15 iterações | 30 iterações. Monte a comparação com os PNGs originais para manter a qualidade. Deixe as imagens grandes e o texto na parte inferior.')

slide(13, 'Comparação dos recortes ampliados')
p('Os recortes da mesma região permitem observar melhor:')
topicos(['A granulação provocada pelo ruído.', 'A uniformização da região central.', 'As mudanças próximas ao contorno inclinado.'])
p('O aumento das iterações reduz a granulação, mas também pode alterar as transições da imagem.')
imagem('Use os recortes apresentados nas Figuras 4 e 5 do artigo. Identifique: Referência → Com ruído → 5 → 15 → 30 iterações. Este slide deve ser principalmente visual. Os recortes precisam mostrar exatamente a mesma região e ter o mesmo tamanho.')

slide(14, 'Avaliação numérica dos resultados')
p('Foi calculado o RMSE, uma medida do erro em relação à imagem de referência.')
p('Quanto menor o valor, maior a proximidade com a referência segundo essa medida.')
tabela([['Versão', 'RMSE'], ['Imagem com ruído', '4,99'], ['5 iterações', '1,81'], ['15 iterações', '1,64'], ['30 iterações', '1,87']])
p('Entre as configurações avaliadas, 15 iterações apresentou o menor erro.')
p('Com 30 iterações, a região central ficou mais uniforme, mas o erro da imagem inteira aumentou.')
imagem('Use a tabela ou um gráfico de barras com os mesmos valores. Destaque o resultado de 15 iterações. Rodapé: Cálculo complementar sobre as imagens de saída.')

slide(15, 'Conclusões')
p('A implementação mostrou que a difusão anisotrópica reduziu o ruído acrescentado e manteve visualmente o contorno principal da imagem.')
topicos(['15 iterações: menor RMSE entre os testes.', '30 iterações: maior uniformidade, mas maior alteração de algumas transições.', 'Mais suavização não significa melhora contínua.', 'A escolha dos parâmetros depende da imagem e do objetivo.'])
p('As conclusões se limitam à imagem e às configurações utilizadas.')
imagem('Coloque um recorte da imagem com ruído ao lado do resultado com 15 iterações.')

slide(16, 'Referências')
p('GONZALEZ; WOODS (2010).\nProcessamento digital de imagens.')
p('PERONA; MALIK (1990).\nScale-Space and Edge Detection Using Anisotropic Diffusion.')
p('GERIG et al. (1992).\nNonlinear Anisotropic Filtering of MRI Data.')
p('TSIOTSIOS; PETROU.\nOn the Choice of the Parameters for Anisotropic Diffusion in Image Processing.')
p('INSIGHT TOOLKIT.\nDocumentação técnica sobre difusão anisotrópica.')
p('MAGNIFIC.\nOrigem da imagem geométrica.')
imagem('Não precisa de imagem. Mantenha os links nas referências ou nas notas do Canva.')

def rodape(c, doc):
    c.saveState()
    c.setStrokeColor(colors.HexColor('#d8e0e5'))
    c.line(55, 48, A4[0]-55, 48)
    c.setFont('Arial', 8)
    c.setFillColor(colors.HexColor('#536574'))
    c.drawString(55, 34, 'Roteiro para o Canva | Difusão anisotrópica | Texto selecionável')
    c.drawRightString(A4[0]-55, 34, f'{doc.page} / 16')
    c.restoreState()

doc = SimpleDocTemplate(str(SAIDA), pagesize=A4, rightMargin=55, leftMargin=55, topMargin=40, bottomMargin=65,
    title='Conteúdo dos slides - Difusão anisotrópica', author='Josué Henrique Baade de Andrade; Lucas Miles')
doc.build(historia, onFirstPage=rodape, onLaterPages=rodape)
print(SAIDA)
