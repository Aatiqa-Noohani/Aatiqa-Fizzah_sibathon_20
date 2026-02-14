# Aatiqa-Fizzah_sibathon_2026
Smart Energy Management System monitors electricity use in real time, predicts future bills, and provides smart recommendations to save energy and reduce costs. It identifies high-consumption devices, suggests renewable options, and shows environmental impact, helping homes and businesses use power efficiently and sustainably.

<div align="center">
  <img src="https://img.icons8.com/fluency/96/lightning-bolt.png" alt="Logo" width="80">
  <h1>⚡ Smart Energy Management System</h1>
  <p><strong>AI-Powered Energy Forecast & Cost Analysis Dashboard</strong></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python" alt="Python">
    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit">
    <img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="ML">
  </p>
</div>

<hr>

## 📖 Overview
The **Smart Energy Management System (SEMS)** is a predictive tool designed to help users understand their energy consumption patterns. It utilizes machine learning to forecast energy loads and provides a comprehensive calculator for appliance-specific costs.

## 🏗️ System Architecture
The project follows a modular design to separate data handling, logic, and presentation:

<table width="100%">
  <tr>
    <td width="50%">
      <h3>1. UI Layer (APP.py)</h3>
      <ul>
        <li>Interactive Streamlit dashboard.</li>
        <li>Custom CSS animations for a modern feel.</li>
        <li>Real-time input sliders for predictions.</li>
      </ul>
    </td>
    <td width="50%">
      <h3>2. ML Logic (predictor.py)</h3>
      <ul>
        <li>Linear Regression model implementation.</li>
        <li>Cyclical feature engineering (Sine/Cosine).</li>
        <li>Automated model saving/loading (Pickle).</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>3. Data Management (data_manager.py)</h3>
      <ul>
        <li>Cleans and prepares historical CSV data.</li>
        <li>Simulates appliance energy usage (kWh).</li>
        <li>Calculates daily/weekly statistics.</li>
      </ul>
    </td>
    <td width="50%">
      <h3>4. Visualization (chart_generator.py)</h3>
      <ul>
        <li>Professional Matplotlib charts.</li>
        <li>Custom themes based on project branding.</li>
        <li>Hourly, weekly, and prediction plots.</li>
      </ul>
    </td>
  </tr>
</table>

## 🚀 Key Features
<ul>
  <li><strong>Predictive Analysis:</strong> Forecasts energy demand based on hour, day, and season.</li>
  <li><strong>Device Simulator:</strong> Compares costs for appliances like ACs, Refrigerators, and more.</li>
  <li><strong>Cost Optimization:</strong> Provides automated tips to reduce bills by up to 35%.</li>
  <li><strong>Configurable:</strong> Centralized settings for energy rates and device specs in <code>config.py</code>.</li>
</ul>

## 🛠️ Installation
<pre>
<code>
# Clone the repository
git clone (https://github.com/Aatiqa-Noohani/Aatiqa-Fizzah_sibathon_20.git)

# Install requirements
pip install pandas numpy scikit-learn matplotlib streamlit
</code>
</pre>

## 🖥️ Usage
To launch the AI dashboard, run the following command in your terminal:
<pre>
<code>streamlit run APP.py</code>
</pre>

## ⚙️ Configuration
You can adjust system-wide constants in <code>config.py</code>:
<ul>
  <li><strong>Energy Price:</strong> Set <code>ENERGY_COST_PER_KWH</code> (Default: $0.12).</li>
  <li><strong>Appliance List:</strong> Modify the <code>DEVICES</code> dictionary to add new items.</li>
  <li><strong>ML Params:</strong> Change <code>PREDICTION_DAYS</code> or test/train split ratios.</li>
</ul>

<hr>

<div align="center">
  <p>Developed with ❤️ for Sustainable Energy Management</p>
</div>
