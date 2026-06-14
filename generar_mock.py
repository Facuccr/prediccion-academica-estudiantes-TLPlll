import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import os

# 1. Asegurarnos de que exista la carpeta
os.makedirs('models', exist_ok=True)

# 2. Crear datos de prueba 
X_dummy = pd.DataFrame([
    { 
        "Marital_status": 1, "Course": 9238, "Tuition_fees_up_to_date": 1,
        "Gender": 1, "Scholarship_holder": 1, "Age_at_enrollment": 20,
        "Debtor": 0, "Curricular_units_1st_sem_approved": 6,
        "Curricular_units_1st_sem_grade": 14.0, "Curricular_units_2nd_sem_approved": 6,
        "Curricular_units_2nd_sem_grade": 14.0
    },
    { 
        "Marital_status": 1, "Course": 9238, "Tuition_fees_up_to_date": 0,
        "Gender": 1, "Scholarship_holder": 0, "Age_at_enrollment": 25,
        "Debtor": 1, "Curricular_units_1st_sem_approved": 2,
        "Curricular_units_1st_sem_grade": 8.0, "Curricular_units_2nd_sem_approved": 1,
        "Curricular_units_2nd_sem_grade": 5.0
    }
])

y_dummy = ["Graduate", "Dropout"]

# 3. Entrenar y exportar el modelo falso sobreescribiendo el archivo vacío
modelo_falso = DecisionTreeClassifier()
modelo_falso.fit(X_dummy, y_dummy)

ruta_guardado = 'models/modelo_estudiantes.pkl'
joblib.dump(modelo_falso, ruta_guardado)

print("¡Éxito! El archivo modelo_estudiantes.pkl ya no está vacío.")