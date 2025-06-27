from pathlib import Path

import pandas as pd
import streamlit as st

from core.parser import parse_resume, _normalize  # noqa: WPS437 (private import for speed)
from core.ranker import Ranker

st.set_page_config(
    page_title="AI‑Powered Resume Screener",
    page_icon="📄",
    layout="wide",
)

st.title("📄 AI‑Powered Resume Screener")

with st.sidebar:
    st.header("1️⃣ Job Description")
    job_description = st.text_area("Paste or type here", height=260)

    st.header("2️⃣ Resumes")
    uploaded_files = st.file_uploader(
        "Upload PDF / DOCX resumes",
        accept_multiple_files=True,
    )

if st.button("🚀 Rank Candidates") and job_description and uploaded_files:
    with st.spinner("Parsing resumes …"):
        resume_objs = []
        for up_file in uploaded_files:
            # Write to a temporary file so pdfplumber / python‑docx can open it.
            tmp_path = Path(st.session_state.get("tmp_dir", "/tmp")) / up_file.name
            tmp_path.write_bytes(up_file.getbuffer())
            resume_objs.append(parse_resume(tmp_path))

    with st.spinner("Computing similarity …"):
        ranker = Ranker()
        ranker.fit([r["raw_text"] for r in resume_objs] + [_normalize(job_description)])
        ranked = ranker.rank(resume_objs, _normalize(job_description))

    df = pd.DataFrame(
        {
            "File": [r["filename"] for r in ranked],
            "Name": [r.get("name") for r in ranked],
            "Skills": [", ".join(r["skills"]) for r in ranked],
            "Score": [round(r["score"], 3) for r in ranked],
        }
    )

    st.success(
        f"Top candidate: **{df.iloc[0]['Name'] or df.iloc[0]['File']}**  — score {df.iloc[0]['Score']:.3f}"
    )
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf‑8")
    st.download_button(
        "⬇️ Download CSV",
        data=csv,
        file_name="ranked_candidates.csv",
        mime="text/csv",
    )
else:
    st.info("Enter a job description and upload resumes to get started.")