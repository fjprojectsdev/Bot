from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import random
import datetime

# Dicionários para armazenar dados
contagem = {}
sorteios = {}
eventos = {}
enquetes = {}
frases = {}
lembretes = {}
jogos_ativo = {}

# Função chamada a cada mensagem
async def contar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user:
        user_id = update.effective_user.id
        nome = update.effective_user.first_name

        if user_id not in contagem:
            contagem[user_id] = {"nome": nome, "mensagens": 0}

        contagem[user_id]["mensagens"] += 1

# Comando para ver ranking
async def ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not contagem:
        await update.message.reply_text("Ainda não há mensagens contadas!")
        return

    ranking_texto = "🏆 Ranking de mensagens:\n\n"
    ordenado = sorted(contagem.values(), key=lambda x: x["mensagens"], reverse=True)

    for i, user in enumerate(ordenado, start=1):
        ranking_texto += f"{i}. {user['nome']}: {user['mensagens']} mensagens\n"

    await update.message.reply_text(ranking_texto)

# Sorteio
async def sorteio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /sorteio <prêmio>\nExemplo: /sorteio Pizza")
        return
    
    premio = " ".join(context.args)
    chat_id = update.effective_chat.id
    sorteios[chat_id] = {"premio": premio, "participantes": [], "criador": update.effective_user.first_name}
    
    await update.message.reply_text(f"🎉 Sorteio criado: {premio}\n\nPara participar, digite /participar")

# Participar do sorteio
async def participar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    nome = update.effective_user.first_name
    
    if chat_id not in sorteios:
        await update.message.reply_text("Não há sorteio ativo!")
        return
    
    if user_id in sorteios[chat_id]["participantes"]:
        await update.message.reply_text("Você já está participando!")
        return
    
    sorteios[chat_id]["participantes"].append({"id": user_id, "nome": nome})
    total = len(sorteios[chat_id]["participantes"])
    await update.message.reply_text(f"✅ {nome} entrou no sorteio! ({total} participantes)")

# Sortear vencedor
async def sortear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    if chat_id not in sorteios or not sorteios[chat_id]["participantes"]:
        await update.message.reply_text("Não há sorteio ativo ou participantes!")
        return
    
    vencedor = random.choice(sorteios[chat_id]["participantes"])
    premio = sorteios[chat_id]["premio"]
    
    await update.message.reply_text(f"🎊 PARABÉNS {vencedor['nome']}!\n\nVocê ganhou: {premio}")
    del sorteios[chat_id]

# Criar evento
async def evento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Use: /evento <data> <descrição>\nExemplo: /evento 15/12 Festa de Natal")
        return
    
    data = context.args[0]
    descricao = " ".join(context.args[1:])
    chat_id = update.effective_chat.id
    
    if chat_id not in eventos:
        eventos[chat_id] = []
    
    eventos[chat_id].append({"data": data, "descricao": descricao})
    await update.message.reply_text(f"📅 Evento criado:\n{data} - {descricao}")

# Ver eventos
async def eventos_lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    if chat_id not in eventos or not eventos[chat_id]:
        await update.message.reply_text("Não há eventos programados!")
        return
    
    texto = "📅 Eventos programados:\n\n"
    for evento in eventos[chat_id]:
        texto += f"• {evento['data']} - {evento['descricao']}\n"
    
    await update.message.reply_text(texto)

# Brincadeiras
async def dado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resultado = random.randint(1, 6)
    await update.message.reply_text(f"🎲 {update.effective_user.first_name} rolou: {resultado}")

async def moeda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resultado = random.choice(["Cara", "Coroa"])
    await update.message.reply_text(f"🪙 {resultado}!")

async def pergunta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respostas = ["Sim", "Não", "Talvez", "Com certeza", "Jamais", "Provavelmente", "Impossível"]
    resposta = random.choice(respostas)
    await update.message.reply_text(f"🔮 {resposta}")

# Enquetes
async def enquete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("Use: /poll <pergunta> <opção1> <opção2> [opção3...]\nExemplo: /poll 'Pizza favorita?' Calabresa Margherita Portuguesa")
        return
    
    pergunta = context.args[0]
    opcoes = context.args[1:]
    chat_id = update.effective_chat.id
    
    enquetes[chat_id] = {"pergunta": pergunta, "opcoes": opcoes, "votos": {i: [] for i in range(len(opcoes))}}
    
    texto = f"📊 ENQUETE: {pergunta}\n\n"
    for i, opcao in enumerate(opcoes):
        texto += f"{i+1}. {opcao}\n"
    texto += "\nVote com /voto <número>"
    
    await update.message.reply_text(texto)

