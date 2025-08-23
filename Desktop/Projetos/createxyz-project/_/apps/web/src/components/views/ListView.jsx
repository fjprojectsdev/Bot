import React from "react";
import {
  Card,
  CardContent,
} from "../ui/card";
import { Button } from "../ui/button";
import { Badge } from "../ui/badge";
import {
  problemTypes,
  urgencyColors,
  statusColors,
} from "../../lib/constants";

function ProblemListItem({ problem, onSelectProblem }) {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-3 flex-1">
            <div
              className={`w-10 h-10 rounded-full ${problemTypes[problem.type].color} flex items-center justify-center text-white relative`}
            >
              {problemTypes[problem.type].icon}
              {problem.status === "resolved" && (
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full border border-white text-xs">
                  ✓
                </div>
              )}
            </div>
            <div className="flex-1">
              <h3 className="font-semibold">
                {problemTypes[problem.type].label}
              </h3>
              <p className="text-sm text-gray-600">{problem.address}</p>
              {problem.description && (
                <p className="text-sm text-gray-700 mt-1">
                  {problem.description}
                </p>
              )}
              <div className="flex items-center space-x-2 mt-2">
                <Badge className={urgencyColors[problem.urgency]}>
                  {problem.urgency === "low"
                    ? "Baixa"
                    : problem.urgency === "medium"
                      ? "Média"
                      : "Alta"}
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
                <span className="text-xs text-gray-500">
                  {problem.confirmations} confirmações
                </span>
              </div>
            </div>
          </div>
          <Button
            onClick={() => onSelectProblem(problem)}
            variant="outline"
            size="sm"
          >
            Ver Detalhes
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

export function ListView({ problems, onSelectProblem }) {
  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">
          Lista de Problemas
        </h2>
        <p className="text-gray-600">{problems.length} problemas encontrados</p>
      </div>
      {problems.length === 0 ? (
        <Card>
          <CardContent className="p-8 text-center text-gray-500">
            <div className="text-4xl mb-4">🔍</div>
            <p>Nenhum problema encontrado com os filtros aplicados.</p>
          </CardContent>
        </Card>
      ) : (
        problems.map((problem) => (
          <ProblemListItem
            key={problem.id}
            problem={problem}
            onSelectProblem={onSelectProblem}
          />
        ))
      )}
    </div>
  );
}
