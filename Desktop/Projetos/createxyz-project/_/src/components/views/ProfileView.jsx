import React from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../ui/card";
import { Badge } from "../ui/badge";

const localRanking = [
  { position: 1, name: "Maria Silva", points: 1250, badge: "🥇" },
  { position: 2, name: "Você", points: 0, badge: "🥈" }, // Points will be replaced
  { position: 3, name: "João Santos", points: 780, badge: "🥉" },
  { position: 4, name: "Ana Costa", points: 650, badge: "🏅" },
  { position: 5, name: "Pedro Lima", points: 520, badge: "🏅" },
];

export function ProfileView({ userPoints, userBadges, problems }) {
  const reportedCount = problems.filter((p) => p.reporter === "Você").length;
  const resolvedCount = problems.filter(
    (p) => p.status === "resolved"
  ).length;

  const ranking = localRanking.map(user => 
    user.name === "Você" ? { ...user, points: userPoints } : user
  );

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Seu Perfil</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="text-center">
              <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-3">
                U
              </div>
              <h3 className="text-xl font-semibold">Usuário Ativo</h3>
              <p className="text-gray-600">{userPoints} pontos acumulados</p>
            </div>

            <div>
              <h4 className="font-semibold mb-2">Conquistas</h4>
              <div className="flex flex-wrap gap-2">
                {userBadges.map((badge) => (
                  <Badge
                    key={badge}
                    variant="secondary"
                    className="bg-yellow-100 text-yellow-800"
                  >
                    🏆 {badge}
                  </Badge>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 pt-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{reportedCount}</div>
                <div className="text-sm text-gray-600">Problemas Reportados</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">23</div>
                <div className="text-sm text-gray-600">Confirmações Feitas</div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">{resolvedCount}</div>
                <div className="text-sm text-gray-600">Problemas Resolvidos</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">⭐</div>
                <div className="text-sm text-gray-600">Nível Guardião</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader>
          <CardTitle>Ranking Local</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {ranking.map((user) => (
              <div
                key={user.position}
                className={`flex items-center justify-between p-2 rounded ${
                  user.name === "Você" ? "bg-blue-50 border border-blue-200" : ""
                }`}
              >
                <div className="flex items-center space-x-3">
                  <span className="text-lg">{user.badge}</span>
                  <span
                    className={`font-medium ${user.name === "Você" ? "text-blue-600" : ""}`}
                  >
                    {user.position}. {user.name}
                  </span>
                </div>
                <span className="text-sm text-gray-600">{user.points} pontos</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
