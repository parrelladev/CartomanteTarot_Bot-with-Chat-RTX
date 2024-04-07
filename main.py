import telebot
import random
import rtx_api_3_5 as rtx_api

# Telegram bot token
bot_token = '6480600722:AAF94PUwyNWwYhFva8mgPi7u5HM5sptcA8w'
bot = telebot.TeleBot(bot_token)

# Porta do seu servidor local para o Chat-With-RTX-python-api
port = "46640"

# Mensagem de boas-vindas
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Eu sou o CartomanteTarot_Bot. Por favor, digite a pergunta que você deseja fazer ao Tarot e espere eu fazer a leitura das cartas.")

# Função para gerar as cartas de tarot
def gerar_cartas():
    cartas = [
        "O Louco", "O Mago", "A Sacerdotisa", "A Imperatriz", "O Imperador",
        "O Hierofante", "Os Amantes", "A Carruagem", "A Justiça", "O Eremita",
        "A Roda da Fortuna", "A Força", "O Enforcado", "A Morte", "A Temperança",
        "O Diabo", "A Torre", "A Estrela", "A Lua", "O Sol", "O Julgamento", "O Mundo"
    ]
    return random.sample(cartas, 3)

# Função para chamar a API do Chat-With-RTX-python-api
def call_rtx_api(prompt):
    return rtx_api.send_message(prompt, port)

# Manipulador de mensagens para interpretar o Tarot
@bot.message_handler(func=lambda message: True)
def interpretar_tarot(message):
    pergunta_usuario = message.text
    cartas_tiradas = gerar_cartas()
    mensagem_cartas = "\n".join([f"{i+1}. {carta}" for i, carta in enumerate(cartas_tiradas)])
    resposta = (
        f"🧙‍♀️ Acabei de tirar do baralho algumas cartas aleatórias para você. Elas são:\n\n"
        f"{mensagem_cartas}\n\n"
    )
    bot.send_message(message.chat.id, resposta)

    prompt_rtx = (
        "A partir de agora, você assumirá o papel de um intérprete de tarô, fornecendo insights e orientações com base nas cartas apontadas a seguir.\n\nSua tarefa é ajudar o usuário a desvendar as mensagens simbólicas do tarô e aplicá-las à situação específica que o usuário irá compartilhar. Por favor, lembre-se de que as interpretações do tarô são subjetivas e destinam-se a promover a reflexão e o autoconhecimento.\n\nSeja respeitoso e sensível ao lidar com questões pessoais. Responda com um linguajar místico. A reposta deve ser curta, tendo somente 700 caracteres. Responda somente a interpretaçao. Responda em primeira pessoa. Responda em Português do Brasil!\n\n"
    )
    cartas_para_rtx = "\n".join(cartas_tiradas)
    prompt_rtx += cartas_para_rtx + "\n\n" + pergunta_usuario
    resposta_rtx = call_rtx_api(prompt_rtx)
    bot.send_message(message.chat.id, resposta_rtx)

# Iniciar o bot
bot.polling()