async def votar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Use: /voto <número>")
        return
    
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    nome = update.effective_user.first_name
    opcao = int(context.args[0]) - 1
    
    if chat_id not in enquetes:
        await update.message.reply_text("Não há enquete ativa!")
        return
    
    if opcao < 0 or opcao >= len(enquetes[chat_id]["opcoes"]):
        await update.message.reply_text("Opção inválida!")
        return
    
    # Remove voto anterior
    for votos in enquetes[chat_id]["votos"].values():
        if user_id in votos:
            votos.remove(user_id)
    
    enquetes[chat_id]["votos"][opcao].append(user_id)
    await update.message.reply_text(f"✅ {nome} votou em: {enquetes[chat_id]['opcoes'][opcao]}")

async def resultado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    if chat_id not in enquetes:
        await update.message.reply_text("Não há enquete ativa!")
        return
    
    enquete_data = enquetes[chat_id]
    texto = f"📊 RESULTADO: {enquete_data['pergunta']}\n\n"
    
    for i, opcao in enumerate(enquete_data['opcoes']):
        votos = len(enquete_data['votos'][i])
        texto += f"{i+1}. {opcao}: {votos} votos\n"
    
    await update.message.reply_text(texto)

# Frases motivacionais
async def frase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    frases_lista = [
        "Acredite em você mesmo! 💪",
        "Cada dia é uma nova oportunidade! 🌅",
        "O sucesso é a soma de pequenos esforços! ⭐",
        "Seja a mudança que você quer ver no mundo! 🌍",
        "Grandes coisas começam com pequenos passos! 👣",
        "Você é mais forte do que imagina! 💎",
        "O impossível é só uma opinião! 🚀"
    ]
    frase_escolhida = random.choice(frases_lista)
    await update.message.reply_text(f"✨ {frase_escolhida}")

# Lembrete
async def lembrete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Use: /aviso <minutos> <mensagem>\nExemplo: /aviso 30 Reunião às 15h")
        return
    
    try:
        minutos = int(context.args[0])
        mensagem = " ".join(context.args[1:])
        
        if minutos > 1440:  # Max 24h
            await update.message.reply_text("Máximo 1440 minutos (24h)!")
            return
        
        context.job_queue.run_once(
            lambda context: context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"⏰ LEMBRETE: {mensagem}"
            ),
            minutos * 60
        )
        
        await update.message.reply_text(f"⏰ Lembrete criado para {minutos} minutos!")
    except ValueError:
        await update.message.reply_text("Tempo deve ser um número!")

# Jogo da adivinhação
async def adivinhar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    numero = random.randint(1, 100)
    jogos_ativo[chat_id] = {"numero": numero, "tentativas": 0}
    
    await update.message.reply_text("🎯 Jogo da Adivinhação!\n\nPensei em um número de 1 a 100.\nUse /num <número> para adivinhar!")

async def tentar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Use: /num <número>")
        return
    
    chat_id = update.effective_chat.id
    
    if chat_id not in jogos_ativo:
        await update.message.reply_text("Nenhum jogo ativo! Use /jogo para começar.")
        return
    
    tentativa = int(context.args[0])
    numero_secreto = jogos_ativo[chat_id]["numero"]
    jogos_ativo[chat_id]["tentativas"] += 1
    tentativas = jogos_ativo[chat_id]["tentativas"]
    nome = update.effective_user.first_name
    
    if tentativa == numero_secreto:
        await update.message.reply_text(f"🎉 PARABÉNS {nome}!\nVocê acertou o número {numero_secreto} em {tentativas} tentativas!")
        del jogos_ativo[chat_id]
    elif tentativa < numero_secreto:
        await update.message.reply_text(f"📈 {nome}, o número é MAIOR que {tentativa}! (Tentativa {tentativas})")
    else:
        await update.message.reply_text(f"📉 {nome}, o número é MENOR que {tentativa}! (Tentativa {tentativas})")

# Escolher pessoa aleatória
async def escolher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not contagem:
        await update.message.reply_text("Nenhum membro ativo encontrado!")
        return
    
    pessoa = random.choice(list(contagem.values()))
    await update.message.reply_text(f"🎯 Escolhido: {pessoa['nome']}!")

