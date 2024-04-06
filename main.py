import dash
import bcrypt
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_bootstrap_components as dbc
from pymongo import MongoClient
import os


# Conectar ao MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['trainview']
usuarios_collection = db['users']

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
from app import app

# Caminho para o arquivo index.py
INDEX_FILE = os.path.join(os.getcwd(), 'index.py')

# Criar modal de login
login_modal = dbc.Modal(
    [
        dbc.ModalHeader("Login"),
        dbc.ModalBody(
            [
                dcc.Input(id='username', type='text', className='form-control', placeholder='Digite seu nome de usuário', style={'color': '#000'}),
                dcc.Input(id='password', type='password', className='form-control', placeholder='Digite sua senha', style={'color': '#000'}),
            ]
        ),
        dbc.ModalFooter(
            [
                dbc.Button('Entrar', id='login-button', color='primary', size='sm', className='w-100'),
                dbc.Button("Fechar", id="close-login", className="ml-auto", color="danger"),
            ]
        ),
    ],
    id="login-modal",
    size="sm",
)

# Criar modal de registro
signup_modal = dbc.Modal(
    [
        dbc.ModalHeader("Registrar"),
        dbc.ModalBody(
            [
                dcc.Input(id='new-username', type='text', className='form-control', placeholder='Digite seu novo nome de usuário', style={'color': '#000'}),
                dcc.Input(id='email', type='email', className='form-control', placeholder='Digite seu email', style={'color': '#000'}),
                dcc.Input(id='new-password', type='password', className='form-control', placeholder='Digite sua nova senha', style={'color': '#000'}),
                dcc.Input(id='confirm-password', type='password', className='form-control', placeholder='Confirme sua nova senha', style={'color': '#000'}),
            ]
        ),
        dbc.ModalFooter(
            [
                dbc.Button('Registrar', id='signup-button', color='secondary', size='sm', className='w-100'),
                dbc.Button("Fechar", id="close-signup", className="ml-auto", color="danger"),
            ]
        ),
    ],
    id="signup-modal",
    size="sm",
)

app.layout = html.Div([
    html.Div(id='dummy', style={'display': 'none'}),  # Elemento de gatilho para abrir o modal de login ao carregar a página
    dbc.Container(
        className='mt-5',
        fluid=True,
        children=[
            dbc.Row(
                className='justify-content-between align-items-center',  # Alinhar os elementos horizontalmente e centralizar verticalmente
                children=[
                    dbc.Col(
                        html.Div(
                            children=[
                                html.Img(id="logo", src=app.get_asset_url("bg_aeria.png"), height=50,
                                style={"margin-bottom": "20px"}),
                                html.H2("TrainView", style={"font-weight": "bold", "font-size": "32px", "marginLeft": "20px", "display": "inline", "color": "#007bff"}),  # Cor azul para o texto do cabeçalho
                            ]
                        ),
                        className='my-2'
                    ),
                    dbc.Col(
                        dbc.Button('Login', id='login-toggle', color='primary', size='sm', className='w-100'),
                        width=1,
                        className='mx-2',
                    ),
                    dbc.Col(
                        dbc.Button('Registrar', id='signup-toggle', color='secondary', size='sm', className='w-100'),
                        width=1,
                        className='mx-2',
                    ),
                ]
            ),
            dbc.Row(
                className='justify-content-center',
                children=[
                    dbc.Col(
                        html.H1('Sistema de Análise de Imagens de Treinos Esportivos', className='display-4'),  # Cor azul para o cabeçalho principal
                        className='text-center',
                    ),
                ]
            ),
            dbc.Row(
                className='justify-content-center',
                children=[
                    dbc.Col(
                        html.H2('Analise e aperfeiçoe seus treinos esportivos!', style={"color": "#6c757d"}),  # Cor cinza para o texto de destaque
                        className='text-center',
                    ),
                ]
            ),
            dbc.Row(
                className='justify-content-center',
                children=[
                    dbc.Col(
                        html.Hr(className='my-2'),
                        className='text-center',
                    ),
                ]
            ),
            dbc.Row(
                className='justify-content-center',
                children=[
                    dbc.Col(
                        html.P('Início rápido:'),
                        className='text-center',
                    ),
                ]
            ),
        ]
    ),
    html.Div(id='output-message', children=[]),
    login_modal,
    signup_modal
])

# Callback para alternar o modal de login
@app.callback(
    Output('login-modal', 'is_open'),
    [Input("login-toggle", "n_clicks"), Input("close-login", "n_clicks")],
    [State("login-modal", "is_open")]
)
def toggle_login_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Callback para alternar o modal de registro
@app.callback(
    Output("signup-modal", "is_open"),
    [Input("signup-toggle", "n_clicks"), Input("close-signup", "n_clicks")],
    [State("signup-modal", "is_open")],
)
def toggle_signup_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('output-message', 'children'),
    [Input('login-button', 'n_clicks'), Input('signup-button', 'n_clicks')],
    [State('username', 'value'), State('password', 'value'), State('new-username', 'value'), State('email', 'value'), State('new-password', 'value'), State('confirm-password', 'value')]
)
def process_login_and_signup(login_clicks, signup_clicks, username, password, new_username, email, new_password, confirm_password):
    if login_clicks:
        if username and password:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = usuarios_collection.find_one({'username': username})
            if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
                return 'Login bem-sucedido!'
            else:
                return 'Credenciais inválidas. Tente novamente.'
    elif signup_clicks:
        if new_username and email and new_password and new_password == confirm_password:
            hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            # Verificar se o usuário já existe
            existing_user = usuarios_collection.find_one({'username': new_username})
            if existing_user:
                return html.Div('Nome de usuário já existe. Escolha outro.', className='alert alert-danger')
            else:
                # Inserir novo usuário no banco de dados
                usuarios_collection.insert_one({'username': new_username, 'email': email, 'password': hashed_password})
                return html.Div('Registro bem-sucedido!', className='alert alert-success')
        else:
            return html.Div('Por favor, preencha todos os campos corretamente.', className='alert alert-danger')
    else:
        return dash.no_update

# Callback para redirecionar para index.py após o login
@app.callback(
    Output('dummy', 'children'),
    [Input('login-button', 'n_clicks')],
    [State('username', 'value'), State('password', 'value')]
)
def redirect_to_index(n_clicks, username, password):
    if n_clicks:
        if username and password:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = usuarios_collection.find_one({'username': username})
            if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
                os.system(f"python {INDEX_FILE}")
    return ''

if __name__ == '__main__':
    app.run_server(debug=True)
