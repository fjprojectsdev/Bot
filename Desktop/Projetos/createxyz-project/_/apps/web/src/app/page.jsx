"use client";

import React from "react";
import { useUrbanMap } from "../hooks/useUrbanMap";
import { Header } from "../components/layout/Header";
import { Navigation } from "../components/layout/Navigation";
import { ProblemFilters } from "../components/problem/ProblemFilters";
import { MapView } from "../components/views/MapView";
import { MapViewReal } from "../components/views/MapViewReal";
import { ListView } from "../components/views/ListView";
import { ReportsView } from "../components/views/ReportsView";
import { NotificationsView } from "../components/views/NotificationsView";
import { ProfileView } from "../components/views/ProfileView";
import { EventsView } from "../components/views/EventsView";
import { RewardsView } from "../components/views/RewardsView";
import { ActivityView } from "../components/views/ActivityView";
import { ProblemDetailsCard } from "../components/problem/ProblemDetailsCard";

function Page() {
  const {
    problems,
    filteredProblems,
    userPoints,
    userBadges,
    selectedProblem,
    setSelectedProblem,
    view,
    setView,
    filters,
    setFilters,
    userLocation,
    notifications,
    unreadCount,
    userEvents,
    redeemedRewards,
    userActivities,
    addConfirmation,
    submitReport,
    updateProblemStatus,
    addComment,
    rateProblem,
    joinEvent,
    leaveEvent,
    redeemReward,
    likeProblem,
    shareProblem,
    markNotificationAsRead,
  } = useUrbanMap();

  const renderView = () => {
    switch (view) {
      case "map":
        // Use real Google Maps if API key is available, otherwise fallback to simulation
        const useRealMap = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;
        const MapComponent = useRealMap ? MapViewReal : MapView;

        return (
          <MapComponent
            problems={filteredProblems}
            userLocation={userLocation}
            selectedProblem={selectedProblem}
            onSelectProblem={setSelectedProblem}
            onAddConfirmation={addConfirmation}
            onUpdateStatus={updateProblemStatus}
            onSubmitReport={submitReport}
          />
        );

      case "list":
        return (
          <>
            <ListView
              problems={filteredProblems}
              onSelectProblem={setSelectedProblem}
            />
            {selectedProblem && (
              <div className="fixed inset-0 bg-black bg-opacity-50 z-40 flex justify-center items-center p-4">
                <div className="w-full max-w-lg max-h-[90vh] overflow-y-auto">
                  <ProblemDetailsCard
                    problem={selectedProblem}
                    onClose={() => setSelectedProblem(null)}
                    onAddConfirmation={addConfirmation}
                    onUpdateStatus={updateProblemStatus}
                    onAddComment={addComment}
                    onRate={rateProblem}
                    onLike={likeProblem}
                    onShare={shareProblem}
                  />
                </div>
              </div>
            )}
          </>
        );

      case "events":
        return (
          <EventsView
            userEvents={userEvents}
            onJoinEvent={joinEvent}
            onLeaveEvent={leaveEvent}
          />
        );

      case "rewards":
        return (
          <RewardsView
            userPoints={userPoints}
            redeemedRewards={redeemedRewards}
            onRedeemReward={redeemReward}
          />
        );

      case "activity":
        return <ActivityView />;

      case "reports":
        return <ReportsView problems={problems} />;

      case "notifications":
        return (
          <NotificationsView
            notifications={notifications}
            onMarkAsRead={markNotificationAsRead}
          />
        );

      case "profile":
        return (
          <ProfileView
            userPoints={userPoints}
            userBadges={userBadges}
            problems={problems}
          />
        );

      default:
        return null;
    }
  };

  return (
    <div className="w-screen min-h-screen bg-gray-50">
      <Header
        userPoints={userPoints}
        unreadCount={unreadCount}
        onSetView={setView}
      />
      <Navigation
        currentView={view}
        onSetView={setView}
        unreadCount={unreadCount}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {(view === "map" || view === "list") && (
          <ProblemFilters filters={filters} onFiltersChange={setFilters} />
        )}

        {renderView()}

        {/* Enhanced Problem Details for Map View */}
        {view === "map" && selectedProblem && (
          <div className="mt-6">
            <ProblemDetailsCard
              problem={selectedProblem}
              onClose={() => setSelectedProblem(null)}
              onAddConfirmation={addConfirmation}
              onUpdateStatus={updateProblemStatus}
              onAddComment={addComment}
              onRate={rateProblem}
              onLike={likeProblem}
              onShare={shareProblem}
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default Page;
