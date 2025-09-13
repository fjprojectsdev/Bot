from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import random
import datetime
import logging

# Configuração
ADMIN_ID = 6670325989  # @FlavioJhonatan

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
            await update.message.reply_text("⚠️ Calma aí! Evite flood no grupo. 😅")
            return  # Não conta mensagem de flood
        
        contagem[user_id]["mensagens"] += 1
        pontos[user_id] += 1
        
        # Verificar badges automáticos
        await verificar_badges(update, user_id)

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
    user_badges = badges.get(user_id, [])
    
    # Calcular nível
    nivel = pts // 100 + 1
    proximo_nivel = (nivel * 100) - pts
    
    texto = f"👤 PERFIL DE {nome}\n\n"
    texto += f"⭐ Nível: {nivel}\n"
    texto += f"🎯 Pontos: {pts}\n"
    texto += f"📈 Para próximo nível: {proximo_nivel} pontos\n"
    texto += f"💬 Mensagens: {msgs}\n\n"
    
    if user_badges:
        texto += "🏆 BADGES:\n"
        for badge in user_badges:
            texto += f"• {badge}\n"
    else:
        texto += "🏆 Nenhum badge ainda\n"
    
    await update.message.reply_text(texto)

# Verificar se é flood
def verificar_flood(user_id, texto):
    agora = datetime.datetime.now()
    
    if user_id not in historico_mensagens:
        historico_mensagens[user_id] = []
    
    # Limpar mensagens antigas (últimos 2 minutos)
    historico_mensagens[user_id] = [
        timestamp for timestamp in historico_mensagens[user_id]
        if (agora - timestamp).total_seconds() < 120
    ]
    
    # Verificar flood: mais de 5 mensagens em 2 min OU mensagem muito curta
    if len(historico_mensagens[user_id]) >= 5:
        return True
    
    if len(texto) < 10:  # Mensagem muito curta
        return True
    
    # Adicionar timestamp atual
    historico_mensagens[user_id].append(agora)
    return False

# Responder perguntas sobre Kenesis automaticamente
async def responder_kenesis(update: Update):
    texto = update.message.text.lower()
    
    # Respostas diretas
    if "kenesis" in texto and "?" in texto:
        await update.message.reply_text("🤖 Kenesis é uma plataforma Web3 que revoluciona a educação através de blockchain e IA. Criadores tokenizam conhecimento via NFT!")
        return
    
    if "web3" in texto and "?" in texto:
        await update.message.reply_text("🤖 Kenesis usa Web3 para criar um ecossistema educacional descentralizado, centrado no criador, com transparência e recompensas globais.")
        return
    
    if "missão" in texto and "?" in texto:
        await update.message.reply_text("🤖 A missão da Kenesis é transformar educação e pesquisa criando um ecossistema Web3 descentralizado que prioriza criadores.")
        return
    
    if "nft" in texto and "?" in texto:
        await update.message.reply_text("🤖 Na Kenesis, criadores tokenizam seu conhecimento através de NFTs, criando um marketplace único de conteúdo educacional.")
        return
    
    # Saudações
    if any(word in texto for word in ["oi", "olá", "bom dia", "boa tarde", "boa noite"]):
        saudacoes = ["Olá! 👋 Bem-vindo à Kenesis!", "Oi! 🚀 Pronto para o futuro da educação?", "E aí! 💡 Vamos aprender juntos?"]
        await update.message.reply_text(random.choice(saudacoes))
        return

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
    if mensagens >= 50 and "Ativo" not in user_badges:
        badges[user_id].append("Ativo")
        pontos[user_id] += 25
        await update.message.reply_text(f"🏆 {nome} ganhou o badge 'Ativo' (+25 pontos!)")
    
    if mensagens >= 100 and "Tagarela" not in user_badges:
        badges[user_id].append("Tagarela")
        pontos[user_id] += 50
        await update.message.reply_text(f"🏆 {nome} ganhou o badge 'Tagarela' (+50 pontos!)")
    
    # Badge de pontos
    if pts >= 500 and "Veterano" not in user_badges:
        badges[user_id].append("Veterano")
        pontos[user_id] += 100
        await update.message.reply_text(f"🏆 {nome} ganhou o badge 'Veterano' (+100 pontos!)")

