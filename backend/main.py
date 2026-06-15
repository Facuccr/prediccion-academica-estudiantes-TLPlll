from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd

# inicializamos la api
app = FastAPI(
    title="API de Predicción de Deserción Estudiantil",
    description="Backend para el Trabajo Práctico Final",
)

# config de cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Cargamos el modelo de Machine Learning en memoria al iniciar el servidor
try:
    modelo = joblib.load("../models/modelo_estudiantes.pkl")
    print("Sistema: Modelo .pkl cargado correctamente en memoria.")

except Exception as e:
    modelo = None
    print(f"Error Critico: Fallo al cargar el modelo predictivo. Detalle: {e}")

# datos de entrada
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

# Rutas de la API
@app.get("/")
def read_root():
    return {"message": "El servidor de la API esta corriendo correctamente con el modelo listo."}

@app.post("/predict")
def predict_dropout(student: StudentData):
    # verificamos que el modelo este cargado en memoria antes de predecir
    if modelo is None:
        raise HTTPException(status_code=500, detail="El modelo de Machine Learning no se encuentra disponible.")

    try:
        #Transformamos los datos del json a un df de pandas
        datos_diccionario = student.model_dump() 
        df_entrada = pd.DataFrame([datos_diccionario])

        #ejecutar la prediccion con Scikit-Learn
        prediccion_array = modelo.predict(df_entrada)
        prediccion_numerica = int(prediccion_array[0]) # se extrae el 0 o el 1

        # mapeo de la prediccion a texto para el cliente
        if prediccion_numerica == 1:
            resultado_final = "Dropout"
        elif prediccion_numerica == 0:
            resultado_final = "Graduate"
        else:
            resultado_final = "Desconocido" 

        return {
            "status": "success",
            "prediction": resultado_final,
            "message": "Prediccion calculada exitosamente."
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en el procesamiento de datos: {str(e)}")