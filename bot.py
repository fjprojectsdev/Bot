from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import random
import datetime

# Dicionários para armazenar dados
contagem = {}
sorteios = {}
lembretes = {}
jogos_ativo = {}

# Sistema de gamificação
pontos = {}  # {user_id: pontos}
badges = {}  # {user_id: [lista_badges]}
missoes = {}  # {chat_id: {missao_id: dados}}
missoes_usuario = {}  # {user_id: {missao_id: status}}
check_ins = {}  # {user_id: {data: True/False}}
engajamento = {}  # {user_id: {acao: contador}}

# Sistema de rastreamento automático
links_rastreamento = {}  # {link_id: {user_id, missao_id, timestamp}}
atividade_tempo = {}  # {user_id: {ultima_acao, tempo_resposta_medio}}
missoes_verificaveis = {}  # {missao_id: {tipo, parametros, completadas}}
historico_mensagens = {}  # {user_id: [timestamps das últimas mensagens]}
checkin_diario = {}  # {data: [user_ids que fizeram checkin]}

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
        
        # Rastrear atividade e tempo de resposta
        await rastrear_atividade(user_id)
        
        # Verificar se é flood
        if verificar_flood(user_id, update.message.text):
            return  # Não conta mensagem de flood
        
        # Verificar badges automáticos
        await verificar_badges(update, user_id)
        
        # Verificar missões de engajamento
        missao_completada = await verificar_missoes_engajamento(user_id, update.effective_chat.id)
        if missao_completada:
            await update.message.reply_text(f"🎉 {nome} completou missão de engajamento!\n+{missao_completada['pontos']} pontos")

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

# Perfil do usuário com dados de engajamento
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
    
    # Dados de engajamento
    atividade = atividade_tempo.get(user_id, {})
    tempo_resposta = atividade.get("tempo_resposta_medio", 0)
    acoes_total = atividade.get("acoes_total", 0)
    
    # Calcular score de confiabilidade
    score_confiabilidade = min(100, (acoes_total * 2) + (50 if tempo_resposta < 300 else 0))
    
    texto = f"👤 PERFIL DE {nome}\n\n"
    texto += f"⭐ Nível: {nivel}\n"
    texto += f"🎯 Pontos: {user_pontos}\n"
    texto += f"📈 Para próximo nível: {proximo_nivel} pontos\n"
    texto += f"💬 Mensagens: {mensagens}\n"
    texto += f"⚡ Ações totais: {acoes_total}\n"
    texto += f"🔒 Score confiabilidade: {score_confiabilidade}%\n\n"
    
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
    
    # Adicionar à lista diária
    if hoje not in checkin_diario:
        checkin_diario[hoje] = []
    checkin_diario[hoje].append(user_id)
    
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

# Tabela de check-ins
async def tabela_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hoje = datetime.date.today().isoformat()
    
    if hoje not in checkin_diario or not checkin_diario[hoje]:
        await update.message.reply_text("📊 Nenhum check-in hoje ainda!")
        return
    
    texto = f"📊 CHECK-INS DE HOJE ({hoje}):\n\n"
    
    for i, user_id in enumerate(checkin_diario[hoje], 1):
        nome = contagem.get(user_id, {}).get("nome", "Usuário")
        sequencia = calcular_sequencia(user_id)
        texto += f"{i}. {nome} - {sequencia} dias seguidos\n"
    
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

# Sistema de rastreamento automático
async def rastrear_atividade(user_id):
    agora = datetime.datetime.now()
    
    if user_id not in atividade_tempo:
        atividade_tempo[user_id] = {"ultima_acao": agora, "tempo_resposta_medio": 0, "acoes_total": 0}
    
    # Calcular tempo de resposta
    if atividade_tempo[user_id]["acoes_total"] > 0:
        tempo_desde_ultima = (agora - atividade_tempo[user_id]["ultima_acao"].replace(tzinfo=None)).total_seconds()
        atividade_tempo[user_id]["tempo_resposta_medio"] = (
            (atividade_tempo[user_id]["tempo_resposta_medio"] * atividade_tempo[user_id]["acoes_total"] + tempo_desde_ultima) /
            (atividade_tempo[user_id]["acoes_total"] + 1)
        )
    
    atividade_tempo[user_id]["ultima_acao"] = agora
    atividade_tempo[user_id]["acoes_total"] += 1

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

