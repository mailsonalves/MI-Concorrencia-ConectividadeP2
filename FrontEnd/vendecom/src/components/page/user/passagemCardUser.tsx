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

}

const PassagemCardUser: React.FC<PassagemCardProps> = ({
  origem,
  destino,
  preco,
  imagemSrc,
  assento,
  id_voo
}) => {
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [voo, setVoo] = useState(false);
  
 
  const handleVoo = () => {
    setIsDialogOpen(true);
  };
  const handleDeleteUser =async () => {
    const user = localStorage.getItem("user");
    const token = localStorage.getItem("token");

    if (!user || !token) {
      //setError("Usuário ou token não encontrado.");
      //setLoading(false);
      return;
    }
    const userDecode = JSON.parse(user);

    try {
      const response = await axios.delete(
        `http://127.0.0.1:8000/ticket/?user_id=${userDecode.id}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      //setVoos(response.data.tickets || []);
    } catch (err) {
      console.error("Erro ao carregar passagens:", err);

      const errorMsg = err.response?.data?.detail || "Erro ao carregar todas as passagens.";
      //setError(errorMsg);
    } 
  };

  return (
    <div className="">
      <div
        onClick={handleVoo}
        className="flex cursor-pointer items-center my-6 gap-6 border-slate-500 border-2 rounded-2xl shadow-black hover:shadow-xl hover:drop-shadow-xl transition-shadow duration-300"
      >
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
              Finalize a compra para o voo com destino a {destino}.
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
              onClick={() => setIsDialogOpen(false)}
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
