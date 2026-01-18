# Research Components Extractor using RAG

This project implements a **Research Components Extractor** using a **Retrieval-Augmented Generation (RAG)** approach. It extracts and summarizes key components of research papers such as **Abstract, Introduction, Methodology, Dataset, Architecture, Contributions, and Limitations**.

---

## 🚀 Features
- Extracts structured components from research papers  
- Uses **RAG** (Retrieval-Augmented Generation) for better accuracy  
- Handles PDF and text-based research documents  
- Outputs summaries for each section  
- Configurable through environment variables  

---

## 📂 Project Structure
```
Research_Components_Extractor_Using_Rag/
│── main.py                # Main entry point
│── requirements.txt       # Python dependencies
│── .env                   # Environment variables (API keys, configs)
│── my_project_env/        # Local virtual environment (not required)
```

---

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd Research_Components_Extractor_Using_Rag
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # For Linux/Mac
   venv\Scripts\activate      # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:  
   Create a `.env` file and add required keys:
   ```
   OPENAI_API_KEY=your_api_key_here
   VECTOR_DB_PATH=./vector_store
   ```

---

## ▶️ Usage
Run the extractor:
```bash
python main.py
```

You will be prompted to provide the path of a research paper (PDF/text), and the system will output extracted components.

---

## 🛠️ Tech Stack
- **Python 3.10+**
- **LangChain** (for RAG pipeline)  
- **OpenAI / HuggingFace models** (for LLMs)  
- **FAISS / Chroma** (for vector storage)  

---

## 📊 Example Output
For a given research paper, the tool extracts:

- **Abstract** → Concise summary of the paper  
- **Introduction** → Research problem and motivation  
- **Methodology** → Techniques and approaches used  
- **Dataset** → Details of datasets used  
- **Architecture** → Model or system design  
- **Contributions** → Key findings of the work  
- **Limitations** → Weaknesses and constraints  

---

## ⚠️ Limitations
- Depends on the quality of PDF/text extraction  
- Requires API access (OpenAI or HuggingFace models)  
- May miss information if paper structure is irregular  

---

## 🤝 Contribution
Feel free to fork this project and submit pull requests for:
- New extraction modules  
- Additional dataset support  
- Better UI integration  

---

## 📜 License
This project is licensed under the MIT License.


---

## 📬 Contact

**Hafiz Abdul Rehman**

- 📧 Email: hafizrehman3321@gmail.com
- 💼 LinkedIn: [Hafiz Abdul Rehman](https://linkedin.com/in/hafiz-abdul-rehman-9990ab329)
- 🐙 GitHub: [Abdul-Insighht](https://github.com/Abdul-Insighht)

---

## 🌟 Show Your Support

If you find this project helpful, please consider:

- ⭐ **Starring** this repository
- 🔄 **Sharing** with others
- 🐛 **Reporting** issues
- 💡 **Suggesting** improvements

---

<p align="center">Made with ❤️ by <b>Hafiz Abdul Rehman</b></p>
