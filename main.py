import random
import telebot
import rtx_api_3_5 as rtx_api

# Constantes
BOT_TOKEN = '6480600722:AAF94PUwyNWwYhFva8mgPi7u5HM5sptcA8w'
PORT = 46640 # Convertido para inteiro

# Inicialização do bot
bot = telebot.TeleBot(BOT_TOKEN)

# Função para gerar cartas
def gerar_cartas():
    cartas = [
        "O Louco", "O Mago", "A Sacerdotisa", "A Imperatriz", "O Imperador",
        "O Hierofante", "Os Amantes", "A Carruagem", "A Justiça", "O Eremita",
        "A Roda da Fortuna", "A Força", "O Enforcado", "A Morte", "A Temperança",
        "O Diabo", "A Torre", "A Estrela", "A Lua", "O Sol", "O Julgamento", "O Mundo"
    ]
    return random.sample(cartas, 3)

# Função para ajustar resposta do RTX
def call_rtx_api(prompt):
    resposta_rtx = rtx_api.send_message(prompt, PORT)
    resposta_rtx = resposta_rtx.replace('<br>Reference files:<br>CartomanteTator_bot.txt', ' 🙏')
    return resposta_rtx

# Função para interpretar o tarot
def interpretar_tarot(message):
    sent = bot.reply_to(message, "🗯️ Por favor, digite a pergunta que você deseja fazer ao Tarot e espere eu fazer a leitura das cartas.")
    bot.register_next_step_handler(sent, processar_pergunta)

# Função para processar a pergunta do usuário
def processar_pergunta(message):
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
    sent_message = bot.send_message(message.chat.id, "🔮 Estou fazendo a leitura. Me dê uns segundinhos...")
    message_id = sent_message.message_id
    cartas_para_rtx = "\n".join(cartas_tiradas)
    prompt_rtx += cartas_para_rtx + "\n\n" + pergunta_usuario
    resposta_rtx = call_rtx_api(prompt_rtx)
    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text=resposta_rtx)

# Manipuladores de mensagens
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("Entender o funcionamento do bot")
    item2 = telebot.types.KeyboardButton("Aprender sobre Tarot")
    item3 = telebot.types.KeyboardButton("Realizar leitura de cartas")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "🧙‍♀️ Olá! Eu sou o CartomanteTarot_Bot.\n\nSelecione uma das opções abaixo para começar:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Realizar leitura de cartas":
        interpretar_tarot(message)
    elif message.text == "Entender o funcionamento do bot":
        bot.send_message(message.chat.id, "Eu sou um bot que utiliza a API do Chat-With-RTX-python-api para interpretar o Tarot. Você pode fazer uma pergunta e eu fornecerei uma leitura baseada nas cartas do Tarot.")
    elif message.text == "Aprender sobre Tarot":
        bot.send_message(message.chat.id, "O Tarot é um sistema de leitura de cartas que utiliza imagens e símbolos para fornecer insights e orientações sobre questões pessoais, profissionais e espirituais.")
    else:
        bot.send_message(message.chat.id, "Desculpe, não consegui entender sua escolha. Por favor, selecione uma das opções no menu.")

# Bot em looping
bot.polling()
