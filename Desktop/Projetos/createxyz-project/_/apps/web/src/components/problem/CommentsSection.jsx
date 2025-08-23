import React, { useState } from "react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";

export function CommentsSection({ comments = [], onAddComment, problemId }) {
  const [newComment, setNewComment] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;

    setIsSubmitting(true);
    await onAddComment(problemId, newComment.trim());
    setNewComment("");
    setIsSubmitting(false);
  };

  return (
    <div className="border-t pt-4 mt-4">
      <h4 className="font-semibold text-sm mb-3 flex items-center">
        💬 Comentários ({comments.length})
      </h4>
      
      {/* Lista de comentários */}
      <div className="space-y-3 mb-4 max-h-40 overflow-y-auto">
        {comments.length === 0 ? (
          <p className="text-gray-500 text-sm italic">
            Seja o primeiro a comentar sobre este problema.
          </p>
        ) : (
          comments.map((comment) => (
            <div key={comment.id} className="bg-gray-50 rounded-lg p-3">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="font-medium text-sm">{comment.author}</span>
                    <span className="text-xs text-gray-500">{comment.time}</span>
                  </div>
                  <p className="text-sm text-gray-700">{comment.text}</p>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Formulário para novo comentário */}
      <form onSubmit={handleSubmit} className="flex space-x-2">
        <Input
          placeholder="Adicione um comentário..."
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          className="flex-1"
          maxLength={300}
        />
        <Button 
          type="submit" 
          size="sm"
          disabled={isSubmitting || !newComment.trim()}
        >
          {isSubmitting ? "..." : "Enviar"}
        </Button>
      </form>
    </div>
  );
}