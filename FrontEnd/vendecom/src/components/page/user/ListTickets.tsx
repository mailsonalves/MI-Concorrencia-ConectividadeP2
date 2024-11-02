import PassagemCardUser from "./passagemCardUser";
import { ScrollArea } from "@/components/ui/scroll-area";
import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";

interface Passagem {
  origem: string;
  destino: string;
  preco?: string;
  imagemSrc: string;
  assento: string;
  id_voo: string
}

function ListTickets() {
  const [voos, setVoos] = useState<Passagem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getVoo = async () => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/voo/find/?voo_id=${id_voo}`
      );
      setVoo(response.data.voos || []); // Ajuste conforme a estrutura real
    } catch (err) {
      console.error(err); // Log do erro
  
    }
  }

  const fetchAllTickets = useCallback(async () => {
    setLoading(true);
    setError(null);

    const user = localStorage.getItem("user");
    const token = localStorage.getItem("token");

    if (!user || !token) {
      setError("Usuário ou token não encontrado.");
      setLoading(false);
      return;
    }
    const userDecode = JSON.parse(user);

    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/ticket/?user_id=${userDecode.id}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setVoos(response.data.tickets || []);
    } catch (err) {
      console.error("Erro ao carregar passagens:", err);

      const errorMsg = err.response?.data?.detail || "Erro ao carregar todas as passagens.";
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
    
  }, []);

  useEffect(() => {
    fetchAllTickets();
  }, [fetchAllTickets]);

  return (
    <section className="max-w-4xl mx-auto">
      {loading ? (
        <p>Carregando...</p>
      ) : error ? (
        <p className="text-red-500">{error}</p>
      ) : (
        <ScrollArea className="h-screen">
          {voos.length > 0 ? (
            voos.map((passagem, index) => (
              <PassagemCardUser
                key={index}
                origem={passagem.origem}
                destino={passagem.destino}
                preco={passagem.preco || "100"}
                imagemSrc={passagem.imagem_companhia || "/logo.jpeg"}
                assento={passagem.assento}
                id_voo={passagem.id_voo}
              />
            ))
          ) : (
            <p>Nenhuma passagem encontrada.</p>
          )}
        </ScrollArea>
      )}
    </section>
  );
}

export default ListTickets;
