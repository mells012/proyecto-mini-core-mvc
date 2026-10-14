import { NavLink } from "react-router-dom";

export default function NavBar() {
  return (
    <header className="navbar">
      <div className="navbar-brand">Mini Core · Ventas y Comisiones</div>
      <nav className="navbar-links">
        <NavLink
          to="/"
          end
          className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
        >
          Ventas
        </NavLink>
        <NavLink
          to="/comisiones"
          className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
        >
          Comisiones
        </NavLink>
      </nav>
    </header>
  );
}
