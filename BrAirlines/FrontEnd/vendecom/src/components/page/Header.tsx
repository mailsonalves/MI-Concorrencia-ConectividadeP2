import { useState, useEffect } from "react";
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuIndicator,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  navigationMenuTriggerStyle,
  NavigationMenuViewport,
} from "@/components/ui/navigation-menu";
import { Link } from "@radix-ui/react-navigation-menu";
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
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuPortal,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import { Label } from "@radix-ui/react-label";
import { Input } from "../ui/input";
import axios from "axios";
import { isUserLoggedIn, logout } from "@/utils/Auth";
import { LogOut, User, Ticket } from "lucide-react";

import { Button } from "@/components/ui/button";

function Header() {
  const [user, setUser] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [cpf, setcCpf] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const [isOpen2, setIsOpen2] = useState(false);
  const [isLogged, setIsLogged] = useState(false);

  useEffect(() => {
    setIsLogged(isUserLoggedIn());
  }, []);
  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem("token");
      if (token) {
        const user = localStorage.getItem("user");
        if (user) {
          setUser(JSON.parse(user));
        }
      }
    };

    fetchUser();
  }, []);
  const handleLogout = async () => {
    logout();
    window.location.href = "/";
  };
  const handleCadastro = async () => {
    if (!username || !password || !name || !cpf) {
      setError("Por favor, preencha todos os campos.");
      return;
    }

    const data = {
      username: username,
      password: password,
      nome: name,
      cpf: cpf,
    };

    try {
      const response = await axios.post("http://127.0.0.1:8001/user/", data);
      
    } catch (err) {
      console.error(err.response ? err.response.data : err);
      if (err.response && err.response.data) {
        setError(
          err.response.data.detail ||
            "Cadastro falhou. Verifique suas credenciais."
        );
      } else {
        setError("Erro de rede. Tente novamente mais tarde.");
      }
    }
  };

  const handleLogin = async () => {
    if (!username || !password) {
      setError("Por favor, preencha todos os campos.");
      return;
    }

    const data = new URLSearchParams({ username, password });

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/auth/token",
        data,
        {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        }
      );

      const { access_token: token } = response.data;
      localStorage.setItem("token", token); // Save token in localStorage
      setIsOpen(false);

      // Fetch user information after successful login
      try {
        const userResponse = await axios.get("http://127.0.0.1:8001/user/", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (userResponse.data) {
          localStorage.setItem("user", JSON.stringify(userResponse.data)); // Save user info in localStorage
          setUser(userResponse.data);
        }
      } catch (userError) {
        console.error("Erro ao obter informações do usuário:", userError);
        setError("Falha ao carregar informações do usuário.");
      }

      window.location.reload();
    } catch (err) {
      console.error(err);
      const errorMsg =
        err.response?.data?.detail ||
        "Login falhou. Verifique suas credenciais.";
      setError(errorMsg);
    }
  };

  return (
    <section className="flex w-full p-6 bg-black">
      <NavigationMenu>
        <NavigationMenuList>
          <NavigationMenuItem>
            <ul className="flex w-screen pr-10 items-center justify-between">
              <Link href="/" className="flex gap-4 items-center">
                <Link>
                  <img src="/brAirlines.jpeg" alt="" className="h-14 rounded-full" />
                </Link>
                <h1 className="text-white text-lg">Brairlines</h1>
              </Link>
              <ul className="flex gap-2  mr-10">
                <li>
                  <Link href="/">
                    <NavigationMenuLink
                      className={navigationMenuTriggerStyle()}
                      vocab="
                      "
                    >
                      Home
                    </NavigationMenuLink>
                  </Link>
                </li>
                <li>
                  <Dialog open={isOpen} onOpenChange={setIsOpen}>
                    <DialogTrigger asChild>
                      {!isLogged ? (
                        <Button variant="default">Sign In</Button>
                      ) : (
                        ""
                      )}
                    </DialogTrigger>

                    <DialogContent className="sm:max-w-[425px]">
                      <DialogHeader>
                        <DialogTitle>Fazer Login</DialogTitle>
                        <DialogDescription>
                          Para continuar, faça login na sua conta ou
                          cadastre-se.
                        </DialogDescription>
                      </DialogHeader>
                      <div className="grid gap-4 py-4">
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="username" className="text-right">
                            Username
                          </Label>
                          <Input
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="col-span-3"
                          />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="password" className="text-right">
                            Password
                          </Label>
                          <Input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="col-span-3"
                          />
                        </div>
                        <div className="text-center">
                          {error && (
                            <p className="text-xs font-bold text-red-500 col-span-4">
                              {error}
                            </p>
                          )}
                        </div>
                      </div>
                      <DialogFooter className=" flex justify-center">
                        <Button onClick={handleLogin}>Login</Button>
                      </DialogFooter>
                    </DialogContent>
                  </Dialog>
                </li>
                <li>
                  <Dialog open={isOpen2} onOpenChange={setIsOpen2}>
                    <DialogTrigger asChild>
                      {!isLogged ? (
                        <Button variant="outline">Sign up</Button>
                      ) : (
                        ""
                      )}
                    </DialogTrigger>

                    <DialogContent className="sm:max-w-[425px]">
                      <DialogHeader>
                        <DialogTitle>Fazer Cadastro</DialogTitle>
                        <DialogDescription>
                          Para continuar, faça login na sua conta ou
                          cadastre-se.
                        </DialogDescription>
                      </DialogHeader>
                      <div className="grid gap-4 py-4">
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="username" className="text-right">
                            Username
                          </Label>
                          <Input
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="col-span-3"
                          />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="password" className="text-right">
                            Name
                          </Label>
                          <Input
                            id="name"
                            type=""
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            className="col-span-3"
                          />
                          <Label htmlFor="username" className="text-right">
                            CPF
                          </Label>
                          <Input
                            id="cpf"
                            value={cpf}
                            onChange={(e) => setcCpf(e.target.value)}
                            className="col-span-3"
                          />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                          <Label htmlFor="password" className="text-right">
                            Password
                          </Label>
                          <Input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="col-span-3"
                          />
                        </div>

                        <div className="text-center">
                          {error && (
                            <p className="text-xs font-bold text-red-500 col-span-4">
                              {error}
                            </p>
                          )}
                        </div>
                      </div>
                      <DialogFooter className=" flex justify-center">
                        <Button onClick={handleCadastro}>Cadastre-se</Button>
                      </DialogFooter>
                    </DialogContent>
                  </Dialog>
                </li>
                <li>
                  {isLogged ? (
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="outline">
                          <p>{user.nome}</p> <User />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent className="w-56 ">
                        <DropdownMenuLabel>My Account</DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        <Link href="/user/tickets">
                        <DropdownMenuItem >
                          
                          <Ticket />
                          <span>My Tickets</span>
                          
                         
                          <DropdownMenuShortcut>⌘S</DropdownMenuShortcut>
                        </DropdownMenuItem>
                        </Link>
                        <DropdownMenuSeparator />

                        <DropdownMenuItem onClick={handleLogout}>
                          <LogOut />
                          <span>Log out</span>
                          <DropdownMenuShortcut>⇧⌘Q</DropdownMenuShortcut>
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  ) : (
                    ""
                  )}
                </li>
              </ul>
            </ul>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>
    </section>
  );
}

export default Header;
