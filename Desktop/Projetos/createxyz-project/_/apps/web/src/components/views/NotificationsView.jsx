import React from "react";
import { Card, CardContent } from "../ui/card";

export function NotificationsView({ notifications, onMarkAsRead }) {
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold text-gray-900">Notificações</h2>
      {notifications.length === 0 ? (
        <Card>
          <CardContent className="p-8 text-center text-gray-500">
            <div className="text-4xl mb-4">🔔</div>
            <p>Nenhuma notificação no momento.</p>
          </CardContent>
        </Card>
      ) : (
        notifications.map((notification) => (
          <Card
            key={notification.id}
            className={`cursor-pointer transition-colors ${
              notification.unread ? "bg-blue-50 border-blue-200" : ""
            }`}
            onClick={() => onMarkAsRead(notification.id)}
          >
            <CardContent className="p-4">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <p
                    className={`${notification.unread ? "font-semibold" : ""}`}
                  >
                    {notification.message}
                  </p>
                  <p className="text-sm text-gray-500 mt-1">
                    {notification.time}
                  </p>
                </div>
                {notification.unread && (
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                )}
              </div>
            </CardContent>
          </Card>
        ))
      )}
    </div>
  );
}
