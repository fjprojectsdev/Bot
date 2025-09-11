from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import random
import datetime

# Dicionários para armazenar dados
contagem = {}
sorteios = {}
eventos = {}

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

# Ajuda
async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """🤖 Comandos disponíveis:

📊 ESTATÍSTICAS:
/ranking - Ver ranking de mensagens

🎉 SORTEIOS:
/sorteio <prêmio> - Criar sorteio
/participar - Entrar no sorteio
/sortear - Escolher vencedor

📅 EVENTOS:
/evento <data> <descrição> - Criar evento
/eventos - Ver eventos programados

🎮 BRINCADEIRAS:
/dado - Rolar dado
/moeda - Cara ou coroa
/pergunta - Resposta aleatória

/ajuda - Ver esta mensagem"""
    
    await update.message.reply_text(texto)

# Inicialização do bot
def main():
    TOKEN = "8211453362:AAHnQJduTD4-UNYoeciAAJTTjK3yB6ZC5oM"
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, contar))
    app.add_handler(CommandHandler("ranking", ranking))
    app.add_handler(CommandHandler("sorteio", sorteio))
    app.add_handler(CommandHandler("participar", participar))
    app.add_handler(CommandHandler("sortear", sortear))
    app.add_handler(CommandHandler("evento", evento))
    app.add_handler(CommandHandler("eventos", eventos_lista))
    app.add_handler(CommandHandler("dado", dado))
    app.add_handler(CommandHandler("moeda", moeda))
    app.add_handler(CommandHandler("pergunta", pergunta))
    app.add_handler(CommandHandler("ajuda", ajuda))
    app.add_handler(CommandHandler("start", ajuda))

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()