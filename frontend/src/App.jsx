import { Route, Routes } from "react-router-dom";
import NavBar from "./components/NavBar";
import Ventas from "./pages/Ventas";
import Comisiones from "./pages/Comisiones";

export default function App() {
  return (
    <div className="app-shell">
      <NavBar />
      <main className="app-content">
        <Routes>
          <Route path="/" element={<Ventas />} />
          <Route path="/comisiones" element={<Comisiones />} />
        </Routes>
      </main>
    </div>
  );
}
