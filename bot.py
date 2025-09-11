from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import random
import datetime

# Dados simples
contagem = {}
pontos = {}
sorteios = {}

# Função básica
async def contar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user:
        user_id = update.effective_user.id
        nome = update.effective_user.first_name

        if user_id not in contagem:
            contagem[user_id] = {"nome": nome, "mensagens": 0}
            pontos[user_id] = 0

        contagem[user_id]["mensagens"] += 1
        pontos[user_id] += 1

# Comandos básicos
async def ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not contagem:
        await update.message.reply_text("Ainda não há mensagens!")
        return

    texto = "🏆 Ranking:\n\n"
    ordenado = sorted(contagem.values(), key=lambda x: x["mensagens"], reverse=True)

    for i, user in enumerate(ordenado[:5], start=1):
        texto += f"{i}. {user['nome']}: {user['mensagens']} msgs\n"

    await update.message.reply_text(texto)

async def perfil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    nome = update.effective_user.first_name
    
    msgs = contagem.get(user_id, {}).get("mensagens", 0)
    pts = pontos.get(user_id, 0)
    
    await update.message.reply_text(f"👤 {nome}\n💬 {msgs} mensagens\n🎯 {pts} pontos")

async def kenesis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """🚀 Kenesis - Future of Education

📱 Website: https://kenesis.io/
📖 Whitepaper: https://kenesis.gitbook.io/whitepaper/
📱 X: https://x.com/kenesis_io
📱 Instagram: https://www.instagram.com/kenesis.io

Knowledge is technological, decentralized and no tracking."""
    
    await update.message.reply_text(texto)

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """🤖 Comandos:

/top - Ranking
/perfil - Seu perfil  
/kenesis - Links Kenesis
/help - Esta ajuda"""
    
    await update.message.reply_text(texto)

def main():
    TOKEN = "8211453362:AAHnQJduTD4-UNYoeciAAJTTjK3yB6ZC5oM"
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, contar))
    app.add_handler(CommandHandler("top", ranking))
    app.add_handler(CommandHandler("perfil", perfil))
    app.add_handler(CommandHandler("kenesis", kenesis))
    app.add_handler(CommandHandler("help", ajuda))
    app.add_handler(CommandHandler("start", ajuda))

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()