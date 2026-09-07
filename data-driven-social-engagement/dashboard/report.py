import streamlit as st
from reports.strategy_report import create_markdown_report
from reports.generate_report import export_to_pdf
import os
import uuid

def render_report(df_content, df_comments, df_trends):
    st.title("Data-Backed Strategy Report")
    
    st.markdown("This report is dynamically generated from the current dataset and analytics outputs.")
    
    if df_content is None or df_content.empty:
        st.warning("Data not available to generate report.")
        return
        
    report_md = create_markdown_report(df_content, df_comments, df_trends)
    
    with st.expander("Preview Strategy Report", expanded=True):
        st.markdown(report_md)
        
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📄 Download Markdown Report",
            data=report_md,
            file_name="social_strategy_report.md",
            mime="text/markdown"
        )
        
    with col2:
        if st.button("Generate PDF Report"):
            with st.spinner("Generating PDF..."):
                try:
                    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                    reports_dir = os.path.join(BASE_DIR, 'data')
                    os.makedirs(reports_dir, exist_ok=True)
                    
                    pdf_path = os.path.join(reports_dir, f"strategy_report_{uuid.uuid4().hex[:8]}.pdf")
                    export_to_pdf(report_md, pdf_path)
                    
                    with open(pdf_path, "rb") as pdf_file:
                        PDFbyte = pdf_file.read()
                        
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=PDFbyte,
                        file_name="social_strategy_report.pdf",
                        mime='application/octet-stream'
                    )
                except Exception as e:
                    st.error(f"Failed to generate PDF: {e}")
                    st.info("You may need to ensure 'fpdf2' is installed via requirements.txt")
