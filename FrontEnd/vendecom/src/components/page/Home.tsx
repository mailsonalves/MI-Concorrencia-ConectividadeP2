import React, { useState, useEffect } from "react";
import { Input } from "../ui/input";
import { Button } from "../ui/button";
import PassagemCard from "../ui/passagemCard";
import { Search } from "lucide-react";
import { ScrollArea } from "../ui/scroll-area";
import axios from "axios";

interface Passagem {
  origem: string;
  destino: string;
  preco?: string; // Inclua a propriedade se a API retornar isso
  imagem_companhia: string; // Inclua a propriedade se a API retornar isso
  companhia_aerea: string
  id: string;
}

function Home() {
  const [origem, setOrigem] = useState("");
  const [destino, setDestino] = useState("");
  const [voos, setvoos] = useState<Passagem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAllVoos = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://127.0.0.1:8000/voo/`);
      setvoos(response.data.voos || []); // Ajuste conforme a estrutura real da resposta
    } catch (err) {
      console.error(err);
      setError("Erro ao carregar todas as voos");
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/voo/find/?origem=${origem}&destino=${destino}`
      );
      setvoos(response.data.voos || []); // Ajuste conforme a estrutura real
      console.log(voos);
      console.log(voos.length);
    } catch (err) {
      console.error(err); // Log do erro
      setError("Erro ao buscar voos");
    } finally {
      setLoading(false);
      setDestino("");
      setOrigem("");
    }
  };
  useEffect(() => {
    fetchAllVoos();
  }, []);

  return (
    <section className="max-w-4xl mx-auto">
      <div className="mt-10">
        <form
          onSubmit={handleSearch}
          className="flex items-center mx-auto gap-5"
        >
          <Input
            placeholder="Origem"
            value={origem}
            onChange={(e) => setOrigem(e.target.value)}
          />
          <Input
            placeholder="Destino"
            value={destino}
            onChange={(e) => setDestino(e.target.value)}
          />
          <Button type="submit">
            {" "}
            <Search />
            Pesquisar
          </Button>
        </form>
      </div>

      {loading && <p>Carregando...</p>}
      {error && <p className="text-red-500">{error}</p>}

      <ScrollArea className="h-screen">
        {voos.length > 0 ? (
          voos.map((passagem, index) => (
            <PassagemCard
              key={index}
              origem={passagem.origem}
              destino={passagem.destino}
              preco={passagem.preco || "100"}
              imagemSrc={passagem.imagem_companhia}
              companhia_aerea={passagem.companhia_aerea}
              id_voo ={passagem.id}
            />
          ))
        ) : (
          <p>Nenhuma voo encontrada.</p>
        )}
      </ScrollArea>
    </section>
  );
}

export default Home;
