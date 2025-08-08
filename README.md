<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
 
</head>
<body>

<h1>🇮🇳 Indian Smart Waste Collection Optimizer</h1>

<p>This project is a <strong>Streamlit-based AI-powered web application</strong> designed to optimize waste collection routes across Indian cities. It combines geospatial mapping, clustering, and vehicle routing algorithms tailored for <strong>Indian road conditions</strong>, helping municipalities and smart cities plan more efficient and eco-friendly waste collection.</p>

<hr>

<h2>📂 Repository Contents</h2>
<ul>
  <li><code>garbage.py</code> – Main Streamlit app with UI, route optimization logic, and mapping.</li>
  <li><code>requirements.txt</code> – List of Python dependencies.</li>
  <li><code>README.md</code> – Project overview and usage instructions.</li>
</ul>

<hr>

<h2>♻️ Waste Categories Considered</h2>
<ul>
  <li>Residential</li>
  <li>Commercial</li>
  <li>Construction</li>
  <li>Organic</li>
</ul>

<hr>

<h2>🛠️ Technologies Used</h2>
<ul>
  <li><strong>Streamlit</strong> – Web app framework</li>
  <li><strong>Folium & streamlit-folium</strong> – Interactive maps</li>
  <li><strong>NumPy, Pandas</strong> – Data handling</li>
  <li><strong>Matplotlib</strong> – Visualizations</li>
  <li><strong>scikit-learn</strong> – Clustering (K-Means)</li>
  <li><strong>OR-Tools</strong> – Vehicle Routing Problem (VRP) optimization by Google</li>
  <li><strong>Python</strong> – Core programming language</li>
</ul>

<hr>

<h2>🚀 How to Run the Project</h2>

<ol>
  <li><strong>Clone the repository</strong>
    <pre><code>git clone https://github.com/smartswagvivek/Garbage-collection.git
cd Garbage-collection</code></pre>
  </li>

  <li><strong>Create virtual environment (optional)</strong>
    <pre><code>python -m venv venv
source venv/bin/activate   # For Linux/macOS
.\venv\Scripts\activate     # For Windows</code></pre>
  </li>

  <li><strong>Install dependencies</strong>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>

  <li><strong>Run the Streamlit app</strong>
    <pre><code>streamlit run garbage.py</code></pre>
  </li>
</ol>

<hr>

<h2>🌏 Features</h2>
<ul>
  <li>Generate <strong>random Indian city waste data</strong></li>
  <li>Calculate distances using <strong>adjusted Haversine formula</strong></li>
  <li>Optimize routes with <strong>Google OR-Tools</strong></li>
  <li>Interactive map visualization via <strong>Folium</strong></li>
  <li>Indian-themed UI and waste education section</li>
  <li>Download routes as CSV for reporting</li>
</ul>

<hr>

<h2>📌 Best Practices Promoted</h2>
<ul>
  <li>Waste segregation at source</li>
  <li>Support for informal waste sector</li>
  <li>Community engagement and education</li>
  <li>Public-private collaboration (PPP model)</li>
</ul>

<hr>

<h2>📧 Contact</h2>
<p>
  <strong>Vivek H S</strong><br>
  📍 Bengaluru, India<br>
  🔗 <a href="https://github.com/smartswagvivek" target="_blank">GitHub: @smartswagvivek</a>
</p>

</body>
</html>
