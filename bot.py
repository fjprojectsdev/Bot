from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import random
import datetime
import logging
import os
import io

# Configuração
ADMIN_IDS = [6670325989, 7645992176, 8008129139]  # @FlavioJhonatan, @RareG_14, @Sinclair_Frost

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

# Sistema de punições
avisos = {}  # {user_id: count}
logs_admin = []  # Lista de eventos para logs

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

# Palavras proibidas
PALAVRAS_SPAM = ['airdrop', 'foxy', 'oxy loyal', 'privado', 'ao vivo', 'não perca', 'chance']

# Função básica
async def contar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message or not update.message.text:
        return
        
    user_id = update.effective_user.id
    nome = update.effective_user.first_name
    texto = update.message.text.lower()

    # Verificar spam de airdrop
    if any(palavra in texto for palavra in PALAVRAS_SPAM):
        try:
            await update.message.delete()
            await update.message.reply_text(f"⚠️ {nome}, mensagem removida por conter spam de airdrop.")
            return
        except:
            pass

    # Inicializar usuário se não existir
    if user_id not in contagem:
        contagem[user_id] = {"nome": nome, "mensagens": 0}
    if user_id not in pontos:
        pontos[user_id] = 0
    if user_id not in badges:
        badges[user_id] = []

    # Responder perguntas sobre Kenesis automaticamente
    try:
        await responder_kenesis(update)
    except Exception as e:
        print(f"Erro na IA: {e}")
    
    # SEMPRE contar a mensagem (flood desabilitado)
    contagem[user_id]["mensagens"] += 1
    pontos[user_id] += 1
    
    # Atualizar nome se mudou
    contagem[user_id]["nome"] = nome
    
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

# Verificar se é flood (desabilitado)
def verificar_flood(user_id, texto):
    # Sistema de flood desabilitado para permitir contagem total
    return False

# Responder perguntas sobre Kenesis automaticamente
async def responder_kenesis(update: Update):
    texto = update.message.text.lower()
    idioma = detectar_idioma(texto)
    
    # Saudações específicas
    saudacoes_pt = ["oi", "olá", "bom dia", "boa tarde", "boa noite"]
    saudacoes_en = ["hi", "hello", "good morning", "good afternoon", "good evening"]
    
    # Verificar se é uma saudação exata
    if any(saudacao == texto.strip() for saudacao in saudacoes_pt + saudacoes_en):
        if idioma == 'pt':
            saudacoes = ["Olá! 👋 Bem-vindo à Kenesis!", "Oi! 🚀 Pronto para o futuro da educação?", "E aí! 💡 Vamos aprender juntos?"]
        else:
            saudacoes = ["Hello! 👋 Welcome to Kenesis!", "Hi! 🚀 Ready for the future of education?", "Hey! 💡 Let's learn together?"]
        await update.message.reply_text(random.choice(saudacoes))
        return
    
    # Respostas sobre Kenesis (apenas com pergunta)
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
    
    if ("missão" in texto or "mission" in texto) and "?" in texto:
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
    username = update.effective_user.username or nome
    
    msgs = contagem.get(user_id, {}).get("mensagens", 0)
    pts = pontos.get(user_id, 0)
    user_badges = badges.get(user_id, [])
    
    # Calcular check-ins
    total_checkins = len(check_ins.get(user_id, {}))
    
    # Calcular convites (referrals)
    convites = users.get(f"@{username}", {}).get("referrals", 0)
    
    # Calcular nível
    nivel = pts // 100 + 1
    proximo_nivel = (nivel * 100) - pts
    
    texto = f"👤 PROFILE OF {nome}\n\n"
    texto += f"⭐ Level: {nivel}\n"
    texto += f"🎯 Points: {pts}\n"
    texto += f"📈 To next level: {proximo_nivel} points\n\n"
    texto += f"📊 PERSONAL STATS:\n"
    texto += f"💬 Messages sent: {msgs}\n"
    texto += f"✅ Check-ins completed: {total_checkins}\n"
    texto += f"👥 Referrals made: {convites}\n\n"
    
    if user_badges:
        texto += "🏆 BADGES:\n"
        for badge in user_badges:
            texto += f"• {badge}\n"
    else:
        texto += "🏆 No badges yet\n"
    
    await update.message.reply_text(texto)

