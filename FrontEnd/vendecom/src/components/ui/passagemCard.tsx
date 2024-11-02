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

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface PassagemCardProps {
  origem: string;
  destino: string;
  preco: string;
  imagemSrc: string;
}

const PassagemCard: React.FC<PassagemCardProps> = ({
  origem,
  destino,
  preco,
  imagemSrc,
}) => {
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const handleVoo = () => {
    setIsDialogOpen(true);
  };

  return (
    <div>
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
          <p className="text-xs">A partir de</p>
          <p className="text-xl font-semibold">R$ {preco}</p>
        </div>
      </div>

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogTrigger asChild>
          <div />
        </DialogTrigger>

        <DialogContent className="sm:max-w-[725px]">
          <DialogHeader>
            <DialogTitle>Comprar passagem</DialogTitle>
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
              <p className="text-sm">Valor</p>

                <p className="text-xl font-semibold">R$ {preco}</p>
                <Select >
                  <SelectTrigger className="w-[180px]" >
                    <SelectValue placeholder="Selecione o assento" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="A1">A1</SelectItem>
                    <SelectItem value="A2">A2</SelectItem>
                  </SelectContent>
                </Select>

            </div>
          </div>

          <DialogFooter className="flex justify-center">
            <Button onClick={() => setIsDialogOpen(false)}>Comprar</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default PassagemCard;
