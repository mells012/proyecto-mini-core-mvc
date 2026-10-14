import { useState } from "react";
import commissionService from "../api/commissionService";

const hoyISO = () => new Date().toISOString().slice(0, 10);
const hace30DiasISO = () => {
  const d = new Date();
  d.setDate(d.getDate() - 30);
  return d.toISOString().slice(0, 10);
};

export default function Comisiones() {
  const [fechaInicio, setFechaInicio] = useState(hace30DiasISO());
  const [fechaFin, setFechaFin] = useState(hoyISO());
  const [reporte, setReporte] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState(null);

  async function handleCalcular(e) {
    e.preventDefault();
    setCargando(true);
    setError(null);
    try {
      const data = await commissionService.calcularComisiones(fechaInicio, fechaFin);
      setReporte(data);
    } catch (err) {
      setError(
        err.response?.data?.fecha_inicio ||
          err.response?.data?.non_field_errors ||
          "No se pudo calcular las comisiones para ese rango."
      );
      setReporte(null);
    } finally {
      setCargando(false);
    }
  }

  return (
    <section className="page">
      <h1>C&aacute;lculo de comisiones</h1>
      <p className="page-subtitle">
        Selecciona un rango de fechas para ver el resumen de comisiones
        agrupado por vendedor, junto con el detalle de cada venta.
      </p>

      <form className="card filter-row" onSubmit={handleCalcular}>
        <div className="form-field">
          <label htmlFor="fecha_inicio">Desde</label>
          <input
            id="fecha_inicio"
            type="date"
            value={fechaInicio}
            onChange={(e) => setFechaInicio(e.target.value)}
            required
          />
        </div>
        <div className="form-field">
          <label htmlFor="fecha_fin">Hasta</label>
          <input
            id="fecha_fin"
            type="date"
            value={fechaFin}
            onChange={(e) => setFechaFin(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn-primary" disabled={cargando}>
          {cargando ? "Calculando..." : "Calcular comisiones"}
        </button>
      </form>

      {error && <div className="alert">{String(error)}</div>}

      {reporte && (
        <>
          <div className="summary-grid">
            <div className="summary-card">
              <span className="summary-label">Vendedores con ventas</span>
              <span className="summary-value">{reporte.cantidad_vendedores}</span>
            </div>
            <div className="summary-card">
              <span className="summary-label">Ventas en el periodo</span>
              <span className="summary-value">{reporte.cantidad_ventas}</span>
            </div>
            <div className="summary-card">
              <span className="summary-label">Total vendido</span>
              <span className="summary-value">
                ${reporte.total_ventas_global.toFixed(2)}
              </span>
            </div>
            <div className="summary-card highlight">
              <span className="summary-label">Total comisiones</span>
              <span className="summary-value">
                ${reporte.total_comision_global.toFixed(2)}
              </span>
            </div>
          </div>

          {reporte.resumen_por_vendedor.length === 0 ? (
            <div className="card">
              <p>No hay ventas registradas en ese rango de fechas.</p>
            </div>
          ) : (
            reporte.resumen_por_vendedor.map((v) => (
              <div className="card" key={v.vendedor_id}>
                <div className="vendor-summary-header">
                  <h2>{v.vendedor_nombre}</h2>
                  <div className="vendor-summary-totals">
                    <span>{v.cantidad_ventas} ventas</span>
                    <span>Total vendido: ${v.total_ventas.toFixed(2)}</span>
                    <span className="highlight-text">
                      Comisi&oacute;n: ${v.total_comision.toFixed(2)}
                    </span>
                  </div>
                </div>
                <table className="table">
                  <thead>
                    <tr>
                      <th>Fecha</th>
                      <th>Monto</th>
                      <th>Regla aplicada</th>
                      <th>%</th>
                      <th>Comisi&oacute;n</th>
                    </tr>
                  </thead>
                  <tbody>
                    {v.detalle_ventas.map((d) => (
                      <tr key={d.venta_id}>
                        <td>{d.fecha}</td>
                        <td>${d.monto.toFixed(2)}</td>
                        <td>{d.regla_aplicada || "Ninguna"}</td>
                        <td>{d.porcentaje}%</td>
                        <td>${d.comision.toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ))
          )}
        </>
      )}
    </section>
  );
}
