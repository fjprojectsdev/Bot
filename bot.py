from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import random
import datetime
import logging

# Configuração
ADMIN_IDS = [6670325989, 7645992176]  # @FlavioJhonatan, @RareG_14

# Log
logging.basicConfig(level=logging.INFO)

# Dados simples
contagem = {}
pontos = {}
sorteios = {}
badges = {}
check_ins = {}
historico_mensagens = {}

# Sistema de referrals
users = {}  # {username: {"referrals": int, "points": int}}

# Base de conhecimento Kenesis
kenesis_knowledge = {
    "kenesis": "Kenesis é uma plataforma Web3 que revoluciona a educação através de blockchain e IA. Criadores tokenizam conhecimento via NFT, aprendizes acessam conteúdo seguro em um marketplace transparente.",
    "web3": "Kenesis usa Web3 para criar um ecossistema educacional descentralizado, centrado no criador, com transparência e recompensas globais.",
    "nft": "Na Kenesis, criadores tokenizam seu conhecimento através de NFTs, criando um marketplace único de conteúdo educacional.",
    "blockchain": "Kenesis usa infraestrutura blockchain robusta com contratos inteligentes auditados e armazenamento descentralizado para máxima segurança.",
    "ia": "A plataforma integra assistentes impulsionados por IA que alimentam o marketplace de conhecimento da Kenesis.",
    "tokenomics": "Kenesis possui tokenomics abrangente com múltiplas fontes de receita, programa de afiliados e recompensas baseadas em tokens.",
    "roadmap": "O roadmap da Kenesis se estende até 2026 para estabelecer liderança global em educação descentralizada.",
    "segurança": "Kenesis implementa sistema de aprovação admin, auditorias de contratos inteligentes e medidas anti-golpes para máxima segurança.",
    "missão": "A missão da Kenesis é transformar educação e pesquisa criando um ecossistema Web3 descentralizado que prioriza criadores e permite compartilhamento global de conhecimento.",
    "marketplace": "O marketplace da Kenesis é alimentado por tokens, transparente e recompensador, conectando criadores e aprendizes globalmente.",
    "descentralizada": "Kenesis constrói um ecossistema de aprendizagem totalmente descentralizado onde o conhecimento é livre e acessível sem controle central.",
    "criadores": "Na Kenesis, criadores podem tokenizar seu conhecimento, receber recompensas justas e participar de um programa de afiliados lucrativo."
}

# Função básica
async def contar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user:
        user_id = update.effective_user.id
        nome = update.effective_user.first_name

        if user_id not in contagem:
            contagem[user_id] = {"nome": nome, "mensagens": 0}
            pontos[user_id] = 0
            badges[user_id] = []

        # Responder perguntas sobre Kenesis automaticamente (sempre)
        try:
            await responder_kenesis(update)
        except Exception as e:
            print(f"Erro na IA: {e}")
        
        # Verificar se é flood
        if verificar_flood(user_id, update.message.text):
            idioma = detectar_idioma(update.message.text)
            if idioma == 'pt':
                await update.message.reply_text("⚠️ Calma aí! Evite flood no grupo. 😅")
            else:
                await update.message.reply_text("⚠️ Slow down! Avoid flooding the group. 😅")
            return  # Não conta mensagem de flood
        
        contagem[user_id]["mensagens"] += 1
        pontos[user_id] += 1
        
        # Verificar badges automáticos
        await verificar_badges(update, user_id)

# Detectar idioma do usuário
def detectar_idioma(texto):
    palavras_pt = ['oi', 'olá', 'bom', 'dia', 'tarde', 'noite', 'obrigado', 'valeu', 'como', 'que', 'qual', 'onde', 'quando', 'por', 'que']
    palavras_en = ['hi', 'hello', 'good', 'morning', 'afternoon', 'evening', 'thanks', 'thank', 'how', 'what', 'where', 'when', 'why']
    
    texto_lower = texto.lower()
    pt_count = sum(1 for palavra in palavras_pt if palavra in texto_lower)
    en_count = sum(1 for palavra in palavras_en if palavra in texto_lower)
    
    return 'pt' if pt_count > en_count else 'en'

