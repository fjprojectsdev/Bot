import React from "react";
import { Card, CardContent } from "../ui/card";
import { problemTypes } from "../../lib/constants";
import { ProblemDetailsCard } from "../problem/ProblemDetailsCard";
import { NewReportDialog } from "../problem/NewReportDialog";

function MapLegend({ userLocation }) {
  return (
    <div className="absolute top-4 left-4 bg-white rounded-lg shadow-lg p-3 max-w-xs">
      <h3 className="font-semibold text-sm mb-2">Legenda</h3>
      {Object.entries(problemTypes).map(([key, type]) => (
        <div key={key} className="flex items-center space-x-2 text-xs mb-1">
          <div className={`w-3 h-3 rounded-full ${type.color}`}></div>
          <span>{type.label}</span>
        </div>
      ))}
      {userLocation && (
        <div className="flex items-center space-x-2 text-xs mt-2 pt-2 border-t">
          <div className="w-3 h-3 rounded-full bg-blue-600"></div>
          <span>Sua localização</span>
        </div>
      )}
    </div>
  );
}

function MapSimulation({
  problems,
  userLocation,
  onMarkerClick,
}) {
  return (
    <Card>
      <CardContent className="p-0">
        <div className="h-96 bg-gradient-to-br from-green-100 to-blue-100 relative rounded-lg overflow-hidden">
          <div className="absolute inset-0 bg-gray-200 opacity-20"></div>

          {userLocation && (
            <div
              className="absolute w-4 h-4 bg-blue-600 rounded-full border-2 border-white shadow-lg"
              style={{ left: "45%", top: "45%" }}
            >
              <div className="absolute inset-0 bg-blue-600 rounded-full animate-ping opacity-75"></div>
            </div>
          )}

          <MapLegend userLocation={userLocation} />

          {problems.map((problem, index) => (
            <div
              key={problem.id}
              className={`absolute w-8 h-8 rounded-full ${problemTypes[problem.type].color} 
                flex items-center justify-center text-white text-lg cursor-pointer transform hover:scale-110 transition-transform shadow-lg`}
              style={{
                left: `${30 + index * 15}%`,
                top: `${40 + index * 10}%`,
              }}
              onClick={() => onMarkerClick(problem)}
            >
              {problemTypes[problem.type].icon}
              {problem.status === "resolved" && (
                <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border border-white">
                  ✓
                </div>
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

export function MapView({
  problems,
  userLocation,
  selectedProblem,
  onSelectProblem,
  onAddConfirmation,
  onUpdateStatus,
  onSubmitReport,
}) {
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

      <MapSimulation
        problems={problems}
        userLocation={userLocation}
        onMarkerClick={onSelectProblem}
      />

      <ProblemDetailsCard
        problem={selectedProblem}
        onClose={() => onSelectProblem(null)}
        onAddConfirmation={onAddConfirmation}
        onUpdateStatus={onUpdateStatus}
      />
    </div>
  );
}
