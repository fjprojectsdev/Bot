import React from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../ui/card";
import { Badge } from "../ui/badge";
import { Button } from "../ui/button";
import { problemTypes } from "../../lib/constants";

const statusRanking = [
  { status: "reported", label: "Reportados", color: "bg-blue-500" },
  { status: "confirmed", label: "Confirmados", color: "bg-yellow-500" },
  { status: "in_progress", label: "Em Andamento", color: "bg-orange-500" },
  { status: "resolved", label: "Resolvidos", color: "bg-green-500" },
];

function StatCard({ label, value, colorClass }) {
  return (
    <Card>
      <CardContent className="p-4">
        <div className="text-center">
          <div className={`text-3xl font-bold ${colorClass}`}>{value}</div>
          <div className="text-sm text-gray-600">{label}</div>
        </div>
      </CardContent>
    </Card>
  );
}

export function ReportsView({ problems }) {
  const totalProblems = problems.length;
  const highUrgency = problems.filter((p) => p.urgency === "high").length;
  const resolved = problems.filter((p) => p.status === "resolved").length;
  const totalConfirmations = problems.reduce((acc, p) => acc + p.confirmations, 0);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Relatórios e Analytics</h2>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard label="Problemas Totais" value={totalProblems} colorClass="text-blue-600" />
        <StatCard label="Alta Urgência" value={highUrgency} colorClass="text-red-600" />
        <StatCard label="Resolvidos" value={resolved} colorClass="text-green-600" />
        <StatCard label="Confirmações Totais" value={totalConfirmations} colorClass="text-orange-600" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader><CardTitle>Ranking por Tipo de Problema</CardTitle></CardHeader>
          <CardContent>
            <div className="space-y-3">
              {Object.entries(problemTypes).map(([key, type]) => {
                const count = problems.filter((p) => p.type === key).length;
                const percentage = totalProblems > 0 ? ((count / totalProblems) * 100).toFixed(1) : 0;
                return (
                  <div key={key} className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <span>{type.icon}</span>
                      <span className="text-sm">{type.label}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div className={`h-2 rounded-full ${type.color}`} style={{ width: `${percentage}%` }}></div>
                      </div>
                      <Badge variant="secondary" className="text-xs">{count}</Badge>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle>Status dos Problemas</CardTitle></CardHeader>
          <CardContent>
            <div className="space-y-3">
              {statusRanking.map((item) => {
                const count = problems.filter((p) => p.status === item.status).length;
                const percentage = totalProblems > 0 ? ((count / totalProblems) * 100).toFixed(1) : 0;
                return (
                  <div key={item.status} className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={`w-3 h-3 rounded-full ${item.color}`}></div>
                      <span className="text-sm">{item.label}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div className={`h-2 rounded-full ${item.color}`} style={{ width: `${percentage}%` }}></div>
                      </div>
                      <Badge variant="secondary" className="text-xs">{count} ({percentage}%)</Badge>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader><CardTitle>Recursos Premium 💎</CardTitle></CardHeader>
        <CardContent>
          <div className="border rounded-lg p-4 bg-gradient-to-r from-blue-50 to-purple-50">
            <h4 className="font-semibold text-lg mb-2">Plano Premium</h4>
            <ul className="space-y-2 text-sm text-gray-600 mb-4">
              <li>• 📊 Relatórios detalhados da vizinhança</li>
              <li>• 🔔 Alertas em tempo real via push</li>
              <li>• 📈 Histórico completo de problemas</li>
              <li>• 🗺️ Rotas otimizadas evitando problemas</li>
              <li>• 📱 App mobile exclusivo</li>
              <li>• 🏆 Ranking premium e badges especiais</li>
            </ul>
            <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
              Assinar por R$ 9,90/mês
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
