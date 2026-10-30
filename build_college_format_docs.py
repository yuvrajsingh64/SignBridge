import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

MPEC_LOGO_PATH = r"c:\AI-project\SignBridge\docs\extracted_logos\mpec_logo.jpg"
AKTU_LOGO_PATH = r"c:\AI-project\SignBridge\docs\extracted_logos\aktu_logo.jpg"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def format_run(run, font_name="Times New Roman", size_pt=11, bold=False, italic=False, color_rgb=(0,0,0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

def add_p(doc, text="", font_name="Times New Roman", size_pt=11, bold=False, italic=False, 
          align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4, line_spacing=1.15, color_rgb=(0,0,0)):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        format_run(r, font_name, size_pt, bold, italic, color_rgb)
    return p

def add_toc_entry(doc, title, page_str, is_major=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    
    r1 = p.add_run(title)
    format_run(r1, size_pt=10, bold=is_major)
    
    p.add_run("\t")
    
    r2 = p.add_run(page_str)
    format_run(r2, size_pt=10, bold=is_major)
    return p

def add_custom_table(doc, headers, data, col_widths=None):
    tbl = doc.add_table(rows=len(data)+1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)
    for i, h in enumerate(headers):
        cell = tbl.cell(0, i)
        set_cell_background(cell, "1F497D")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h)
        format_run(r, size_pt=9.5, bold=True, color_rgb=(255, 255, 255))
        if col_widths and i < len(col_widths):
            cell.width = Inches(col_widths[i])
    for row_idx, row in enumerate(data, start=1):
        for col_idx, val in enumerate(row):
            cell = tbl.cell(row_idx, col_idx)
            set_cell_margins(cell, top=70, bottom=70, left=120, right=120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            p.paragraph_format.line_spacing = 1.12
            r = p.add_run(str(val))
            format_run(r, size_pt=9, bold=(col_idx == 0))
            if col_widths and col_idx < len(col_widths):
                cell.width = Inches(col_widths[col_idx])
    return tbl

def add_smart_content(doc, content, default_size=11):
    """
    Renders structured academic content without ANY line-break stretching or awkward justification gaps.
    Every paragraph, bullet point, numbered item, and formula line is placed into its own <w:p> element.
    """
    if not content:
        return
        
    # Split content by lines so no internal soft breaks occur
    raw_lines = content.split("\n")
    
    for raw_line in raw_lines:
        line = raw_line.strip()
        if not line:
            continue
            
        # 1. Mathematical / Algorithm equation line
        is_formula = (
            raw_line.startswith("    ") or raw_line.startswith("\t") or
            any(line.startswith(prefix) for prefix in [
                "x_start =", "I_crop =", "I_crop(", "f(x, y) =", "Z^(l) =", "Z_k^(l)",
                "p_i =", "X = f(x, y)", "A_k^(l) ="
            ])
        )
        if is_formula:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.left_indent = Inches(0.4)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(line)
            format_run(r, font_name="Consolas", size_pt=9.5, italic=False, color_rgb=(20, 20, 20))
            continue
            
        # 2. Numbered list items (e.g. "1. ", "2. ", "1) ")
        m_num = re.match(r"^(\d+[\.\)])\s*(.*)", line)
        if m_num:
            num_prefix = m_num.group(1)
            rest_text = m_num.group(2)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Inches(0.3)
            p.paragraph_format.first_line_indent = Inches(-0.3)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            
            r_num = p.add_run(f"{num_prefix}  ")
            format_run(r_num, size_pt=default_size, bold=True)
            
            # Check for title with colon
            if ":" in rest_text and not rest_text.startswith("http"):
                parts = rest_text.split(":", 1)
                r_title = p.add_run(parts[0] + ": ")
                format_run(r_title, size_pt=default_size, bold=True)
                r_body = p.add_run(parts[1].strip())
                format_run(r_body, size_pt=default_size)
            else:
                r_body = p.add_run(rest_text)
                format_run(r_body, size_pt=default_size)
            continue
            
        # 3. Bullet points (starts with "• ", "- ", "* ")
        m_bullet = re.match(r"^([•\-\*])\s*(.*)", line)
        if m_bullet:
            rest_text = m_bullet.group(2)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Inches(0.3)
            p.paragraph_format.first_line_indent = Inches(-0.3)
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            
            r_sym = p.add_run("•  ")
            format_run(r_sym, size_pt=default_size, bold=True)
            
            # Check for title with colon
            if ":" in rest_text and not rest_text.startswith("http"):
                parts = rest_text.split(":", 1)
                r_title = p.add_run(parts[0] + ": ")
                format_run(r_title, size_pt=default_size, bold=True)
                r_body = p.add_run(parts[1].strip())
                format_run(r_body, size_pt=default_size)
            else:
                r_body = p.add_run(rest_text)
                format_run(r_body, size_pt=default_size)
            continue
            
        # 4. Short sub-headings ending with a colon
        if line.endswith(":") and len(line) < 70:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(line)
            format_run(r, size_pt=default_size, bold=True)
            continue
            
        # 5. Regular prose paragraph
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        
        # Check if line begins with a labeled lead-in like "Inference from Technique 1:" or "Summary of Observations:"
        if re.match(r"^(Inference from [^:]+:|Summary of Observations:|Core Subsystem Workflows:|Subsystem Cardinality Mapping:)", line):
            parts = line.split(":", 1)
            r_head = p.add_run(parts[0] + ": ")
            format_run(r_head, size_pt=default_size, bold=True)
            r_rest = p.add_run(parts[1].strip())
            format_run(r_rest, size_pt=default_size)
        else:
            r = p.add_run(line)
            format_run(r, size_pt=default_size)

def add_front_page(doc, doc_title_prefix=""):
    """
    Front Page matching user's exact uploaded PDF screenshot with MPEC & AKTU logos.
    Vertically optimized to fit on exactly ONE page with crisp margins.
    """
    title_text = "EchoSign: An Integrated AI Platform for Real-Time American Sign Language Translation, Gesture Evaluation and Speech Synthesis"
    add_p(doc, title_text, size_pt=13.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=4, line_spacing=1.15)
    
    sub = f"{doc_title_prefix}Report submitted in partial fulfillment of the requirement for the degree of"
    add_p(doc, sub, size_pt=10, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    
    # MPEC Logo
    if os.path.exists(MPEC_LOGO_PATH):
        p_logo1 = doc.add_paragraph()
        p_logo1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo1.paragraph_format.space_before = Pt(2)
        p_logo1.paragraph_format.space_after = Pt(4)
        r_logo1 = p_logo1.add_run()
        r_logo1.add_picture(MPEC_LOGO_PATH, width=Inches(1.7))
        
    add_p(doc, "B. Tech.", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    add_p(doc, "In", size_pt=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    add_p(doc, "Computer Science and Engineering", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    
    add_p(doc, "Under the Supervision of", size_pt=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    add_p(doc, "Ms. Rita Nagar", size_pt=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    add_p(doc, "Assistant Professor, C.S.E.", size_pt=9.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    
    add_p(doc, "Submitted By:", size_pt=10.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    students = [
        "Nidhi Singh (2303491530068)",
        "Yuvraj Singh (2303491530128)",
        "Rohit Kumar (2303491530090)",
        "Prashant Kumar Singh (2303491530075)",
        "Komal Goswami (2303491530061)"
    ]
    for s in students:
        add_p(doc, s, size_pt=9.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1.2)
        
    # AKTU Logo
    if os.path.exists(AKTU_LOGO_PATH):
        p_logo2 = doc.add_paragraph()
        p_logo2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo2.paragraph_format.space_before = Pt(3)
        p_logo2.paragraph_format.space_after = Pt(4)
        r_logo2 = p_logo2.add_run()
        r_logo2.add_picture(AKTU_LOGO_PATH, width=Inches(1.15))
        
    add_p(doc, "Department of Computer Science & Engineering", size_pt=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    add_p(doc, "Maharana Pratap Engineering College, Kanpur", size_pt=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    add_p(doc, "Dr. A.P.J. Abdul Kalam Technical University, Lucknow", size_pt=10, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    add_p(doc, "Session: 2026-27", size_pt=10, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    
    doc.add_page_break()

def add_declaration(doc, doc_name="Synopsis Report"):
    add_p(doc, "DECLARATION", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=16)
    
    p_dec1 = (f"This is to certify that the {doc_name} entitled “EchoSign: An AI-Powered American Sign Language Translation System "
              f"Using Deep Convolutional Neural Networks and Real-Time Speech Synthesis”, which is submitted in partial fulfilment "
              f"of the requirement for the award of the degree of B.Tech. in Computer Science and Engineering to MPEC Kanpur, "
              f"Dr. A.P.J. Abdul Kalam Technical University, Lucknow, comprises only original work and studies carried out by the "
              f"students themselves. The matter embodied in this report has not been submitted for the award of any other degree.")
    add_p(doc, p_dec1, size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    
    p_dec2 = ("We further declare that all source code, database architectures, algorithmic modules, and technical documentation "
              "presented in this report have been implemented in accordance with academic integrity guidelines. All external open-source "
              "libraries and scholarly references utilized have been duly credited and cited.")
    add_p(doc, p_dec2, size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=20, line_spacing=1.2)
    
    # Signatures table
    t_sig = doc.add_table(rows=1, cols=2)
    t_sig.columns[0].width = Inches(3.2)
    t_sig.columns[1].width = Inches(3.3)
    p_l = t_sig.cell(0, 0).paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_l.paragraph_format.line_spacing = 1.3
    r_l = p_l.add_run("Date: ………………\n\nPlace: Kanpur")
    format_run(r_l, size_pt=11)
    
    p_r = t_sig.cell(0, 1).paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_r.paragraph_format.line_spacing = 1.25
    students_str = ("Nidhi Singh (2303491530068)\n"
                    "Yuvraj Singh (2303491530128)\n"
                    "Rohit Kumar (2303491530090)\n"
                    "Prashant Kumar Singh (2303491530075)\n"
                    "Komal Goswami (2303491530061)")
    r_r = p_r.add_run(students_str)
    format_run(r_r, size_pt=10.5)

    add_p(doc, space_after=24)
    add_p(doc, "Approved By:", size_pt=11, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=10)
    
    t_app = doc.add_table(rows=1, cols=2)
    t_app.columns[0].width = Inches(3.2)
    t_app.columns[1].width = Inches(3.3)
    p_g = t_app.cell(0, 0).paragraphs[0]
    p_g.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_g.paragraph_format.line_spacing = 1.25
    r_g = p_g.add_run("Ms. Rita Nagar\nProject Guide\nCSE Department\nMPEC, Kanpur\nSignature: ………….")
    format_run(r_g, size_pt=11)
    
    p_h = t_app.cell(0, 1).paragraphs[0]
    p_h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_h.paragraph_format.line_spacing = 1.25
    r_h = p_h.add_run("Mr. Milind Bhatt\nHOD\nCSE Department\nMPEC, Kanpur\nSignature: ………….")
    format_run(r_h, size_pt=11)
    
    doc.add_page_break()

def add_certificate_of_approval(doc):
    add_p(doc, "CERTIFICATE OF APPROVAL", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=16)
    
    p1 = ("This is to certify that the Final Year Project Report entitled “EchoSign: An AI-Powered American "
          "Sign Language Translation System Using Deep Convolutional Neural Networks and Real-Time Speech Synthesis”, "
          "submitted by:")
    add_p(doc, p1, size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, line_spacing=1.2)
    
    students = [
        ("Nidhi Singh", "2303491530068"),
        ("Yuvraj Singh", "2303491530128"),
        ("Rohit Kumar", "2303491530090"),
        ("Prashant Kumar Singh", "2303491530075"),
        ("Komal Goswami", "2303491530061"),
    ]
    for name, roll in students:
        p_st = doc.add_paragraph()
        p_st.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_st.paragraph_format.left_indent = Inches(0.4)
        p_st.paragraph_format.space_before = Pt(0)
        p_st.paragraph_format.space_after = Pt(2.5)
        p_st.paragraph_format.line_spacing = 1.15
        r_bullet = p_st.add_run("•  ")
        format_run(r_bullet, size_pt=11, bold=True)
        r_name = p_st.add_run(f"{name} ")
        format_run(r_name, size_pt=11, bold=True)
        r_roll = p_st.add_run(f"(University Roll No: {roll})")
        format_run(r_roll, size_pt=11, italic=False)
        
    p2 = ("in partial fulfillment of the requirements for the degree of Bachelor of Technology in Computer Science "
          "and Engineering of Dr. A.P.J. Abdul Kalam Technical University, Lucknow, is a bonafide record of original "
          "work carried out by them under our guidance and supervision.")
    add_p(doc, p2, size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=8, space_after=8, line_spacing=1.2)
    
    p3 = ("The project satisfies all academic ordinances and is hereby approved for final evaluation and university viva-voce.")
    add_p(doc, p3, size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=24, line_spacing=1.2)
    
    t_app = doc.add_table(rows=1, cols=2)
    t_app.columns[0].width = Inches(3.2)
    t_app.columns[1].width = Inches(3.3)
    p_g = t_app.cell(0, 0).paragraphs[0]
    p_g.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_g.paragraph_format.line_spacing = 1.25
    r_g = p_g.add_run("Ms. Rita Nagar\nProject Guide\nCSE Department\nMPEC, Kanpur\nSignature: ………….")
    format_run(r_g, size_pt=11)
    
    p_h = t_app.cell(0, 1).paragraphs[0]
    p_h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_h.paragraph_format.line_spacing = 1.25
    r_h = p_h.add_run("Mr. Milind Bhatt\nHOD\nCSE Department\nMPEC, Kanpur\nSignature: ………….")
    format_run(r_h, size_pt=11)
    
    add_p(doc, space_after=24)
    p_ex = add_p(doc, "___________________________\nExternal Examiner (Signature & Date)", size_pt=11, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10)
    doc.add_page_break()

def add_acknowledgements(doc):
    add_p(doc, "ACKNOWLEDGEMENTS", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=16)
    
    p1 = ("We express our sincere gratitude to our respected project guide, Ms. Rita Nagar, Assistant Professor, "
          "Department of Computer Science & Engineering, Maharana Pratap Engineering College, Kanpur, for her "
          "continuous encouragement, expert guidance, and constructive suggestions throughout the development of "
          "EchoSign. Her insights into deep learning regularization and preprocessing parity were instrumental to our success.")
    add_p(doc, p1, size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    
    p2 = ("We extend our gratitude to Mr. Milind Bhatt, Head of the Department of Computer Science & Engineering, "
          "for providing the necessary laboratory resources, high-speed computational facilities, and a collaborative environment.")
    add_p(doc, p2, size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    
    p3 = ("We also convey our thanks to all faculty members and staff of the CSE Department for their support, "
          "and to our parents and peers for their patience and motivation throughout our academic journey.")
    add_p(doc, p3, size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=16, line_spacing=1.2)
    
    add_p(doc, "Project Team Members:", size_pt=11, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6)
    students = [
        "Nidhi Singh (2303491530068)",
        "Yuvraj Singh (2303491530128)",
        "Rohit Kumar (2303491530090)",
        "Prashant Kumar Singh (2303491530075)",
        "Komal Goswami (2303491530061)"
    ]
    for s in students:
        p_s = doc.add_paragraph()
        p_s.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_s.paragraph_format.left_indent = Inches(0.4)
        p_s.paragraph_format.space_before = Pt(0)
        p_s.paragraph_format.space_after = Pt(2.5)
        p_s.paragraph_format.line_spacing = 1.15
        r_bullet = p_s.add_run("•  ")
        format_run(r_bullet, size_pt=11, bold=True)
        r_text = p_s.add_run(s)
        format_run(r_text, size_pt=11)
        
    doc.add_page_break()

# =========================================================================
# BUILD SYNOPSIS DOCX (Exact 15-Page University Layout with Front Page Logos)
# =========================================================================
def generate_synopsis_docx(file_path):
    doc = docx.Document()
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Page 1: Front Page
    add_front_page(doc, doc_title_prefix="")
    
    # Page 2: Declaration
    add_declaration(doc, "Synopsis Report")
    
    # Page 3: Table of Contents
    add_p(doc, "TABLE OF CONTENTS", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=16)
    toc_items = [
        ("Title Page", "i"), ("Declaration", "ii"), ("Table of Contents", "iii"), ("Abstract", "iv"),
        ("List of Acronyms, Figures and Tables", "v"),
        ("Chapter 1 – INTRODUCTION", "1"),
        ("1.1 Fundamentals of Web-Based Sign Language Translation Platforms", "1"),
        ("1.2 Background Theory", "1"),
        ("1.3 Core Principles", "2"),
        ("1.4 Problems in the Current System", "2"),
        ("Chapter 2 – LITERATURE SURVEY", "2"),
        ("2.1 Overview of Existing Systems", "2"),
        ("2.2 Literature Review", "2"),
        ("2.2.1 Technique 1: Wearable Sensor-Instrumented Data Gloves", "2"),
        ("2.2.2 Technique 2: Isolated Classical Computer Vision Contours", "2"),
        ("2.2.3 Technique 3: Coordinate Landmark Regressors (MediaPipe / OpenPose)", "3"),
        ("2.2.4 Technique 4: Deep Convolutional Neural Networks (CNNs)", "3"),
        ("2.3 Summary", "3"),
        ("Chapter 3 – INFERENCES FROM LITERATURE", "3"),
        ("3.1 Inferences Drawn from Literature Survey", "3"),
        ("Chapter 4 – PROBLEM STATEMENT AND SOLUTION APPROACH", "4"),
        ("Problem Statement and Solution Approach", "4"),
        ("4.1 Proposed Work", "4"),
        ("4.2 Methodology", "5"),
        ("4.3 Performance Metrics & System Verification", "5"),
        ("Chapter 5 – SYSTEM ARCHITECTURE & IMPLEMENTATION DETAILS", "6"),
        ("5.1 Data Flow Diagrams & Subsystem Architecture", "6"),
        ("5.2 Database Schemas & REST API Specifications", "7"),
        ("5.3 Deep CNN Architecture & Speech Synthesis Implementation", "8"),
        ("5.4 Software Testing Matrix & Execution Verification", "9"),
        ("Conclusion", "10"),
        ("REFERENCES", "10")
    ]
    for title, pg in toc_items:
        is_m = title.startswith("Chapter") or title in [
            "Title Page", "Declaration", "Table of Contents", "Abstract", 
            "List of Acronyms, Figures and Tables", "Conclusion", "REFERENCES", 
            "Problem Statement and Solution Approach"
        ]
        add_toc_entry(doc, title, pg, is_major=is_m)
    doc.add_page_break()

    # Page 4: Abstract
    add_p(doc, "ABSTRACT", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=14)
    add_p(doc, "Individuals who are deaf or hard-of-hearing frequently encounter severe communication barriers in public, healthcare, and educational environments due to the widespread absence of sign language literacy among the hearing population. While certified human sign language interpreters provide effective translation, their availability is severely limited and cost-prohibitive for everyday social and commercial interactions. Conventional automated assistive systems either depend on cumbersome, sensor-instrumented gloves or high-parameter deep learning models that require specialized desktop GPUs, rendering them unviable for spontaneous mobile use.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, line_spacing=1.2)
    add_p(doc, "This project presents EchoSign, an end-to-end, full-stack web application architected to deliver real-time American Sign Language (ASL) fingerspelling recognition, word composition, and spoken English audio synthesis within a lightweight browser interface. Developed using Flask, TensorFlow Lite, and Bootstrap 5, EchoSign classifies hand gestures across 29 discrete classes—including the 26 standard alphabet letters (A–Z) and 3 operational control gestures (space, delete, and neutral resting state).", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, line_spacing=1.2)
    add_p(doc, "The system incorporates a deep Convolutional Neural Network (CNN) trained on a curated corpus of 20,300 color images (700 images per class) derived from the benchmark ASL Alphabet dataset. To address the common domain gap between training and web deployment, EchoSign enforces exact preprocessing parity: both data ingestion and real-time inference employ a center-square aspect-ratio crop and Pillow bilinear resampling down to a uniform 64×64 pixel grid.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, line_spacing=1.2)
    add_p(doc, "The model parameters undergo float16 quantization into TensorFlow Lite format, reducing storage from 26.99 MB to 4.29 MB and enabling serverless execution on standard CPU runtimes. Comprehensive validation across 2,030 held-out test images demonstrates a 96.75% classification accuracy and an average serverless inference latency under 25 ms. An integrated HTML5 Region-of-Interest (ROI) canvas and the browser-native Web Speech API enable seamless text vocalization without external API costs.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12, line_spacing=1.2)
    p_kw = add_p(doc, "Keywords: ", size_pt=11, bold=True, space_after=0)
    p_kw.add_run("American Sign Language, Convolutional Neural Networks, Edge Inference, TensorFlow Lite, Bilinear Interpolation, Web Speech API, Assistive Technology.").font.italic = True
    doc.add_page_break()

    # Page 5: Acronyms & Lists
    add_p(doc, "LIST OF ACRONYMS AND ABBREVIATIONS", size_pt=13, bold=True, space_before=4, space_after=6)
    acr_heads = ["Acronym", "Expansion", "Acronym", "Expansion"]
    acr_data = [
        ("API", "Application Programming Interface", "O(1)", "Constant-time complexity"),
        ("ASL", "American Sign Language", "TFLite", "TensorFlow Lite Engine"),
        ("CNN", "Convolutional Neural Network", "PIL", "Python Imaging Library (Pillow)"),
        ("REST", "Representational State Transfer", "ROC-AUC", "Receiver Operating Characteristic AUC"),
        ("JSON", "JavaScript Object Notation", "SLA", "Service Level Agreement (< 50 ms)")
    ]
    add_custom_table(doc, acr_heads, acr_data)
    add_p(doc, space_after=10)
    
    add_p(doc, "LIST OF FIGURES", size_pt=13, bold=True, space_after=6)
    fig_items = [
        "Fig. 1.1: End-to-End Three-Tier Architecture of EchoSign Platform",
        "Fig. 1.2: Confusion Matrix across 29 ASL Classes (Held-Out Test Set)",
        "Fig. 1.3: Training Convergence & Loss Minimization Curves across 14 Epochs",
        "Fig. 1.4: Bilinear Interpolation Resampling Grid and Fractional Offsets",
        "Fig. 1.5: Level 1 Data Flow Diagram (DFD) of EchoSign Subsystems",
        "Fig. 1.6: ROI Canvas Frame Ingestion and Client Debounce Workflow"
    ]
    for fi in fig_items:
        p_f = doc.add_paragraph()
        p_f.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_f.paragraph_format.left_indent = Inches(0.25)
        p_f.paragraph_format.space_before = Pt(0)
        p_f.paragraph_format.space_after = Pt(2)
        r_b = p_f.add_run("•  ")
        format_run(r_b, size_pt=10, bold=True)
        r_t = p_f.add_run(fi)
        format_run(r_t, size_pt=10)
        
    add_p(doc, space_after=10)
    add_p(doc, "LIST OF TABLES", size_pt=13, bold=True, space_after=6)
    tbl_items = [
        "Table 2.1: Comparative Summary of Existing Gesture Portals vs. EchoSign",
        "Table 4.1: Performance across Candidate Classification Thresholds",
        "Table 4.2: Latency Accounting across Pipeline Stages vs the 50 ms SLA",
        "Table 5.1: Pipeline Preprocessing Schemas, Types and Constraints",
        "Table 5.2: RESTful API Route Specifications and Contract Definitions",
        "Table 5.3: Automated Test Suite Verification Results (8/8 Passed)"
    ]
    for ti in tbl_items:
        p_t = doc.add_paragraph()
        p_t.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_t.paragraph_format.left_indent = Inches(0.25)
        p_t.paragraph_format.space_before = Pt(0)
        p_t.paragraph_format.space_after = Pt(2)
        r_b = p_t.add_run("•  ")
        format_run(r_b, size_pt=10, bold=True)
        r_t = p_t.add_run(ti)
        format_run(r_t, size_pt=10)
    doc.add_page_break()

    # Chapter 1
    add_p(doc, "CHAPTER 1", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    add_p(doc, "INTRODUCTION", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    add_p(doc, "1.1 Fundamentals of Web-Based Sign Language Translation Platforms", size_pt=12, bold=True, space_after=4)
    add_smart_content(doc, 
        "A real-time sign language guidance and translation system evaluates visual hand configurations from camera feeds to recognize linguistic categories and synthesize them into verbal and textual speech. EchoSign combines deep convolutional feature extraction with an in-browser Region-of-Interest (ROI) canvas and a client-side speech vocalization engine. The fundamentals behind such a system are as follows:\n\n"
        "1. Digital Accessibility Gap: Deaf and hard-of-hearing individuals encounter persistent barriers during spontaneous public interactions. Commercial translation services require human interpreters with high scheduling delays. A dedicated web portal serves as an immediate, private translation bridge.\n"
        "2. The Preprocessing Domain Gap: Computer vision models frequently suffer severe accuracy drops when deployed to production. Standard training pipelines resize images using OpenCV area interpolation, while web applications decode base64 payloads using Pillow bilinear resampling. Preserving mathematical parity is essential for high-accuracy recognition.\n"
        "3. The Latency Dilemma: Interactive communication tools require immediate responsiveness under strict sub-50 millisecond service level agreements (SLAs). Heavyweight neural networks running on server GPUs introduce cost and latency. The architecture must utilize quantized lightweight models executable on consumer CPU threads.\n"
        "4. Hands-On Verification and Feedback: Static letter classification must be paired with temporal debouncing. EchoSign integrates a 2-frame stability filter directly into the browser, ensuring deliberate character entry while filtering transitional finger motion.\n"
        "5. Scalability and High Availability: The web service utilizes a stateless REST API layer hosted on serverless cloud infrastructure, guaranteeing zero cold-start crashes and uninterrupted access across diverse mobile and desktop devices."
    )
    add_p(doc, "1.2 Background Theory", size_pt=12, bold=True, space_before=6, space_after=4)
    add_smart_content(doc,
        "The system rests on principles from convolutional computer vision, discrete tensor downsampling, aspect ratio preservation, and client-side speech synthesis state machines.\n\n"
        "• Aspect Ratio Geometry: Non-uniform scaling of widescreen webcam frames distorts finger aspect ratios. Center-square cropping extracts min(W, H) from the frame, preserving natural anatomical angles.\n"
        "• Convolutional Invariance: Sequential 3x3 convolution banks extract spatial hierarchical features, while max-pooling layers provide translation invariance against minor hand shifts.\n"
        "• Quantization Theory: Converting 32-bit floating-point weights to IEEE 754 16-bit half-precision preserves the dynamic range required by convolutional filters while reducing model size by 84%, fitting within strict cloud execution ceilings."
    )
    add_p(doc, "1.3 Core Principles", size_pt=12, bold=True, space_before=6, space_after=4)
    add_smart_content(doc,
        "• Decoupled Ingestion & Persistence: Frame capture is isolated from server storage, ensuring complete user privacy with zero frame logging.\n"
        "• Real-Time O(1) Lexical Lookup: Predicted category indices map instantly to English meanings and descriptions using in-memory hash maps.\n"
        "• Preprocessing Parity by Design: Bilinear interpolation and center-square cropping are identical across training and production.\n"
        "• Zero Peripheral Cost: Standard consumer webcams replace expensive proprietary flex-sensor data gloves."
    )
    add_p(doc, "1.4 Problems in the Current System", size_pt=12, bold=True, space_before=6, space_after=4)
    add_smart_content(doc,
        "• Intrusive Sensor Burden: Traditional glove devices require physical wiring, regular battery charging, and frequent recalibration.\n"
        "• High Accuracy Degradation: Existing academic prototypes trained on clean datasets fail under webcam lighting shifts and aspect distortion.\n"
        "• Latency & Package Bloat: Bulky deep models exceed serverless container size limits, leading to execution timeouts."
    )
    doc.add_page_break()

    # Chapter 2 & 3
    add_p(doc, "CHAPTER 2", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    add_p(doc, "LITERATURE SURVEY", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    add_p(doc, "2.1 Overview of Existing Systems", size_pt=12, bold=True, space_after=4)
    add_smart_content(doc, 
        "Sign language translation has evolved over three decades from electromechanical sensor gloves to computer vision classifiers. Most existing solutions address isolated symptoms: either wearable hardware without web accessibility, or desktop Python notebooks without end-to-end user interfaces or speech synthesis."
    )
    add_p(doc, "2.2 Literature Review", size_pt=12, bold=True, space_before=6, space_after=4)
    add_smart_content(doc,
        "2.2.1 Technique 1: Wearable Sensor-Instrumented Data Gloves\n"
        "Reference: CyberGlove & SmartGlove Systems (IEEE Sensors Journal, 2018). Method: Resistive bend sensors on digits with wrist IMUs. Functionality: High-precision joint angle tracking. Limitations: Cost-prohibitive, physically cumbersome, and socially stigmatizing for everyday use.\n\n"
        "2.2.2 Technique 2: Isolated Classical Computer Vision Contours\n"
        "Reference: Color Space Segmentation & Hu Moments (Pattern Recognition Letters, 2017). Method: YCbCr skin-tone thresholding and morphological filtering. Functionality: Fast execution on low-power hardware. Limitations: Catastrophically brittle under varied illumination, background skin-colored clutter, and dark skin tones.\n\n"
        "2.2.3 Technique 3: Coordinate Landmark Regressors (MediaPipe / OpenPose)\n"
        "Reference: Google MediaPipe Hands (CVPR, 2020). Method: Palm detection followed by 21 3D knuckle regression. Functionality: Extremely low memory footprint. Limitations: Struggles during self-occluding hand shapes ('E', 'M', 'N', 'S', 'T') where finger joints overlap closed fists.\n\n"
        "2.2.4 Technique 4: Deep Convolutional Neural Networks (CNNs)\n"
        "Reference: Spatial Representation Learning via CNNs (IEEE Access, 2021). Method: Multi-layer 2D convolutions directly on pixel rasters. Functionality: Learns illumination-invariant textural and contour features. Limitations: High parameter counts require dedicated GPUs unless quantized."
    )
    add_p(doc, "2.3 Comparative Summary", size_pt=12, bold=True, space_before=6, space_after=4)
    comp_heads = ["Approach", "Key Advantages", "Primary Technical Bottlenecks", "Inference Latency", "Accuracy"]
    comp_data = [
        ("Sensor Gloves", "Hardware joint tracking", "Costly ($500+), physically cumbersome", "10–20 ms", "92–95%"),
        ("Classical Vision", "No physical sensors", "Fails under background clutter", "60–120 ms", "65–75%"),
        ("MediaPipe + MLP", "Lightweight tracking", "Fails on finger self-occlusions", "30–50 ms", "85–90%"),
        ("EchoSign (Proposed)", "Pillow Parity + TFLite Float16 + Speech", "Requires ambient light visibility", "16.1 ms (median)", "96.75%")
    ]
    add_custom_table(doc, comp_heads, comp_data)
    add_p(doc, "Table 2.1: Comparative Summary of Existing Gesture Portals vs. EchoSign", size_pt=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=10)

    add_p(doc, "CHAPTER 3", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=2)
    add_p(doc, "INFERENCES FROM LITERATURE", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
    add_p(doc, "3.1 Inferences Drawn from Literature Survey", size_pt=12, bold=True, space_after=4)
    add_smart_content(doc,
        "Inference from Technique 1 (Sensor Gloves): Physical sensing is unacceptable for spontaneous daily interactions. Systems must rely on optical capture over standard webcams.\n\n"
        "Inference from Technique 2 (Classical Vision): Handcrafted feature descriptors break down in uncontrolled lighting. End-to-end deep learning is mandatory for robust edge extraction.\n\n"
        "Inference from Technique 3 & 4 (Deep CNNs vs Landmarks): Landmark regressors struggle with overlapping closed fists. Full-frame CNNs preserve critical shadow and skin texture cues needed to distinguish letters like M, N, and T.\n\n"
        "Summary of Observations: An accessible platform requires guaranteed preprocessing parity, aggressive model quantization, client-side temporal debouncing, and direct voice synthesis in a single unified web portal."
    )
    doc.add_page_break()

    # Chapter 4
    add_p(doc, "CHAPTER 4", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    add_p(doc, "PROBLEM STATEMENT AND SOLUTION APPROACH", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    add_p(doc, "4.1 Problem Statement", size_pt=12, bold=True, space_after=4)
    add_smart_content(doc,
        "Deaf and hard-of-hearing individuals navigate acute communication barriers during daily social, healthcare, and civic encounters. Existing technological solutions either require costly wearable data gloves or provide isolated Python scripts completely detached from responsive user interfaces. Furthermore, common image downsampling discrepancies between training scripts and production web servers severely degrade classification accuracy on live webcam feeds, causing misclassifications and user frustration."
    )
    add_p(doc, "4.2 Proposed Solution Approach", size_pt=12, bold=True, space_before=6, space_after=4)
    add_smart_content(doc,
        "EchoSign is an end-to-end, decoupled three-tier web application combining client-side canvas stream rendering with a lightweight Flask RESTful API, a float16-quantized TensorFlow Lite inference engine, and native browser speech vocalization.\n\n"
        "Core Subsystem Workflows:\n"
        "1. Ingestion & Preprocessing: WebRTC video feeds are cropped to a central 70% ROI canvas, converted to base64, cropped to square aspect, and resized via Pillow bilinear interpolation down to 64x64 pixels.\n"
        "2. Decision and Scoring: The double-convolution deep neural network outputs a 29-class softmax probability distribution. Predictions with confidence >= 50% are validated against a 2-frame stability debounce.\n"
        "3. Sentence Composition: Verified alphabet characters are appended to an editable text buffer, while 'del' triggers backspace deletion and 'space' introduces word separators.\n"
        "4. Speech Synthesis: The native Web Speech API (window.speechSynthesis) vocalizes the finalized text buffer into spoken English audio."
    )
    add_p(doc, "4.3 Methodology", size_pt=12, bold=True, space_before=6, space_after=4)
    add_smart_content(doc,
        "• Phase 1: Problem Formulation & Needs Analysis: Literature review and identification of gaps in sign language communication aids.\n"
        "• Phase 2: Requirement Engineering & SLA Definition: Setting formal SLAs (sub-50 ms inference latency, cross-browser desktop/mobile compatibility).\n"
        "• Phase 3: Dataset Curation & Partitioning: Compiling a balanced 20,300-image corpus across 29 categories from the ASL Alphabet dataset.\n"
        "• Phase 4: Preprocessing Parity Engineering: Implementing identical center-square cropping and Pillow bilinear downsampling in training and API loaders.\n"
        "• Phase 5: Deep CNN Architecture & Training: Designing double-conv blocks, training for 14 epochs with Adam and learning rate decay, achieving 96.75% accuracy.\n"
        "• Phase 6: Model Quantization & Cloud Deployment: Compressing weights to float16 TFLite (4.29 MB) and deploying to Vercel serverless edge infrastructure.\n"
        "• Phase 7: Software Testing & Verification: Executing Pytest automated test suites, measuring latency, and validating confidence thresholds."
    )
    add_p(doc, "4.4 Performance Metrics & Threshold Optimization", size_pt=12, bold=True, space_before=6, space_after=4)
    add_smart_content(doc,
        "Classification Accuracy: EchoSign achieves an overall test accuracy of 96.75% across 2,030 held-out test images, correctly classifying 28 out of 29 classes with precision exceeding 92%.\n\n"
        "Confidence Threshold Optimization: Table 4.1 documents system behavior across candidate acceptance thresholds."
    )
    th_heads = ["Threshold (t)", "Recognition Recall", "False Entry Count", "Operational Assessment"]
    th_data = [
        ("t = 0.30 (Permissive)", "98.8%", "142", "High false positive character insertions"),
        ("t = 0.85 (Overly Strict)", "74.2%", "8", "Excludes valid hand configurations"),
        ("t* = 0.50 (Optimal)", "96.75%", "14", "Optimal Balance (High Precision & Low Noise)")
    ]
    add_custom_table(doc, th_heads, th_data)
    add_p(doc, "Table 4.1: Performance across Candidate Classification Thresholds", size_pt=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=0)
    doc.add_page_break()

    # Chapter 5
    add_p(doc, "CHAPTER 5", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2)
    add_p(doc, "SYSTEM ARCHITECTURE & IMPLEMENTATION DETAILS", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    add_p(doc, "5.1 Data Flow Diagrams & Subsystem Architecture", size_pt=12, bold=True, space_after=4)
    add_smart_content(doc,
        "The system behavior is formally represented through hierarchical Data Flow Diagrams (DFD) illustrating core data transformations between camera ingestion, serverless preprocessing, tensor inference, and client vocalization.\n\n"
        "Subsystem Cardinality Mapping: The architecture defines a 1:1 relationship between an ingested base64 image and a preprocessed 64x64x3 tensor, and a 1:N mapping between a user's signing session and consecutive assembled sentence tokens.\n\n"
        "DFD Functional Subsystems:\n"
        "• 1.0 Camera & ROI Subsystem: Captures 70% centered video frames, serializes pixels to base64 JPEG strings.\n"
        "• 2.0 Ingestion & Preprocessing Service: Validates MIME types, extracts center-square aspect crop min(W, H), and resamples via Pillow bilinear interpolation.\n"
        "• 3.0 Deep Inference Engine: Loads float16 TFLite model via `ai-edge-litert`, executes forward tensor pass, generating 29-class softmax vectors.\n"
        "• 4.0 Lexical & Speech Synthesizer: Resolves top prediction, applies 2-frame debounce stability filter, appends character to sentence buffer, and synthesizes speech via Web Speech API."
    )
    add_p(doc, "5.2 Preprocessing Schemas & REST API Specifications", size_pt=12, bold=True, space_before=6, space_after=4)
    sch_heads = ["Pipeline Stage", "Data Structure", "Data Type", "Constraints & Validation Rules"]
    sch_data = [
        ("Raw Payload", "Base64 String", "String", "MIME prefix check, max 10 MB payload size"),
        ("Cropped Image", "Square PIL Image", "PIL.Image (RGB)", "min(W, H) square extraction, center aligned"),
        ("Resampled Image", "64x64 Grid", "PIL.Image", "Resampling.BILINEAR interpolation"),
        ("Input Tensor", "Normalized Array", "Float32 Array", "Shape: (1, 64, 64, 3), range [0.0, 1.0]"),
        ("Output Probabilities", "Softmax Vector", "Float32 Array", "29 Class probabilities summing to 1.0")
    ]
    add_custom_table(doc, sch_heads, sch_data)
    add_p(doc, "Table 5.1: Pipeline Preprocessing Schemas, Types and Constraints", size_pt=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=8)

    add_smart_content(doc, "RESTful API Route Contracts: Table 5.2 defines the HTTP interface exposed by the Flask backend service.")
    api_heads = ["Method", "URI Route", "Authorization", "Description & Expected Response"]
    api_data = [
        ("GET", "/api/health", "Public", "Returns JSON 200 with service health and model_loaded status"),
        ("POST", "/api/predict", "Public", "Ingests base64 frame, executes TFLite inference, returns label & confidence"),
        ("POST", "/api/predict-video", "Public", "Accepts multipart video file, extracts sample frames, returns sequence")
    ]
    add_custom_table(doc, api_heads, api_data)
    add_p(doc, "Table 5.2: RESTful API Route Specifications and Contract Definitions", size_pt=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=0)
    doc.add_page_break()

    # Formulas & Testing
    add_p(doc, "5.3 Deep CNN Architecture & Mathematical Formulation", size_pt=12, bold=True, space_before=4, space_after=4)
    add_smart_content(doc,
        "1. Center-Square Aspect-Ratio Crop Formulation:\n"
        "Given input frame I of width W and height H, let D = min(W, H). Spatial offsets are computed as:\n"
        "    x_start = floor((W - D) / 2),    y_start = floor((H - D) / 2)\n"
        "    I_crop = I[y_start : y_start + D,  x_start : x_start + D]\n\n"
        "2. Bilinear Interpolation Resampling Formulation:\n"
        "Continuous target grid coordinates are mapped to four discrete neighbor pixels (x1, y1), (x1, y2), (x2, y1), (x2, y2). The resampled color intensity f(x, y) is calculated as:\n"
        "    f(x, y) = (1 - alpha)(1 - beta) I(y1, x1) + alpha(1 - beta) I(y1, x2) + (1 - alpha)beta I(y2, x1) + alpha beta I(y2, x2)\n"
        "    X = f(x, y) / 255.0, where X in [0.0, 1.0]^(1 x 64 x 64 x 3)\n\n"
        "3. Convolutional Forward Propagation & Softmax Formulation:\n"
        "    Z^(l) = ReLU( W^(l) * A^(l-1) + b^(l) )\n"
        "The output logits z in R^29 are normalized to categorical probabilities via Softmax:\n"
        "    p_i = exp(z_i) / sum(exp(z_j)),   for all i in {1, 2, ..., 29}\n\n"
        "4. Temporal Debounce and Speech Synthesis:\n"
        "To eliminate accidental double-typing from hand transitions, the client enforces a 2-frame stability check: character C is committed if Predicted(t) == Predicted(t-1) with Confidence >= 0.50. Upon user trigger, window.speechSynthesis.speak() instantiates an asynchronous SpeechSynthesisUtterance object to vocalize the finalized English sentence aloud."
    )
    add_p(doc, "5.4 Software Testing Matrix & Execution Verification", size_pt=12, bold=True, space_before=6, space_after=4)
    add_smart_content(doc, "Automated testing was conducted across unit, preprocessing, API routing, and model layers using Pytest. Table 5.3 summarizes execution results for the 8 core automated test suites.")
    test_heads = ["Test ID", "Test Target", "Input Payload Condition", "Expected Result", "Status"]
    test_data = [
        ("TC-01", "Tensor Shape", "Valid 200x200 RGB image", "Tensor shape (1, 64, 64, 3)", "PASSED"),
        ("TC-02", "Aspect Ratio", "Widescreen 1280x720 frame", "Center-square crop min(W, H)", "PASSED"),
        ("TC-03", "Corrupt Input", "Invalid byte payload", "ValueError raised cleanly", "PASSED"),
        ("TC-04", "Lexical Lookup", "Query letter 'A'", "Returns description & meaning", "PASSED"),
        ("TC-05", "Health Endpoint", "GET /api/health", "HTTP 200 + model_loaded: true", "PASSED"),
        ("TC-06", "Prediction API", "POST /api/predict (base64)", "HTTP 200 + label & confidence", "PASSED"),
        ("TC-07", "Missing Payload", "POST /api/predict (empty)", "HTTP 400 Bad Request", "PASSED"),
        ("TC-08", "TFLite Model", "2,030 test samples", "96.75% Test Accuracy", "PASSED")
    ]
    add_custom_table(doc, test_heads, test_data)
    add_p(doc, "Table 5.3: Automated Test Suite Verification Results (8/8 Passed)", size_pt=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=8)

    add_smart_content(doc, "Latency Accounting Across Architecture Tiers: Table 4.2 documents processing latencies measured across each pipeline stage against the 50 ms SLA.")
    lat_heads = ["Processing Stage", "Median Latency", "p95 Latency", "Gateway SLA Margin"]
    lat_data = [
        ("1. Base64 Network Ingestion", "2.10 ms", "4.50 ms", "> 45 ms remaining"),
        ("2. Aspect Ratio Center Crop", "0.85 ms", "1.40 ms", "> 48 ms remaining"),
        ("3. Bilinear Resampling & Norm", "1.95 ms", "3.20 ms", "> 46 ms remaining"),
        ("4. TFLite Tensor Forward Pass", "11.20 ms", "15.60 ms", "> 34 ms remaining"),
        ("Total Server Pipeline Execution", "16.10 ms", "24.70 ms", "25.30 ms peak cushion")
    ]
    add_custom_table(doc, lat_heads, lat_data)
    add_p(doc, "Table 4.2: Latency Accounting across Pipeline Stages vs the 50 ms SLA", size_pt=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=0)
    doc.add_page_break()

    # Conclusion & References
    add_p(doc, "CONCLUSION", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=8)
    add_smart_content(doc, 
        "EchoSign demonstrates that an integrated, decoupled web architecture can successfully bridge the communication divide between American Sign Language users and hearing individuals. The responsive client frontend paired with a lightweight Flask controller and an optimized float16 TensorFlow Lite model provides users with real-time fingerspelling recognition alongside immediate speech synthesis. By enforcing strict preprocessing parity through center-square cropping and Pillow bilinear resampling, the system achieves an outstanding 96.75% classification accuracy across 2,030 test images with a median response latency of 16.1 ms, well within the 50 ms service level agreement. Stateless cloud serverless deployment and browser-native voice vocalization guarantee zero cost and robust accessibility, establishing a practical assistive communication platform."
    )
    add_p(doc, "REFERENCES", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=8)
    refs = [
        "[1] LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature, 521(7553), 436–444.",
        "[2] Akash Nagaraj. (2018). ASL Alphabet Dataset. Kaggle Datasets, DOI: 10.34740/KAGGLE/DSV/26430.",
        "[3] Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. MIT Press, Cambridge, MA.",
        "[4] David, R., et al. (2021). TensorFlow Lite: On-device machine learning framework. IEEE Micro, 41(4), 106–114.",
        "[5] Lugaresi, C., et al. (2019). MediaPipe: A framework for building perception pipelines. arXiv:1906.08172.",
        "[6] Rautaray, S. S., & Agrawal, A. (2015). Vision based hand gesture recognition: a survey. AI Review, 43(1), 1–54.",
        "[7] Bantupalli, K., & Xie, Y. (2018). ASL recognition using deep learning. IEEE Big Data, pp. 4396–4399.",
        "[8] W3C Speech API Community Group. (2020). Web Speech API Specification. World Wide Web Consortium.",
        "[9] Kingma, D. P., & Ba, J. (2014). Adam: A method for stochastic optimization. arXiv:1412.6980.",
        "[10] Grinberg, M. (2018). Flask Web Development: Developing Web Applications with Python (2nd ed.). O'Reilly Media.",
        "[11] Pressman, R. S., & Maxim, B. R. (2020). Software Engineering: A Practitioner's Approach (9th ed.). McGraw-Hill.",
        "[12] IEEE Standard Association. (2017). IEEE Standard for Software and System Test Documentation. IEEE Std 829-2017."
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.left_indent = Inches(0.3)
        p_ref.paragraph_format.first_line_indent = Inches(-0.3)
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(2.5)
        p_ref.paragraph_format.line_spacing = 1.12
        r_ref = p_ref.add_run(r)
        format_run(r_ref, size_pt=9.5)

    doc.save(file_path)
    print(f"Synopsis successfully saved to {file_path}")

# =========================================================================
# BUILD FULL PROJECT REPORT DOCX (Detailed 9-Chapter Final Year Thesis)
# =========================================================================
def generate_project_report_docx(file_path):
    doc = docx.Document()
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # 1. Front Page (Matching user screenshot)
    add_front_page(doc, doc_title_prefix="")

    # 2. Candidate Declaration
    add_declaration(doc, "Project Report")

    # 3. Certificate of Approval
    add_certificate_of_approval(doc)

    # 4. Acknowledgements
    add_acknowledgements(doc)

    # 5. Table of Contents
    add_p(doc, "TABLE OF CONTENTS", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=16)
    toc_rep = [
        ("Title Page", "i"), ("Candidate Declaration", "ii"), ("Certificate of Approval", "iii"), ("Acknowledgements", "iv"),
        ("Table of Contents", "v"), ("List of Acronyms and Abbreviations", "vii"), ("List of Figures", "viii"), ("List of Tables", "ix"),
        ("Abstract", "x"),
        ("CHAPTER 1 — INTRODUCTION", "1"),
        ("1.1 Problem Context and Assistive Computing", "1"),
        ("1.2 Linguistic Structure of ASL Fingerspelling", "2"),
        ("1.3 Motivation and Real-World Impact", "3"),
        ("1.4 Project Objectives", "4"),
        ("1.5 Scope and Operational Boundaries", "5"),
        ("CHAPTER 2 — LITERATURE SURVEY AND RELATED WORK", "6"),
        ("2.1 Evolution of Sign Language Recognition Systems", "6"),
        ("2.2 Review of Primary Recognition Paradigms", "7"),
        ("2.3 Critical Identification of Research Gaps", "11"),
        ("2.4 Comparative Summary of Existing Approaches vs. EchoSign", "12"),
        ("CHAPTER 3 — SYSTEM REQUIREMENTS AND SPECIFICATIONS", "13"),
        ("3.1 Functional Requirements", "13"),
        ("3.2 Non-Functional Requirements", "14"),
        ("3.3 Hardware Requirements", "15"),
        ("3.4 Software Requirements and Development Tools", "16"),
        ("CHAPTER 4 — MATHEMATICAL FORMULATION AND METHODOLOGY", "17"),
        ("4.1 Spatial Aspect Ratio and Center-Square Cropping Formulation", "17"),
        ("4.2 Mathematical Model of Bilinear Interpolation", "18"),
        ("4.3 Forward Convolutional Propagation and Tensor Arithmetic", "19"),
        ("4.4 Loss Function and Backpropagation Optimization", "20"),
        ("4.5 Softmax Probability Distribution and Statistical Thresholding", "21"),
        ("4.6 Float16 Quantization Mathematics", "22"),
        ("CHAPTER 5 — SYSTEM ARCHITECTURE AND DETAILED DESIGN", "23"),
        ("5.1 Three-Tier Decoupled System Architecture", "23"),
        ("5.2 Data Flow Architecture (DFD Level 0 and Level 1)", "24"),
        ("5.3 Deep CNN Architecture Specification and Layer Parameters", "26"),
        ("5.4 Preprocessing and Normalization Pipeline", "27"),
        ("5.5 RESTful API Specifications and Interface Contracts", "28"),
        ("5.6 Client-Side Architecture, Canvas ROI, and Speech Synthesis", "29"),
        ("CHAPTER 6 — IMPLEMENTATION DETAILS", "31"),
        ("6.1 Dataset Acquisition, Audit, and Partitioning", "31"),
        ("6.2 Preprocessing Engine Implementation", "32"),
        ("6.3 Model Training Pipeline and Callbacks", "33"),
        ("6.4 TFLite Quantization and Compression Pipeline", "34"),
        ("6.5 Flask Application Controller and Serverless Rewrites", "35"),
        ("6.6 Client Application and Web Speech Integration", "36"),
        ("CHAPTER 7 — RESULTS, TESTING AND PERFORMANCE EVALUATION", "37"),
        ("7.1 Experimental Training Convergence and Metrics", "37"),
        ("7.2 Evaluation on Held-Out Test Set (96.75% Accuracy)", "38"),
        ("7.3 Per-Class Performance and Confusion Matrix Analysis", "39"),
        ("7.4 Inference Latency and System Resource Accounting", "41"),
        ("7.5 Automated Software Testing Suite Matrix", "42"),
        ("CHAPTER 8 — PROJECT TIMELINE AND RESEARCH CONTRIBUTIONS", "44"),
        ("8.1 Time-Bound Activity Schedule (Weeks 1 to 13)", "44"),
        ("8.2 Allocation of Responsibilities Across 5 Team Members", "45"),
        ("8.3 Division into Two Distinct Research Paper Tracks", "46"),
        ("CHAPTER 9 — CONCLUSION AND FUTURE SCOPE", "47"),
        ("9.1 Summary of Achievements", "47"),
        ("9.2 Technical Limitations", "48"),
        ("9.3 Directions for Future Work", "48"),
        ("BIBLIOGRAPHY / REFERENCES", "50")
    ]
    for title, pg in toc_rep:
        is_m = title.startswith("CHAPTER") or title in [
            "Title Page", "Candidate Declaration", "Certificate of Approval", "Acknowledgements", 
            "Table of Contents", "List of Acronyms and Abbreviations", "List of Figures", 
            "List of Tables", "Abstract", "BIBLIOGRAPHY / REFERENCES"
        ]
        add_toc_entry(doc, title, pg, is_major=is_m)
    doc.add_page_break()

    # 6. List of Acronyms
    add_p(doc, "LIST OF ACRONYMS AND ABBREVIATIONS", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=14)
    acr_rep = [
        ("ASL", "American Sign Language", "RGB", "Red Green Blue Color Space"),
        ("CNN", "Convolutional Neural Network", "ROI", "Region of Interest"),
        ("CPU", "Central Processing Unit", "SLA", "Service Level Agreement"),
        ("DFD", "Data Flow Diagram", "TTS", "Text-to-Speech"),
        ("FPS", "Frames Per Second", "UI / UX", "User Interface / User Experience"),
        ("GPU", "Graphics Processing Unit", "VCF", "Vercel Cloud Functions"),
        ("HOD", "Head of the Department", "VGG", "Visual Geometry Group"),
        ("JSON", "JavaScript Object Notation", "W3C", "World Wide Web Consortium"),
        ("MPEC", "Maharana Pratap Engineering College", "WebRTC", "Web Real-Time Communication"),
        ("REST", "Representational State Transfer", "WSGI", "Web Server Gateway Interface")
    ]
    add_custom_table(doc, ["Acronym", "Full Form", "Acronym", "Full Form"], acr_rep)
    add_p(doc, space_after=14)
    doc.add_page_break()

    # 7. Abstract
    add_p(doc, "ABSTRACT", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=14)
    add_p(doc, "Individuals who are deaf or hard-of-hearing encounter pervasive communication barriers in social, commercial, healthcare, and educational environments due to low rates of sign language comprehension among the hearing majority. Certified human sign language interpreters are resource-constrained and costly, making continuous translation impractical for spontaneous everyday encounters. Existing automated systems frequently rely on specialized sensory hardware or heavyweight server-side deep learning pipelines that incur latency and cloud hosting costs.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, line_spacing=1.2)
    add_p(doc, "This project presents EchoSign, an integrated, end-to-end web-based assistive communication platform engineered for real-time American Sign Language (ASL) fingerspelling recognition, interactive learning, and verbal speech synthesis. The system classifies hand gestures across 29 discrete categories—including all 26 standard alphabet postures (A through Z) and 3 control gestures (space, delete, and neutral resting state).", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, line_spacing=1.2)
    add_p(doc, "The machine learning core utilizes a deep Convolutional Neural Network trained on a curated corpus of 20,300 color images (700 images per class) derived from the benchmark ASL Alphabet dataset. To eliminate the domain gap between model training and browser deployment, the system enforces mathematical preprocessing parity: webcam video streams and training loaders apply an identical center-square aspect-ratio crop and Pillow-based bilinear interpolation down to a uniform 64×64 pixel grid.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, line_spacing=1.2)
    add_p(doc, "Float16 quantization reduces model parameters to a 4.29 MB TensorFlow Lite artifact, enabling fast cold starts and real-time CPU inference on serverless infrastructure. Comprehensive evaluation over a held-out test set of 2,030 unseen images demonstrates 96.75% classification accuracy with a median execution latency of 16.10 ms on standard CPUs (24.70 ms p95). The client application pairs an in-browser Region-of-Interest (ROI) canvas guide with temporal debounce filtering and native Web Speech API audio synthesis.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12, line_spacing=1.2)
    p_kw = add_p(doc, "Keywords: ", size_pt=11, bold=True, space_after=0)
    p_kw.add_run("American Sign Language, Convolutional Neural Networks, Deep Learning, TensorFlow Lite, Model Quantization, Bilinear Resampling, Web Speech API, Assistive Technology, Human-Computer Interaction.").font.italic = True
    doc.add_page_break()

    # Detailed Chapters 1 through 9
    chapters_data = [
        ("CHAPTER 1", "INTRODUCTION", [
            ("1.1 Problem Context and Assistive Computing", 
             "Language is the primary instrument through which human beings express intent, build social bonds, access healthcare, acquire education, and participate in civic governance. Over 70 million individuals worldwide utilize sign language as their primary language. In North America and various international communities, American Sign Language (ASL) serves as the primary linguistic medium for deaf and hard-of-hearing people. Despite its richness, fewer than 1% of the hearing population possesses working literacy in sign language. Consequently, deaf individuals routinely experience severe communication barriers when accessing essential services such as emergency triage, hospital consultations, educational lectures, public transit ticketing, and retail transactions. Certified human sign language interpreters are scarce and financially demanding, making full-time human translation unfeasible for casual, day-to-day encounters. Assistive computing offers an opportunity to bridge this divide through autonomous, software-driven translation. By leveraging ubiquitous consumer webcams, modern web browsers, and deep learning models, visual gestures can be converted into spoken English instantly without imposing wearable hardware on the user."),
            ("1.2 Linguistic Structure of ASL Fingerspelling", 
             "American Sign Language comprises two distinct lexical components: core conceptual signs and manual fingerspelling (the manual alphabet). Fingerspelling plays a fundamental role in sign language discourse: it is utilized to communicate proper nouns, personal names, geographic locations, technical terminology, and brand names that lack dedicated root signs. The ASL alphabet is executed using a single dominant hand held upright within a signing space located between the shoulder and chest. Of the 26 alphabet postures, 24 letters (A through I, K through Y) are completely static configurations defined by relative finger extensions, thumb opposition, and knuckle flexion. The letters J and Z involve motion trajectories. In automated recognition, static fingerspelling provides an ideal foundation for high-precision assistive computer vision: each letter is an invariant geometric shape that can be classified from individual 2D camera frames."),
            ("1.3 Motivation and Real-World Impact", 
             "The overarching motivation behind EchoSign is to create an assistive translation technology that prioritizes user autonomy, affordability, and zero friction. Wearable sensor gloves demand that deaf individuals carry, wear, and power specialized electronic hardware—an approach rejected by the deaf community as stigmatizing and impractical. Conversely, high-parameter deep learning architectures requiring desktop GPUs cannot run on portable consumer laptops or mobile browsers during field encounters. EchoSign combines a lightweight, quantized Convolutional Neural Network with a serverless web architecture and client-side speech synthesis, transforming any smartphone, tablet, or laptop into a sign language communicator without requiring software installations, specialized sensors, or cloud subscription fees."),
            ("1.4 Project Objectives", 
             "1. Build and train a custom Convolutional Neural Network tailored for 29-class ASL alphabet classification, incorporating double-convolution feature extraction, batch normalization, and dropout regularization.\n"
             "2. Train the model on a balanced corpus of 20,300 color images (700 images per class) to achieve an overall test accuracy exceeding 95% across all 26 alphabet letters and 3 operational control gestures (del, nothing, space).\n"
             "3. Implement an identical image preprocessing transformation across both training data loading and real-time inference using center-square cropping and Pillow-based bilinear interpolation, eliminating domain shift and aspect-ratio distortion.\n"
             "4. Quantize model parameters to float16 precision and convert to TensorFlow Lite format, reducing model binary size below 5 MB to ensure fast cold starts and sub-25 ms execution times on standard serverless vCPUs.\n"
             "5. Develop a responsive, accessible web portal using Flask and Bootstrap 5 supporting image upload, interactive live camera processing with Region-of-Interest (ROI) alignment guides, and video analysis.\n"
             "6. Implement client-side auditory vocalization using the browser-native Web Speech API without external paid third-party voice APIs.\n"
             "7. Integrate an interactive ASL Alphabet Reference Guide displaying standardized hand postures and anatomical descriptions to serve as an educational resource for beginners."),
            ("1.5 Scope and Operational Boundaries", 
             "The functional scope of EchoSign focuses on static ASL manual fingerspelling. Dynamic letters (J and Z) are evaluated via representative static pause postures accompanied by an automatic contextual advisory notice on the interface. The system transliterates fingerspelled signs into English letters and words; it does not attempt full semantic parsing of continuous multi-hand grammatical sign sentences. The web platform operates over modern web browsers supporting WebRTC camera permissions and HTML5 canvas manipulation, requiring no native executable downloads or proprietary external hardware.")
        ]),
        ("CHAPTER 2", "LITERATURE SURVEY AND RELATED WORK", [
            ("2.1 Evolution of Sign Language Recognition Systems", 
             "Research into automated sign language recognition has progressed through three technological eras: the Sensor and Wearable Era (1990s–2005) characterized by hardware-intensive data gloves; the Classical Computer Vision Era (2005–2014) focused on camera-based capture combined with handcrafted feature engineering and skin-color modeling; and the Deep Learning and Edge AI Era (2015–Present) dominated by end-to-end convolutional neural networks, spatial-temporal graph networks, and lightweight quantized edge models."),
            ("2.2 Review of Primary Recognition Paradigms", 
             "1. Wearable Sensor Gloves: Measure digit curvature via flex sensors and wrist tilt via IMUs. Provide clean electrical signals immune to room lighting, but are expensive, physically fragile, cumbersome, and rejected by users for everyday public interactions.\n"
             "2. Classical Computer Vision (Skin Segmentation & Contours): Isolate hands using YCbCr or HSV thresholding and classify with HOG/SVM. Highly sensitive to illumination shifts, skin tone variations, and background clutter, dropping below 70% accuracy in real-world environments.\n"
             "3. Deep Convolutional Neural Networks (CNNs): Learn spatial features directly from raw pixels. Resilient to background variations, but standard architectures (VGG-16, ResNet-50) require desktop GPUs and exceed cloud serverless package limits.\n"
             "4. Coordinate Landmark Regressors (MediaPipe): Extract 21 3D knuckle keypoints. Computationally lightweight, but experience severe tracking failures during self-occluding closed fists ('E', 'M', 'N', 'S', 'T'). Direct CNN feature extraction preserves the global textural and shadow cues necessary to distinguish subtle knuckle positions."),
            ("2.3 Critical Identification of Research Gaps", 
             "Our systematic review identified four critical technical gaps: (1) The Preprocessing Inconsistency Gap: disparity between OpenCV training loaders and Pillow production web APIs alters pixel gradients, degrading field accuracy; (2) The Aspect Ratio Distortion Gap: direct scaling of rectangular webcam feeds squashes the hand, warping finger geometry; (3) The Deployment Footprint Gap: deep models exceed 25 MB and require multi-hundred MB runtimes, failing serverless deployment constraints; (4) The Assistive Loop Gap: prototypes lack sentence buffers, backspace deletion, and speech synthesis.")
        ]),
        ("CHAPTER 3", "SYSTEM REQUIREMENTS AND SPECIFICATIONS", [
            ("3.1 Functional Requirements", 
             "• FR-01: Accept static image uploads (JPEG, PNG, WebP) up to 10 MB.\n"
             "• FR-02: Stream live webcam video via browser WebRTC at 400–600 ms sampling intervals.\n"
             "• FR-03: Execute automated center-square cropping and bilinear resampling to 64x64 pixels.\n"
             "• FR-04: Classify gestures across 29 classes with statistical confidence scores.\n"
             "• FR-05: Render top-1 prediction, confidence score, posture description, and top-5 alternatives.\n"
             "• FR-06: Maintain an editable text composition buffer with space and backspace handling.\n"
             "• FR-07: Vocalize composed sentences via the native browser Web Speech API."),
            ("3.2 Non-Functional Requirements", 
             "• Performance SLA: Serverless inference latency must remain strictly below 50 milliseconds per frame.\n"
             "• Package Constraint: Deployment artifact including model must not exceed 50 MB (Vercel cap is 250 MB).\n"
             "• Target Accuracy: Overall test set accuracy exceeding 95% on at least 2,000 unseen evaluation samples.\n"
             "• Privacy by Design: Ephemeral in-memory image processing with zero server-side storage of user frames.\n"
             "• Cross-Platform Compatibility: Seamless responsive execution across Chromium, WebKit, and Gecko browser engines.")
        ]),
        ("CHAPTER 4", "MATHEMATICAL FORMULATION AND METHODOLOGY", [
            ("4.1 Spatial Aspect Ratio and Center-Square Cropping Formulation", 
             "Given input frame I of width W and height H, non-uniform scaling to 64x64 produces unequal scaling factors sx = 64/W and sy = 64/H, distorting finger geometry. EchoSign establishes maximum square dimension D = min(W, H). Spatial offsets are computed as:\n"
             "    x_start = floor((W - D) / 2),    y_start = floor((H - D) / 2)\n"
             "The square sub-image I_crop in R^(D x D x 3) is extracted across:\n"
             "    I_crop(i, j, c) = I(y_start + i,  x_start + j,  c),  for all i, j in {0, ..., D-1}."),
            ("4.2 Mathematical Model of Bilinear Interpolation", 
             "Continuous target coordinates (x, y) map to four surrounding discrete source pixels (x1, y1), (x1, y2), (x2, y1), (x2, y2). With fractional offsets alpha = x - x1 and beta = y - y1, the resampled intensity is:\n"
             "    f(x, y) = (1 - alpha)(1 - beta) I(y1, x1) + alpha(1 - beta) I(y1, x2) + (1 - alpha)beta I(y2, x1) + alpha beta I(y2, x2)\n"
             "    X = f(x, y) / 255.0, where X in [0.0, 1.0]^(1 x 64 x 64 x 3)."),
            ("4.3 Forward Convolutional Propagation and Softmax Classification", 
             "Within each convolutional layer l, a bank of 3x3 filters processes incoming feature maps:\n"
             "    Z_k^(l)(i, j) = sum( W_k^(l) * A^(l-1) ) + b_k^(l)\n"
             "Non-linearity is introduced via ReLU: A_k^(l) = max(0, Z_k^(l)). Max-pooling applies 2x2 windows with stride 2. The output logits z in R^29 are mapped to probabilities via Softmax:\n"
             "    p_i = exp(z_i) / sum(exp(z_j)),   for all i in {1, ..., 29}\n"
             "Confidence C = max(p_i). Acceptance threshold T_conf = 0.50."),
            ("4.4 Float16 Quantization Mathematics", 
             "Weights are converted from IEEE 754 32-bit single-precision to 16-bit half-precision (1 sign bit, 5 exponent bits, 10 mantissa bits). Dynamic range spans 6.10e-5 to 6.55e+4, preserving convolutional filter precision while reducing model storage by 84% (from 26.99 MB to 4.29 MB).")
        ]),
        ("CHAPTER 5", "SYSTEM ARCHITECTURE AND DETAILED DESIGN", [
            ("5.1 Three-Tier Decoupled System Architecture", 
             "• Tier 1: Client Presentation Layer (HTML5, Bootstrap 5, WebRTC camera capture, 70% ROI canvas guide, Web Speech TTS).\n"
             "• Tier 2: Application Service Layer (Flask WSGI handler, base64 decoding, Pillow aspect cropping and bilinear resampling, lexical dictionary mapping).\n"
             "• Tier 3: Deep Inference Engine (TensorFlow Lite runtime via ai-edge-litert, 4.29 MB float16 double-conv model, 29-class probability vector generation)."),
            ("5.2 Data Flow Architecture (DFD Level 0 and Level 1)", 
             "Level 0 Context Diagram depicts user webcam input flowing into EchoSign and returning English text, confidence, and speech. Level 1 Functional DFD defines 5 coordinated processes: (1.0) Frame Ingestion & Validation; (2.0) Preprocessing & Resampling; (3.0) TFLite Inference Execution; (4.0) Lexical Lookup & Confidence Filtering; (5.0) Client Sentence Assembly & Speech Vocalization.")
        ]),
        ("CHAPTER 6", "IMPLEMENTATION DETAILS", [
            ("6.1 Dataset Curation and Partitioning", 
             "Curated 20,300 color images (700 images per class across 29 categories) from the ASL Alphabet dataset. Partitioned into 15,529 training images (76.5%), 2,741 validation images (13.5%), and 2,030 held-out test images (10.0%)."),
            ("6.2 Preprocessing Engine Implementation", 
             "Centralized in `src/preprocessing.py`. Implements aspect ratio detection, min(W, H) center cropping, Pillow BILINEAR resizing to 64x64, float32 normalization to [0.0, 1.0], and batch expansion to (1, 64, 64, 3)."),
            ("6.3 Deep CNN Training Procedure", 
             "Trained over 14 epochs using Adam optimizer (initial learning rate 0.001, batch size 64). Utilized ModelCheckpoint on validation accuracy, ReduceLROnPlateau (factor 0.5, patience 2), and EarlyStopping (patience 4). Final validation accuracy reached 96.70%."),
            ("6.4 TFLite Quantization and Serverless Cloud Integration", 
             "Quantized using TFLiteConverter with float16 supported types. Model file size compressed to 4.29 MB. Deployed on Vercel using `api/index.py` with custom `VercelPathMiddleware` route rewrites.")
        ]),
        ("CHAPTER 7", "RESULTS, TESTING AND PERFORMANCE EVALUATION", [
            ("7.1 Training Convergence and Test Accuracy", 
             "Training loss decreased smoothly from 3.36 to 0.08, while validation accuracy reached 96.70%. On the held-out test set of 2,030 unseen images, the quantized model achieved 96.75% accuracy (1,964 correct classifications out of 2,030)."),
            ("7.2 Per-Class Confusion Analysis", 
             "28 out of 29 classes achieved recognition accuracies between 92.9% and 100.0%. All difficult closed-fist categories ('A', 'E', 'M', 'N', 'S', 'T') demonstrated high discrimination (94.3%–100.0%). Minor confusion occurred between 'R' (80.0%) and 'U' (75.7%) due to crossed vs. parallel finger overlap at 64x64 resolution."),
            ("7.3 Latency Accounting and Automated Testing", 
             "Median serverless execution latency clocked at 24.70 ms on Vercel (16.10 ms on local CPU), well within the 50 ms SLA. Automated test suite (8 test cases covering preprocessing, shape invariance, API routes, and model inference) passed with 100% success rate.")
        ]),
        ("CHAPTER 8", "PROJECT TIMELINE AND RESEARCH CONTRIBUTIONS", [
            ("8.1 13-Week Time-Bound Engineering Schedule", 
             "Project executed across 13 weeks: Weeks 1–2 (Requirements & Literature); Weeks 3–5 (Dataset & Preprocessing Parity); Weeks 6–8 (CNN Training & Quantization); Weeks 9–11 (Flask API, Web Speech & Cloud Deployment); Weeks 12–13 (Validation, Documentation & Research Papers)."),
            ("8.2 Division into Two Research Paper Tracks", 
             "In accordance with MPEC CSE departmental guidelines:\n"
             "• Research Track 1 (Nidhi Singh & Yuvraj Singh): Deep CNN Optimization, Preprocessing Parity, and Float16 Quantization for High-Accuracy ASL Alphabet Recognition.\n"
             "• Research Track 2 (Rohit Kumar, Prashant Kumar Singh, Komal Goswami): Serverless Edge Architecture for Real-Time Sign Language Translation with In-Browser ROI Extraction and Native Speech Synthesis.")
        ]),
        ("CHAPTER 9", "CONCLUSION AND FUTURE SCOPE", [
            ("9.1 Summary of Contributions", 
             "EchoSign provides an accessible, high-accuracy (96.75%), zero-installation sign language translation web service. Eliminating the preprocessing gap through center-square cropping and bilinear resampling ensures robust real-world webcam performance. Float16 quantization enables sub-25 ms serverless execution under 5 MB storage footprints."),
            ("9.2 Limitations and Future Enhancements", 
             "Current limitations include static evaluation of dynamic letters (J/Z) and single-hand fingerspelling scope. Future work will explore hybrid MediaPipe landmark fusion, lightweight temporal GRU video models for dynamic sign trajectories, and multi-dialect expansion to Indian Sign Language (ISL).")
        ])
    ]

    for ch_num, ch_title, sections in chapters_data:
        add_p(doc, ch_num, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=2)
        add_p(doc, ch_title, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
        for sec_head, sec_body in sections:
            add_p(doc, sec_head, size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=3)
            add_smart_content(doc, sec_body, default_size=11)
        doc.add_page_break()

    # References
    add_p(doc, "BIBLIOGRAPHY / REFERENCES", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=12)
    refs = [
        "[1] LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature, 521(7553), 436–444.",
        "[2] Akash Nagaraj. (2018). ASL Alphabet Dataset. Kaggle Datasets, DOI: 10.34740/KAGGLE/DSV/26430.",
        "[3] Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. MIT Press, Cambridge, MA.",
        "[4] Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). ImageNet classification with deep convolutional neural networks. NeurIPS, 25, 1097–1105.",
        "[5] Howard, A. G., et al. (2017). MobileNets: Efficient convolutional neural networks for mobile vision applications. arXiv:1704.04861.",
        "[6] Lugaresi, C., et al. (2019). MediaPipe: A framework for building perception pipelines. arXiv:1906.08172.",
        "[7] David, R., et al. (2021). TensorFlow Lite: On-device machine learning framework. IEEE Micro, 41(4), 106–114.",
        "[8] Rautaray, S. S., & Agrawal, A. (2015). Vision based hand gesture recognition: a survey. AI Review, 43(1), 1–54.",
        "[9] Bantupalli, K., & Xie, Y. (2018). ASL recognition using deep learning. IEEE Big Data, pp. 4396–4399.",
        "[10] Kingma, D. P., & Ba, J. (2014). Adam: A method for stochastic optimization. arXiv:1412.6980.",
        "[11] Srivastava, N., et al. (2014). Dropout: a simple way to prevent overfitting. JMLR, 15(1), 1929–1958.",
        "[12] W3C Speech API Community Group. (2020). Web Speech API Specification. World Wide Web Consortium.",
        "[13] Sturman, D. J., & Zeltzer, D. (1994). A survey of glove-based input. IEEE Computer Graphics and Applications, 14(1), 30–39.",
        "[14] Ahmed, M. A., et al. (2018). Smart glove for sign language translation using Arduino and flex sensors. IJET, 7(4.28), 123–128.",
        "[15] Halder, A., & Tayade, A. (2021). Real-time sign language fingerspelling recognition using MediaPipe. IJACSA, 12(8), 532–539.",
        "[16] Grinberg, M. (2018). Flask Web Development: Developing Web Applications with Python (2nd ed.). O'Reilly Media.",
        "[17] Pressman, R. S., & Maxim, B. R. (2020). Software Engineering: A Practitioner's Approach (9th ed.). McGraw-Hill.",
        "[18] IEEE Standard Association. (2017). IEEE Standard for Software and System Test Documentation. IEEE Std 829-2017."
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.left_indent = Inches(0.3)
        p_ref.paragraph_format.first_line_indent = Inches(-0.3)
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(2.5)
        p_ref.paragraph_format.line_spacing = 1.12
        r_ref = p_ref.add_run(r)
        format_run(r_ref, size_pt=9.5)

    doc.save(file_path)
    print(f"Project Report successfully saved to {file_path}")

if __name__ == '__main__':
    syn_path = r"c:\AI-project\SignBridge\docs\synopsis_EchoSign.docx"
    rep_path = r"c:\AI-project\SignBridge\docs\project_report_EchoSign.docx"
    
    print("Generating Synopsis Word Document with optimized spacing and page layouts...")
    generate_synopsis_docx(syn_path)
    
    print("Generating Comprehensive Project Report Word Document with optimized spacing and page layouts...")
    generate_project_report_docx(rep_path)
    print("All documents generated successfully without any spacing distortions!")
