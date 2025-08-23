import React from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../ui/card";
import { Badge } from "../ui/badge";
import { userActivity } from "../../lib/constants";

function ActivityItem({ activity }) {
  return (
    <div className="flex items-start space-x-4 p-4 border-l-4 border-blue-200 bg-blue-50/30 rounded-r-lg">
      <div className="flex-shrink-0">
        <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
          <span className="text-lg">{activity.icon}</span>
        </div>
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between">
          <p className="text-sm font-medium text-gray-900">
            {activity.description}
          </p>
          <Badge className="bg-green-100 text-green-800">
            +{activity.points} pts
          </Badge>
        </div>
        <p className="text-xs text-gray-500 mt-1">{activity.time}</p>
      </div>
    </div>
  );
}

export function ActivityView() {
  const totalPointsEarned = userActivity.reduce((sum, activity) => sum + activity.points, 0);
  const activitiesThisWeek = userActivity.filter(activity => 
    activity.time.includes('hora') || activity.time.includes('dia')
  ).length;
  
  const activityTypes = {
    report: { label: "Reportes", count: userActivity.filter(a => a.type === 'report').length },
    confirmation: { label: "Confirmações", count: userActivity.filter(a => a.type === 'confirmation').length },
    comment: { label: "Comentários", count: userActivity.filter(a => a.type === 'comment').length },
    event: { label: "Eventos", count: userActivity.filter(a => a.type === 'event').length }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Histórico de Atividades</h2>
        <p className="text-gray-600">Acompanhe suas contribuições para a cidade</p>
      </div>

      {/* Estatísticas da atividade */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">{userActivity.length}</div>
              <div className="text-sm text-gray-600">Atividades Total</div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600">{totalPointsEarned}</div>
              <div className="text-sm text-gray-600">Pontos Ganhos</div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600">{activitiesThisWeek}</div>
              <div className="text-sm text-gray-600">Esta Semana</div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-orange-600">⭐</div>
              <div className="text-sm text-gray-600">Usuário Ativo</div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Breakdown por tipo de atividade */}
      <Card>
        <CardHeader>
          <CardTitle>Resumo por Tipo de Atividade</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {Object.entries(activityTypes).map(([key, type]) => (
              <div key={key} className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-gray-900">{type.count}</div>
                <div className="text-sm text-gray-600">{type.label}</div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Timeline de atividades */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <span>📅</span>
            <span>Timeline de Atividades</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {userActivity.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <div className="text-4xl mb-4">📝</div>
                <p>Nenhuma atividade registrada ainda.</p>
                <p className="text-sm mt-2">Comece reportando um problema para ver seu histórico aqui!</p>
              </div>
            ) : (
              userActivity.map((activity) => (
                <ActivityItem key={activity.id} activity={activity} />
              ))
            )}
          </div>
        </CardContent>
      </Card>

      {/* Conquistas e milestones */}
      <Card className="bg-gradient-to-r from-yellow-50 to-orange-50 border-yellow-200">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <span>🏆</span>
            <span>Próximas Conquistas</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-white rounded-lg border">
              <div className="flex items-center space-x-3">
                <span className="text-2xl">🔥</span>
                <div>
                  <div className="font-medium">Streak de 7 dias</div>
                  <div className="text-sm text-gray-600">Seja ativo por 7 dias consecutivos</div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm font-medium">3/7 dias</div>
                <div className="text-xs text-gray-500">+200 pontos</div>
              </div>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-white rounded-lg border">
              <div className="flex items-center space-x-3">
                <span className="text-2xl">📊</span>
                <div>
                  <div className="font-medium">Reporter Expert</div>
                  <div className="text-sm text-gray-600">Reporte 10 problemas</div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm font-medium">1/10 reportes</div>
                <div className="text-xs text-gray-500">+500 pontos</div>
              </div>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-white rounded-lg border">
              <div className="flex items-center space-x-3">
                <span className="text-2xl">👥</span>
                <div>
                  <div className="font-medium">Participante Ativo</div>
                  <div className="text-sm text-gray-600">Participe de 5 eventos</div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm font-medium">1/5 eventos</div>
                <div className="text-xs text-gray-500">+300 pontos</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}