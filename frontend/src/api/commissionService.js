import api from "./axios";

/**
 * Servicio centralizado para hablar con la API del backend.
 * Agrupa: vendedores, reglas, ventas (CRUD) y el calculo de comisiones.
 */
export const commissionService = {
  // --- Vendedores -----------------------------------------------------
  getVendedores: () => api.get("/vendedores/").then((res) => res.data),

  // --- Reglas de comision ----------------------------------------------
  getReglas: () => api.get("/reglas/").then((res) => res.data),

  // --- Ventas (CRUD) -----------------------------------------------------
  getVentas: (params = {}) =>
    api.get("/ventas/", { params }).then((res) => res.data),

  crearVenta: (venta) => api.post("/ventas/", venta).then((res) => res.data),

  eliminarVenta: (id) => api.delete(`/ventas/${id}/`),

  // --- Calculo de comisiones por rango de fechas -------------------------
  calcularComisiones: (fechaInicio, fechaFin) =>
    api
      .post("/ventas/calcular-comisiones/", {
        fecha_inicio: fechaInicio,
        fecha_fin: fechaFin,
      })
      .then((res) => res.data),
};

export default commissionService;
