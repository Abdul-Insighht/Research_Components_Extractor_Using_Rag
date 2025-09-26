

# paper_extractor_app.py
import streamlit as st
import io
import os
import json
import re
import textwrap
from dotenv import load_dotenv
from pypdf import PdfReader
import requests

# LangChain / Google Gemini
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# --------------------------
# Configuration
# --------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("🔑 GOOGLE_API_KEY not found. Put it into a .env file like: GOOGLE_API_KEY=your_api_key")
    st.stop()

# deterministic extraction
MODEL = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=API_KEY, temperature=0)

# --------------------------
# Enhanced Custom CSS with Dark Professional Theme
# --------------------------
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .main {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        min-height: 100vh;
        font-family: 'Inter', sans-serif;
    }
    
    .main > div {
        background: transparent;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .header-subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
        font-weight: 300;
        color: #e2e8f0;
    }
    
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }
    
    /* Upload section styling */
    .upload-container {
        background: rgba(30, 41, 59, 0.9);
        border: 2px dashed #3b82f6;
        border-radius: 15px;
        padding: 2.5rem;
        margin: 2rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .upload-container h3 {
        color: #e2e8f0;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    
    /* Results section styling */
    .results-container {
        background: rgba(30, 41, 59, 0.95);
        border-radius: 15px;
        padding: 2.5rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Card styling */
    .info-card {
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #3b82f6;
        color: #e2e8f0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .success-card {
        background: linear-gradient(135deg, #065f46 0%, #047857 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #10b981;
        color: #d1fae5;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #92400e 0%, #b45309 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #f59e0b;
        color: #fef3c7;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .summary-card {
        background: linear-gradient(135deg, #581c87 0%, #7c3aed 100%);
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 4px solid #8b5cf6;
        color: #e9d5ff;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border-radius: 30px;
        border: none;
        padding: 1rem 2.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f1f5f9;
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid #3b82f6;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Field styling */
    .field-container {
        background: rgba(51, 65, 85, 0.8);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 3px solid #3b82f6;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .field-label {
        font-weight: 600;
        color: #60a5fa;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .field-value {
        color: #e2e8f0;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* List styling */
    .custom-list {
        background: rgba(51, 65, 85, 0.6);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .list-item {
        background: rgba(71, 85, 105, 0.8);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 3px solid #60a5fa;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        color: #e2e8f0;
        line-height: 1.7;
    }
    
    .list-item strong {
        color: #93c5fd;
        font-weight: 600;
    }
    
    /* Evidence styling */
    .evidence-item {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 3px solid #34d399;
        font-style: italic;
        color: #a7f3d0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(51, 65, 85, 0.8);
        color: #e2e8f0;
        border: 1px solid #475569;
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 1px #3b82f6;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: rgba(51, 65, 85, 0.8);
        border: 2px dashed #475569;
        border-radius: 8px;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #94a3b8;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        color: #94a3b8;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
    }
    
    /* Markdown text color */
    .markdown-text-container {
        color: #e2e8f0;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(51, 65, 85, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
    }
    </style>
    """, unsafe_allow_html=True)

# --------------------------
# Helpers: PDF reading + chunking (unchanged)
# --------------------------
def read_pdf_bytes(pdf_bytes: bytes):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = []
    for p in reader.pages:
        try:
            txt = p.extract_text() or ""
        except Exception:
            txt = ""
        # normalize whitespace
        txt = "\n".join([line.strip() for line in txt.splitlines() if line.strip()])
        pages.append(txt)
    return pages

def chunk_pages(pages_text, max_chars=12000, max_pages_per_chunk=5):
    chunks = []
    cur_pages = []
    cur_len = 0
    start_page = 1
    for i, pg in enumerate(pages_text, start=1):
        add_len = len(pg)
        page_count = len(cur_pages) + 1
        if (cur_len + add_len > max_chars) or (page_count > max_pages_per_chunk):
            chunks.append({
                "start_page": start_page,
                "end_page": start_page + len(cur_pages) - 1,
                "text": "\n\n".join(cur_pages)
            })
            cur_pages = [pg]
            cur_len = add_len
            start_page = i
        else:
            cur_pages.append(pg)
            cur_len += add_len
    if cur_pages:
        chunks.append({
            "start_page": start_page,
            "end_page": start_page + len(cur_pages) - 1,
            "text": "\n\n".join(cur_pages)
        })
    return chunks

# --------------------------
# Prompt templates (unchanged + new summary prompt)
# --------------------------
CHUNK_PROMPT_TPL = textwrap.dedent("""
You are an expert academic information extractor. Extract information ONLY from the CHUNK below.
Return EXACTLY one JSON object and nothing else.

Schema (types):
{{
  "title": null | string,
  "venue": null | string,
  "year": null | integer,
  "datasets": [{{"name": string, "page": integer, "quote": string}}],
  "limitations_addressed": [{{"heading": string, "explanation": string, "page": integer, "quote": string}}],
  "contributions": [{{"heading": string, "explanation": string, "page": integer, "quote": string}}],
  "methods": [{{"heading": string, "explanation": string, "page": integer, "quote": string}}],
  "paper_limitations": [{{"heading": string, "explanation": string, "page": integer, "quote": string}}],
  "evidence": [{{"page": integer, "quote": string}}]
}}

Rules:
- DO NOT invent data. If a field is not present in this chunk, use null (for scalars) or [] (for lists).
- For lists (datasets, limitations_addressed, etc.) produce objects with page and short quote (<=25 words).
- Use page numbers that correspond to the actual PDF pages (between {start_page} and {end_page}).
- Keep quotes short and directly from the text.
- For headings use short phrase (3-6 words). Explanations: 1-2 concise sentences.
- Do NOT output additional commentary or markdown.

CHUNK PAGES: {start_page} - {end_page}
CHUNK TEXT:
---
{chunk_text}
---
""")

REDUCER_PROMPT_TPL = textwrap.dedent("""
You are an expert data merger for structured JSONs extracted from chunks of a PDF.
You will be given a JSON array of partial extraction objects (each following the schema below).
Merge them into a single final JSON object following the same schema.

Schema of each partial:
{{
  "title": null | string,
  "venue": null | string,
  "year": null | integer,
  "datasets": [{{"name": string, "page": integer, "quote": string}}],
  "limitations_addressed": [...],
  "contributions": [...],
  "methods": [...],
  "paper_limitations": [...],
  "evidence": [...]
}}

Merging rules:
- For scalar fields (title, venue, year): prefer entries which have evidence (non-null) and choose the one with the clearest quote. If multiple different values exist and it's ambiguous, set null.
- For list fields: combine all items, deduplicate by normalized key (for datasets normalize by removing non-alphanumeric and lowercasing; for headings normalize by lowercasing and trimming). Preserve the original 'name'/'heading' as first occurrence.
- Evidence: include unique evidence items sorted by page.
- Do NOT invent missing information.

Return exactly one JSON object and nothing else.

Partials:
{partials_json}
""")

# NEW: Summary prompt template
SUMMARY_PROMPT_TPL = textwrap.dedent("""
You are an expert academic summarizer. Create a comprehensive summary of this research paper.

Paper content:
---
{paper_text}
---

Please provide a structured summary with the following sections:

**Abstract/Overview** (2-3 sentences): Main purpose and key findings
**Problem Statement** (1-2 sentences): What problem does this paper address?
**Methodology** (2-3 sentences): How did they approach the problem?
**Key Contributions** (3-4 bullet points): Main innovations or findings
**Results** (1-2 sentences): What were the main outcomes?
**Limitations** (1-2 sentences): What are the acknowledged limitations?
**Impact** (1-2 sentences): Why is this work important?

Keep the summary concise but comprehensive, focusing on the most important aspects of the research.
""")

# --------------------------
# Parse model JSON robustly (unchanged)
# --------------------------
def parse_json_loose(s: str):
    if not isinstance(s, str):
        return s
    text = s.strip()
    # remove triple-fence blocks
    if text.startswith("```"):
        text = re.sub(r"^```[\w]*", "", text)
        text = text.rsplit("```", 1)[0]
    # find first { ... } block
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in model output.")
    json_text = text[start:end+1]
    return json.loads(json_text)

# --------------------------
# LLM call helper (unchanged)
# --------------------------
def llm_json_call(prompt_text: str):
    res = MODEL.invoke(prompt_text)
    content = getattr(res, "content", res)
    return parse_json_loose(content)

def llm_text_call(prompt_text: str):
    """For non-JSON responses like summaries"""
    res = MODEL.invoke(prompt_text)
    content = getattr(res, "content", res)
    return content

# --------------------------
# Normalization helpers (unchanged)
# --------------------------
def normalize_dataset_key(name: str):
    # remove non-alphanum, lower
    return re.sub(r"[^0-9a-z]", "", name.lower())

def dedupe_datasets(dataset_objs):
    seen = {}
    result = []
    for d in dataset_objs:
        name = d.get("name", "").strip()
        if not name:
            continue
        key = normalize_dataset_key(name)
        if key not in seen:
            seen[key] = True
            result.append(d)
    return result

def dedupe_list_of_heading_objs(items):
    seen = set()
    out = []
    for it in items:
        heading = (it.get("heading") or "").strip()
        if not heading:
            continue
        key = heading.lower()
        if key not in seen:
            seen.add(key)
            out.append(it)
    return out

# --------------------------
# Enhanced rendering helpers
# --------------------------
def render_basic_info(merged):
    """Render basic paper information in cards"""
    st.markdown('<div class="section-header">📝 Paper Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="field-container">
            <div class="field-label">📋 Title</div>
            <div class="field-value">{merged.get('title') or '<em>Not mentioned in paper</em>'}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="field-container">
            <div class="field-label">🏛️ Venue</div>
            <div class="field-value">{merged.get('venue') or '<em>Not mentioned in paper</em>'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="field-container">
            <div class="field-label">📅 Year</div>
            <div class="field-value">{merged.get('year') or '<em>Not mentioned in paper</em>'}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Normalize dataset list to simple names for display
        dataset_names = []
        for d in merged.get("datasets", []):
            name = d.get("name") if isinstance(d, dict) else d
            if name and name not in dataset_names:
                dataset_names.append(name)
        
        datasets_display = ", ".join(dataset_names) if dataset_names else '<em>Not mentioned in paper</em>'
        st.markdown(f"""
        <div class="field-container">
            <div class="field-label">🗂️ Datasets</div>
            <div class="field-value">{datasets_display}</div>
        </div>
        """, unsafe_allow_html=True)

def render_heading_expl_list(st_title, items, icon="📌"):
    """Render lists with enhanced styling"""
    st.markdown(f'<div class="section-header">{icon} {st_title}</div>', unsafe_allow_html=True)
    
    if not items:
        st.markdown(f"""
        <div class="warning-card">
            <em>Not mentioned in paper</em>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown('<div class="custom-list">', unsafe_allow_html=True)
    for it in items:
        heading = it.get("heading") or ""
        explanation = it.get("explanation") or ""
        page = it.get("page")
        quote = it.get("quote")
        
        evidence_text = ""
        if page and quote:
            evidence_text = f'<div style="margin-top: 1rem; font-size: 0.9em; color: #94a3b8; font-style: italic;"><strong>📄 Page {page}:</strong> "{quote}"</div>'
        
        if heading and explanation:
            content = f'<strong>{heading.strip()}</strong><br/><div style="margin-top: 0.5rem;">{explanation.strip()}</div>{evidence_text}'
        elif explanation:
            content = f'{explanation.strip()}{evidence_text}'
        else:
            content = f'{heading.strip()}{evidence_text}'
            
        st.markdown(f'<div class="list-item">{content}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_evidence(evidence_items):
    """Render evidence with special styling"""
    if not evidence_items:
        return
        
    st.markdown('<div class="section-header">🔍 Supporting Evidence</div>', unsafe_allow_html=True)
    
    for e in evidence_items:
        pnum = e.get("page", "?")
        quote = e.get("quote", "")
        st.markdown(f"""
        <div class="evidence-item">
            <strong>📄 Page {pnum}:</strong> "{quote}"
        </div>
        """, unsafe_allow_html=True)

def render_summary(summary_text):
    """Render paper summary with special styling"""
    st.markdown('<div class="section-header">📊 Paper Summary</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="summary-card">
        <div class="markdown-text-container">
            {summary_text.replace(chr(10), '<br/>')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --------------------------
# Enhanced Streamlit UI
# --------------------------
st.set_page_config(
    page_title="Research PDF Extractor", 
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
load_custom_css()

# Enhanced header
st.markdown("""
<div class="header-container">
    <div class="header-title">📚 Research PDF Extractor</div>
    <div class="header-subtitle">AI-Powered Academic Paper Analysis, Information Extraction & Summarization</div>
</div>
""", unsafe_allow_html=True)

# Main upload section
st.markdown('<div class="upload-container">', unsafe_allow_html=True)
st.markdown('<h3 style="color: #e2e8f0; margin-bottom: 1.5rem;">📁 Upload Your Research Paper</h3>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    uploaded_file = st.file_uploader("Choose PDF file", type=["pdf"], help="Select a research paper in PDF format")
    pdf_url = st.text_input("Or enter PDF URL", placeholder="https://example.com/paper.pdf", help="Provide a direct link to a PDF file")

with col2:
    title_hint = st.text_input("Paper title (optional)", placeholder="Enter paper title to help with extraction", help="If you know the paper title, it can improve extraction accuracy")
    
    st.markdown("""
    <div style="color: #e2e8f0; margin-top: 1rem;">
        <h4 style="color: #60a5fa; margin-bottom: 1rem;">🎯 What will be extracted:</h4>
        <ul style="list-style-type: none; padding-left: 0;">
            <li style="margin: 0.5rem 0;">📋 <strong>Basic Info:</strong> Title, venue, publication year</li>
            <li style="margin: 0.5rem 0;">🗂️ <strong>Datasets:</strong> All mentioned datasets</li>
            <li style="margin: 0.5rem 0;">🎯 <strong>Contributions:</strong> Key research contributions</li>
            <li style="margin: 0.5rem 0;">🔧 <strong>Methods:</strong> Approaches and methodologies</li>
            <li style="margin: 0.5rem 0;">⚠️ <strong>Limitations:</strong> Both addressed and paper's own</li>
            <li style="margin: 0.5rem 0;">📊 <strong>Summary:</strong> Comprehensive paper overview</li>
            <li style="margin: 0.5rem 0;">🔍 <strong>Evidence:</strong> Supporting quotes and references</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Process button with enhanced styling
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Extract & Summarize", type="primary", use_container_width=True):
        # Load PDF bytes
        if not uploaded_file and not pdf_url:
            st.markdown("""
            <div class="warning-card">
                ⚠️ <strong>Missing Input:</strong> Please upload a PDF file or provide a PDF URL to continue.
            </div>
            """, unsafe_allow_html=True)
            st.stop()
            
        # Loading indicator
        with st.spinner("Loading PDF..."):
            try:
                if uploaded_file:
                    pdf_bytes = uploaded_file.read()
                    st.markdown(f"""
                    <div class="info-card">
                        📁 <strong>File loaded:</strong> {uploaded_file.name} ({len(pdf_bytes):,} bytes)
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    r = requests.get(pdf_url, timeout=60)
                    r.raise_for_status()
                    pdf_bytes = r.content
                    st.markdown(f"""
                    <div class="info-card">
                        🌐 <strong>URL loaded:</strong> {len(pdf_bytes):,} bytes retrieved
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="warning-card">
                    ❌ <strong>Error loading PDF:</strong> {str(e)}
                </div>
                """, unsafe_allow_html=True)
                st.stop()

        # Process PDF
        with st.spinner("Extracting text from PDF..."):
            pages = read_pdf_bytes(pdf_bytes)
            if not pages or all(p.strip()=="" for p in pages):
                st.markdown("""
                <div class="warning-card">
                    ❌ <strong>No extractable text found:</strong> This PDF might be scanned or image-based. Please provide a searchable PDF or use OCR preprocessing.
                </div>
                """, unsafe_allow_html=True)
                st.stop()

            st.markdown(f"""
            <div class="success-card">
                ✅ <strong>PDF processed successfully:</strong> {len(pages)} pages of text extracted
            </div>
            """, unsafe_allow_html=True)

        # Chunk processing
        chunks = chunk_pages(pages, max_chars=12000, max_pages_per_chunk=5)
        
        st.markdown(f"""
        <div class="info-card">
            🔄 <strong>Processing:</strong> Analyzing {len(chunks)} chunks with AI model...
        </div>
        """, unsafe_allow_html=True)

        # Progress tracking
        partials = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, ch in enumerate(chunks, start=1):
            status_text.text(f"Processing chunk {i}/{len(chunks)} (pages {ch['start_page']}-{ch['end_page']})")
            
            prompt = CHUNK_PROMPT_TPL.format(
                chunk_text=ch["text"], 
                start_page=ch["start_page"], 
                end_page=ch["end_page"]
            )
            
            try:
                partial = llm_json_call(prompt)
            except Exception as e:
                partial = {
                    "title": None, "venue": None, "year": None,
                    "datasets": [], "limitations_addressed": [], "contributions": [],
                    "methods": [], "paper_limitations": [], "evidence": []
                }
                partial["_error"] = str(e)
            
            partials.append(partial)
            progress_bar.progress(i/len(chunks))

        status_text.text("Merging results...")

        # Merge results
        try:
            partials_json = json.dumps(partials, ensure_ascii=False)
            reducer_prompt = REDUCER_PROMPT_TPL.format(partials_json=partials_json)
            merged = llm_json_call(reducer_prompt)
        except Exception as e:
            st.warning(f"Merger failed: {e}. Using fallback merge.")
            # fallback: naive merge
            merged = {
                "title": None, "venue": None, "year": None,
                "datasets": [], "limitations_addressed": [], "contributions": [],
                "methods": [], "paper_limitations": [], "evidence": []
            }
            # naive aggregation
            for p in partials:
                for k in merged.keys():
                    if isinstance(merged[k], list):
                        merged[k].extend(p.get(k, []) or [])
                    else:
                        if not merged[k] and p.get(k):
                            merged[k] = p.get(k)

        # Post-process: dedupe datasets & headings
        merged["datasets"] = dedupe_datasets(merged.get("datasets", []))
        merged["limitations_addressed"] = dedupe_list_of_heading_objs(merged.get("limitations_addressed", []))
        merged["contributions"] = dedupe_list_of_heading_objs(merged.get("contributions", []))
        merged["methods"] = dedupe_list_of_heading_objs(merged.get("methods", []))
        merged["paper_limitations"] = dedupe_list_of_heading_objs(merged.get("paper_limitations", []))

        # If title missing, use hint
        if not merged.get("title") and title_hint:
            merged["title"] = title_hint

        # NEW: Generate paper summary
        status_text.text("Generating paper summary...")
        try:
            # Take first 5 pages or up to 15000 chars for summary
            summary_text = "\n\n".join(pages[:5])
            if len(summary_text) > 15000:
                summary_text = summary_text[:15000] + "..."
            
            summary_prompt = SUMMARY_PROMPT_TPL.format(paper_text=summary_text)
            paper_summary = llm_text_call(summary_prompt)
        except Exception as e:
            paper_summary = f"Summary generation failed: {str(e)}"

        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()

        # Display results with enhanced UI using tabs
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        
        # Create tabs for different views
        tab1, tab2 = st.tabs(["📊 Summary & Overview", "📝 Detailed Extraction"])
        
        with tab1:
            # Paper Summary (NEW)
            render_summary(paper_summary)
            
            # Basic information
            render_basic_info(merged)
            
        with tab2:
            # Detailed sections
            render_heading_expl_list("Limitations Addressed", merged.get("limitations_addressed", []), "🎯")
            render_heading_expl_list("Contributions & Solutions", merged.get("contributions", []), "💡")
            render_heading_expl_list("Methods & Approaches", merged.get("methods", []), "🔧")
            render_heading_expl_list("Paper Limitations", merged.get("paper_limitations", []), "⚠️")
            
            # Evidence section
            render_evidence(merged.get("evidence", []))
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Download section
        st.markdown('<div class="section-header">💾 Export Results</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Download JSON extraction
            out_bytes = json.dumps(merged, ensure_ascii=False, indent=2).encode("utf-8")
            st.download_button(
                "⬇️ Download Extraction (JSON)",
                data=out_bytes,
                file_name="paper_extraction.json",
                mime="application/json",
                use_container_width=True
            )
            
        with col2:
            # Download summary as text
            summary_bytes = f"PAPER SUMMARY\n{'='*50}\n\n{paper_summary}".encode("utf-8")
            st.download_button(
                "📄 Download Summary (TXT)",
                data=summary_bytes,
                file_name="paper_summary.txt",
                mime="text/plain",
                use_container_width=True
            )

        # Success message
        st.markdown("""
        <div class="success-card">
            🎉 <strong>Processing Complete!</strong> Your research paper has been successfully analyzed, summarized, and all available information has been extracted. 
            If some fields show "Not mentioned", they may not be present in the searchable text or could be in figures/images only.
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>🤖 Powered by Google Gemini AI • 📚 Built for Academic Research • 🔬 Enhanced with Summarization</p>
    <p><em>For scanned PDFs, consider using OCR preprocessing (pdf2image + pytesseract) before upload.</em></p>
    <p style="margin-top: 1rem; font-size: 0.9em; opacity: 0.7;">
        ✨ Features: Structure Extraction • Intelligent Summarization • Evidence Collection • Export Options
    </p>
</div>
""", unsafe_allow_html=True)