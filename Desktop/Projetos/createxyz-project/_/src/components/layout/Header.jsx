import React from "react";
import { Badge } from "../ui/badge";
import { Button } from "../ui/button";

export function Header({ userPoints, unreadCount, onSetView }) {
  return (
    <div className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">
              M
            </div>
            <h1 className="text-xl font-bold text-gray-900">Mapa Urbano</h1>
          </div>
          <div className="flex items-center space-x-4">
            <div className="relative">
              <button
                onClick={() => onSetView("notifications")}
                className="relative p-2 text-gray-600 hover:text-gray-900"
              >
                🔔
                {unreadCount > 0 && (
                  <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                    {unreadCount}
                  </span>
                )}
              </button>
            </div>
            <Badge variant="secondary" className="text-blue-600">
              {userPoints} pontos
            </Badge>
            <Button
              variant="outline"
              size="sm"
              onClick={() => onSetView("profile")}
            >
              Perfil
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
