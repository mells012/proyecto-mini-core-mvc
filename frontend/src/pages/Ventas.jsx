import { useEffect, useState } from "react";
import commissionService from "../api/commissionService";

const hoyISO = () => new Date().toISOString().slice(0, 10);

export default function Ventas() {
  const [ventas, setVentas] = useState([]);
  const [vendedores, setVendedores] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  const [form, setForm] = useState({
    vendedor: "",
    monto: "",
    fecha: hoyISO(),
    descripcion: "",
  });

  async function cargarDatos() {
    setCargando(true);
    setError(null);
    try {
      const [ventasData, vendedoresData] = await Promise.all([
        commissionService.getVentas(),
        commissionService.getVendedores(),
      ]);
      setVentas(ventasData);
      setVendedores(vendedoresData);
    } catch (err) {
      setError("No se pudo conectar con el backend. Verifica que la API este corriendo.");
    } finally {
      setCargando(false);
    }
  }

  useEffect(() => {
    cargarDatos();
  }, []);

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!form.vendedor || !form.monto || !form.fecha) return;

    try {
      await commissionService.crearVenta({
        vendedor: Number(form.vendedor),
        monto: Number(form.monto),
        fecha: form.fecha,
        descripcion: form.descripcion,
      });
      setForm((prev) => ({ ...prev, monto: "", descripcion: "" }));
      cargarDatos();
    } catch (err) {
      setError("No se pudo registrar la venta. Revisa los datos ingresados.");
    }
  }

  async function handleDelete(id) {
    if (!window.confirm("Eliminar esta venta?")) return;
    try {
      await commissionService.eliminarVenta(id);
      setVentas((prev) => prev.filter((v) => v.id !== id));
    } catch (err) {
      setError("No se pudo eliminar la venta.");
    }
  }

  return (
    <section className="page">
      <h1>Ventas</h1>
      <p className="page-subtitle">
        Registra nuevas ventas y consulta el listado. La comisi&oacute;n
        estimada se calcula autom&aacute;ticamente seg&uacute;n las reglas
        vigentes.
      </p>

      {error && <div className="alert">{error}</div>}

      <form className="card form-grid" onSubmit={handleSubmit}>
        <div className="form-field">
          <label htmlFor="vendedor">Vendedor</label>
          <select
            id="vendedor"
            name="vendedor"
            value={form.vendedor}
            onChange={handleChange}
            required
          >
            <option value="">Selecciona...</option>
            {vendedores.map((v) => (
              <option key={v.id} value={v.id}>
                {v.nombre}
              </option>
            ))}
          </select>
        </div>

        <div className="form-field">
          <label htmlFor="monto">Monto ($)</label>
          <input
            id="monto"
            name="monto"
            type="number"
            min="0"
            step="0.01"
            value={form.monto}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-field">
          <label htmlFor="fecha">Fecha</label>
          <input
            id="fecha"
            name="fecha"
            type="date"
            value={form.fecha}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-field form-field-wide">
          <label htmlFor="descripcion">Descripci&oacute;n (opcional)</label>
          <input
            id="descripcion"
            name="descripcion"
            type="text"
            value={form.descripcion}
            onChange={handleChange}
            placeholder="Ej. Venta de equipo X"
          />
        </div>

        <button type="submit" className="btn-primary">
          Agregar venta
        </button>
      </form>

      <div className="card">
        <h2>Listado de ventas</h2>
        {cargando ? (
          <p>Cargando...</p>
        ) : ventas.length === 0 ? (
          <p>No hay ventas registradas todav&iacute;a.</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Vendedor</th>
                <th>Monto</th>
                <th>Fecha</th>
                <th>Descripci&oacute;n</th>
                <th>Comisi&oacute;n estimada</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {ventas.map((venta) => (
                <tr key={venta.id}>
                  <td>{venta.vendedor_nombre}</td>
                  <td>${Number(venta.monto).toFixed(2)}</td>
                  <td>{venta.fecha}</td>
                  <td>{venta.descripcion || "—"}</td>
                  <td>
                    {venta.comision_estimada !== null
                      ? `$${venta.comision_estimada.toFixed(2)}`
                      : "Sin regla aplicada"}
                  </td>
                  <td>
                    <button
                      className="btn-danger"
                      onClick={() => handleDelete(venta.id)}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}
