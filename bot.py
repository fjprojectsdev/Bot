from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import random
import datetime

# Dicionários para armazenar dados
contagem = {}
sorteios = {}
enquetes = {}
lembretes = {}
jogos_ativo = {}

# Sistema de gamificação
pontos = {}  # {user_id: pontos}
badges = {}  # {user_id: [lista_badges]}
missoes = {}  # {chat_id: {missao_id: dados}}
missoes_usuario = {}  # {user_id: {missao_id: status}}
check_ins = {}  # {user_id: {data: True/False}}
engajamento = {}  # {user_id: {acao: contador}}

# Função chamada a cada mensagem
async def contar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user:
        user_id = update.effective_user.id
        nome = update.effective_user.first_name

        if user_id not in contagem:
            contagem[user_id] = {"nome": nome, "mensagens": 0}
            pontos[user_id] = 0
            badges[user_id] = []
            engajamento[user_id] = {"mensagens": 0, "comandos": 0, "missoes": 0}

        contagem[user_id]["mensagens"] += 1
        engajamento[user_id]["mensagens"] += 1
        
        # Sistema de pontos por mensagem
        pontos[user_id] += 1
        
        # Verificar badges automáticos
        await verificar_badges(update, user_id)

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
    chat_id = update.effective_chat.id
    sorteios[chat_id] = {"premio": "Prêmio", "participantes": [], "criador": update.effective_user.first_name}
    
    await update.message.reply_text(f"🎉 Sorteio criado!\n\nPara participar, digite /entrar")

# Participar do sorteio
async def participar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    nome = update.effective_user.first_name
    
    if chat_id not in sorteios:
        await update.message.reply_text("Não há sorteio ativo!")
        return
    
    if any(p["id"] == user_id for p in sorteios[chat_id]["participantes"]):
        await update.message.reply_text("Você já está participando!")
        return
    
    sorteios[chat_id]["participantes"].append({"id": user_id, "nome": nome})
    total = len(sorteios[chat_id]["participantes"])
    
    # Dar pontos por participar
    pontos[user_id] = pontos.get(user_id, 0) + 5
    
    await update.message.reply_text(f"✅ {nome} entrou no sorteio! ({total} participantes) (+5 pontos!)")

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

# Poll simples
async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    pergunta = "Melhor time?"
    opcoes = ["Flamengo", "Vasco"]
    
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
    pontos[user_id] = pontos.get(user_id, 0) + 5
    
    await update.message.reply_text(f"✅ {nome} votou em: {enquetes[chat_id]['opcoes'][opcao]} (+5 pontos!)")

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

# Escolher pessoa aleatória
async def escolher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not contagem:
        await update.message.reply_text("Nenhum membro ativo encontrado!")
        return
    
    pessoa = random.choice(list(contagem.values()))
    await update.message.reply_text(f"🎯 Escolhido: {pessoa['nome']}!")

# Sistema de gamificação
async def verificar_badges(update, user_id):
    nome = contagem[user_id]["nome"]
    mensagens = contagem[user_id]["mensagens"]
    user_badges = badges[user_id]
    
    # Badge de mensagens
    if mensagens >= 100 and "Tagarela" not in user_badges:
        badges[user_id].append("Tagarela")
        pontos[user_id] += 50
        await update.message.reply_text(f"🏆 {nome} ganhou o badge 'Tagarela' (+50 pontos!)")
    
    if mensagens >= 500 and "Comunicador" not in user_badges:
        badges[user_id].append("Comunicador")
        pontos[user_id] += 100
        await update.message.reply_text(f"🏆 {nome} ganhou o badge 'Comunicador' (+100 pontos!)")

# Perfil do usuário
async def perfil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    nome = update.effective_user.first_name
    
    if user_id not in pontos:
        pontos[user_id] = 0
        badges[user_id] = []
    
    user_pontos = pontos[user_id]
    user_badges = badges[user_id]
    mensagens = contagem.get(user_id, {}).get("mensagens", 0)
    
    # Calcular nível
    nivel = user_pontos // 100 + 1
    proximo_nivel = (nivel * 100) - user_pontos
    
    texto = f"👤 PERFIL DE {nome}\n\n"
    texto += f"⭐ Nível: {nivel}\n"
    texto += f"🎯 Pontos: {user_pontos}\n"
    texto += f"📈 Para próximo nível: {proximo_nivel} pontos\n"
    texto += f"💬 Mensagens: {mensagens}\n\n"
    
    if user_badges:
        texto += "🏆 BADGES:\n"
        for badge in user_badges:
            texto += f"• {badge}\n"
    else:
        texto += "🏆 Nenhum badge ainda\n"
    
    await update.message.reply_text(texto)

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

# Criar missão
async def criar_missao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("Use: /missao <título> <pontos> <descrição>\nExemplo: /missao 'Participar enquete' 25 'Vote na próxima enquete'")
        return
    
    chat_id = update.effective_chat.id
    titulo = context.args[0]
    try:
        pts = int(context.args[1])
    except ValueError:
        await update.message.reply_text("Pontos deve ser um número!")
        return
    
    descricao = " ".join(context.args[2:])
    missao_id = len(missoes.get(chat_id, {})) + 1
    
    if chat_id not in missoes:
        missoes[chat_id] = {}
    
    missoes[chat_id][missao_id] = {
        "titulo": titulo,
        "pontos": pts,
        "descricao": descricao,
        "ativa": True
    }
    
    await update.message.reply_text(f"🎯 NOVA MISSÃO CRIADA!\n\n📋 {titulo}\n🎯 {pts} pontos\n📝 {descricao}\n\nUse /missoes para ver todas")