# Meus pontos
async def meus_pontos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    nome = update.effective_user.first_name
    pts = pontos.get(user_id, 0)
    nivel = pts // 100 + 1
    proximo_nivel = (nivel * 100) - pts
    
    texto = f"🎯 {nome}'s Points:\n\n"
    texto += f"Current Points: {pts}\n"
    texto += f"Level: {nivel}\n"
    texto += f"Points to next level: {proximo_nivel}\n"
    
    await update.message.reply_text(texto)

async def kenesis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """KENESIS - Future of Education

Kenesis is revolutionizing education through Web3 technology. Follow us on social media and be part of the future of decentralized learning.

SOCIAL MEDIA LINKS:

X (Twitter): https://x.com/kenesis_io
TikTok: https://www.tiktok.com/@kenesis_io
Threads: https://www.threads.com/@kenesis.io
Medium: https://medium.com/@kenesisofficial
YouTube: https://www.youtube.com/@kenesis_io
LinkedIn: https://www.linkedin.com/company/kenesis-io/
Telegram: https://t.me/KenesisOfficial
Instagram: https://www.instagram.com/kenesis.io

OFFICIAL RESOURCES:

Website: https://kenesis.io/
Whitepaper: https://kenesis.gitbook.io/whitepaper/

Knowledge is technological, decentralized and no tracking."""
    
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

