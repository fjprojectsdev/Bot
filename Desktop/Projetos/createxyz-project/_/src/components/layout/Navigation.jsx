import React from "react";

const TABS = [
  { key: "map", label: "Mapa", icon: "🗺️" },
  { key: "list", label: "Lista", icon: "📋" },
  { key: "reports", label: "Analytics", icon: "📊" },
  { key: "activity", label: "Atividade", icon: "⚡" },
  { key: "notifications", label: "Notificações", icon: "🔔" },
  { key: "profile", label: "Perfil", icon: "👤" },
];

export function Navigation({ currentView, onSetView, unreadCount }) {
  return (
    <div className="bg-white border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <nav className="flex space-x-4 lg:space-x-6 overflow-x-auto">
          {TABS.map((tab) => (
            <button
              key={tab.key}
              onClick={() => onSetView(tab.key)}
              className={`py-4 px-2 border-b-2 font-medium text-sm relative whitespace-nowrap ${
                currentView === tab.key
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              <span className="mr-1 lg:mr-2">{tab.icon}</span>
              <span className="hidden sm:inline">{tab.label}</span>
              {tab.key === "notifications" && unreadCount > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">
                  {unreadCount}
                </span>
              )}
            </button>
          ))}
        </nav>
      </div>
    </div>
  );
}
