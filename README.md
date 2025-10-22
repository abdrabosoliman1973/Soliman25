# 📚 Academic Paraphraser with LM Studio

This Streamlit app provides a clean academic paraphrasing interface powered by locally hosted LM Studio models (Mistral, LLaMA, T5, etc.).

---

## 🚀 Features
- Upload `.txt` or `.docx` files
- Choose from multiple LM Studio models
- Paraphrase academic text while preserving citations, numbers, and tone
- Download results as `.txt` or `.docx`

---

## 🧰 Requirements
- Python 3.9+
- LM Studio running locally at `http://localhost:1234`
- Streamlit Cloud or local environment

---

## ⚙️ Installation
```bash
git clone https://github.com/<your-username>/academic-paraphraser.git
cd academic-paraphraser
pip install -r requirements.txt
streamlit run app.py
