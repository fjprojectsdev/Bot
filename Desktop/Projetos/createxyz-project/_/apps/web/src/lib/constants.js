export const problemTypes = {
  pothole: { labelKey: "problems.pothole", icon: "🕳️", color: "bg-orange-500" },
  streetlight: {
    labelKey: "problems.streetlight",
    icon: "💡",
    color: "bg-yellow-500",
  },
  traffic: {
    labelKey: "problems.traffic",
    icon: "🚦",
    color: "bg-red-500",
  },
  flooding: { labelKey: "problems.flooding", icon: "🌊", color: "bg-blue-500" },
};

export const urgencyColors = {
  low: "bg-green-100 text-green-800",
  medium: "bg-yellow-100 text-yellow-800",
  high: "bg-red-100 text-red-800",
};

export const statusColors = {
  reported: "bg-blue-100 text-blue-800",
  confirmed: "bg-yellow-100 text-yellow-800",
  in_progress: "bg-orange-100 text-orange-800",
  resolved: "bg-green-100 text-green-800",
};

export const initialProblems = [
  {
    id: "1",
    type: "pothole",
    location: { lat: -23.5505, lng: -46.6333 },
    address: "Av. Paulista, 1000 - São Paulo/SP",
    urgency: "high",
    status: "confirmed",
    confirmations: 15,
    date: "2024-01-15",
    reporter: "João Silva",
    photo: null,
    description: "Buraco grande que pode causar acidentes",
    comments: [
      {
        id: 1,
        author: "Maria Santos",
        text: "Confirmo, quase furei o pneu aqui!",
        time: "2 horas atrás",
      },
      {
        id: 2,
        author: "Pedro Lima",
        text: "Prefeitura já foi notificada",
        time: "1 hora atrás",
      },
    ],
    rating: null,
    likes: 12,
    neighborhood: "Bela Vista",
  },
  {
    id: "2",
    type: "streetlight",
    location: { lat: -23.5489, lng: -46.6388 },
    address: "Rua Augusta, 500 - São Paulo/SP",
    urgency: "medium",
    status: "in_progress",
    confirmations: 8,
    date: "2024-01-14",
    reporter: "Maria Santos",
    photo: null,
    description: "Poste apagado há uma semana",
    comments: [
      {
        id: 3,
        author: "João Silva",
        text: "Área muito perigosa à noite",
        time: "3 horas atrás",
      },
    ],
    rating: null,
    likes: 5,
    neighborhood: "Consolação",
  },
  {
    id: "3",
    type: "flooding",
    location: { lat: -23.552, lng: -46.63 },
    address: "Rua da Consolação, 200 - São Paulo/SP",
    urgency: "high",
    status: "resolved",
    confirmations: 23,
    date: "2024-01-13",
    reporter: "Pedro Costa",
    photo: null,
    description: "Alagamento recorrente em dias de chuva",
    comments: [
      {
        id: 4,
        author: "Ana Costa",
        text: "Problema resolvido! Obrigada!",
        time: "30 min atrás",
      },
    ],
    rating: 5,
    likes: 18,
    neighborhood: "República",
  },
];

export const initialNotifications = [
  {
    id: 1,
    message: "Novo problema reportado próximo a você!",
    time: "5 min atrás",
    unread: true,
    type: "proximity",
    problemId: "1",
  },
  {
    id: 2,
    message: "Problema confirmado: +10 pontos!",
    time: "1 hora atrás",
    unread: false,
    type: "points",
    problemId: "2",
  },
  {
    id: 3,
    message: "🎉 Parabéns! Você subiu para o nível Guardião!",
    time: "2 horas atrás",
    unread: true,
    type: "achievement",
  },
];





export const userActivity = [
  {
    id: 1,
    type: "report",
    description: "Reportou buraco na Av. Paulista",
    points: 50,
    time: "2 horas atrás",
    icon: "📝",
  },
  {
    id: 2,
    type: "confirmation",
    description: "Confirmou problema de iluminação",
    points: 10,
    time: "1 dia atrás",
    icon: "✅",
  },
  {
    id: 3,
    type: "comment",
    description: "Comentou em problema resolvido",
    points: 5,
    time: "2 dias atrás",
    icon: "💬",
  },
  {
    id: 4,
    type: "event",
    description: "Participou do mutirão de limpeza",
    points: 100,
    time: "3 dias atrás",
    icon: "🎯",
  },
];

export const neighborhoodStats = [
  {
    name: "Bela Vista",
    totalProblems: 45,
    resolvedProblems: 32,
    avgResolutionTime: "5 dias",
    mostCommonType: "pothole",
    resolutionRate: 71,
  },
  {
    name: "Consolação",
    totalProblems: 38,
    resolvedProblems: 28,
    avgResolutionTime: "4 dias",
    mostCommonType: "streetlight",
    resolutionRate: 74,
  },
  {
    name: "República",
    totalProblems: 52,
    resolvedProblems: 41,
    avgResolutionTime: "3 dias",
    mostCommonType: "flooding",
    resolutionRate: 79,
  },
  {
    name: "Vila Madalena",
    totalProblems: 29,
    resolvedProblems: 24,
    avgResolutionTime: "2 dias",
    mostCommonType: "pothole",
    resolutionRate: 83,
  },
];
