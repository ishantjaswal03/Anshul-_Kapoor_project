# AI-Powered Predictive Maintenance System for Industrial Equipment

**A College Project Report**

## 1. Title Page
**Project Title**: AI-Powered Predictive Maintenance System  
**Product Domain**: Industrial IoT & Machine Learning  
**Core Technologies**: Python, Flask, React/Next.js, Scikit-learn, AWS (Infrastructure Placeholder)

---

## 2. Certificate / Declaration
This is to certify that the project titled "AI-Powered Predictive Maintenance System" is a bona fide work carried out by the student as an implementation of advanced Machine Learning and Web Development concepts.

---

## 3. Acknowledgement
I would like to express my gratitude to the faculty and mentors for their guidance during the development of this project. Special thanks to the open-source community for providing the tools and libraries (Scikit-learn, React, Tailwind CSS) that made this implementation possible.

---

## 4. Abstract
Predictive Maintenance (PdM) is a strategy that uses data analysis tools and techniques to detect anomalies in equipment and potential defects so they can be fixed before failure. This project implements a full-stack PdM system featuring a premium web-based dashboard and a robust Machine Learning backend. Utilizing Random Forest and Isolation Forest algorithms, the system provides real-time failure probability and anomaly detection based on industrial telemetry data such as temperature, vibration, and pressure.

---

## 5. Introduction
In modern manufacturing, unexpected equipment failure leads to significant downtime and financial loss. Traditional maintenance strategies—reactive (fix when broken) or preventive (fix on a schedule)—are often inefficient. This project presents a "Predictive" approach, leveraging historical sensor data and real-time telemetry to forecast health status dynamically.

---

## 6. Problem Statement
Many industrial setups rely on manual monitoring or rigid schedules, leading to:
- Excessive downtime due to unforeseen failures.
- Unnecessary costs from premature part replacements.
- Safety risks in critical machinery environments.

---

## 7. Objectives of the Project
- To develop an AI model capable of predicting equipment failure with high accuracy.
- To detect operational anomalies using unsupervised learning techniques.
- To provide a modern, user-friendly interface for operations monitoring.
- To implement a secure authentication and role-based access system (Pro/Premium).

---

## 8. Scope of the Project
The project covers:
- Synthetic data generation for manufacturing environments.
- Feature engineering of telemetry sensor data.
- Backend API development using Flask.
- Frontend development with Next.js and Tailwind CSS.
- Integration of predictive and anomaly detection models.

---

## 9. Literature Review
The project draws inspiration from industry standards like the NASA Turbofan Engine Degradation Dataset and modern PdM frameworks. Research indicates that Ensemble methods (Random Forest) consistently outperform simpler models in classification tasks involving sensor data, while Isolation Forests are highly effective for high-dimensional anomaly detection.

---

## 10. Dataset Description
The system utilizes a generated dataset of 5,000 samples simulating various industrial machines (M001-M004).
**Features included**:
- `temperature`: Operating temperature (°C)
- `vibration`: Mechanical vibration (mm/s)
- `pressure`: Hydraulic/Pneumatic pressure (psi)
- `rpm`: Rotation speed
- `power_consumption`: Energy usage (kW)
- `cycle_count` & `operating_hours`: Total usage metrics

---

## 11. Data Preprocessing
- **Handling Categorical Data**: `machine_id` is encoded using Label Encoding.
- **Normalization**: Numerical features are scaled using `StandardScaler` to ensure mean=0 and variance=1, which is critical for model stability.
- **Label Generation**: A failure label is synthetically derived based on thresholds (e.g., Temp > 85°C) to simulate real-world failure conditions.

---

## 12. Feature Selection / Engineering
The primary features were selected based on their physical relevance to machine wear and tear. No complex engineering like FFT was performed for this version, but simple usage ratios (Operating Hours/Cycle Count) were considered as part of the feature set.

---

## 13. Model Selection (Algorithms Used)
- **Random Forest Classifier**: Chosen for its robustness to noise and ability to handle non-linear relationships.
- **Isolation Forest**: Used for unsupervised anomaly detection to catch "unknown unknowns" or outliers that don't fit the standard failure profile.

---

## 14. Model Training
- **Training Set**: 80% of the data.
- **Testing Set**: 20% of the data.
- **Process**: Models are trained on the scaled feature set and saved using `joblib` for persistent use in the API.

---

## 15. Model Evaluation (Accuracy, Metrics)
The model achieved high performance on synthetic data:
- **Precision / Recall**: High F1-score for failure classification.
- **Confusion Matrix**: Minimal false negatives (critical for avoiding missed failures).
- **Anomaly Detection**: Effectively flags samples outside the 95th percentile of normal operation.

---

## 16. Result Analysis
Analysis shows that Temperature and Vibration are the strongest predictors of impending failure. The Isolation Forest successfully flags rare events even when specific failure thresholds aren't breached, providing an extra layer of safety.

---

## 17. System Architecture / Workflow Diagram
1. **User** enters telemetry via Dashboard.
2. **Next.js Frontend** sends JSON request to Flask API.
3. **Flask Backend** validates user session and plan (Free/Premium).
4. **ML Engine** loads pre-trained pkl models and preprocessors.
5. **Prediction Result** is returned to the UI for visualization.

---

## 18. Tools & Technologies Used
- **Languages**: Python, JavaScript/TypeScript.
- **Backend Framework**: Flask.
- **Frontend Framework**: Next.js, React, Tailwind CSS.
- **ML Libraries**: Scikit-learn, Pandas, NumPy.
- **Persistence**: Json-based User DB, Joblib for Models.

---

## 19. Implementation Details
The backend uses a `wraps`-based decorator (`login_required`) to protect AI endpoints. The frontend uses `Framer Motion` for smooth transitions and a glassmorphism design for a premium interactive experience.

---

## 20. Advantages of the System
- **Real-time Insights**: Near-instant feedback on machine health.
- **Hybrid Detection**: Combines supervised failure prediction with unsupervised anomaly detection.
- **Scalability**: Can be extended to thousands of machines via API.

---

## 21. Limitations
- **Synthetic Data**: Accuracy in real-world scenarios depends on high-quality sensor data.
- **Connectivity**: Requires active internet/network access for the client-server interaction.

---

## 22. Future Scope
- Integration with live IoT sensors (MQTT protocol).
- Adding Generative AI (LLM) for detailed maintenance advice.
- Deployment via AWS Lambda and API Gateway for enterprise scale.

---

## 23. Conclusion
The AI-Powered Predictive Maintenance System successfully demonstrates how machine learning can transform industrial operations. By providing actionable insights through a modern interface, it fulfills the objective of making predictive analytics accessible to factory floor operators.

---

## 24. References / Bibliography
1. Scikit-learn Documentation.
2. Flask Web Development by Miguel Grinberg.
3. Next.js Documentation (Vercel).
4. "An Introduction to Predictive Maintenance" by R. Keith Mobley.

---

## 25. Appendix (Code / Screenshots)
- **Backend Entry Point**: `app.py`
- **ML Workflow**: `predictive_model.py`
- **Dashboard UI**: `src/app/dashboard/page.tsx`
- (Screenshots available in the project assets folder)
