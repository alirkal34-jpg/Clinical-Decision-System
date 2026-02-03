# ❤️ Cardiovascular Risk Assessment Dashboard

> A containerized **Clinical Decision Support System (CDSS)** engineered to predict cardiovascular health metrics in real-time, built with **Streamlit** and deployed via **Docker**.

![Docker](https://img.shields.io/badge/Container-Docker-blue?logo=docker&logoColor=white) ![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?logo=streamlit&logoColor=white) ![Python](https://img.shields.io/badge/Language-Python_3.9-yellow?logo=python&logoColor=white) ![Status](https://img.shields.io/badge/Deployment-Ready-success)

## 🩺 The Engineering Context

In healthcare informatics, reproducibility and isolation are critical. "It works on my machine" is not acceptable when dealing with medical algorithms.

This project solves dependency hell by fully **containerizing the application environment**, ensuring that the risk calculation model runs identically on any server, laptop, or cloud instance.

## ⚡ Key Features

* **Dockerized Architecture:** Fully isolated runtime environment using a multi-stage build process.
* **Interactive CDSS:** Real-time risk assessment dashboard built with **Streamlit**, allowing doctors to input patient vitals (Age, BMI, BP) and get instant feedback.
* **Data-Driven Insights:** Processes **70,000+ patient records** (`cardio_train.csv`) to visualize correlation heatmaps and risk distribution.
* **Reproducible Environment:** Includes `.devcontainer` configuration for standardized development workflows.

## 🛠️ Project Structure

<img width="1009" height="345" alt="image" src="https://github.com/user-attachments/assets/606b7361-4fad-4f52-9a74-b25e551e4aa5" />