# Piada
async def piada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    piadas = [
        "Por que os pássaros voam para o sul no inverno? Porque é longe demais para ir andando! 😂",
        "O que o pato disse para a pata? Vem quá! 🦆",
        "Por que o livro de matemática estava triste? Porque tinha muitos problemas! 📚",
        "O que a impressora falou para a outra impressora? Essa folha é sua ou é impressão minha? 🖨️",
        "Por que o café foi à polícia? Porque foi coado! ☕"
    ]
    piada_escolhida = random.choice(piadas)
    await update.message.reply_text(piada_escolhida)

# Calcular idade
async def idade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 3:
        await update.message.reply_text("Use: /calc <dia> <mês> <ano>\nExemplo: /calc 15 03 1990")
        return
    
    try:
        dia, mes, ano = map(int, context.args)
        nascimento = datetime.date(ano, mes, dia)
        hoje = datetime.date.today()
        idade_anos = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        
        await update.message.reply_text(f"🎂 Você tem {idade_anos} anos!")
    except ValueError:
        await update.message.reply_text("Data inválida!")

# Ajuda atualizada
async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """🤖 COMANDOS DISPONÍVEIS:

📊 ESTATÍSTICAS:
/top - Ranking de mensagens

🎉 SORTEIOS:
/sorteio <prêmio> - Criar sorteio
/entrar - Entrar no sorteio
/sortear - Escolher vencedor

📅 EVENTOS:
/evento <data> <descrição> - Criar evento
/agenda - Ver eventos

📊 ENQUETES:
/poll <pergunta> <op1> <op2> - Criar enquete
/voto <número> - Votar
/resultado - Ver resultado

🎮 JOGOS:
/dado - Rolar dado
/moeda - Cara ou coroa
/jogo - Jogo de adivinhação
/num <número> - Tentar adivinhar

🎯 UTILIDADES:
/random - Escolher pessoa aleatória
/frase - Frase motivacional
/piada - Piada aleatória
/calc <dia> <mês> <ano> - Calcular idade
/aviso <min> <msg> - Criar lembrete
/magic - Resposta mágica

/help - Ver comandos"""
    
    await update.message.reply_text(texto)

# Inicialização do bot
def main():
    TOKEN = "8211453362:AAHnQJduTD4-UNYoeciAAJTTjK3yB6ZC5oM"
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, contar))
    # Comandos principais
    app.add_handler(CommandHandler("top", ranking))
    app.add_handler(CommandHandler("ranking", ranking))  # Mantém o antigo
    
    # Sorteios
    app.add_handler(CommandHandler("sorteio", sorteio))
    app.add_handler(CommandHandler("entrar", participar))
    app.add_handler(CommandHandler("participar", participar))  # Mantém o antigo
    app.add_handler(CommandHandler("sortear", sortear))
    
    # Eventos
    app.add_handler(CommandHandler("evento", evento))
    app.add_handler(CommandHandler("agenda", eventos_lista))
    app.add_handler(CommandHandler("eventos", eventos_lista))  # Mantém o antigo
    
    # Enquetes
    app.add_handler(CommandHandler("poll", enquete))
    app.add_handler(CommandHandler("enquete", enquete))  # Mantém o antigo
    app.add_handler(CommandHandler("voto", votar))
    app.add_handler(CommandHandler("votar", votar))  # Mantém o antigo
    app.add_handler(CommandHandler("resultado", resultado))
    
    # Jogos
    app.add_handler(CommandHandler("dado", dado))
    app.add_handler(CommandHandler("moeda", moeda))
    app.add_handler(CommandHandler("jogo", adivinhar))
    app.add_handler(CommandHandler("adivinhar", adivinhar))  # Mantém o antigo
    app.add_handler(CommandHandler("num", tentar))
    app.add_handler(CommandHandler("tentar", tentar))  # Mantém o antigo
    
    # Utilidades
    app.add_handler(CommandHandler("random", escolher))
    app.add_handler(CommandHandler("escolher", escolher))  # Mantém o antigo
    app.add_handler(CommandHandler("frase", frase))
    app.add_handler(CommandHandler("piada", piada))
    app.add_handler(CommandHandler("calc", idade))
    app.add_handler(CommandHandler("idade", idade))  # Mantém o antigo
    app.add_handler(CommandHandler("aviso", lembrete))
    app.add_handler(CommandHandler("lembrete", lembrete))  # Mantém o antigo
    app.add_handler(CommandHandler("magic", pergunta))
    app.add_handler(CommandHandler("pergunta", pergunta))  # Mantém o antigo
    
    # Ajuda
    app.add_handler(CommandHandler("help", ajuda))
    app.add_handler(CommandHandler("ajuda", ajuda))  # Mantém o antigo
    app.add_handler(CommandHandler("start", ajuda))

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()