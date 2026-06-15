from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd

# 1. Inicialización de la API
app = FastAPI(
    title="API de Predicción de Deserción Estudiantil",
    description="Backend para el Trabajo Práctico Final",
    version="1.0.0"
)

# 2. Configuración de CORS (Permite que Tomás se conecte desde React/Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Cargar el modelo de Machine Learning en memoria al iniciar el servidor
try:
    modelo = joblib.load("models/modelo_estudiantes.pkl")
    print("--------------------------------------------------")
    print("¡ÉXITO! Modelo .pkl cargado correctamente en memoria.")
    print("--------------------------------------------------")
except Exception as e:
    modelo = None
    print("--------------------------------------------------")
    print(f"ERROR CRÍTICO al cargar el modelo: {e}")
    print("--------------------------------------------------")

# 4. Esquema de Datos de Entrada (Contrato con el Frontend)
class StudentData(BaseModel):
    Marital_status: int = Field(..., description="Estado civil del estudiante")
    Course: int = Field(..., description="Código numérico del curso/carrera")
    Tuition_fees_up_to_date: int = Field(..., description="1 si tiene las cuotas al día, 0 si no")
    Gender: int = Field(..., description="1 para masculino, 0 para femenino")
    Scholarship_holder: int = Field(..., description="1 si tiene beca, 0 si no")
    Age_at_enrollment: int = Field(..., description="Edad al momento de la inscripción")
    Debtor: int = Field(..., description="1 si es deudor, 0 si no")
    Curricular_units_1st_sem_approved: int = Field(..., description="Materias aprobadas en el 1er semestre")
    Curricular_units_1st_sem_grade: float = Field(..., description="Nota promedio del 1er semestre")
    Curricular_units_2nd_sem_approved: int = Field(..., description="Materias aprobadas en el 2do semestre")
    Curricular_units_2nd_sem_grade: float = Field(..., description="Nota promedio del 2do semestre")

# 5. Rutas de la API
@app.get("/")
def read_root():
    return {"message": "El servidor de la API está corriendo correctamente con el modelo listo."}

@app.post("/predict")
def predict_dropout(student: StudentData):
    # Verificamos que el modelo esté cargado en memoria antes de predecir
    if modelo is None:
        raise HTTPException(status_code=500, detail="El modelo de Machine Learning no está disponible en el servidor.")

    try:
        # A. Transformar los datos del JSON (objeto Pydantic) a un DataFrame de Pandas de 1 fila
        datos_diccionario = student.model_dump() 
        df_entrada = pd.DataFrame([datos_diccionario])

        # B. Ejecutar la predicción con Scikit-Learn
        prediccion_array = modelo.predict(df_entrada)
        resultado_final = prediccion_array[0].item() # Extrae el string resultado (ej. "Graduate" o "Dropout")

        return {
            "status": "success",
            "prediction": resultado_final,
            "message": "Predicción calculada exitosamente a través del modelo matemático."
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en el procesamiento de datos: {str(e)}")