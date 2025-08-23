import React, { useState, useCallback } from "react";
import { APIProvider, Map, Marker } from "@vis.gl/react-google-maps";
import { Card, CardContent } from "../ui/card";
import { problemTypes } from "../../lib/constants";
import { ProblemDetailsCard } from "../problem/ProblemDetailsCard";
import { NewReportDialog } from "../problem/NewReportDialog";

const API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;

export function MapViewReal({
  problems,
  userLocation,
  selectedProblem,
  onSelectProblem,
  onAddConfirmation,
  onUpdateStatus,
  onSubmitReport,
}) {
  const [mapCenter] = useState(
    userLocation || { lat: -23.5505, lng: -46.6333 }
  );

  const handleMarkerClick = useCallback((problem) => {
    onSelectProblem(problem);
  }, [onSelectProblem]);

  const getMarkerIcon = (problem) => {
    const type = problemTypes[problem.type];
    if (!type) return "🔴";
    
    // Adicionar indicador de status
    if (problem.status === "resolved") {
      return "✅";
    }
    return type.icon;
  };

  const getMarkerColor = (problem) => {
    const urgencyColors = {
      low: "#22c55e",
      medium: "#f59e0b", 
      high: "#ef4444"
    };
    return urgencyColors[problem.urgency] || "#6b7280";
  };

  if (!API_KEY) {
    return (
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              Mapa de Problemas Urbanos
            </h2>
            <p className="text-gray-600">{problems.length} problemas encontrados</p>
          </div>
          <NewReportDialog userLocation={userLocation} onSubmit={onSubmitReport} />
        </div>

        <Card>
          <CardContent className="p-8 text-center">
            <div className="text-4xl mb-4">🗺️</div>
            <h3 className="text-lg font-semibold mb-2">Mapa do Google não configurado</h3>
            <p className="text-gray-600 mb-4">
              Para ver o mapa real, é necessário configurar a API Key do Google Maps.
            </p>
            <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
              <p className="text-sm text-yellow-800">
                <strong>Para desenvolvedores:</strong> Configure a variável de ambiente 
                NEXT_PUBLIC_GOOGLE_MAPS_API_KEY com sua chave da API do Google Maps.
              </p>
            </div>
          </CardContent>
        </Card>

        <ProblemDetailsCard
          problem={selectedProblem}
          onClose={() => onSelectProblem(null)}
          onAddConfirmation={onAddConfirmation}
          onUpdateStatus={onUpdateStatus}
        />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">
            Mapa de Problemas Urbanos
          </h2>
          <p className="text-gray-600">{problems.length} problemas encontrados</p>
        </div>
        <NewReportDialog userLocation={userLocation} onSubmit={onSubmitReport} />
      </div>

      {/* Mapa real do Google */}
      <Card>
        <CardContent className="p-0">
          <div className="h-96 w-full rounded-lg overflow-hidden">
            <APIProvider apiKey={API_KEY}>
              <Map
                style={{ width: "100%", height: "100%" }}
                defaultCenter={mapCenter}
                defaultZoom={14}
                gestureHandling="greedy"
                disableDefaultUI={false}
                mapTypeControl={false}
                streetViewControl={false}
                fullscreenControl={false}
              >
                {/* Localização do usuário */}
                {userLocation && (
                  <Marker
                    position={userLocation}
                    title="Sua localização"
                  />
                )}

                {/* Marcadores dos problemas */}
                {problems.map((problem) => (
                  <Marker
                    key={problem.id}
                    position={problem.location}
                    title={`${problemTypes[problem.type]?.label} - ${problem.address}`}
                    onClick={() => handleMarkerClick(problem)}
                  />
                ))}
              </Map>
            </APIProvider>
          </div>
        </CardContent>
      </Card>

      {/* Legenda do mapa */}
      <Card>
        <CardContent className="p-4">
          <h3 className="font-semibold text-sm mb-3">Legenda do Mapa</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
            {Object.entries(problemTypes).map(([key, type]) => (
              <div key={key} className="flex items-center space-x-2 text-sm">
                <span className="text-lg">{type.icon}</span>
                <span className="text-gray-700">{type.label}</span>
              </div>
            ))}
          </div>
          <div className="mt-4 pt-3 border-t">
            <div className="flex items-center space-x-4 text-sm text-gray-600">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                <span>Baixa urgência</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                <span>Média urgência</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                <span>Alta urgência</span>
              </div>
              <div className="flex items-center space-x-2">
                <span>✅</span>
                <span>Resolvido</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Estatísticas por proximidade */}
      {userLocation && (
        <Card className="bg-blue-50 border-blue-200">
          <CardContent className="p-4">
            <h3 className="font-semibold text-sm mb-3 flex items-center">
              📍 Problemas Próximos a Você
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {problems.filter(p => p.status !== "resolved").length}
                </div>
                <div className="text-sm text-gray-600">Problemas Ativos</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-red-600">
                  {problems.filter(p => p.urgency === "high").length}
                </div>
                <div className="text-sm text-gray-600">Alta Urgência</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {problems.filter(p => p.status === "resolved").length}
                </div>
                <div className="text-sm text-gray-600">Resolvidos</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      <ProblemDetailsCard
        problem={selectedProblem}
        onClose={() => onSelectProblem(null)}
        onAddConfirmation={onAddConfirmation}
        onUpdateStatus={onUpdateStatus}
      />
    </div>
  );
}