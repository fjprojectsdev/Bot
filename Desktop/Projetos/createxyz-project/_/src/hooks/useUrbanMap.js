import { useState, useEffect, useMemo } from "react";
import {
  initialProblems,
  initialNotifications,
  problemTypes,
  rewardItems,
  userActivity,
} from "../lib/constants";

export function useUrbanMap() {
  const [problems, setProblems] = useState(initialProblems);
  const [userPoints, setUserPoints] = useState(850);
  const [userBadges] = useState([
    "Guardião da Rua",
    "Reporter Ativo",
    "Vigilante Urbano",
  ]);
  const [selectedProblem, setSelectedProblem] = useState(null);
  const [view, setView] = useState("map");
  const [filters, setFilters] = useState({
    type: "",
    urgency: "",
    status: "",
    search: "",
  });
  const [userLocation, setUserLocation] = useState(null);
  const [notifications, setNotifications] = useState(initialNotifications);
  const [userEvents, setUserEvents] = useState([1]); // Usuário já participa do evento 1
  const [redeemedRewards, setRedeemedRewards] = useState([]);
  const [userActivities, setUserActivities] = useState(userActivity);

  useEffect(() => {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          });
        },
        (error) => {
          console.log("Erro ao obter localização:", error);
        },
      );
    }
  }, []);

  const addNotification = (message, type = "general", problemId = null) => {
    setNotifications((prev) => [
      {
        id: Date.now(),
        message,
        time: "Agora",
        unread: true,
        type,
        problemId,
      },
      ...prev,
    ]);
  };

  const addActivity = (type, description, points) => {
    const newActivity = {
      id: Date.now(),
      type,
      description,
      points,
      time: "Agora",
      icon:
        type === "report"
          ? "📝"
          : type === "confirmation"
            ? "✅"
            : type === "comment"
              ? "💬"
              : "🎯",
    };
    setUserActivities((prev) => [newActivity, ...prev]);
  };

  const addConfirmation = (problemId) => {
    setProblems(
      problems.map((p) =>
        p.id === problemId
          ? {
              ...p,
              confirmations: p.confirmations + 1,
              urgency:
                p.confirmations + 1 > 15
                  ? "high"
                  : p.confirmations + 1 > 8
                    ? "medium"
                    : "low",
              status: p.confirmations + 1 > 10 ? "confirmed" : p.status,
            }
          : p,
      ),
    );
    setUserPoints((prev) => prev + 10);
    addNotification("Problema confirmado: +10 pontos!", "points", problemId);
    addActivity("confirmation", "Confirmou um problema", 10);
  };

  const submitReport = async (reportData) => {
    const { type, address, description, photoUrl } = reportData;

    const problem = {
      id: Date.now().toString(),
      type,
      location: userLocation || {
        lat: -23.5505 + Math.random() * 0.01,
        lng: -46.6333 + Math.random() * 0.01,
      },
      address,
      urgency: "low",
      status: "reported",
      confirmations: 1,
      date: new Date().toISOString().split("T")[0],
      reporter: "Você",
      photo: photoUrl,
      description,
      comments: [],
      rating: null,
      likes: 0,
      neighborhood: "Centro", // Simplificado
    };

    setProblems((prev) => [...prev, problem]);
    setUserPoints((prev) => prev + 50);
    addNotification(
      "Problema reportado com sucesso: +50 pontos!",
      "points",
      problem.id,
    );
    addActivity("report", `Reportou ${problemTypes[type].label}`, 50);
  };

  const updateProblemStatus = (problemId, newStatus) => {
    setProblems(
      problems.map((p) =>
        p.id === problemId ? { ...p, status: newStatus } : p,
      ),
    );

    if (newStatus === "resolved") {
      addNotification(
        "Problema marcado como resolvido! Ajude avaliando a solução.",
        "resolved",
        problemId,
      );
    }
  };

  const addComment = async (problemId, commentText) => {
    const newComment = {
      id: Date.now(),
      author: "Você",
      text: commentText,
      time: "Agora",
    };

    setProblems(
      problems.map((p) =>
        p.id === problemId
          ? { ...p, comments: [...(p.comments || []), newComment] }
          : p,
      ),
    );

    setUserPoints((prev) => prev + 5);
    addNotification("Comentário adicionado: +5 pontos!", "points", problemId);
    addActivity("comment", "Comentou em um problema", 5);
  };

  const rateProblem = async (problemId, rating) => {
    setProblems(
      problems.map((p) => (p.id === problemId ? { ...p, rating } : p)),
    );

    setUserPoints((prev) => prev + 15);
    addNotification("Avaliação registrada: +15 pontos!", "points", problemId);
    addActivity("rating", `Avaliou resolução com ${rating} estrelas`, 15);
  };

  const joinEvent = (eventId) => {
    setUserEvents((prev) => [...prev, eventId]);
    setUserPoints((prev) => prev + 20);
    addNotification("Participação confirmada no evento: +20 pontos!", "event");
    addActivity("event", "Confirmou participação em evento", 20);
  };

  const leaveEvent = (eventId) => {
    setUserEvents((prev) => prev.filter((id) => id !== eventId));
    addNotification("Participação cancelada no evento.", "event");
  };

  const redeemReward = (rewardId, rewardPoints) => {
    if (userPoints >= rewardPoints) {
      setRedeemedRewards((prev) => [...prev, rewardId]);
      setUserPoints((prev) => prev - rewardPoints);
      const reward = rewardItems.find((r) => r.id === rewardId);
      addNotification(`Recompensa resgatada: ${reward.name}!`, "reward");
      addActivity("redeem", `Resgatou ${reward.name}`, -rewardPoints);
    }
  };

  const likeProblem = (problemId) => {
    setProblems(
      problems.map((p) =>
        p.id === problemId ? { ...p, likes: (p.likes || 0) + 1 } : p,
      ),
    );
    setUserPoints((prev) => prev + 2);
    addActivity("like", "Curtiu um problema", 2);
  };

  const shareProblem = (problemId) => {
    const problem = problems.find((p) => p.id === problemId);
    if (problem && navigator.share) {
      navigator.share({
        title: `${problemTypes[problem.type].label} em ${problem.address}`,
        text: problem.description,
        url: window.location.href,
      });
    } else {
      // Fallback para copy to clipboard
      const shareText = `Veja este problema na cidade: ${problemTypes[problem.type].label} em ${problem.address}. ${problem.description}`;
      navigator.clipboard.writeText(shareText);
      addNotification(
        "Link do problema copiado para área de transferência!",
        "share",
      );
    }
    setUserPoints((prev) => prev + 5);
    addActivity("share", "Compartilhou um problema", 5);
  };

  const markNotificationAsRead = (notificationId) => {
    setNotifications(
      notifications.map((n) =>
        n.id === notificationId ? { ...n, unread: false } : n,
      ),
    );
  };

  const filteredProblems = useMemo(() => {
    return problems.filter((problem) => {
      if (filters.type && problem.type !== filters.type) return false;
      if (filters.urgency && problem.urgency !== filters.urgency) return false;
      if (filters.status && problem.status !== filters.status) return false;
      if (filters.search) {
        const searchLower = filters.search.toLowerCase();
        return (
          problem.address.toLowerCase().includes(searchLower) ||
          problem.description.toLowerCase().includes(searchLower) ||
          problemTypes[problem.type].label.toLowerCase().includes(searchLower)
        );
      }
      return true;
    });
  }, [problems, filters]);

  const unreadCount = notifications.filter((n) => n.unread).length;

  const handleSelectProblem = (problem) => {
    setSelectedProblem(problem);
    if (problem && view !== "map") {
      // In list view, we show a modal, so no need to switch view.
    } else if (problem) {
      setView("map");
    }
  };

  // Detectar problemas próximos (simulado)
  useEffect(() => {
    if (userLocation && problems.length > 0) {
      const nearbyProblems = problems.filter(
        (p) =>
          p.status !== "resolved" &&
          !notifications.some(
            (n) => n.problemId === p.id && n.type === "proximity",
          ),
      );

      if (nearbyProblems.length > 0 && Math.random() > 0.7) {
        // 30% chance para demo
        const randomProblem =
          nearbyProblems[Math.floor(Math.random() * nearbyProblems.length)];
        setTimeout(() => {
          addNotification(
            `Novo problema reportado próximo a você: ${problemTypes[randomProblem.type].label}`,
            "proximity",
            randomProblem.id,
          );
        }, 5000);
      }
    }
  }, [userLocation, problems.length]);

  return {
    problems,
    filteredProblems,
    userPoints,
    userBadges,
    selectedProblem,
    setSelectedProblem: handleSelectProblem,
    view,
    setView,
    filters,
    setFilters,
    userLocation,
    notifications,
    unreadCount,
    userEvents,
    redeemedRewards,
    userActivities,
    addConfirmation,
    submitReport,
    updateProblemStatus,
    addComment,
    rateProblem,
    joinEvent,
    leaveEvent,
    redeemReward,
    likeProblem,
    shareProblem,
    markNotificationAsRead,
  };
}
