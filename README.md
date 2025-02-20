# SmartFlow-AI
*SmartFlow-AI* is an AI-powered learning roadmap generator that helps users create structured step-by-step learning paths for any topic. It uses OpenAI GPT to generate learning steps and Graphviz to visualize them in an interactive flowchart.

## Features
- Generate customized learning roadmaps for any topic
- Interactive flowchart visualization using Graphviz
- User-friendly web interface
- Export roadmaps in multiple formats (PNG, PDF)
- Customizable learning paths

## Installation

### Prerequisites
- Node.js (v14 or higher)
- Python (v3.8 or higher)
- OpenAI API Key
- Graphviz installed on your system

### Setup Steps

1. Install Graphviz (System Dependency)
```bash
brew install graphviz
```

### Setup
1. Clone the repository
```bash
git clone https://github.com/tamilselvan-sde/SmartFlow-AI.git
cd SmartFlow-AI
```
```
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```


```
cd frontend
npm install

```


```
cd backend
source venv/bin/activate  # On Windows use: venv\Scripts\activate
python app.py
```

```
SmartFlow-AI/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── venv/
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── output/
│   └── sample_roadmaps/
└── README.md

```
## Contact & Support
For any queries, issues, or support:

- Email: tamilselvan-sde@gmail.com
- Create an issue on GitHub
