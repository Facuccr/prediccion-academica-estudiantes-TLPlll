import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    Marital_status: 1,
    Course: 9238,
    Tuition_fees_up_to_date: 1,
    Gender: 1,
    Scholarship_holder: 0,
    Age_at_enrollment: 20,
    Debtor: 0,
    Curricular_units_1st_sem_approved: 6,
    Curricular_units_1st_sem_grade: 13.5,
    Curricular_units_2nd_sem_approved: 5,
    Curricular_units_2nd_sem_grade: 12.8,
  });

  const [resultado, setResultado] = useState(null);
  const [esRiesgo, setEsRiesgo] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: Number(value),
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResultado(null);
    setError(null);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/predict",
        formData,
      );

      const resultadoTexto = response.data.prediction;

      if (resultadoTexto === "Graduate") {
        setResultado("Probable Graduación (Graduate)");
        setEsRiesgo(false);
      } else {
        setResultado("Riesgo de Deserción (Dropout)");
        setEsRiesgo(true);
      }
    } catch (err) {
      console.error(err);
      setError(
        "Error de conexión con la API. Verifica que el backend esté corriendo.",
      );
    }
  };

  return (
    <div className="dashboard">
      <header className="header">
        <h1>Sistema de Retención Estudiantil</h1>
        <p>Motor de predicción de IA para alertas tempranas</p>
      </header>

      <form onSubmit={handleSubmit} className="form-container">
        {/* SECCIÓN 1: Perfil del Estudiante */}
        <section className="form-section">
          <h2>Perfil del Estudiante</h2>
          <div className="grid-2-cols">
            <div className="input-group">
              <label>Edad al Inscribirse:</label>
              <input
                type="number"
                name="Age_at_enrollment"
                value={formData.Age_at_enrollment}
                onChange={handleChange}
              />
            </div>
            <div className="input-group">
              <label>Código de Carrera:</label>
              <input
                type="number"
                name="Course"
                value={formData.Course}
                onChange={handleChange}
              />
            </div>

            {/* Convertido a Select */}
            <div className="input-group">
              <label>Género:</label>
              <select
                name="Gender"
                value={formData.Gender}
                onChange={handleChange}
              >
                <option value={1}>Masculino</option>
                <option value={0}>Femenino</option>
              </select>
            </div>

            {/* Convertido a Select */}
            <div className="input-group">
              <label>Estado Civil:</label>
              <select
                name="Marital_status"
                value={formData.Marital_status}
                onChange={handleChange}
              >
                <option value={1}>Soltero</option>
                <option value={2}>Casado</option>
                <option value={3}>Viudo</option>
                <option value={4}>Divorciado</option>
                <option value={5}>Unión de hecho</option>
                <option value={6}>Separado Legalmente</option>
              </select>
            </div>
          </div>
        </section>

        {/* SECCIÓN 2: Situación Financiera */}
        <section className="form-section highlight-section">
          <h2>Situación Financiera</h2>
          <div className="grid-3-cols">
            {/* Convertido a Select */}
            <div className="input-group">
              <label>Cuotas al Día:</label>
              <select
                name="Tuition_fees_up_to_date"
                value={formData.Tuition_fees_up_to_date}
                onChange={handleChange}
              >
                <option value={1}>Sí</option>
                <option value={0}>No</option>
              </select>
            </div>

            {/* Convertido a Select */}
            <div className="input-group">
              <label>Es Deudor:</label>
              <select
                name="Debtor"
                value={formData.Debtor}
                onChange={handleChange}
              >
                <option value={1}>Sí</option>
                <option value={0}>No</option>
              </select>
            </div>

            {/* Convertido a Select */}
            <div className="input-group">
              <label>Tiene Beca:</label>
              <select
                name="Scholarship_holder"
                value={formData.Scholarship_holder}
                onChange={handleChange}
              >
                <option value={1}>Sí</option>
                <option value={0}>No</option>
              </select>
            </div>
          </div>
        </section>

        {/* SECCIÓN 3: Rendimiento Académico (Se mantienen como Inputs) */}
        <section className="form-section">
          <h2>Rendimiento Académico</h2>
          <div className="grid-2-cols">
            <div className="input-group">
              <label>Materias Aprobadas (1er Sem):</label>
              <input
                type="number"
                name="Curricular_units_1st_sem_approved"
                value={formData.Curricular_units_1st_sem_approved}
                onChange={handleChange}
              />
            </div>
            <div className="input-group">
              <label>Nota Promedio (1er Sem):</label>
              <input
                type="number"
                step="any"
                name="Curricular_units_1st_sem_grade"
                value={formData.Curricular_units_1st_sem_grade}
                onChange={handleChange}
              />
            </div>
            <div className="input-group">
              <label>Materias Aprobadas (2do Sem):</label>
              <input
                type="number"
                name="Curricular_units_2nd_sem_approved"
                value={formData.Curricular_units_2nd_sem_approved}
                onChange={handleChange}
              />
            </div>
            <div className="input-group">
              <label>Nota Promedio (2do Sem):</label>
              <input
                type="number"
                step="any"
                name="Curricular_units_2nd_sem_grade"
                value={formData.Curricular_units_2nd_sem_grade}
                onChange={handleChange}
              />
            </div>
          </div>
        </section>

        <button type="submit" className="btn-submit">
          Ejecutar Predicción
        </button>
      </form>

      {/* ÁREA DE RESULTADOS */}
      {resultado && (
        <div className={`result-box ${esRiesgo ? "danger" : "success"}`}>
          <h2>{resultado}</h2>
          <p>
            {esRiesgo
              ? "Acción requerida: Derivar perfil a tutorías para intervención inmediata."
              : "Perfil académico estable. Continuar monitoreo regular."}
          </p>
        </div>
      )}
      {error && (
        <div className="result-box error">
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}

export default App;
