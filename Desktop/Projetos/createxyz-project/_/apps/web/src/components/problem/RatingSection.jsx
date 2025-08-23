import React, { useState } from "react";
import { Button } from "../ui/button";

export function RatingSection({ rating, onRate, problemId, status }) {
  const [selectedRating, setSelectedRating] = useState(rating || 0);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Só permitir avaliação se o problema foi resolvido e ainda não foi avaliado
  if (status !== "resolved") return null;

  const handleRate = async (stars) => {
    if (rating) return; // Já foi avaliado
    
    setIsSubmitting(true);
    setSelectedRating(stars);
    await onRate(problemId, stars);
    setIsSubmitting(false);
  };

  const renderStars = () => {
    return Array.from({ length: 5 }, (_, index) => {
      const starNumber = index + 1;
      const isFilled = starNumber <= (rating || selectedRating);
      
      return (
        <button
          key={index}
          onClick={() => !rating && handleRate(starNumber)}
          disabled={rating || isSubmitting}
          className={`text-2xl ${
            isFilled ? "text-yellow-400" : "text-gray-300"
          } ${
            !rating && !isSubmitting ? "hover:text-yellow-400 cursor-pointer" : "cursor-default"
          } transition-colors`}
        >
          ⭐
        </button>
      );
    });
  };

  return (
    <div className="border-t pt-4 mt-4">
      <h4 className="font-semibold text-sm mb-3 flex items-center">
        ⭐ Avaliação da Resolução
      </h4>
      
      {rating ? (
        <div className="flex items-center space-x-2">
          <div className="flex">{renderStars()}</div>
          <span className="text-sm text-gray-600">
            Problema avaliado com {rating} estrela{rating !== 1 ? "s" : ""}
          </span>
        </div>
      ) : (
        <div className="space-y-2">
          <p className="text-sm text-gray-600">
            Como você avalia a resolução deste problema?
          </p>
          <div className="flex items-center space-x-1">
            {renderStars()}
          </div>
          <p className="text-xs text-gray-500">
            Sua avaliação ajuda a melhorar os serviços públicos
          </p>
        </div>
      )}
    </div>
  );
}