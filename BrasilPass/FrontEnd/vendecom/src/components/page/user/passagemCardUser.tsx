import React, { useState } from "react";
import { Plane } from "lucide-react";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

import axios from "axios";

interface PassagemCardProps {
  origem: string;
  destino: string;
  preco: string;
  imagemSrc: string;
  assento: string;
  id_voo: string;
  id_passagem: string;

}

const PassagemCardUser: React.FC<PassagemCardProps> = ({
  origem,
  destino,
  preco,
  imagemSrc,
  assento,
  id_passagem,
  id_voo
}) => {
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [voo, setVoo] = useState(false);
  
 
  const handleVoo = () => {
    setIsDialogOpen(true);
  };
    const handleDeleteTicket = async () => {
    const token = localStorage.getItem("token");


    try {
      await axios.delete(
        `http://127.0.0.1:8000/ticket/${id_passagem}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      console.log("Ticket deletado com sucesso");
      window.location.reload();
    } catch (err) {
      console.error("Erro ao deletar ticket:", err);
      const errorMsg = err.response?.data?.detail || "Erro ao deletar o ticket.";
      console.error(errorMsg);
    }
  };


  return (
    <div className="">
      <div
        onClick={handleVoo}
        className="flex mx-10 cursor-pointer items-center my-6 gap-6 border-slate-500 border rounded-2xl shadow-black  hover:scale-105 transition-transform duration-300">
        <img
          className="h-36 rounded-tl-2xl rounded-bl-2xl"
          src={imagemSrc}
          alt=""
        />
        <div>
          <div className="flex gap-2">
            <Plane />
            <h1 className="text-xl font-bold">
              Voo de {origem} para {destino}
            </h1>
          </div>
          <p className="text-slate-500 font-bold">passagem</p>
          <div className="flex items-center gap-">
                <p className="text-xl font-bold">Valor:</p>
                <p className="text-xl text-slate-500 font-bold">
                  R$ {preco}
                </p>
              </div>
        </div>
      </div>

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogTrigger asChild>
          <div />
        </DialogTrigger>

        <DialogContent className="sm:max-w-[725px]">
          <DialogHeader>
            <DialogTitle>Informações da Passagem</DialogTitle>
            <DialogDescription>
              Clique em deletar para cancelar sua passagem.
            </DialogDescription>
          </DialogHeader>
          <div className="flex items-center gap-4">
            <img
              className="h-36 rounded-tl-2xl rounded-bl-2xl"
              src={imagemSrc}
              alt=""
            />
            <div className="space-y-1">
              <div className="flex gap-2 ">
                <Plane />
                <h1 className="text-xl font-bold">
                  Voo de {origem} para {destino}
                </h1>
              </div>

              <p className="text-slate-500 font-bold">passagem</p>
              <div className="flex items-center gap-">
                <p className="text-lg font-bold">Valor:</p>
                <p className="text-lg text-slate-500 font-bold">
                  R$ {preco}
                </p>
              </div>
              <div className="flex items-center gap-2">
                <p className="text-lg font-bold">Assento:</p>
                <p className="text-lg text-slate-500 font-bold">
                   {assento}
                </p>
              </div>
              
            </div>
          </div>

          <DialogFooter className="flex justify-center">
            <Button
              variant={"destructive"}
              onClick={handleDeleteTicket}
            >
              Deletar
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default PassagemCardUser;