# Ver missões
async def ver_missoes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    if chat_id not in missoes or not missoes[chat_id]:
        await update.message.reply_text("Nenhuma missão ativa!")
        return
    
    texto = "🎯 MISSÕES ATIVAS:\n\n"
    for missao_id, dados in missoes[chat_id].items():
        if dados["ativa"]:
            texto += f"#{missao_id} - {dados['titulo']}\n"
            texto += f"🎯 {dados['pontos']} pontos\n"
            texto += f"📝 {dados['descricao']}\n\n"
    
    await update.message.reply_text(texto)

# Completar missão
async def completar_missao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Use: /completar <número_missão>")
        return
    
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    nome = update.effective_user.first_name
    missao_id = int(context.args[0])
    
    if chat_id not in missoes or missao_id not in missoes[chat_id]:
        await update.message.reply_text("Missão não encontrada!")
        return
    
    if user_id not in missoes_usuario:
        missoes_usuario[user_id] = {}
    
    if missao_id in missoes_usuario[user_id]:
        await update.message.reply_text("Você já completou esta missão!")
        return
    
    # Completar missão
    missao = missoes[chat_id][missao_id]
    missoes_usuario[user_id][missao_id] = True
    pontos[user_id] = pontos.get(user_id, 0) + missao["pontos"]
    engajamento[user_id]["missoes"] = engajamento.get(user_id, {}).get("missoes", 0) + 1
    
    await update.message.reply_text(f"✅ {nome} completou a missão '{missao['titulo']}'!\n+{missao['pontos']} pontos")

# Quiz interativo
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    perguntas = [
        {"pergunta": "Qual a capital do Brasil?", "opcoes": ["Rio de Janeiro", "São Paulo", "Brasília"], "correta": 2},
        {"pergunta": "Quantos dias tem um ano?", "opcoes": ["364", "365", "366"], "correta": 1},
        {"pergunta": "Qual o maior planeta?", "opcoes": ["Terra", "Júpiter", "Saturno"], "correta": 1}
    ]
    
    quiz_escolhido = random.choice(perguntas)
    chat_id = update.effective_chat.id
    
    # Armazenar quiz ativo
    if chat_id not in jogos_ativo:
        jogos_ativo[chat_id] = {}
    
    jogos_ativo[chat_id]["quiz"] = quiz_escolhido
    
    texto = f"🧠 QUIZ TIME!\n\n❓ {quiz_escolhido['pergunta']}\n\n"
    for i, opcao in enumerate(quiz_escolhido['opcoes']):
        texto += f"{i+1}. {opcao}\n"
    texto += "\nResponda com /resposta <número>"
    
    await update.message.reply_text(texto)

# Responder quiz
async def responder_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Use: /resposta <número>")
        return
    
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    nome = update.effective_user.first_name
    resposta = int(context.args[0]) - 1
    
    if chat_id not in jogos_ativo or "quiz" not in jogos_ativo[chat_id]:
        await update.message.reply_text("Nenhum quiz ativo!")
        return
    
    quiz = jogos_ativo[chat_id]["quiz"]
    
    if resposta == quiz["correta"]:
        pontos[user_id] = pontos.get(user_id, 0) + 20
        await update.message.reply_text(f"✅ Correto, {nome}! +20 pontos")
    else:
        await update.message.reply_text(f"❌ Errado, {nome}. A resposta correta era: {quiz['opcoes'][quiz['correta']]}")
    
    # Remover quiz
    del jogos_ativo[chat_id]["quiz"]

# Ajuda
async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """🤖 COMANDOS DISPONÍVEIS:

🎮 GAMIFICAÇÃO:
/perfil - Seu perfil e badges
/rank - Ranking de pontos
/checkin - Check-in diário (+10 pts)
/missoes - Ver missões ativas
/completar <num> - Completar missão
/quiz - Quiz interativo (+20 pts)
/resposta <num> - Responder quiz

📊 ESTATÍSTICAS:
/top - Ranking de mensagens

🎉 SORTEIOS:
/sorteio - Criar sorteio
/entrar - Entrar no sorteio
/sortear - Escolher vencedor

📊 ENQUETES:
/poll - Criar enquete
/voto <número> - Votar
/resultado - Ver resultado

🎯 UTILIDADES:
/random - Escolher pessoa aleatória
/frase - Frase motivacional
/aviso <min> <msg> - Criar lembrete

🛠️ ADMIN:
/missao <título> <pts> <desc> - Criar missão

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
    
    # Sorteios
    app.add_handler(CommandHandler("sorteio", sorteio))
    app.add_handler(CommandHandler("entrar", participar))
    app.add_handler(CommandHandler("sortear", sortear))
    
    # Enquetes
    app.add_handler(CommandHandler("poll", poll))
    app.add_handler(CommandHandler("voto", votar))
    app.add_handler(CommandHandler("resultado", resultado))
    
    # Utilidades
    app.add_handler(CommandHandler("random", escolher))
    app.add_handler(CommandHandler("frase", frase))
    app.add_handler(CommandHandler("aviso", lembrete))
    
    # Gamificação
    app.add_handler(CommandHandler("perfil", perfil))
    app.add_handler(CommandHandler("rank", rank_pontos))
    app.add_handler(CommandHandler("checkin", checkin))
    app.add_handler(CommandHandler("missoes", ver_missoes))
    app.add_handler(CommandHandler("missao", criar_missao))
    app.add_handler(CommandHandler("completar", completar_missao))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("resposta", responder_quiz))
    
    # Ajuda
    app.add_handler(CommandHandler("help", ajuda))
    app.add_handler(CommandHandler("start", ajuda))

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()