import streamlit as st
from PIL import Image
from ocr_engine import run_ocr


st.set_page_config(
    page_title="Text Recognition",
    layout="wide",
)

st.markdown("""
<style>
    .stButton > button {
        background-color: #1a1a2e;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        padding: 0.6em;
    }
    .stButton > button:hover {
        background-color:  #333333;
        color: white !important;
        border-color: #333333;
    }

    .st-key-blue_download_btn button {
            background-color: #0066cc; 
            color: white !important;
            border-color: #0066cc ;
            border-radius: 8px ;
    }
        
    .st-key-blue_download_btn button:hover {
            background-color: #0052a3;
            border-color: #0052a3;
    }
            
    .result-box {
        background: #f0f4ff;
        border-left: 5px solid #4A90E2;
        padding: 16px 20px;
        border-radius: 0 8px 8px 0;
        font-family: monospace;
        white-space: pre-wrap;
        font-size: 0.95rem;
        min-height: 80px;
    }
    .pass  { color: #28a745; font-weight: bold; font-size: 1.1rem; }
    .fail  { color: #dc3545; font-weight: bold; font-size: 1.1rem; }
    .info-row { background: #e8f4f8; padding: 10px 16px;
                border-radius: 8px; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)


st.title(" Text Recognizer")
st.markdown("---")

left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("Input")

    uploaded = st.file_uploader(
        "Upload an image (PNG, JPG, BMP, TIFF)",
        type=["png", "jpg", "jpeg", "bmp", "tiff"],
    )

    st.markdown("**Page Segmentation Mode (PSM)**")
    psm_map = {
        "PSM 3 – Fully automatic (default)":            3,
        "PSM 6 – Single uniform block of text":         6,
        "PSM 7 – Single text line (headers / plates)":  7,
        "PSM 11 – Sparse / scattered text (invoices)": 11,
    }
    psm_label = st.selectbox("", list(psm_map.keys()), label_visibility="collapsed")
    psm = psm_map[psm_label]

    show_steps = st.checkbox("Show pre-processing steps", value=True)

    run_btn = st.button("Run OCR")

    if uploaded:
        st.image(uploaded, caption="Uploaded image",width="stretch")

with right:
    st.subheader("Results")

    if run_btn:
        if not uploaded:
            st.error("Please upload an image first.")
        else:
            image = Image.open(uploaded).convert("RGB")

            with st.spinner("Running OCR pipeline…"):
                result = run_ocr(image, psm=psm)

            if show_steps:
                st.markdown("**Pre-processing Steps:**")
                t1, t2, t3, t4 = st.tabs(
                    ["1 . Original", "2 . Grayscale", "3 . Threshold", "4 . Deskewed"]
                )
                with t1:
                    st.image(result["original"], width="stretch")
                with t2:
                    st.image(result["gray"],     width="stretch", clamp=True)
                with t3:
                    st.image(result["thresh"],   width="stretch", clamp=True)
                with t4:
                    st.image(result["deskewed"], width="stretch", clamp=True)

            st.markdown("**Extracted Text:**")
            display_text = result["text"] if result["text"] else "(no text detected)"
            st.markdown(
                f'<div class="result-box">{display_text}</div>',
                unsafe_allow_html=True
            )

            conf = result["confidence"]
            gate_pass = conf >= 80.0
            css_class = "pass" if gate_pass else "fail"
            gate_label = "PASSES 80% confidence gate" if gate_pass else "BELOW 80% threshold"

            st.markdown(
                f'<p class="{css_class}">Confidence: {conf:.1f}% &nbsp;|&nbsp; {gate_label}</p>',
                unsafe_allow_html=True,
            )

            words = [w for w in result["text"].split() if w.strip()]
            st.markdown(
                f'<div class="info-row">&nbsp;'
                f'Words detected: <b>{len(words)}</b> &nbsp;|&nbsp; '
                f'Characters: <b>{len(result["text"])}</b> &nbsp;|&nbsp; '
                f'PSM used: <b>{psm}</b></div>',
                unsafe_allow_html=True,
            )
            st.space("small") 

            st.download_button(
                label="Download extracted text(.txt)",
                data=result["text"],
                file_name="ocr_output.txt",
                mime="text/plain",
                key="blue_download_btn"
            )
    else:
        st.info("Upload an image and click **Run OCR** to begin.")

