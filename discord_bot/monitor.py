from http.client import HTTPSConnection  # Importa o módulo para conexão HTTPS
import sys  # Importa o módulo sys para manipulação de erros e saída padrão
import json  # Importa o módulo json para trabalhar com dados em formato JSON

def get_connection():
    """Estabelece uma conexão HTTPS com o Discord."""
    return HTTPSConnection("discordapp.com", 443)

def read_messages(conn, channel_id):
    """Lê e imprime mensagens, incluindo conteúdo embutido e horários, do canal Discord especificado."""
    try:
        conn.request("GET", f"/api/v6/channels/{channel_id}/messages", headers=headers)  # Faz a requisição GET para obter as mensagens do canal
        resp = conn.getresponse()  # Obtém a resposta da requisição

        if resp.status == 200:  # Verifica se a resposta foi bem-sucedida
            messages = json.loads(resp.read())  # Carrega as mensagens JSON da resposta
            for message in messages:  # Itera sobre cada mensagem
                content = message['content']  # Obtém o conteúdo da mensagem
                if 'embeds' in message:  # Verifica se a mensagem possui conteúdo embutido
                    embeds = message['embeds']  # Obtém os conteúdos embutidos
                    for embed in embeds:  # Itera sobre cada conteúdo embutido
                        if 'title' in embed:  # Verifica se o conteúdo embutido possui título
                            content += f"\nTítulo Embutido: {embed['title']}"  # Adiciona o título ao conteúdo
                        if 'description' in embed:  # Verifica se o conteúdo embutido possui descrição
                            content += f"\nDescrição Embutida: {embed['description']}"  # Adiciona a descrição ao conteúdo
                        # Adicione mais campos conforme necessário
                print(f"Mensagem: {content} - Horário: {message['timestamp']}\n{'=' * 50}")  # Imprime a mensagem e o horário

        else:
            sys.stderr.write(f"Recebido HTTP {resp.status}: {resp.reason}\n")  # Imprime um erro se a resposta não for bem-sucedida

    except Exception as e:
        sys.stderr.write(f"Falha ao ler as mensagens: {e}\n")  # Imprime um erro em caso de falha na leitura das mensagens

if __name__ == '__main__':
    # Carrega as informações do usuário do arquivo
    try:
        with open("info.txt", "r") as file:
            user_info = file.read().splitlines()  # Lê as linhas do arquivo e divide em uma lista
            user_agent = user_info[0]  # Obtém o agente do usuário
            token = user_info[1]  # Obtém o token do Discord
            channel_id = user_info[3]  # Obtém o ID do canal

        headers = {
            "content-type": "application/json",
            "user-agent": user_agent,
            "authorization": token,
            "host": "discordapp.com"
        }

        conn = get_connection()  # Estabelece uma conexão HTTPS com o Discord
        read_messages(conn, channel_id)  # Lê as mensagens do canal especificado

    except Exception as e:
        sys.stderr.write(f"Ocorreu um erro: {e}\n")  # Imprime um erro em caso de falha geral