# Criar missão
async def criar_missao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Use: /missao <tipo> <pontos> [link]\nTipos: link, checkin, engajamento")
        return
    
    chat_id = update.effective_chat.id
    tipo = context.args[0].lower()
    
    try:
        pts = int(context.args[1])
    except ValueError:
        await update.message.reply_text("Pontos deve ser um número!")
        return
    
    missao_id = len(missoes.get(chat_id, {})) + 1
    
    if chat_id not in missoes:
        missoes[chat_id] = {}
    
    if tipo == "link":
        if len(context.args) < 3:
            await update.message.reply_text("Use: /missao link <pontos> <seu_link>\nExemplo: /missao link 50 https://instagram.com/p/abc123")
            return
        
        link_personalizado = context.args[2]
        link_id = f"track_{missao_id}_{random.randint(1000, 9999)}"
        
        missoes[chat_id][missao_id] = {
            "titulo": "Acessar Link",
            "pontos": pts,
            "tipo": "link",
            "link_id": link_id,
            "link_original": link_personalizado,
            "ativa": True
        }
        
        await update.message.reply_text(f"🔗 MISSÃO LINK CRIADA!\n\n📋 Acessar: {link_personalizado}\n🎯 {pts} pontos\n\n✅ Use /link {link_id} após acessar o link!")
    
    elif tipo == "checkin":
        missoes[chat_id][missao_id] = {
            "titulo": "Check-in Especial",
            "pontos": pts,
            "tipo": "checkin",
            "ativa": True
        }
        
        await update.message.reply_text(f"✅ MISSÃO CHECK-IN CRIADA!\n\n📋 Check-in Especial\n🎯 {pts} pontos\n\n⏰ Faça /checkin para completar")
    
    elif tipo == "engajamento":
        missoes[chat_id][missao_id] = {
            "titulo": "Engajamento Ativo",
            "pontos": pts,
            "tipo": "engajamento",
            "meta_mensagens": 10,
            "ativa": True
        }
        
        await update.message.reply_text(f"💬 MISSÃO ENGAJAMENTO CRIADA!\n\n📋 Enviar 10 mensagens válidas\n🎯 {pts} pontos\n\n🚫 Flood não conta!")

# Confirmar acesso ao link
async def confirmar_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /link <id>")
        return
    
    link_id = context.args[0]
    user_id = update.effective_user.id
    nome = update.effective_user.first_name
    
    # Verificar se é um link válido
    missao_encontrada = None
    
    for chat_id, missoes_chat in missoes.items():
        for missao_id, dados in missoes_chat.items():
            if dados.get("link_id") == link_id and dados["ativa"]:
                missao_encontrada = dados
                break
    
    if not missao_encontrada:
        await update.message.reply_text("ID inválido!")
        return
    
    # Verificar se já completou
    if user_id not in missoes_usuario:
        missoes_usuario[user_id] = {}
    
    if link_id in missoes_usuario[user_id]:
        await update.message.reply_text("Você já completou esta missão!")
        return
    
    # Registrar conclusão
    missoes_usuario[user_id][link_id] = True
    pontos[user_id] = pontos.get(user_id, 0) + missao_encontrada["pontos"]
    
    await update.message.reply_text(f"✅ {nome} acessou o link!\n+{missao_encontrada['pontos']} pontos\n\n🔗 Link: {missao_encontrada['link_original']}")



# Verificar missões de engajamento automaticamente
async def verificar_missoes_engajamento(user_id, chat_id):
    if chat_id not in missoes:
        return
    
    for missao_id, dados in missoes[chat_id].items():
        if dados["tipo"] == "engajamento" and dados["ativa"]:
            mensagens_usuario = contagem.get(user_id, {}).get("mensagens", 0)
            meta = dados.get("meta_mensagens", 10)
            
            if mensagens_usuario >= meta:
                # Verificar se já completou
                if user_id not in missoes_usuario:
                    missoes_usuario[user_id] = {}
                
                missao_key = f"eng_{missao_id}"
                if missao_key not in missoes_usuario[user_id]:
                    missoes_usuario[user_id][missao_key] = True
                    pontos[user_id] = pontos.get(user_id, 0) + dados["pontos"]
                    return dados  # Retorna para notificar
    return None

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



# Ajuda
async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = """🤖 COMANDOS DISPONÍVEIS:

🎮 GAMIFICAÇÃO:
/perfil - Seu perfil e badges
/rank - Ranking de pontos
/checkin - Check-in diário (+10 pts)
/missoes - Ver missões ativas

📊 ESTATÍSTICAS:
/top - Ranking de mensagens

🎉 SORTEIOS:
/sorteio - Criar sorteio
/entrar - Entrar no sorteio
/sortear - Escolher vencedor

🎯 UTILIDADES:
/random - Escolher pessoa aleatória

🛠️ ADMIN:
/missao <tipo> <pts> [link] - Criar missão
/tabela - Ver check-ins de hoje

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
    
    # Utilidades
    app.add_handler(CommandHandler("random", escolher))
    
    # Gamificação
    app.add_handler(CommandHandler("perfil", perfil))
    app.add_handler(CommandHandler("rank", rank_pontos))
    app.add_handler(CommandHandler("checkin", checkin))
    app.add_handler(CommandHandler("missoes", ver_missoes))
    app.add_handler(CommandHandler("missao", criar_missao))
    
    # Sistema de rastreamento
    app.add_handler(CommandHandler("link", confirmar_link))
    app.add_handler(CommandHandler("tabela", tabela_checkin))
    
    # Ajuda
    app.add_handler(CommandHandler("help", ajuda))

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()