# Verificar se é flood (ajustado para 3 mensagens)
def verificar_flood(user_id, texto):
    agora = datetime.datetime.now()
    
    if user_id not in historico_mensagens:
        historico_mensagens[user_id] = []
    
    # Limpar mensagens antigas (últimos 1 minuto)
    historico_mensagens[user_id] = [
        timestamp for timestamp in historico_mensagens[user_id]
        if (agora - timestamp).total_seconds() < 60
    ]
    
    # Verificar flood: mais de 3 mensagens em 1 min
    if len(historico_mensagens[user_id]) >= 3:
        return True
    
    # Adicionar timestamp atual
    historico_mensagens[user_id].append(agora)
    return False

# Responder perguntas sobre Kenesis automaticamente
async def responder_kenesis(update: Update):
    texto = update.message.text.lower()
    idioma = detectar_idioma(texto)
    
    # Respostas sobre Kenesis
    if "kenesis" in texto and "?" in texto:
        if idioma == 'pt':
            await update.message.reply_text("🤖 Kenesis é uma plataforma Web3 que revoluciona a educação através de blockchain e IA. Criadores tokenizam conhecimento via NFT!")
        else:
            await update.message.reply_text("🤖 Kenesis is a Web3 platform that revolutionizes education through blockchain and AI. Creators tokenize knowledge via NFT!")
        return
    
    if "web3" in texto and "?" in texto:
        if idioma == 'pt':
            await update.message.reply_text("🤖 Kenesis usa Web3 para criar um ecossistema educacional descentralizado, centrado no criador, com transparência e recompensas globais.")
        else:
            await update.message.reply_text("🤖 Kenesis uses Web3 to create a decentralized educational ecosystem, creator-centered, with transparency and global rewards.")
        return
    
    if "missão" in texto or "mission" in texto and "?" in texto:
        if idioma == 'pt':
            await update.message.reply_text("🤖 A missão da Kenesis é transformar educação e pesquisa criando um ecossistema Web3 descentralizado que prioriza criadores.")
        else:
            await update.message.reply_text("🤖 Kenesis' mission is to transform education and research by creating a decentralized Web3 ecosystem that prioritizes creators.")
        return
    
    if "nft" in texto and "?" in texto:
        if idioma == 'pt':
            await update.message.reply_text("🤖 Na Kenesis, criadores tokenizam seu conhecimento através de NFTs, criando um marketplace único de conteúdo educacional.")
        else:
            await update.message.reply_text("🤖 In Kenesis, creators tokenize their knowledge through NFTs, creating a unique marketplace for educational content.")
        return
    
    # Saudações
    if any(word in texto for word in ["oi", "olá", "bom dia", "boa tarde", "boa noite", "hi", "hello", "good morning", "good afternoon", "good evening"]):
        if idioma == 'pt':
            saudacoes = ["Olá! 👋 Bem-vindo à Kenesis!", "Oi! 🚀 Pronto para o futuro da educação?", "E aí! 💡 Vamos aprender juntos?"]
        else:
            saudacoes = ["Hello! 👋 Welcome to Kenesis!", "Hi! 🚀 Ready for the future of education?", "Hey! 💡 Let's learn together?"]
        await update.message.reply_text(random.choice(saudacoes))
        return

# Comandos básicos
async def ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not contagem:
        await update.message.reply_text("📊 No messages yet!")
        return

    texto = "🏆 Messages Ranking:\n\n"
    ordenado = sorted(contagem.values(), key=lambda x: x["mensagens"], reverse=True)

    for i, user in enumerate(ordenado[:5], start=1):
        texto += f"{i}. {user['nome']}: {user['mensagens']} msgs\n"

    await update.message.reply_text(texto)

async def perfil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    nome = update.effective_user.first_name
    
    msgs = contagem.get(user_id, {}).get("mensagens", 0)
    pts = pontos.get(user_id, 0)
    user_badges = badges.get(user_id, [])
    
    # Calcular nível
    nivel = pts // 100 + 1
    proximo_nivel = (nivel * 100) - pts
    
    texto = f"👤 PROFILE OF {nome}\n\n"
    texto += f"⭐ Level: {nivel}\n"
    texto += f"🎯 Points: {pts}\n"
    texto += f"📈 To next level: {proximo_nivel} points\n"
    texto += f"💬 Messages: {msgs}\n\n"
    
    if user_badges:
        texto += "🏆 BADGES:\n"
        for badge in user_badges:
            texto += f"• {badge}\n"
    else:
        texto += "🏆 No badges yet\n"
    
    await update.message.reply_text(texto)

