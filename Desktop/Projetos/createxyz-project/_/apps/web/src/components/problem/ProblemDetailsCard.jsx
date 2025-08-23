import React from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../../components/ui/card";
import { Button } from "../../components/ui/button";
import { Badge } from "../../components/ui/badge";
import { problemTypes, urgencyColors, statusColors } from "../../lib/constants";
import { CommentsSection } from "./CommentsSection";
import { RatingSection } from "./RatingSection";

export function ProblemDetailsCard({
  problem,
  onClose,
  onAddConfirmation,
  onUpdateStatus,
  onAddComment,
  onRate,
  onLike,
  onShare,
}) {
  if (!problem) return null;

  const handleLike = () => {
    if (onLike) {
      onLike(problem.id);
    }
  };

  const handleShare = () => {
    if (onShare) {
      onShare(problem.id);
    }
  };

  return (
    <Card className="border-2 border-blue-200">
      <CardHeader>
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <CardTitle className="flex items-center space-x-2">
              <span>{problemTypes[problem.type].icon}</span>
              <span>{problemTypes[problem.type].label}</span>
            </CardTitle>
            <p className="text-gray-600 mt-1">{problem.address}</p>
            {problem.description && (
              <p className="text-sm text-gray-700 mt-2">
                {problem.description}
              </p>
            )}
          </div>
          <Button variant="ghost" onClick={onClose}>
            ×
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div className="flex items-center justify-between flex-wrap gap-2">
            <div className="flex items-center space-x-2">
              <Badge className={urgencyColors[problem.urgency]}>
                {problem.urgency === "low"
                  ? "Baixa"
                  : problem.urgency === "medium"
                    ? "Média"
                    : "Alta"}{" "}
                Urgência
              </Badge>
              <Badge className={statusColors[problem.status]}>
                {problem.status === "reported"
                  ? "Reportado"
                  : problem.status === "confirmed"
                    ? "Confirmado"
                    : problem.status === "in_progress"
                      ? "Em Andamento"
                      : "Resolvido"}
              </Badge>
            </div>
            <span className="text-sm text-gray-500">
              {problem.confirmations} confirmações
            </span>
          </div>

          {problem.photo && (
            <div className="mt-3">
              <img
                src={problem.photo}
                alt="Foto do problema"
                className="w-full max-w-sm h-48 object-cover rounded-lg"
              />
            </div>
          )}

          <p className="text-sm text-gray-600">
            Reportado por {problem.reporter} em {problem.date}
            {problem.neighborhood && (
              <span className="ml-2">• {problem.neighborhood}</span>
            )}
          </p>

          {/* Botões de ação */}
          <div className="flex flex-wrap gap-2">
            {problem.status !== "resolved" && (
              <Button
                onClick={() => onAddConfirmation(problem.id)}
                className="flex-1"
                variant="outline"
              >
                Confirmar Problema (+10 pontos)
              </Button>
            )}
            {problem.status === "confirmed" && (
              <Button
                onClick={() => onUpdateStatus(problem.id, "in_progress")}
                className="flex-1"
                variant="outline"
              >
                Marcar Em Andamento
              </Button>
            )}
            {problem.status === "in_progress" && (
              <Button
                onClick={() => onUpdateStatus(problem.id, "resolved")}
                className="flex-1 bg-green-600 hover:bg-green-700"
              >
                Marcar como Resolvido
              </Button>
            )}
          </div>

          {/* Botões de interação social */}
          <div className="flex items-center justify-between pt-2 border-t">
            <div className="flex items-center space-x-4">
              <button
                onClick={handleLike}
                className="flex items-center space-x-1 text-sm text-gray-600 hover:text-red-500 transition-colors"
              >
                <span>❤️</span>
                <span>{problem.likes || 0}</span>
              </button>

              <button
                onClick={handleShare}
                className="flex items-center space-x-1 text-sm text-gray-600 hover:text-blue-500 transition-colors"
              >
                <span>📤</span>
                <span>Compartilhar</span>
              </button>

              <span className="text-sm text-gray-500">
                💬 {problem.comments?.length || 0} comentários
              </span>
            </div>
          </div>

          {/* Seção de avaliação (apenas para problemas resolvidos) */}
          {onRate && (
            <RatingSection
              rating={problem.rating}
              onRate={onRate}
              problemId={problem.id}
              status={problem.status}
            />
          )}

          {/* Seção de comentários */}
          {onAddComment && (
            <CommentsSection
              comments={problem.comments || []}
              onAddComment={onAddComment}
              problemId={problem.id}
            />
          )}
        </div>
      </CardContent>
    </Card>
  );
}
