from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# 1. Inicialización
app = FastAPI(
    title="API de Predicción de Deserción Estudiantil",
    description="Backend para el Trabajo Práctico Final",
    version="1.0.0"
)

# 2. Configuración de CORS (IMPORTANTE: va justo después de crear 'app')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Definición de Datos
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

# 4. Rutas
@app.get("/")
def read_root():
    return {"message": "El servidor de la API está corriendo correctamente con CORS habilitado."}

@app.post("/predict")
def predict_dropout(student: StudentData):
    if student.Tuition_fees_up_to_date == 0 or student.Debtor == 1:
        prediction_simulada = "Dropout"
    else:
        prediction_simulada = "Graduate"

    return {
        "status": "success",
        "prediction": prediction_simulada,
        "message": "Predicción simulada correctamente."
    }