async def kenesis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """⌨️ Kenesis - Future of Education

Kenesis is just getting started… Follow us on social media and be part of the future of education.

📱 X: https://x.com/kenesis_io?s=21&t=iiRYsbGEbXUkxpvkzfIcDQ
📱 TikTok: https://www.tiktok.com/@kenesis_io?_t=ZM-8zZ5xi8KaWM&_r=1
📱 Threads: https://www.threads.com/@kenesis.io?igshid=NTc4MTIwNjQ2YQ==
💡 Medium: https://medium.com/@kenesisofficial
📱 Website: https://kenesis.io/
📱 YouTube: https://www.youtube.com/@kenesis_io
📱 LinkedIn: https://www.linkedin.com/company/kenesis-io/
📱 Telegram: https://t.me/KenesisOfficial
📱 Instagram: https://www.instagram.com/kenesis.io?igsh=NmRqdjNjZDR2c2g3&utm_source=qr
📖 Whitepaper: https://kenesis.gitbook.io/whitepaper/

🚀 Knowledge is no longer limited, it is technological, decentralized and no tracking."""
    
    await update.message.reply_text(texto)

# Verificar badges automáticos
async def verificar_badges(update, user_id):
    nome = contagem[user_id]["nome"]
    mensagens = contagem[user_id]["mensagens"]
    pts = pontos[user_id]
    user_badges = badges[user_id]
    
    # Badge de mensagens
    if mensagens >= 50 and "Active" not in user_badges:
        badges[user_id].append("Active")
        pontos[user_id] += 25
        await update.message.reply_text(f"🏆 {nome} earned the 'Active' badge (+25 points!)")
    
    if mensagens >= 100 and "Talkative" not in user_badges:
        badges[user_id].append("Talkative")
        pontos[user_id] += 50
        await update.message.reply_text(f"🏆 {nome} earned the 'Talkative' badge (+50 points!)")
    
    # Badge de pontos
    if pts >= 500 and "Veteran" not in user_badges:
        badges[user_id].append("Veteran")
        pontos[user_id] += 100
        await update.message.reply_text(f"🏆 {nome} earned the 'Veteran' badge (+100 points!)")

# Check-in diário
async def checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    nome = update.effective_user.first_name
    hoje = datetime.date.today().isoformat()
    
    if user_id not in check_ins:
        check_ins[user_id] = {}
    
    if hoje in check_ins[user_id]:
        await update.message.reply_text(f"✅ {nome}, you already checked in today!")
        return
    
    # Fazer check-in
    check_ins[user_id][hoje] = True
    pontos[user_id] = pontos.get(user_id, 0) + 10
    
    # Verificar sequência
    sequencia = calcular_sequencia(user_id)
    bonus = 0
    
    if sequencia >= 7:
        bonus = 50
        pontos[user_id] += bonus
    elif sequencia >= 3:
        bonus = 20
        pontos[user_id] += bonus
    
    texto = f"✅ Check-in completed, {nome}!\n+10 points"
    if bonus > 0:
        texto += f"\n🔥 {sequencia} days streak! +{bonus} bonus points!"
    
    await update.message.reply_text(texto)

def calcular_sequencia(user_id):
    if user_id not in check_ins:
        return 0
    
    sequencia = 0
    data_atual = datetime.date.today()
    
    while True:
        data_str = data_atual.isoformat()
        if data_str in check_ins[user_id]:
            sequencia += 1
            data_atual -= datetime.timedelta(days=1)
        else:
            break
    
    return sequencia

# Ranking de pontos
async def rank_pontos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not pontos:
        await update.message.reply_text("📊 No points registered yet!")
        return
    
    # Ordenar por pontos
    ranking_texto = "🏆 POINTS RANKING:\n\n"
    ordenado = sorted(pontos.items(), key=lambda x: x[1], reverse=True)
    
    for i, (user_id, pts) in enumerate(ordenado[:10], start=1):
        nome = contagem.get(user_id, {}).get("nome", "User")
        nivel = pts // 100 + 1
        ranking_texto += f"{i}. {nome}: {pts} pts (Lv.{nivel})\n"
    
    await update.message.reply_text(ranking_texto)

# Funções auxiliares
def is_admin(user_id):
    return user_id in ADMIN_IDS

