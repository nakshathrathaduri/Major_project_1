from fpdf import FPDF

def export_to_pdf(markdown_text, output_path):
    """
    Simple export of markdown to PDF using fpdf2.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Very simple markdown parser for PDF
    for line in markdown_text.split('\n'):
        if line.startswith('# '):
            pdf.set_font("helvetica", "B", 18)
            pdf.cell(0, 10, line[2:], ln=True)
        elif line.startswith('## '):
            pdf.set_font("helvetica", "B", 14)
            pdf.cell(0, 10, line[3:], ln=True)
        elif line.startswith('### '):
            pdf.set_font("helvetica", "B", 12)
            pdf.cell(0, 8, line[4:], ln=True)
        elif line.startswith('* '):
            pdf.set_font("helvetica", "", 11)
            # Remove bold markdown asterisks for simple rendering
            clean_line = line.replace('**', '')
            pdf.multi_cell(0, 6, clean_line)
        elif line.strip() == '':
            pdf.ln(4)
        else:
            pdf.set_font("helvetica", "", 11)
            clean_line = line.replace('**', '')
            pdf.multi_cell(0, 6, clean_line)
            
    pdf.output(output_path)
    return output_path