# Check-in diário
async def checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    nome = update.effective_user.first_name
    hoje = datetime.date.today().isoformat()
    
    if user_id not in check_ins:
        check_ins[user_id] = {}
    
    if hoje in check_ins[user_id]:
        await update.message.reply_text(f"✅ {nome}, você já fez check-in hoje!")
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
    
    texto = f"✅ Check-in realizado, {nome}!\n+10 pontos"
    if bonus > 0:
        texto += f"\n🔥 Sequência de {sequencia} dias! +{bonus} pontos bônus!"
    
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
        await update.message.reply_text("Ainda não há pontos registrados!")
        return
    
    # Ordenar por pontos
    ranking_texto = "🏆 RANKING DE PONTOS:\n\n"
    ordenado = sorted(pontos.items(), key=lambda x: x[1], reverse=True)
    
    for i, (user_id, pts) in enumerate(ordenado[:10], start=1):
        nome = contagem.get(user_id, {}).get("nome", "Usuário")
        nivel = pts // 100 + 1
        ranking_texto += f"{i}. {nome}: {pts} pts (Nv.{nivel})\n"
    
    await update.message.reply_text(ranking_texto)

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """🤖 COMANDOS DISPONÍVEIS:

🎮 GAMIFICAÇÃO:
/perfil - Seu perfil e badges
/checkin - Check-in diário (+10 pts)
/rank - Ranking de pontos

📊 ESTATÍSTICAS:
/top - Ranking de mensagens
/ranking_geral - Ranking completo

🚀 KENESIS:
/kenesis - Links das redes sociais

🤖 IA ATIVA:
- Pergunte "O que é Kenesis?"
- Pergunte "Como funciona Web3?"
- Pergunte "Qual a missão?"
- Diga "Oi" para saudação

🛠️ ADMIN:
/add_referrals @user qtd
/add_points @user qtd
/reset_month
/announce_prizes

/help - Ver comandos"""
    
    await update.message.reply_text(texto)

# Funções auxiliares
def is_admin(user_id):
    return user_id == ADMIN_ID

# Adicionar referrals (admin)
async def add_referrals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Apenas admin pode usar este comando.")
        return
    
    try:
        username = context.args[0]
        amount = int(context.args[1])
        
        if username not in users:
            users[username] = {"referrals": 0, "points": 0}
        
        users[username]["referrals"] += amount
        await update.message.reply_text(f"✅ Adicionado {amount} referrals para {username}.")
    except:
        await update.message.reply_text("⚠️ Uso: /add_referrals @username quantidade")

# Adicionar pontos (admin)
async def add_points_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Apenas admin pode usar este comando.")
        return
    
    try:
        username = context.args[0]
        amount = int(context.args[1])
        
        if username not in users:
            users[username] = {"referrals": 0, "points": 0}
        
        users[username]["points"] += amount
        await update.message.reply_text(f"✅ Adicionado {amount} pontos para {username}.")
    except:
        await update.message.reply_text("⚠️ Uso: /add_points @username quantidade")

# Ranking geral
async def ranking_geral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not users:
        await update.message.reply_text("📊 Ainda não há dados.")
        return
    
    sorted_users = sorted(users.items(), key=lambda x: (x[1]['points'] + x[1]['referrals']), reverse=True)
    
    msg = "🏆 TOP MEMBROS:\n\n"
    for i, (username, data) in enumerate(sorted_users[:10], start=1):
        score = data['points'] + data['referrals']
        msg += f"{i}. {username} — {score} pts\n"
        msg += f"   Referrals: {data['referrals']} | Pontos: {data['points']}\n\n"
    
    await update.message.reply_text(msg)

# Reset mensal (admin)
async def reset_month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Apenas admin pode resetar.")
        return
    
    users.clear()
    await update.message.reply_text("♻️ Scores mensais resetados.")

# Anunciar prêmios (admin)
async def announce_prizes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Apenas admin pode anunciar.")
        return
    
    msg = (
        "🎉 DISTRIBUIÇÃO DE PRÊMIOS:\n\n"
        "🥇 Top 1: $500\n"
        "🥈 Top 2: $300\n"
        "🥉 Top 3: $200\n"
        "🏆 Top 4-10: $50 cada\n\n"
        "📊 Use /ranking_geral para ver posições!"
    )
    
    await update.message.reply_text(msg)

def main():
    TOKEN = "8211453362:AAHnQJduTD4-UNYoeciAAJTTjK3yB6ZC5oM"
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, contar))
    app.add_handler(CommandHandler("top", ranking))
    app.add_handler(CommandHandler("perfil", perfil))
    app.add_handler(CommandHandler("checkin", checkin))
    app.add_handler(CommandHandler("rank", rank_pontos))
    app.add_handler(CommandHandler("kenesis", kenesis))
    app.add_handler(CommandHandler("help", ajuda))
    app.add_handler(CommandHandler("start", ajuda))
    
    # Sistema de referrals
    app.add_handler(CommandHandler("add_referrals", add_referrals))
    app.add_handler(CommandHandler("add_points", add_points_admin))
    app.add_handler(CommandHandler("ranking_geral", ranking_geral))
    app.add_handler(CommandHandler("reset_month", reset_month))
    app.add_handler(CommandHandler("announce_prizes", announce_prizes))

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()