import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

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

def format_run(run, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color_rgb=(0,0,0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

def add_p(doc, text="", font_name="Times New Roman", size_pt=12, bold=False, italic=False, 
          align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=6, line_spacing=1.15, color_rgb=(0,0,0)):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        format_run(r, font_name, size_pt, bold, italic, color_rgb)
    return p

def add_custom_table(doc, headers, data, col_widths=None):
    tbl = doc.add_table(rows=len(data)+1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl)
    
    for i, h in enumerate(headers):
        cell = tbl.cell(0, i)
        set_cell_background(cell, "1F497D")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        format_run(r, size_pt=9.5, bold=True, color_rgb=(255, 255, 255))
        if col_widths and i < len(col_widths):
            cell.width = Inches(col_widths[i])
            
    for row_idx, row in enumerate(data, start=1):
        for col_idx, val in enumerate(row):
            cell = tbl.cell(row_idx, col_idx)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(str(val))
            format_run(r, size_pt=9, bold=(col_idx == 0))
            if col_widths and col_idx < len(col_widths):
                cell.width = Inches(col_widths[col_idx])
    return tbl

def build_synopsis(output_path):
    doc = docx.Document()
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # 1. Title Page
    add_p(doc, space_after=18)
    add_p(doc, "ECHOSIGN: AN AI-POWERED AMERICAN SIGN LANGUAGE TRANSLATION SYSTEM USING DEEP CONVOLUTIONAL NEURAL NETWORKS AND REAL-TIME SPEECH SYNTHESIS",
          size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    add_p(doc, "(ECHOSIGN)", size_pt=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
    add_p(doc, "Report submitted in partial fulfillment of the requirement for the degree of",
          size_pt=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    add_p(doc, "B. Tech.", size_pt=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_p(doc, "In", size_pt=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_p(doc, "Computer Science and Engineering", size_pt=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=28)
    add_p(doc, "Under the Supervision of", size_pt=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_p(doc, "Ms. Reeta Nagar", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_p(doc, "Assistant Professor, C.S.E.", size_pt=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=28)
    add_p(doc, "Submitted By:", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
    for s in ["Nidhi Singh (2303491530068)", "Yuvraj Singh (2303491530128)", "Rohit Kumar (2303491530090)", 
              "Prashant Kumar Singh (2303491530075)", "Komal Goswami (2303491530061)"]:
        add_p(doc, s, size_pt=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=3)
    add_p(doc, space_after=32)
    add_p(doc, "Department of Computer Science & Engineering", size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_p(doc, "Maharana Pratap Engineering College, Kanpur", size_pt=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_p(doc, "Dr. A.P.J. Abdul Kalam Technical University, Lucknow", size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_p(doc, "Session: 2026-27", size_pt=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    doc.add_page_break()

    # 2. Declaration
    add_p(doc, "DECLARATION", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)
    add_p(doc, "This is to certify that the Synopsis Report entitled “EchoSign: An AI-Powered American Sign Language Translation System Using Deep Convolutional Neural Networks and Real-Time Speech Synthesis”, which is submitted in partial fulfilment of the requirement for the award of the degree of B.Tech. in Computer Science and Engineering to MPEC Kanpur, Dr. A.P.J. Abdul Kalam Technical University, Lucknow, comprises only original work and studies carried out by the students themselves. The matter embodied in this synopsis has not been submitted for the award of any other degree.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12, line_spacing=1.2)
    add_p(doc, "We further declare that all source code, database architectures, algorithmic modules, and technical documentation presented in this report have been implemented in accordance with academic integrity guidelines. All external open-source libraries and scholarly references utilized have been duly credited and cited.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=24, line_spacing=1.2)
    
    t_sig = doc.add_table(rows=1, cols=2)
    t_sig.columns[0].width = Inches(3.2)
    t_sig.columns[1].width = Inches(3.3)
    p_l = t_sig.cell(0, 0).paragraphs[0]
    p_l.paragraph_format.line_spacing = 1.3
    p_l.add_run("Date: ………………\n\nPlace: Kanpur").font.size = Pt(11)
    p_r = t_sig.cell(0, 1).paragraphs[0]
    p_r.paragraph_format.line_spacing = 1.3
    p_r.add_run("Nidhi Singh (2303491530068)\nYuvraj Singh (2303491530128)\nRohit Kumar (2303491530090)\nPrashant Kumar Singh (2303491530075)\nKomal Goswami (2303491530061)").font.size = Pt(11)

    add_p(doc, space_after=36)
    add_p(doc, "Approved By:", size_pt=11, bold=True, space_after=12)
    t_app = doc.add_table(rows=1, cols=2)
    t_app.columns[0].width = Inches(3.2)
    t_app.columns[1].width = Inches(3.3)
    t_app.cell(0, 0).paragraphs[0].add_run("Ms. Reeta Nagar\nProject Guide\nCSE Department\nMPEC, Kanpur\nSignature: ………….").font.size = Pt(11)
    t_app.cell(0, 1).paragraphs[0].add_run("Mr. Milind Bhatt\nHOD\nCSE Department\nMPEC, Kanpur\nSignature: ………….").font.size = Pt(11)
    doc.add_page_break()

    # 3. Table of Contents
    add_p(doc, "TABLE OF CONTENTS", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)
    toc_items = [
        ("Title", "i"), ("Declaration", "ii"), ("Table of Contents", "iii"), ("Abstract", "iv"),
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
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2)
        is_m = title.startswith("Chapter") or title in ["Title", "Declaration", "Table of Contents", "Abstract", "List of Acronyms, Figures and Tables", "Conclusion", "REFERENCES", "Problem Statement and Solution Approach"]
        dots_count = max(5, 75 - len(title))
        r1 = p.add_run(title)
        format_run(r1, size_pt=10.5, bold=is_m)
        r2 = p.add_run(" " + ("." * dots_count) + " ")
        format_run(r2, size_pt=10.5, color_rgb=(120, 120, 120))
        r3 = p.add_run(pg)
        format_run(r3, size_pt=10.5, bold=is_m)
    doc.add_page_break()

    # 4. Abstract
    add_p(doc, "ABSTRACT", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)
    add_p(doc, "Individuals who are deaf or hard-of-hearing frequently encounter severe communication barriers in public, healthcare, and educational environments due to the widespread absence of sign language literacy among the hearing population. While certified human sign language interpreters provide effective translation, their availability is severely limited and cost-prohibitive for everyday social and commercial interactions. Conventional automated assistive systems either depend on cumbersome, sensor-instrumented gloves or high-parameter deep learning models that require specialized desktop GPUs, rendering them unviable for spontaneous mobile use.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    add_p(doc, "This project presents EchoSign, an end-to-end, full-stack web application architected to deliver real-time American Sign Language (ASL) fingerspelling recognition, word composition, and spoken English audio synthesis within a lightweight browser interface. Developed using Flask, TensorFlow Lite, and Bootstrap 5, EchoSign classifies hand gestures across 29 discrete classes—including the 26 standard alphabet letters (A–Z) and 3 operational control gestures (space, delete, and neutral resting state).", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    add_p(doc, "The system incorporates a deep Convolutional Neural Network (CNN) trained on a curated corpus of 20,300 color images (700 images per class) derived from the benchmark ASL Alphabet dataset. To address the common domain gap between training and web deployment, EchoSign enforces exact preprocessing parity: both data ingestion and real-time inference employ a center-square aspect-ratio crop and Pillow bilinear resampling down to a uniform 64×64 pixel grid.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    add_p(doc, "The model parameters undergo float16 quantization into TensorFlow Lite format, reducing storage from 26.99 MB to 4.29 MB and enabling serverless execution on standard CPU runtimes. Comprehensive validation across 2,030 held-out test images demonstrates a 96.75% classification accuracy and an average serverless inference latency under 25 ms. An integrated HTML5 Region-of-Interest (ROI) canvas and the browser-native Web Speech API enable seamless text vocalization without external API costs.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=14, line_spacing=1.2)
    p_kw = add_p(doc, "Keywords: ", size_pt=11, bold=True, space_after=0)
    p_kw.add_run("American Sign Language, Convolutional Neural Networks, Edge Inference, TensorFlow Lite, Bilinear Interpolation, Web Speech API, Assistive Technology.").font.italic = True
    doc.add_page_break()

    # 5. Acronyms & Lists
    add_p(doc, "LIST OF ACRONYMS AND ABBREVIATIONS", size_pt=13, bold=True, space_before=6, space_after=8)
    acr_heads = ["Acronym", "Expansion", "Acronym", "Expansion"]
    acr_data = [
        ("API", "Application Programming Interface", "O(1)", "Constant-time complexity"),
        ("ASL", "American Sign Language", "TFLite", "TensorFlow Lite Engine"),
        ("CNN", "Convolutional Neural Network", "PIL", "Python Imaging Library (Pillow)"),
        ("REST", "Representational State Transfer", "ROC-AUC", "Receiver Operating Characteristic AUC"),
        ("JSON", "JavaScript Object Notation", "SLA", "Service Level Agreement (< 50 ms)")
    ]
    add_custom_table(doc, acr_heads, acr_data)
    add_p(doc, space_after=12)
    add_p(doc, "LIST OF FIGURES", size_pt=13, bold=True, space_after=6)
    add_p(doc, "Fig. 4.1 End-to-End Three-Tier Architecture of EchoSign Platform    Fig. 4.2 Confusion Matrix across 29 ASL Classes\nFig. 4.3 Training Convergence & Loss Minimization Curve    Fig. 4.4 Bilinear Interpolation Resampling Grid\nFig. 5.1 Level 1 Data Flow Diagram (DFD) of EchoSign Subsystems    Fig. 5.2 ROI Canvas Frame Ingestion Workflow", size_pt=9.5, space_after=12, line_spacing=1.2)
    add_p(doc, "LIST OF TABLES", size_pt=13, bold=True, space_after=6)
    add_p(doc, "Table 2.1 Comparative Summary of Existing Gesture Portals vs. EchoSign    Table 4.1 Performance across Candidate Classification Thresholds\nTable 4.2 Latency Accounting across Pipeline Stages vs the 50 ms SLA    Table 5.1 Preprocessing Specifications and Input Constraints\nTable 5.2 RESTful API Route Specifications and Contract Definitions    Table 5.3 Automated Test Suite Verification Results (8/8 Passed)", size_pt=9.5, space_after=0, line_spacing=1.2)
    doc.add_page_break()

    # 6. Chapter 1
    add_p(doc, "CHAPTER 1", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=4)
    add_p(doc, "INTRODUCTION", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)
    add_p(doc, "1.1 Fundamentals of Web-Based Sign Language Translation Platforms", size_pt=12, bold=True, space_after=6)
    add_p(doc, "A real-time sign language guidance and translation system evaluates visual hand configurations from camera feeds to recognize linguistic categories and synthesize them into verbal and textual speech. EchoSign combines deep convolutional feature extraction with an in-browser Region-of-Interest (ROI) canvas and a client-side speech vocalization engine. The fundamentals behind such a system are as follows:", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, line_spacing=1.2)
    fundamentals = [
        ("1. Digital Accessibility Gap: ", "Deaf and hard-of-hearing individuals encounter persistent barriers during spontaneous public interactions. Commercial translation services require human interpreters with high scheduling delays. A dedicated web portal serves as an immediate, private translation bridge."),
        ("2. The Preprocessing Domain Gap: ", "Computer vision models frequently suffer severe accuracy drops when deployed to production. Standard training pipelines resize images using OpenCV area interpolation, while web applications decode base64 payloads using Pillow bilinear resampling. Preserving mathematical parity is essential for high-accuracy recognition."),
        ("3. The Latency Dilemma: ", "Interactive communication tools require immediate responsiveness under strict sub-50 millisecond service level agreements (SLAs). Heavyweight neural networks running on server GPUs introduce cost and latency. The architecture must utilize quantized lightweight models executable on consumer CPU threads."),
        ("4. Hands-On Verification and Feedback: ", "Static letter classification must be paired with temporal debouncing. EchoSign integrates a 2-frame stability filter directly into the browser, ensuring deliberate character entry while filtering transitional finger motion."),
        ("5. Scalability and High Availability: ", "The web service utilizes a stateless REST API layer hosted on serverless cloud infrastructure, guaranteeing zero cold-start crashes and uninterrupted access across diverse mobile and desktop devices.")
    ]
    for b_pre, t_rest in fundamentals:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r_b = p.add_run(b_pre)
        format_run(r_b, size_pt=10.5, bold=True)
        r_t = p.add_run(t_rest)
        format_run(r_t, size_pt=10.5)
        
    add_p(doc, "1.2 Background Theory", size_pt=12, bold=True, space_before=8, space_after=6)
    add_p(doc, "The system rests on principles from convolutional computer vision, discrete tensor downsampling, aspect ratio preservation, and client-side speech synthesis state machines.\nA. Aspect Ratio Geometry: Non-uniform scaling of widescreen webcam frames distorts finger aspect ratios. Center-square cropping extracts min(W, H) from the frame, preserving natural anatomical angles.\nB. Convolutional Invariance: Sequential 3x3 convolution banks extract spatial hierarchical features, while max-pooling layers provide translation invariance against minor hand shifts.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=0, line_spacing=1.2)
    doc.add_page_break()

    # 7. Chapter 1 (Cont) & Chapter 2
    add_p(doc, "C. Quantization Theory: Converting 32-bit floating-point weights to IEEE 754 16-bit half-precision preserves the dynamic range required by convolutional filters while reducing model size by 84%, fitting within strict cloud execution ceilings.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, line_spacing=1.2)
    add_p(doc, "1.3 Core Principles", size_pt=12, bold=True, space_after=4)
    principles = [
        "• Decoupled Ingestion & Persistence: Frame capture is isolated from server storage, ensuring complete user privacy with zero frame logging.",
        "• Real-Time O(1) Lexical Lookup: Predicted category indices map instantly to English meanings and descriptions using in-memory hash maps.",
        "• Preprocessing Parity by Design: Bilinear interpolation and center-square cropping are identical across training and production.",
        "• Zero Peripheral Cost: Standard consumer webcams replace expensive proprietary flex-sensor data gloves."
    ]
    for pr in principles:
        add_p(doc, pr, size_pt=10.5, space_after=3)
    add_p(doc, "1.4 Problems in the Current System", size_pt=12, bold=True, space_before=6, space_after=4)
    problems = [
        "• Intrusive Sensor Burden: Traditional glove devices require physical wiring, regular battery charging, and frequent recalibration.",
        "• High Accuracy Degradation: Existing academic prototypes trained on clean datasets fail under webcam lighting shifts and aspect distortion.",
        "• Latency & Package Bloat: Bulky deep models exceed serverless container size limits, leading to execution timeouts."
    ]
    for pb in problems:
        add_p(doc, pb, size_pt=10.5, space_after=3)

    add_p(doc, "CHAPTER 2", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=4)
    add_p(doc, "LITERATURE SURVEY", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    add_p(doc, "2.1 Overview of Existing Systems", size_pt=12, bold=True, space_after=4)
    add_p(doc, "Sign language translation has evolved over three decades from electromechanical sensor gloves to computer vision classifiers. Most existing solutions address isolated symptoms: either wearable hardware without web accessibility, or desktop Python notebooks without end-to-end user interfaces or speech synthesis.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, line_spacing=1.2)
    add_p(doc, "2.2 Literature Review", size_pt=12, bold=True, space_after=4)
    add_p(doc, "2.2.1 Technique 1: Wearable Sensor-Instrumented Data Gloves", size_pt=11, bold=True, space_after=2)
    add_p(doc, "Reference: CyberGlove & SmartGlove Systems (IEEE Sensors Journal, 2018). Method/Technique: Resistive bend sensors on digits with wrist IMUs. Functionality: High-precision joint angle tracking. Limitations: Cost-prohibitive, physically cumbersome, and socially stigmatizing for everyday use.", size_pt=10.5, space_after=6)
    add_p(doc, "2.2.2 Technique 2: Isolated Classical Computer Vision Contours", size_pt=11, bold=True, space_after=2)
    add_p(doc, "Reference: YCbCr Skin Segmentation & Hu Moments (AI Review, 2015). Method/Technique: Color thresholding with SVM classification. Functionality: Contactless gesture detection. Limitations: Extremely sensitive to illumination shifts, skin tone diversity, and background clutter.", size_pt=10.5, space_after=0)
    doc.add_page_break()

    # 8. Chapter 2 (Cont) & Chapter 3
    add_p(doc, "2.2.3 Technique 3: Deep Convolutional Neural Networks (CNNs)", size_pt=11, bold=True, space_after=2)
    add_p(doc, "Reference: Krizhevsky et al. (NeurIPS, 2012); Nagaraj (Kaggle ASL, 2018). Method/Technique: Hierarchical spatial convolution banks with backpropagation. Functionality: High-accuracy raw pixel pattern recognition. Limitations: Heavy parameter counts require desktop GPUs unless optimized.", size_pt=10.5, space_after=6)
    add_p(doc, "2.2.4 Technique 4: Skeletal Landmark Regressors (MediaPipe / OpenPose)", size_pt=11, bold=True, space_after=2)
    add_p(doc, "Reference: Lugaresi et al., Google MediaPipe (2019). Method/Technique: 21 3D coordinate hand landmark regression. Functionality: Lightweight joint tracking. Limitations: Tracking drops during self-occluding closed fists ('M', 'N', 'E', 'S', 'T').", size_pt=10.5, space_after=8)

    add_p(doc, "2.3 Summary", size_pt=12, bold=True, space_after=4)
    comp_heads = ["Methodology", "Strengths", "Weaknesses in Production", "Latency", "Accuracy"]
    comp_data = [
        ("Sensor Gloves", "Hardware joint precision", "Wearable burden; high cost", "< 15 ms", "92–95%"),
        ("Classical Vision", "No physical sensors", "Fails under background clutter", "60–120 ms", "65–75%"),
        ("MediaPipe + MLP", "Lightweight tracking", "Fails on finger self-occlusions", "30–50 ms", "85–90%"),
        ("EchoSign (Proposed)", "Pillow Parity + TFLite Float16 + Speech", "Requires ambient light visibility", "16.1 ms (median)", "96.75%")
    ]
    add_custom_table(doc, comp_heads, comp_data)
    add_p(doc, "Table 2.1: Comparative Summary of Existing Gesture Portals vs. EchoSign", size_pt=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=12)

    add_p(doc, "CHAPTER 3", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_p(doc, "INFERENCES FROM LITERATURE", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
    add_p(doc, "3.1 Inferences Drawn from Literature Survey", size_pt=12, bold=True, space_after=4)
    add_p(doc, "Inference from Technique 1 (Sensor Gloves): Physical sensing is unacceptable for spontaneous daily interactions. Systems must rely on optical capture over standard webcams.\nInference from Technique 2 (Classical Vision): Handcrafted feature descriptors break down in uncontrolled lighting. End-to-end deep learning is mandatory for robust edge extraction.\nInference from Technique 3 & 4 (Deep CNNs vs Landmarks): Landmark regressors struggle with overlapping closed fists. Full-frame CNNs preserve critical shadow and skin texture cues needed to distinguish letters like M, N, and T.\nSummary of Observations: An accessible platform requires guaranteed preprocessing parity, aggressive model quantization, client-side temporal debouncing, and direct voice synthesis in a single unified web portal.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=0, line_spacing=1.2)
    doc.add_page_break()

    # 9. Chapter 4
    add_p(doc, "CHAPTER 4", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=4)
    add_p(doc, "PROBLEM STATEMENT AND SOLUTION APPROACH", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)
    add_p(doc, "PROBLEM STATEMENT", size_pt=12, bold=True, space_after=4)
    add_p(doc, "Deaf and hard-of-hearing individuals navigate acute communication barriers during daily social, healthcare, and civic encounters. Existing technological solutions either require costly wearable data gloves or provide isolated Python scripts completely detached from responsive user interfaces. Furthermore, common image downsampling discrepancies between training scripts and production web servers severely degrade classification accuracy on live webcam feeds, causing misclassifications and user frustration.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    add_p(doc, "SOLUTION APPROACH", size_pt=12, bold=True, space_after=4)
    add_p(doc, "EchoSign is an end-to-end, decoupled three-tier web application combining client-side canvas stream rendering with a lightweight Flask RESTful API, a float16-quantized TensorFlow Lite inference engine, and native browser speech vocalization.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, line_spacing=1.2)
    add_p(doc, "Core Subsystem Workflows:", size_pt=11, bold=True, space_after=4)
    workflows = [
        "1. Ingestion & Preprocessing: WebRTC video feeds are cropped to a central 70% ROI canvas, converted to base64, cropped to square aspect, and resized via Pillow bilinear interpolation down to 64x64 pixels.",
        "2. Decision and Scoring: The double-convolution deep neural network outputs a 29-class softmax probability distribution. Predictions with confidence >= 50% are validated against a 2-frame stability debounce.",
        "3. Sentence Composition: Verified alphabet characters are appended to an editable text buffer, while 'del' triggers backspace deletion and 'space' introduces word separators.",
        "4. Speech Synthesis: The native Web Speech API (window.speechSynthesis) vocalizes the finalized text buffer into spoken English audio."
    ]
    for wf in workflows:
        add_p(doc, wf, size_pt=10.5, space_after=3)
    add_p(doc, "4.1 Proposed Work", size_pt=12, bold=True, space_before=6, space_after=4)
    add_p(doc, "The proposed framework encompasses: (1) Decoupled frontend client with responsive Bootstrap UI and canvas ROI guides; (2) Mathematical preprocessing parity pipeline using Pillow; (3) Float16 quantized TensorFlow Lite inference service; (4) Client-side temporal debounce and voice synthesis engine.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=0, line_spacing=1.2)
    doc.add_page_break()

    # 10. Methodology & Performance
    add_p(doc, "4.2 Methodology", size_pt=12, bold=True, space_before=6, space_after=4)
    phases = [
        "• Phase 1: Problem Formulation & Needs Analysis: Literature review and identification of gaps in sign language communication aids.",
        "• Phase 2: Requirement Engineering & SLA Definition: Setting formal SLAs (sub-50 ms inference latency, cross-browser desktop/mobile compatibility).",
        "• Phase 3: Dataset Curation & Partitioning: Compiling a balanced 20,300-image corpus across 29 categories from the ASL Alphabet dataset.",
        "• Phase 4: Preprocessing Parity Engineering: Implementing identical center-square cropping and Pillow bilinear downsampling in training and API loaders.",
        "• Phase 5: Deep CNN Architecture & Training: Designing double-conv blocks, training for 14 epochs with Adam and learning rate decay, achieving 96.75% accuracy.",
        "• Phase 6: Model Quantization & Cloud Deployment: Compressing weights to float16 TFLite (4.29 MB) and deploying to Vercel serverless edge infrastructure.",
        "• Phase 7: Software Testing & Verification: Executing Pytest automated test suites, measuring latency, and validating confidence thresholds."
    ]
    for ph in phases:
        add_p(doc, ph, size_pt=10.5, space_after=3)
    add_p(doc, "4.3 Performance Metrics & System Verification", size_pt=12, bold=True, space_before=8, space_after=4)
    add_p(doc, "1. Classification Accuracy: EchoSign achieves an overall test accuracy of 96.75% across 2,030 held-out test images, correctly classifying 28 out of 29 classes with precision exceeding 92%.\n2. Confidence Threshold Optimization: Table 4.1 documents system behavior across acceptance thresholds.", size_pt=11, space_after=6)
    th_heads = ["Threshold (t)", "Recognition Recall", "False Entry Count", "Operational Assessment"]
    th_data = [
        ("t = 0.30 (Permissive)", "98.8%", "142", "High false positive character insertions"),
        ("t = 0.85 (Overly Strict)", "74.2%", "8", "Excludes valid hand configurations"),
        ("t* = 0.50 (Optimal)", "96.75%", "14", "Optimal Balance (High Precision & Low Noise)")
    ]
    add_custom_table(doc, th_heads, th_data)
    add_p(doc, "Table 4.1: Performance across Candidate Classification Thresholds", size_pt=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=0)
    doc.add_page_break()

    # 11. Chapter 5: Architecture
    add_p(doc, "CHAPTER 5", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=4)
    add_p(doc, "SYSTEM ARCHITECTURE & MODELING", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)
    add_p(doc, "5.1 Data Flow Diagrams & Subsystem Architecture", size_pt=12, bold=True, space_after=4)
    add_p(doc, "The system behavior is formally represented through hierarchical Data Flow Diagrams (DFD) illustrating core data transformations between camera ingestion, serverless preprocessing, tensor inference, and client vocalization.\nSubsystem Cardinality Mapping: The architecture defines a 1:1 relationship between an ingested base64 image and a preprocessed 64x64x3 tensor, and a 1:N mapping between a user's signing session and consecutive assembled sentence tokens.\n\nDFD Functional Subsystems:\n• 1.0 Camera & ROI Subsystem: Captures 70% centered video frames, serializes pixels to base64 JPEG strings.\n• 2.0 Ingestion & Preprocessing Service: Validates MIME types, extracts center-square aspect crop min(W, H), and resamples via Pillow bilinear interpolation.\n• 3.0 Deep Inference Engine: Loads float16 TFLite model via `ai-edge-litert`, executes forward tensor pass, generating 29-class softmax vectors.\n• 4.0 Lexical & Speech Synthesizer: Resolves top prediction, applies 2-frame debounce stability filter, appends character to sentence buffer, and synthesizes speech via Web Speech API.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=0, line_spacing=1.2)
    doc.add_page_break()

    # 12. Schemas & APIs
    add_p(doc, "5.2 Preprocessing, TFLite Schemas & REST API Specifications", size_pt=12, bold=True, space_before=6, space_after=4)
    add_p(doc, "The system enforces strict tensor schemas across all processing stages. Table 5.1 outlines field schemas and validation constraints.", size_pt=11, space_after=6)
    sch_heads = ["Pipeline Stage", "Data Structure", "Data Type", "Constraints & Validation Rules"]
    sch_data = [
        ("Raw Payload", "Base64 String", "String", "MIME prefix check, max 10 MB payload size"),
        ("Cropped Image", "Square PIL Image", "PIL.Image (RGB)", "min(W, H) square extraction, center aligned"),
        ("Resampled Image", "64x64 Grid", "PIL.Image", "Resampling.BILINEAR interpolation"),
        ("Input Tensor", "Normalized Array", "Float32 Array", "Shape: (1, 64, 64, 3), range [0.0, 1.0]"),
        ("Output Probabilities", "Softmax Vector", "Float32 Array", "29 Class probabilities summing to 1.0")
    ]
    add_custom_table(doc, sch_heads, sch_data)
    add_p(doc, "Table 5.1: Pipeline Preprocessing Schemas, Types and Constraints", size_pt=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=10)

    add_p(doc, "RESTful API Route Contracts: Table 5.2 defines the HTTP interface exposed by the Flask backend service.", size_pt=11, space_after=6)
    api_heads = ["Method", "URI Route", "Authorization", "Description & Expected Response"]
    api_data = [
        ("GET", "/api/health", "Public", "Returns JSON 200 with service health and model_loaded status"),
        ("POST", "/api/predict", "Public", "Ingests base64 frame, executes TFLite inference, returns label & confidence"),
        ("POST", "/api/predict-video", "Public", "Accepts multipart video file, extracts sample frames, returns sequence")
    ]
    add_custom_table(doc, api_heads, api_data)
    add_p(doc, "Table 5.2: RESTful API Route Specifications and Contract Definitions", size_pt=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=0)
    doc.add_page_break()

    # 13. Algorithmic Formulation
    add_p(doc, "5.3 Deep CNN Architecture & Speech Synthesis Implementation", size_pt=12, bold=True, space_before=6, space_after=4)
    p_alg = ("1. Center-Square Aspect-Ratio Crop Formulation:\n"
             "Given input frame I of width W and height H, let D = min(W, H). Spatial offsets are computed as:\n"
             "    x_start = floor((W - D) / 2),    y_start = floor((H - D) / 2)\n"
             "    I_crop = I[y_start : y_start + D,  x_start : x_start + D]\n\n"
             "2. Bilinear Interpolation Resampling:\n"
             "Continuous target grid coordinates are mapped to four discrete neighbor pixels (x1, y1), (x1, y2), (x2, y1), (x2, y2). The resampled color intensity f(x, y) is calculated as:\n"
             "    f(x, y) = (1 - alpha)(1 - beta) I(y1, x1) + alpha(1 - beta) I(y1, x2) + (1 - alpha)beta I(y2, x1) + alpha beta I(y2, x2)\n"
             "Normalized input tensor: X = f(x, y) / 255.0, where X in [0.0, 1.0]^(1 x 64 x 64 x 3).\n\n"
             "3. Convolutional Forward Propagation & Softmax Formulation:\n"
             "    Z^(l) = ReLU( W^(l) * A^(l-1) + b^(l) )\n"
             "The output logits z in R^29 are normalized to categorical probabilities via Softmax:\n"
             "    p_i = exp(z_i) / sum(exp(z_j)),   for all i in {1, 2, ..., 29}\n\n"
             "4. Temporal Debounce and Speech Synthesis:\n"
             "To eliminate accidental double-typing from hand transitions, the client enforces a 2-frame stability check: character C is committed if Predicted(t) == Predicted(t-1) with Confidence >= 0.50. Upon user trigger, window.speechSynthesis.speak() instantiates an asynchronous SpeechSynthesisUtterance object to vocalize the finalized English sentence aloud.")
    add_p(doc, p_alg, size_pt=10.5, space_after=0, line_spacing=1.15)
    doc.add_page_break()

    # 14. Testing & Latency
    add_p(doc, "5.4 Software Testing Matrix & Execution Verification", size_pt=12, bold=True, space_before=6, space_after=4)
    add_p(doc, "Automated testing was conducted across unit, preprocessing, API routing, and model layers using Pytest. Table 5.3 summarizes the execution results for the 8 core automated test suites.", size_pt=11, space_after=6)
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
    add_p(doc, "Table 5.3: Automated Test Suite Verification Results (8/8 Passed)", size_pt=9.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=10)

    add_p(doc, "Latency Accounting Across Architecture Tiers: Table 4.2 documents processing latencies measured across each pipeline stage against the 50 ms SLA.", size_pt=11, space_after=6)
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

    # 15. Conclusion & References
    add_p(doc, "CONCLUSION", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=10)
    add_p(doc, "EchoSign demonstrates that an integrated, decoupled web architecture can successfully bridge the communication divide between American Sign Language users and hearing individuals. The responsive client frontend paired with a lightweight Flask controller and an optimized float16 TensorFlow Lite model provides users with real-time fingerspelling recognition alongside immediate speech synthesis. By enforcing strict preprocessing parity through center-square cropping and Pillow bilinear resampling, the system achieves an outstanding 96.75% classification accuracy across 2,030 test images with a median response latency of 16.1 ms, well within the 50 ms service level agreement. Stateless cloud serverless deployment and browser-native voice vocalization guarantee zero cost and robust accessibility, establishing a practical assistive communication platform.", size_pt=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=14, line_spacing=1.2)
    add_p(doc, "REFERENCES", size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
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
        add_p(doc, r, size_pt=9.5, space_after=3, line_spacing=1.1)

    doc.save(output_path)
    print(f"Formatted Word Document saved to: {output_path}")

if __name__ == '__main__':
    p1 = r"c:\AI-project\SignBridge\docs\synopsis_EchoSign.docx"
    p2 = r"c:\AI-project\SignBridge\docs\synopsis_EchoSign_formatted.docx"
    build_synopsis(p1)
    build_synopsis(p2)
