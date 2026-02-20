import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm';

// 🔌 Conexión a Supabase
const SUPABASE_URL = "https://vwcjstnodqtjtnxlhaur.supabase.co";
const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ3Y2pzdG5vZHF0anRueGxoYXVyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEyNTE5NzksImV4cCI6MjA4NjgyNzk3OX0.Lc8XGm4uiGhsEmbKwT3K0_28SNG-Q-6XQFK99vry9ow";

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

// 🚀 FUNCIÓN PRINCIPAL
async function cargarDashboard() {
    await cargarKPIs();
    await graficaInspeccionesPorMes();
    await graficaMantenimientosEstado();
    await graficaDeterioroPromedio();
}

// ================= KPI =================

async function cargarKPIs() {

    const { count: estructurasCount } = await supabase
        .from('estructuras')
        .select('*', { count: 'exact', head: true });

    const { count: inspeccionesCount } = await supabase
        .from('inspecciones')
        .select('*', { count: 'exact', head: true });

    const { count: mantenimientosCount } = await supabase
        .from('mantenimientos')
        .select('*', { count: 'exact', head: true });

    const { count: sensoresCount } = await supabase
        .from('sensores')
        .select('*', { count: 'exact', head: true });

    // 👉 Mostrar en el HTML
    document.getElementById("kpiEstructuras").textContent = estructurasCount ?? 0;
    document.getElementById("kpiInspecciones").textContent = inspeccionesCount ?? 0;
    document.getElementById("kpiMantenimientos").textContent = mantenimientosCount ?? 0;
    document.getElementById("kpiSensores").textContent = sensoresCount ?? 0;
}



// ================= GRÁFICA 1 =================
// Inspecciones por mes

async function graficaInspeccionesPorMes() {
    const { data } = await supabase
        .from('inspecciones')
        .select('fecha');

    const conteo = {};

    data.forEach(item => {
        const mes = new Date(item.fecha).toLocaleString('es-MX', { month: 'short' });

        if (!conteo[mes]) conteo[mes] = 0;
        conteo[mes]++;
    });

    const labels = Object.keys(conteo);
    const valores = Object.values(conteo);

    new Chart(document.getElementById('graficaInspecciones'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Inspecciones por mes',
                data: valores
            }]
        }
    });
}

// ================= GRÁFICA 2 =================
// Mantenimientos por estado

async function graficaMantenimientosEstado() {
    const { data } = await supabase
        .from('mantenimientos')
        .select('estado');

    const conteo = {};

    data.forEach(item => {
        const estado = item.estado;

        if (!conteo[estado]) conteo[estado] = 0;
        conteo[estado]++;
    });

    new Chart(document.getElementById('graficaMantenimientos'), {
        type: 'pie',
        data: {
            labels: Object.keys(conteo),
            datasets: [{
                data: Object.values(conteo)
            }]
        }
    });
}

// ================= GRÁFICA 3 =================
// Nivel de deterioro promedio

async function graficaDeterioroPromedio() {
    const { data } = await supabase
        .from('evaluaciones')
        .select('nivel_deterioro');

    const promedio = data.reduce((acc, val) => acc + val.nivel_deterioro, 0) / data.length;

    new Chart(document.getElementById('graficaDeterioro'), {
        type: 'doughnut',
        data: {
            labels: ['Deterioro promedio'],
            datasets: [{
                data: [promedio, 10 - promedio]
            }]
        }
    });
}

async function testSupabase() {
    const { data, error } = await supabase
      .from('estructuras')
      .select('*')
  
    console.log("DATA:", data)
    console.log("ERROR:", error)
  }
  
  testSupabase()


// ================= INIT =================
cargarDashboard();
