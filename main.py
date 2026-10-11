import flet as ft
from models import criar_tabelas, salvar_usuario,listar_usuarios

# Cor de fundo de cada card, de acordo com a classificação do IMC
CORES_IMC = {
    "Abaixo do peso": ft.Colors.BLUE_400,
    "Peso normal": ft.Colors.GREEN_600,
    "Sobrepeso": ft.Colors.ORANGE_400,
    "Obesidade grau 1": ft.Colors.ORANGE_700,
    "Obesidade grau 2": ft.Colors.RED_400,
    "Obesidade grau 3": ft.Colors.RED_900,
}
# Cria um card colorido com o nome, a classificação e o valor do IMC
def criar_card(nome, imc, classificacao):
    cor = CORES_IMC.get(classificacao, ft.Colors.GREY_600)

    return ft.Container(
        content=ft.Row(
            controls=[
                # Coluna da esquerda: nome e classificação
                ft.Column(
                    controls=[
                        ft.Text(nome, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text(classificacao, size=14, color=ft.Colors.WHITE),
                    ],
                    expand=True,
                ),
                # Valor do IMC, do lado direito
                ft.Text(
                    f"IMC {imc:.1f}",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=cor,
        padding=15,
        border_radius=10,
        margin=8,
    )


# Função principal da aplicação. O Flet a chama e lhe entrega a "page",
# que é a janela onde os componentes são colocados.
def main(page: ft.Page):
    page.title = "Cálculo de IMC"  # define o título da janela
    page.window.height = 700
    page.window.width = 700
    page.window.resizable = False
    page.window.alignment = ft.Alignment.CENTER

    # Garante que a tabela exista antes de qualquer operação com o banco.
    criar_tabelas()

    # Aviso no topo: começa invisível e ganha cor conforme o resultado
    aviso = ft.Container(
        content=ft.Text("", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        bgcolor=ft.Colors.RED_600,
        padding=15,
        border_radius=8,
        visible=False,
    )

    # Mostra o aviso no topo: verde para sucesso, vermelho para erro
    def mostrar_aviso(texto, sucesso=False):
        aviso.bgcolor = ft.Colors.GREEN_600 if sucesso else ft.Colors.RED_600
        aviso.content.value = texto
        aviso.visible = True

    # Campo de texto onde o usuário digita as informações.
    campo_nome = ft.TextField(label="Nome",expand=True)
    campo_idade = ft.TextField(label="Idade",expand=True)
    campo_peso = ft.TextField(label="Peso (Kg)",expand=True)
    campo_altura = ft.TextField(label="Altura (m)",expand=True)

    # Primeira linha: campo 1 e campo 2 lado a lado
    linha1 = ft.Row(controls=[campo_nome, campo_idade])
    # Segunda linha: campo 3 e campo 4 lado a lado
    linha2 = ft.Row(controls=[campo_altura, campo_peso])

    # Texto usado para exibir mensagens de sucesso ou erro.
    #mensagem = ft.Text()

    # Lista de resultados que aparece abaixo do botão
    lista_resultados = ft.ListView(expand=True, spacing=8)

    # Função chamada quando o botão é clicado.
    def ao_clicar(e):
        # Lê os textos digitados e remove espaços no início e no fim
        nome = campo_nome.value.strip()
        idade_txt = campo_idade.value.strip()
        altura_txt = campo_altura.value.strip()
        peso_txt = campo_peso.value.strip()

        # Bloqueia o cálculo se algum campo estiver em branco
        if not nome or not idade_txt or not altura_txt or not peso_txt:
            mostrar_aviso("Preencha todos os campos.")
            return

        # Converte os textos para números. Aceita vírgula no lugar do ponto.
        try:
            idade = int(idade_txt)
            altura = float(altura_txt.replace(",", "."))
            peso = float(peso_txt.replace(",", "."))
        except ValueError:
            mostrar_aviso("Idade, altura e peso devem ser números.")
            return

        # Evita divisão por zero e valores sem sentido
        if altura <= 0 or peso <= 0:
            mostrar_aviso("Altura e peso devem ser maiores que zero.")
            return

        # Salva no banco e recebe id, IMC e classificação
        novo_id, imc, classificacao = salvar_usuario(nome, idade, peso, altura)

        # Adiciona o card na lista de resultados
        lista_resultados.controls.append(criar_card(nome, imc, classificacao))
        mostrar_aviso("Cálculo salvo com sucesso!", sucesso=True)

        # Limpa os campos para o próximo cálculo
        campo_nome.value = ""
        campo_idade.value = ""
        campo_altura.value = ""
        campo_peso.value = ""
    
     # Funções assíncronas, porque push_route precisa de await
    async def ir_para_historico(e):
        await page.push_route("/historico")

    async def voltar_inicio(e):
        await page.push_route("/")
        
    # Adiciona os componentes à página, na ordem em que devem aparecer.
    # Tela 1: calculadora. A route "/" é a tela inicial.
    tela_calculadora = ft.View(
        # Monta a tela de histórico lendo os dados atuais do banco
        route="/",
        padding=20,
        controls=[
            aviso,
            ft.Text(
                "Calculadora de IMC",
                size=36,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
                align=ft.Alignment.CENTER,
            ),
            ft.Column(
                controls=[
                    ft.Row(controls=[campo_nome, campo_idade]),
                    ft.Row(controls=[campo_altura, campo_peso]),
                ]
            ),
            ft.Row(
                controls=[
                    ft.Button(
                        content=ft.Text("Calcular", size=16),
                        on_click=ao_clicar,
                        width=200,
                        height=45,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            # Botão que leva à rota "/historico"
            ft.Row(
                controls=[
                    ft.TextButton(
                        "Ver histórico",
                        icon=ft.Icons.HISTORY,
                        #on_click=lambda e: page.push_route("/historico"),
                        on_click=ir_para_historico,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Resultados desta sessão", size=18, weight=ft.FontWeight.BOLD),
                        lista_resultados,
                    ]
                ),
                bgcolor=ft.Colors.BLUE_700,
                border_radius=12,
                padding=15,
            ),
        ],
    )
                              
    # Monta a tela de histórico lendo os dados atuais do banco
    def montar_historico():
        lista_historico = ft.ListView(spacing=8, expand=True)

        registros = listar_usuarios()
        if not registros:
            lista_historico.controls.append(ft.Text("Nenhum cálculo salvo ainda."))

        for nome, imc, classificacao in registros:
            lista_historico.controls.append(criar_card(nome, imc, classificacao))

        return ft.View(
            route="/historico",
            padding=20,
            controls=[
                ft.Text(
                    "Histórico de cálculos",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700,
                ),
                ft.Container(
                    content=lista_historico,
                    expand=True,
                    bgcolor=ft.Colors.BLUE_700,
                    border_radius=12,
                    padding=15,
                ),
                ft.TextButton(
                    "Voltar",
                    icon=ft.Icons.ARROW_BACK,
                    #on_click=lambda e: page.push_route("/"),
                    on_click=voltar_inicio,
                ),
            ],
        )

    # Chamada sempre que a rota muda
    def mudar_rota(e):
        page.views.clear()
        page.views.append(tela_calculadora)
        if page.route == "/historico":
            page.views.append(montar_historico())
        page.update()  # envia a nova tela para a janela
    page.on_route_change = mudar_rota
    mudar_rota(None)
# Inicia a aplicação Flet e informa qual função deve construir a interface.
ft.run(main)