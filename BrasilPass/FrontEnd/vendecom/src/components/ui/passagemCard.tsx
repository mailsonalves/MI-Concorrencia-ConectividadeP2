import React, { useState, useCallback } from "react";
import axios from "axios";
import { Plane, Smile, Frown } from "lucide-react";
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
  companhia_aerea: string;
  id_voo: string;
}

const PassagemCard: React.FC<PassagemCardProps> = ({
  id_voo,
  origem,
  destino,
  preco,
  imagemSrc,
  companhia_aerea,
}) => {
  const [isDialogOpen, setIsDialogOpen] = useState<boolean>(false);
  const [assento, setAssento] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [sucess, setSucess] = useState<string | null>(null);

  const handleVoo = () => {
    setIsDialogOpen(true);
  };

  const handleBuyPass = useCallback(async () => {
    setLoading(true);
    setError(null);
    setSucess(null); // Limpa a mensagem de sucesso anterior
  
    const user = localStorage.getItem("user");
    const token = localStorage.getItem("token");
  
    if (!user || !token) {
      setError("Efetue o login para continuar.");
      setLoading(false);
      return;
    }
  
    const userDecode = JSON.parse(user);
  
    const requestData = {
      id_voo,
      id_passageiro: userDecode.id,
      cpf: userDecode.cpf,
      assento,
      companhia_aerea,
    };
  
    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/ticket/buy_ticket/?user_id=${userDecode.id}`,
        requestData,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
  
      // Confirmação visual de sucesso e reset do estado
      setSucess("Passagem comprada com sucesso!");
      setTimeout(() => setSucess(null), 5000); // Remove a mensagem de sucesso após 5 segundos

    } catch (err) {
      console.error("Erro ao comprar passagem:", err);
  
      let errorMsg = "Erro ao carregar todas as passagens.";
      if (err.response) {
        if (err.response.status === 401) {
          errorMsg = "Sessão expirada. Faça login novamente.";
        } else if (err.response.status === 500) {
          errorMsg = "Erro no servidor. Tente novamente mais tarde.";
        } 
        else if (err.response.status === 400) {
          errorMsg = "Assento Ocupado";
        }
        else {
          errorMsg = err.response.data?.detail || errorMsg;
        }
      }
      setError(errorMsg);
      setTimeout(() => setError(null), 5000);
    } finally {
      setLoading(false);
    }
  }, [id_voo, assento, companhia_aerea]);
  

  return (
    <div>
      <div
        onClick={handleVoo}
        className="flex mx-10 cursor-pointer items-center my-6 gap-6 border-slate-500 border rounded-2xl shadow-black  hover:scale-105 transition-transform duration-300"

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
              <Select onValueChange={(value) => setAssento(value)}>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Selecione o assento" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="A1">A1</SelectItem>
                  <SelectItem value="A2">A2</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          <div className="text-center">
            {error && (
              <div>
                <p className="flex justify-center gap-2 text-xs items-center font-bold text-red-600 col-span-4">
                  <span>
                    <Frown />
                  </span>
                  {error}
                </p>
              </div>
            )}
            {sucess && (
              <div>
                <p className="flex justify-center gap-2 text-xs items-center font-bold text-green-600 col-span-4">
                  <span>
                    <Smile />
                  </span>
                  {sucess}
                </p>
              </div>
            )}
          </div>
          <DialogFooter className="flex justify-center">
            <Button onClick={handleBuyPass} disabled={loading}>
              {loading ? "Processando..." : "Comprar"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default PassagemCard;