# Add referrals (admin) - Suporta múltiplos usuários
async def add_referrals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Only admin can use this command.")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Usage: /addrefs @username amount [or multiple: @user1 amount1 @user2 amount2]")
        return
    
    try:
        results = []
        args = context.args
        
        # Processar argumentos em pares (username, amount)
        for i in range(0, len(args), 2):
            if i + 1 >= len(args):
                break
                
            username = args[i].lower()
            amount = int(args[i + 1])
            
            # Garantir que o usuário existe no sistema
            if username not in users:
                users[username] = {"referrals": 0, "points": 0}
            
            users[username]["referrals"] += amount
            results.append(f"✅ {username}: +{amount} referrals")
            logs_admin.append(f"Admin added {amount} referrals to {username} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Resposta consolidada
        response = "📊 REFERRALS ADDED:\n\n" + "\n".join(results)
        response += f"\n\n🏆 Use /refsrank to see updated ranking"
        
        await update.message.reply_text(response)
        
    except ValueError:
        await update.message.reply_text("⚠️ Error: Make sure amounts are valid numbers")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error processing command: {str(e)}")

# Remove referrals (admin)
async def remove_referrals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Only admin can use this command.")
        return
    
    try:
        username = context.args[0].lower()
        amount = int(context.args[1])
        
        if username not in users:
            users[username] = {"referrals": 0, "points": 0}
        
        users[username]["referrals"] = max(0, users[username]["referrals"] - amount)
        await update.message.reply_text(f"✅ Removed {amount} referrals from {username}.")
        logs_admin.append(f"Admin removed {amount} referrals from {username} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except:
        await update.message.reply_text("⚠️ Usage: /removerefs @username amount")

# Delete referrals (admin)
async def delete_referrals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Only admin can use this command.")
        return
    
    try:
        username = context.args[0].lower()
        
        if username in users:
            old_refs = users[username]["referrals"]
            del users[username]  # Remove o usuário completamente
            await update.message.reply_text(f"✅ Deleted user {username} completely ({old_refs} referrals removed).")
            logs_admin.append(f"Admin deleted user {username} completely ({old_refs} referrals) - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            await update.message.reply_text(f"❌ User {username} not found.")
    except:
        await update.message.reply_text("⚠️ Usage: /delrefs @username")

# Add points (admin)
async def add_points_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Only admin can use this command.")
        return
    
    try:
        username = context.args[0].lower()
        amount = int(context.args[1])
        
        if username not in users:
            users[username] = {"referrals": 0, "points": 0}
        
        users[username]["points"] += amount
        await update.message.reply_text(f"✅ Added {amount} points to {username}.")
        logs_admin.append(f"Admin added {amount} points to {username} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except:
        await update.message.reply_text("⚠️ Usage: /addpoints @username amount")

# Remove points (admin)
async def remove_points_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Only admin can use this command.")
        return
    
    try:
        username = context.args[0].lower()
        amount = int(context.args[1])
        
        if username not in users:
            users[username] = {"referrals": 0, "points": 0}
        
        users[username]["points"] = max(0, users[username]["points"] - amount)
        await update.message.reply_text(f"✅ Removed {amount} points from {username}.")
        logs_admin.append(f"Admin removed {amount} points from {username} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except:
        await update.message.reply_text("⚠️ Usage: /removepoints @username amount")

# Delete points (admin)
async def delete_points_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Only admin can use this command.")
        return
    
    try:
        username = context.args[0].lower()
        
        if username in users:
            old_points = users[username]["points"]
            users[username]["points"] = 0
            await update.message.reply_text(f"✅ Deleted all points from {username} ({old_points} removed).")
            logs_admin.append(f"Admin deleted all points from {username} ({old_points}) - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            await update.message.reply_text(f"❌ User {username} not found.")
    except:
        await update.message.reply_text("⚠️ Usage: /delpoints @username")

# General ranking
async def ranking_geral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not users:
        await update.message.reply_text("📊 No data yet.")
        return
    
    sorted_users = sorted(users.items(), key=lambda x: (x[1]['points'] + x[1]['referrals']), reverse=True)
    
    msg = "🏆 TOP MEMBERS:\n\n"
    for i, (username, data) in enumerate(sorted_users, start=1):
        score = data['points'] + data['referrals']
        msg += f"{i}. {username} — {score} pts\n"
        msg += f"   Referrals: {data['referrals']} | Points: {data['points']}\n\n"
    
    await update.message.reply_text(msg)

# Referrals ranking
async def referrals_ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not users:
        await update.message.reply_text("📊 No referral data yet.")
        return
    
    # Ordenar todos os usuários por referrals (incluindo os com 0)
    sorted_users = sorted(users.items(), key=lambda x: x[1]['referrals'], reverse=True)
    
    msg = "🔗 REFERRALS RANKING:\n\n"
    count = 0
    for username, data in sorted_users:
        count += 1
        msg += f"{count}. {username} — {data['referrals']} referrals\n"
    
    if count == 0:
        msg += "No users registered yet."
    
    await update.message.reply_text(msg)

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    texto = """🤖 AVAILABLE COMMANDS:

🎮 GAMIFICATION:
/profile - Your profile and badges
/mypoints - Your current points
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

/help - View commands"""
    
    # Adicionar comandos admin apenas para admins
    if is_admin(user_id):
        texto += """\n\n🛠️ ADMIN COMMANDS:
/addrefs @user amount - Add referrals (supports multiple)
/importrefs - Bulk import (multiline format)
/removerefs @user amount - Remove referrals
/delrefs @user - Delete all referrals
/addpoints @user amount - Add points
/removepoints @user amount - Remove points
/delpoints @user - Delete all points
/checkuser @user - Check user ranking position
/debug - Debug message counting
/clear - Clear spam messages
/logs - View admin logs

📁 FILE IMPORT:
Send 'refs.txt' or 'refs.csv' file with format:
@user1,5
@user2,3"""
    
    await update.message.reply_text(texto)

# Sistema de punições
async def aplicar_punicao(update: Update, user_id: int):
    nome = update.effective_user.first_name
    idioma = detectar_idioma(update.message.text)
    
    if user_id not in avisos:
        avisos[user_id] = 0
    
    avisos[user_id] += 1
    
    if avisos[user_id] == 1:
        if idioma == 'pt':
            await update.message.reply_text(f"⚠️ {nome}, primeiro aviso! Evite flood no grupo.")
        else:
            await update.message.reply_text(f"⚠️ {nome}, first warning! Avoid flooding the group.")
    
    elif avisos[user_id] == 2:
        pontos[user_id] = max(0, pontos.get(user_id, 0) - 10)
        if idioma == 'pt':
            await update.message.reply_text(f"⚠️ {nome}, segundo aviso! -10 pontos por spam.")
        else:
            await update.message.reply_text(f"⚠️ {nome}, second warning! -10 points for spam.")
    
    elif avisos[user_id] == 3:
        pontos[user_id] = max(0, pontos.get(user_id, 0) - 25)
        if idioma == 'pt':
            await update.message.reply_text(f"⚠️ {nome}, terceiro aviso! -25 pontos. Próxima vez será removido.")
        else:
            await update.message.reply_text(f"⚠️ {nome}, third warning! -25 points. Next time you'll be removed.")
    
    else:
        try:
            await update.effective_chat.ban_chat_member(user_id)
            if idioma == 'pt':
                await update.message.reply_text(f"🚫 {nome} foi removido do grupo por spam repetido.")
            else:
                await update.message.reply_text(f"🚫 {nome} has been removed from the group for repeated spam.")
            
            logs_admin.append(f"User {nome} ({user_id}) removed for spam - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except:
            if idioma == 'pt':
                await update.message.reply_text(f"⚠️ {nome} deveria ser removido, mas o bot não tem permissão.")
            else:
                await update.message.reply_text(f"⚠️ {nome} should be removed, but bot lacks permission.")

# Admin tools
async def logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Only admin can use this command.")
        return
    
    if not logs_admin:
        await update.message.reply_text("📊 No admin logs yet.")
        return
    
    texto = "📊 ADMIN LOGS (Last 10):\n\n"
    for log in logs_admin[-10:]:
        texto += f"• {log}\n"
    
    # Dividir mensagem se muito longa
    if len(texto) > 4000:
        await update.message.reply_text(texto[:4000] + "...")
    else:
        await update.message.reply_text(texto)

# Limpar mensagens de spam (admin)
async def clear_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Only admin can use this command.")
        return
    
    try:
        chat_id = update.effective_chat.id
        message_id = update.message.message_id
        
        deleted = 0
        for i in range(1, 11):
            try:
                await context.bot.delete_message(chat_id, message_id - i)
                deleted += 1
            except:
                continue
        
        await update.message.reply_text(f"✅ {deleted} mensagens removidas.")
        logs_admin.append(f"Admin cleared {deleted} spam messages - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {str(e)}")

# Importação em lote de referrals
async def import_referrals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Only admin can use this command.")
        return
    
    # Obter o texto da mensagem após o comando
    message_text = update.message.text
    lines = message_text.split('\n')[1:]  # Pular a primeira linha com o comando
    
    if not lines or all(not line.strip() for line in lines):
        await update.message.reply_text("⚠️ Usage:\n/importrefs\n@user1 5\n@user2 3\n@user3 10")
        return
    
    results = []
    errors = []
    
    for line in lines:
        line = line.strip()
        if not line:  # Linha vazia para o loop
            break
            
        try:
            parts = line.split()
            if len(parts) != 2:
                errors.append(f"❌ Invalid format: {line}")
                continue
                
            username = parts[0].lower()
            amount = int(parts[1])
            
            if username not in users:
                users[username] = {"referrals": 0, "points": 0}
            
            users[username]["referrals"] += amount
            results.append(f"✅ {username}: +{amount} referrals")
            logs_admin.append(f"Admin imported {amount} referrals to {username} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except ValueError:
            errors.append(f"❌ Invalid number in: {line}")
        except Exception as e:
            errors.append(f"❌ Error in line '{line}': {str(e)}")
    
    # Resposta consolidada
    response = f"📊 BULK IMPORT COMPLETED:\n\n"
    if results:
        response += "\n".join(results)
    if errors:
        response += "\n\n⚠️ ERRORS:\n" + "\n".join(errors)
    
    response += f"\n\n🏆 Total processed: {len(results)} users"
    
    await update.message.reply_text(response)

# Processar arquivo de referrals
async def process_referrals_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    
    document = update.message.document
    if not document:
        return
    
    # Verificar se é um arquivo de referrals
    filename = document.file_name.lower()
    if not (filename == 'refs.txt' or filename == 'refs.csv' or 'refs' in filename):
        return
    
    try:
        # Baixar o arquivo
        file = await context.bot.get_file(document.file_id)
        file_content = await file.download_as_bytearray()
        
        # Decodificar o conteúdo
        content = file_content.decode('utf-8')
        lines = content.strip().split('\n')
        
        results = []
        errors = []
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):  # Pular linhas vazias e comentários
                continue
            
            try:
                # Suportar tanto vírgula quanto espaço como separador
                if ',' in line:
                    parts = line.split(',')
                else:
                    parts = line.split()
                
                if len(parts) != 2:
                    errors.append(f"❌ Line {line_num}: Invalid format '{line}'")
                    continue
                
                username = parts[0].strip().lower()
                amount = int(parts[1].strip())
                
                if username not in users:
                    users[username] = {"referrals": 0, "points": 0}
                
                users[username]["referrals"] += amount
                results.append(f"✅ {username}: +{amount} referrals")
                logs_admin.append(f"Admin imported {amount} referrals to {username} from file - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
            except ValueError:
                errors.append(f"❌ Line {line_num}: Invalid number in '{line}'")
            except Exception as e:
                errors.append(f"❌ Line {line_num}: Error in '{line}' - {str(e)}")
        
        # Resposta consolidada
        response = f"📁 FILE IMPORT COMPLETED ({filename}):\n\n"
        if results:
            # Limitar a resposta se muitos resultados
            if len(results) > 20:
                response += "\n".join(results[:20])
                response += f"\n... and {len(results) - 20} more users"
            else:
                response += "\n".join(results)
        
        if errors:
            response += "\n\n⚠️ ERRORS:\n" + "\n".join(errors[:10])
            if len(errors) > 10:
                response += f"\n... and {len(errors) - 10} more errors"
        
        response += f"\n\n🏆 Total processed: {len(results)} users"
        
        await update.message.reply_text(response)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error processing file: {str(e)}")

# Verificar posição de usuário específico (admin)
async def check_user_ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Only admin can use this command.")
        return
    
    try:
        username = context.args[0].lower()
        
        if username not in users:
            await update.message.reply_text(f"❌ User {username} not found in database.")
            return
        
        user_data = users[username]
        
        # Posição no ranking de referrals
        sorted_refs = sorted(users.items(), key=lambda x: x[1]['referrals'], reverse=True)
        ref_position = next((i+1 for i, (user, _) in enumerate(sorted_refs) if user == username), "N/A")
        
        msg = f"🔍 USER CHECK: {username}\n\n"
        msg += f"🔗 Referrals: {user_data['referrals']}\n"
        msg += f"🎯 Points: {user_data['points']}\n"
        msg += f"🏆 Total Score: {user_data['points'] + user_data['referrals']}\n\n"
        msg += f"🏅 Referrals Rank: #{ref_position}"
        
        await update.message.reply_text(msg)
        
    except:
        await update.message.reply_text("⚠️ Usage: /checkuser @username")

# Debug - Verificar contagem (admin)
async def debug_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Only admin can use this command.")
        return
    
    user_id = update.effective_user.id
    nome = update.effective_user.first_name
    
    msg = f"🔍 DEBUG INFO:\n\n"
    msg += f"Your User ID: {user_id}\n"
    msg += f"Your Name: {nome}\n\n"
    
    if user_id in contagem:
        msg += f"Messages in DB: {contagem[user_id]['mensagens']}\n"
        msg += f"Points in DB: {pontos.get(user_id, 0)}\n"
    else:
        msg += "User not found in database\n"
    
    msg += f"\nTotal users in DB: {len(contagem)}\n"
    msg += f"This message should increment your count by 1"
    
    await update.message.reply_text(msg)

def main():
    TOKEN = os.getenv('BOT_TOKEN', '8211453362:AAHJfblRYpJjh63dWQlnGGjsZHWXGiwmCKs')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, contar))
    app.add_handler(MessageHandler(filters.Document.ALL, process_referrals_file))
    
    # Commands in English
    app.add_handler(CommandHandler("messages", ranking))
    app.add_handler(CommandHandler("profile", perfil))
    app.add_handler(CommandHandler("checkin", checkin))
    app.add_handler(CommandHandler("points", rank_pontos))
    app.add_handler(CommandHandler("kenesis", kenesis))
    app.add_handler(CommandHandler("links", kenesis))
    app.add_handler(CommandHandler("help", ajuda))
    app.add_handler(CommandHandler("start", ajuda))
    
    # Referral system
    app.add_handler(CommandHandler("addrefs", add_referrals))
    app.add_handler(CommandHandler("removerefs", remove_referrals))
    app.add_handler(CommandHandler("delrefs", delete_referrals))
    app.add_handler(CommandHandler("addpoints", add_points_admin))
    app.add_handler(CommandHandler("removepoints", remove_points_admin))
    app.add_handler(CommandHandler("delpoints", delete_points_admin))
    app.add_handler(CommandHandler("ranking", ranking_geral))
    app.add_handler(CommandHandler("refsrank", referrals_ranking))
    app.add_handler(CommandHandler("mypoints", meus_pontos))
    app.add_handler(CommandHandler("logs", logs))
    app.add_handler(CommandHandler("clear", clear_spam))
    app.add_handler(CommandHandler("checkuser", check_user_ranking))
    app.add_handler(CommandHandler("importrefs", import_referrals))
    app.add_handler(CommandHandler("debug", debug_count))

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()