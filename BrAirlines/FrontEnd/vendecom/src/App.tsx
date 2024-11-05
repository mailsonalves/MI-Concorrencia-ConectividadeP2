
import Header from "./components/page/header";
import Home from "./components/page/Home";
import { Outlet } from "react-router-dom";

function App() {
  return (
    <section className="mx-auto overflow-x-hidden ">
      <Header />
      <Outlet/>
    </section>
  );
}

export default App;
