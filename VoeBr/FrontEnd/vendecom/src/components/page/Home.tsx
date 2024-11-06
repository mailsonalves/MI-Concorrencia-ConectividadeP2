import React, { useState, useEffect } from "react";
import { Input } from "../ui/input";
import { Button } from "../ui/button";
import PassagemCard from "../ui/passagemCard";
import { Search } from "lucide-react";
import { ScrollArea } from "../ui/scroll-area";
import axios from "axios";
import { FourSquare } from "react-loading-indicators";

interface Passagem {
  origem: string;
  destino: string;
  preco?: string; // Inclua a propriedade se a API retornar isso
  imagem_companhia: string; // Inclua a propriedade se a API retornar isso
  companhia_aerea: string;
  id: string;
}

function Home() {
  const [origem, setOrigem] = useState("");
  const [destino, setDestino] = useState("");
  const [voos, setVoos] = useState<Passagem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAllVoos = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://127.0.0.1:8002/voo/`);
      setVoos(response.data.voos || []); // Ajuste conforme a estrutura real da resposta
    } catch (err) {
      console.error(err);
      setError("Erro ao carregar todos os voos");
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
        `http://127.0.0.1:8002/voo/find/?origem=${origem}&destino=${destino}`
      );
      setVoos(response.data.voos || []); // Ajuste conforme a estrutura real
    } catch (err) {
      console.error(err);
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
      <div className=" flex gap-4 justify-center items-center  text-white font-bold rounded-bl-2xl rounded-br-2xl text-4xl py-5 bg-black border-t-2 border-white">
        <form onSubmit={handleSearch} className="flex items-center mx-auto gap-5">
          <Input
            placeholder="Origem"
            value={origem}
            onChange={(e) => setOrigem(e.target.value)}
            className="bg-white text-black caret-black"
          />
          <Input
            placeholder="Destino"
            value={destino}
            onChange={(e) => setDestino(e.target.value)}
            className="bg-white text-black caret-black"
          />
          <Button type="submit" variant={"secondary"}>
            <Search />
            Pesquisar
          </Button>
        </form>
      </div>

      <div className="flex justify-center">
        {loading && <div className="mt-28">
          <FourSquare  color="#000000" size="medium" text="" textColor="" />
        </div>}
        {error && <p className="text-red-500">{error}</p>}
      </div>

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
              id_voo={passagem.id}
            />
          ))
        ) : (
          !loading && (
            <div className="flex flex-col items-center justify-center ">
              <p className="text-center font-bold mt-10 text-red-600">
              Não encontramos voos correspondentes à sua pesquisa.
              </p>
              
              <img
                className="h-96 mt-4"
                src="/notfoundticket.png"
                alt="Imagem de passagem não encontrada"
              />
            </div>
          )
        )}
      </ScrollArea>
    </section>
  );
}

export default Home;