# Add referrals (admin)
async def add_referrals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Only admin can use this command.")
        return
    
    try:
        username = context.args[0]
        amount = int(context.args[1])
        
        if username not in users:
            users[username] = {"referrals": 0, "points": 0}
        
        users[username]["referrals"] += amount
        await update.message.reply_text(f"✅ Added {amount} referrals to {username}.")
    except:
        await update.message.reply_text("⚠️ Usage: /addrefs @username amount")

# Remove referrals (admin)
async def remove_referrals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Only admin can use this command.")
        return
    
    try:
        username = context.args[0]
        amount = int(context.args[1])
        
        if username not in users:
            users[username] = {"referrals": 0, "points": 0}
        
        users[username]["referrals"] = max(0, users[username]["referrals"] - amount)
        await update.message.reply_text(f"✅ Removed {amount} referrals from {username}.")
    except:
        await update.message.reply_text("⚠️ Usage: /removerefs @username amount")

# Add points (admin)
async def add_points_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Only admin can use this command.")
        return
    
    try:
        username = context.args[0]
        amount = int(context.args[1])
        
        if username not in users:
            users[username] = {"referrals": 0, "points": 0}
        
        users[username]["points"] += amount
        await update.message.reply_text(f"✅ Added {amount} points to {username}.")
    except:
        await update.message.reply_text("⚠️ Usage: /addpoints @username amount")

# General ranking
async def ranking_geral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not users:
        await update.message.reply_text("📊 No data yet.")
        return
    
    sorted_users = sorted(users.items(), key=lambda x: (x[1]['points'] + x[1]['referrals']), reverse=True)
    
    msg = "🏆 TOP MEMBERS:\n\n"
    for i, (username, data) in enumerate(sorted_users[:10], start=1):
        score = data['points'] + data['referrals']
        msg += f"{i}. {username} — {score} pts\n"
        msg += f"   Referrals: {data['referrals']} | Points: {data['points']}\n\n"
    
    await update.message.reply_text(msg)

# Referrals ranking
async def referrals_ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not users:
        await update.message.reply_text("📊 No referral data yet.")
        return
    
    sorted_users = sorted(users.items(), key=lambda x: x[1]['referrals'], reverse=True)
    
    msg = "🔗 REFERRALS RANKING:\n\n"
    for i, (username, data) in enumerate(sorted_users[:10], start=1):
        if data['referrals'] > 0:
            msg += f"{i}. {username} — {data['referrals']} referrals\n"
    
    if msg == "🔗 REFERRALS RANKING:\n\n":
        msg += "No referrals yet."
    
    await update.message.reply_text(msg)

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """🤖 AVAILABLE COMMANDS:

🎮 GAMIFICATION:
/profile - Your profile and badges
/checkin - Daily check-in (+10 pts)
/points - Points ranking

📊 STATISTICS:
/messages - Messages ranking
/ranking - Complete ranking
/refsrank - Referrals ranking

🚀 KENESIS:
/kenesis - Social media links

🤖 AI ACTIVE:
- Ask "What is Kenesis?"
- Ask "How does Web3 work?"
- Ask "What's the mission?"
- Say "Hi" for greeting

🛠️ ADMIN:
/addrefs @user amount
/removerefs @user amount
/addpoints @user amount

/help - View commands"""
    
    await update.message.reply_text(texto)

def main():
    TOKEN = "8211453362:AAHnQJduTD4-UNYoeciAAJTTjK3yB6ZC5oM"
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, contar))
    
    # Commands in English
    app.add_handler(CommandHandler("messages", ranking))
    app.add_handler(CommandHandler("profile", perfil))
    app.add_handler(CommandHandler("checkin", checkin))
    app.add_handler(CommandHandler("points", rank_pontos))
    app.add_handler(CommandHandler("kenesis", kenesis))
    app.add_handler(CommandHandler("help", ajuda))
    app.add_handler(CommandHandler("start", ajuda))
    
    # Referral system
    app.add_handler(CommandHandler("addrefs", add_referrals))
    app.add_handler(CommandHandler("removerefs", remove_referrals))
    app.add_handler(CommandHandler("addpoints", add_points_admin))
    app.add_handler(CommandHandler("ranking", ranking_geral))
    app.add_handler(CommandHandler("refsrank", referrals_ranking))

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()