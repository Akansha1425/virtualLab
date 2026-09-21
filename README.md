# KGIRS Virtual Lab

A Streamlit-based Virtual Laboratory for learning **Information Retrieval (IR)** and **Knowledge Graphs (KG)** through theory, simulations, quizzes, and reports.

## Features

- 📘 Theory module
- 🧪 Interactive simulation
- 📝 Quiz with scoring
- 📄 Report generation
- 🔍 Document retrieval
- 🌐 Knowledge Graph visualization

## Project Structure

```text
virtuallab/
├── app.py
├── theory.py
├── simulation.py
├── quiz.py
├── report.py
├── retriever.py
├── graph_builder.py
├── document_loader.py
├── requirements.txt
└── documents/
```

## Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/virtuallab.git
cd virtuallab
```

2. Create a virtual environment

```bash
python -m venv .venv
```

3. Activate the environment

**Windows**

```bash
.venv\Scripts\activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Run the Streamlit app

```bash
streamlit run app.py
```

## Technologies Used

- Python
- Streamlit
- NetworkX
- Plotly
- LangChain

## Author
Akansha Zambare
Developed as an academic Virtual Lab project.
