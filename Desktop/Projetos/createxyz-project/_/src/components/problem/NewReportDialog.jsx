import React, { useState, useCallback } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../ui/dialog";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { problemTypes } from "../../lib/constants";
import useUpload from "../../utils/useUpload";


export function NewReportDialog({ userLocation, onSubmit }) {
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newReport, setNewReport] = useState({
    type: "",
    address: "",
    description: "",
    photo: null,
  });
  const [loading, setLoading] = useState(false);
  const [upload, { loading: uploadLoading }] = useUpload();
  
  const handlePhotoUpload = useCallback(async (file) => {
    if (!file) return null;
    try {
      const reader = new FileReader();
      return new Promise((resolve) => {
        reader.onload = async (e) => {
          const { url, error } = await upload({ base64: e.target.result });
          if (error) {
            console.error("Erro no upload:", error);
            resolve(null);
          } else {
            resolve(url);
          }
        };
        reader.readAsDataURL(file);
      });
    } catch (error) {
      console.error("Erro no upload:", error);
      return null;
    }
  }, [upload]);

  const handleSubmit = async () => {
    if (!newReport.type || !newReport.address) return;
    setLoading(true);

    let photoUrl = null;
    if (newReport.photo) {
      photoUrl = await handlePhotoUpload(newReport.photo);
    }
    
    await onSubmit({ ...newReport, photoUrl });

    setNewReport({ type: "", address: "", description: "", photo: null });
    setLoading(false);
    setIsDialogOpen(false);
  };

  return (
    <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
      <DialogTrigger asChild>
        <Button className="bg-blue-600 hover:bg-blue-700">
          + Reportar Problema
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Reportar Novo Problema</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <Select
            value={newReport.type}
            onValueChange={(value) =>
              setNewReport({ ...newReport, type: value })
            }
          >
            <SelectTrigger>
              <SelectValue placeholder="Tipo do problema" />
            </SelectTrigger>
            <SelectContent>
              {Object.entries(problemTypes).map(([key, type]) => (
                <SelectItem key={key} value={key}>
                  {type.icon} {type.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Input
            placeholder="Endereço ou localização"
            value={newReport.address}
            onChange={(e) =>
              setNewReport({ ...newReport, address: e.target.value })
            }
          />
          <textarea
            placeholder="Descrição detalhada do problema"
            value={newReport.description}
            onChange={(e) =>
              setNewReport({
                ...newReport,
                description: e.target.value,
              })
            }
            className="w-full h-20 px-3 py-2 border border-gray-300 rounded-md resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Foto (opcional)
            </label>
            <input
              type="file"
              accept="image/*"
              onChange={(e) =>
                setNewReport({
                  ...newReport,
                  photo: e.target.files[0],
                })
              }
              className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
          </div>
          {userLocation && (
            <div className="text-sm text-green-600 flex items-center">
              📍 Localização detectada automaticamente
            </div>
          )}
          <Button
            onClick={handleSubmit}
            className="w-full"
            disabled={loading || uploadLoading || !newReport.type || !newReport.address}
          >
            {loading || uploadLoading ? "Enviando..." : "Enviar Relatório (+50 pontos)"}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
