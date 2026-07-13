import sys
import gradio as gr
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.model_selection import train_test_split

# --- 1. DATA LOADING AND INITIALIZATION ---
try:
  dt = pd.read_csv("studentPerformance.csv")
except FileNotFoundError:
  print("--- ERROR: DATA FILE NOT FOUND ---")
  print(
      "The file 'studentPerformance.csv' must be placed in the same directory as"
      " this Python script."
  )
  sys.exit(1)

# Séparer Features et Targets
X = dt[["Study_Hours", "Attendance", "Practice_Tests"]]
y = dt["Final_Score"]  # Score final (Regression target)
z = dt["Pass_Fail"]  # 0 ou 1 (Classification target)

# Découpage train/test
x_train, x_test, y_train, y_test, z_train, z_test = train_test_split(
    X, y, z, test_size=0.3, random_state=2
)

# Entraînement des modèles
lr_model = LinearRegression()
lr_model.fit(x_train, y_train)

reg_log = LogisticRegression(solver="liblinear", random_state=42)
reg_log.fit(x_train, z_train)

# --- 3. ÉVALUATION DES MODÈLES ---
y_pred_lr = lr_model.predict(x_test)
z_pred_log = reg_log.predict(x_test)

mae = mean_absolute_error(y_test, y_pred_lr)
y_mean = y_test.mean()
mae_percent = (mae / y_mean) * 100
accuracy = accuracy_score(z_test, z_pred_log)


# --- 4. FONCTION DE PRÉDICTION ---
def predict(study_hours, attendance, practice_tests):
  user_data = pd.DataFrame(
      [[study_hours, attendance, practice_tests]],
      columns=["Study_Hours", "Attendance", "Practice_Tests"],
  )

  pred_score_raw = lr_model.predict(user_data)[0]
  pred_score = max(0, min(100, pred_score_raw))

  pred_pass = reg_log.predict(user_data)[0]
  pred_proba = reg_log.predict_proba(user_data)[0][1]

  result = "✅ PASS (réussi)" if pred_pass == 1 else "❌ FAIL (échoué)"
  return round(pred_score, 2), f"{pred_proba*100:.1f}%", result


# --- 5. INTERFACE GRADIO ---
with gr.Blocks(title="Student Performance Prediction") as demo:
  gr.Markdown("# 🎓 Student Performance Prediction")
  gr.Markdown("---")
  gr.Markdown(
      "Enter the student metrics to predict their Final Score and Pass/Fail"
      " Outcome."
  )

  with gr.Row():
    study_hours = gr.Slider(
        minimum=0,
        maximum=10,
        value=5,
        step=0.1,
        label="Study Hours (0.0 - 10.0)",
    )
    attendance = gr.Slider(
        minimum=50, maximum=100, value=75, step=1, label="Attendance (%)"
    )
    practice_tests = gr.Slider(
        minimum=0, maximum=20, value=2, step=1, label="Practice Tests"
    )

  predict_btn = gr.Button("Prédire la Performance")

  with gr.Column():
    final_score = gr.Number(label="📊 Final Score (0-100)", precision=2)
    prob_pass = gr.Textbox(label="🔮 Probabilité de PASS")
    result_text = gr.Textbox(label="🎯 Résultat")

  predict_btn.click(
      fn=predict,
      inputs=[study_hours, attendance, practice_tests],
      outputs=[final_score, prob_pass, result_text],
  )

  gr.Markdown("---")
  gr.Markdown("## Performance des Modèles (Calculé sur l'ensemble de Test)")

  with gr.Row():
    gr.Textbox(
        label="Régression Linéaire (Score)",
        value=f"Erreur Absolue Moyenne (MAE) : {mae:.2f} points",
        interactive=False,
        scale=1,
    )
    gr.Textbox(
        label="Taux d'Erreur Relatif",
        value=f"Erreur Relative (Score) : {mae_percent:.2f}%",
        interactive=False,
        scale=1,
    )

  gr.Textbox(
      label="Régression Logistique (Pass/Fail)",
      value=f"Précision (Accuracy) : {accuracy*100:.2f}%",
      interactive=False,
  )

if __name__ == "__main__":
  # Configured to bind to port 7860 on the server for Nginx
  demo.launch(server_name="0.0.0.0", server_port=7860)
