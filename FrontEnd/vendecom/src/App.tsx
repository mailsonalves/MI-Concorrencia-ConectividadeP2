import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import { Button } from "./components/ui/button";
import { Form } from "./components/ui/form";
import { Input } from "./components/ui/input";
import { Label } from "@radix-ui/react-label";
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
import Header from "./components/page/header";

function App() {
  return (
    <section className="flex mx-auto bg-black justify-center">
      <Header/>
    </section>
  );
}

export default App;
