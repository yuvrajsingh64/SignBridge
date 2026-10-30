# ECHOSIGN: AN AI-POWERED AMERICAN SIGN LANGUAGE TRANSLATION SYSTEM USING DEEP CONVOLUTIONAL NEURAL NETWORKS AND REAL-TIME SPEECH SYNTHESIS

### Synopsis Report submitted in partial fulfillment of the requirement for the degree of
## Bachelor of Technology
### In
## Computer Science and Engineering

---

<div align="center">

### Under the Supervision of:
**Ms. Reeta Nagar**  
Assistant Professor, Department of Computer Science & Engineering  
Maharana Pratap Engineering College, Kanpur  

<br>

### Submitted By (Project Team - 5 Members):
| S. No. | Student Name | University Roll Number | Research Team Division |
|:---:|:---|:---:|:---|
| 1 | **Nidhi Singh** | 2303491530068 | Research Team 1 (AI/ML & Vision) |
| 2 | **Yuvraj Singh** | 2303491530128 | Research Team 1 (AI/ML & Vision) |
| 3 | **Rohit Kumar** | 2303491530090 | Research Team 2 (Systems & Cloud) |
| 4 | **Prashant Kumar Singh** | 2303491530075 | Research Team 2 (Systems & Cloud) |
| 5 | **Komal Goswami** | 2303491530061 | Research Team 2 (Systems & Cloud) |

<br>

### Department of Computer Science & Engineering
## Maharana Pratap Engineering College, Kanpur
### Dr. A.P.J. Abdul Kalam Technical University, Lucknow
**Academic Session: 2026–2027**

</div>

---

\newpage

## DECLARATION

This is to certify that the Synopsis Report entitled **“EchoSign: An AI-Powered American Sign Language Translation System Using Deep Convolutional Neural Networks and Real-Time Speech Synthesis”**, submitted in partial fulfillment of the requirements for the award of the degree of **Bachelor of Technology in Computer Science and Engineering** to **Maharana Pratap Engineering College, Kanpur**, affiliated with **Dr. A.P.J. Abdul Kalam Technical University, Lucknow**, is an authentic record of our own work carried out under the supervision of **Ms. Reeta Nagar**, Assistant Professor, Department of Computer Science & Engineering.

The matter embodied in this synopsis report has not been submitted by us or any other candidate for the award of any other degree or diploma to any other institute or university.

All source code, deep learning model architectures, image preprocessing pipelines, application programming interfaces, and experimental evaluation datasets reported herein are genuine and developed by our team. All external open-source software libraries, datasets, and literature references have been appropriately credited and cited.

<br>

**Date:** 30th October 2026  
**Place:** Kanpur  

<br>

**Signatures of the Candidates:**

1. **Nidhi Singh** (Roll No: 2303491530068) &nbsp;&nbsp; ____________________
2. **Yuvraj Singh** (Roll No: 2303491530128) &nbsp;&nbsp; ____________________
3. **Rohit Kumar** (Roll No: 2303491530090) &nbsp;&nbsp; ____________________
4. **Prashant Kumar Singh** (Roll No: 2303491530075) &nbsp;&nbsp; ____________________
5. **Komal Goswami** (Roll No: 2303491530061) &nbsp;&nbsp; ____________________

<br>

---

<br>

### CERTIFICATE OF APPROVAL

This is to certify that the project synopsis entitled **“EchoSign: An AI-Powered American Sign Language Translation System Using Deep Convolutional Neural Networks and Real-Time Speech Synthesis”**, prepared by **Nidhi Singh (2303491530068), Yuvraj Singh (2303491530128), Rohit Kumar (2303491530090), Prashant Kumar Singh (2303491530075), and Komal Goswami (2303491530061)**, has been reviewed and found satisfactory for submission as a Final Year Project Synopsis in partial fulfillment of the B.Tech degree curriculum.

<br><br>

___________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ___________________________  
**Ms. Reeta Nagar** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Mr. Milind Bhatt**  
Project Guide &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Head of Department  
Department of CSE &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Department of CSE  
MPEC, Kanpur &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; MPEC, Kanpur  

---

\newpage

## TABLE OF CONTENTS

| S. No. | Contents | Page No. |
|:---:|:---|:---:|
| | **Title Page** | i |
| | **Declaration** | ii |
| | **Certificate of Approval** | iii |
| | **Table of Contents** | iv |
| | **List of Acronyms and Abbreviations** | v |
| | **List of Figures and Tables** | vi |
| | **Abstract** | vii |
| **1.** | **CHAPTER 1 — INTRODUCTION** | **1** |
| 1.1 | Background and Motivation | 1 |
| 1.2 | Overview of EchoSign | 1 |
| 1.3 | Objectives of the Project | 2 |
| 1.4 | Scope of the Project | 2 |
| **2.** | **CHAPTER 2 — LITERATURE REVIEW** | **3** |
| 2.1 | Review of Existing Gesture Recognition Techniques | 3 |
| 2.2 | Limitations of Existing Approaches | 4 |
| 2.3 | Comparative Summary of Existing Solutions | 5 |
| **3.** | **CHAPTER 3 — REAL-WORLD APPLICATIONS** | **6** |
| 3.1 | Practical Applications of EchoSign | 6 |
| 3.2 | Target User Demographics | 7 |
| **4.** | **CHAPTER 4 — INFERENCES DRAWN FROM LITERATURE** | **8** |
| 4.1 | Research Gaps and Key Technical Inferences | 8 |
| 4.2 | Division of Two Research Paper Tracks | 9 |
| **5.** | **CHAPTER 5 — PROBLEM STATEMENT AND SOLUTION APPROACH** | **10** |
| 5.1 | Problem Statement | 10 |
| 5.2 | Proposed Solution Architecture | 10 |
| 5.3 | Algorithmic and Mathematical Formulation | 11 |
| 5.4 | Hardware and Software Requirements | 12 |
| 5.5 | Testing and Quality Assurance Plan | 13 |
| **6.** | **CHAPTER 6 — PROPOSED TIME-BOUND PROGRESS OF THE PROJECT** | **14** |
| 6.1 | Project Development Schedule (Weeks 1 to 13) | 14 |
| 6.2 | Team Member Responsibilities & Milestone Deliverables | 15 |
| | **CONCLUSION** | **16** |
| | **BIBLIOGRAPHY / REFERENCES** | **17** |

---

\newpage

## LIST OF ACRONYMS AND ABBREVIATIONS

| Acronym | Complete Expansion |
|:---|:---|
| **AI** | Artificial Intelligence |
| **ASL** | American Sign Language |
| **API** | Application Programming Interface |
| **CNN** | Convolutional Neural Network |
| **CPU** | Central Processing Unit |
| **FPS** | Frames Per Second |
| **HTTP** | HyperText Transfer Protocol |
| **JSON** | JavaScript Object Notation |
| **KB / MB** | Kilobyte / Megabyte |
| **PIL** | Python Imaging Library (Pillow) |
| **ReLU** | Rectified Linear Unit |
| **REST** | Representational State Transfer |
| **RGB** | Red, Green, Blue Color Model |
| **ROI** | Region of Interest |
| **SLA** | Service Level Agreement |
| **TFLite** | TensorFlow Lite Engine |
| **TTS** | Text-To-Speech Synthesis |
| **UI / UX** | User Interface / User Experience |
| **WSGI** | Web Server Gateway Interface |

---

## LIST OF FIGURES AND TABLES

### List of Figures
- **Figure 5.1:** High-Level Layered System Architecture of EchoSign Platform *(Page 11)*
- **Figure 5.2:** End-to-End Image Ingestion and Prediction Pipeline *(Page 12)*
- **Figure 6.1:** Proposed 13-Week Time-Bound Project Activity Schedule *(Page 15)*

### List of Tables
- **Table 2.1:** Comparative Analysis of Gesture Recognition Techniques vs. EchoSign *(Page 5)*
- **Table 4.1:** Two-Track Research Paper Division & Authorship *(Page 9)*
- **Table 5.1:** Hardware Environment Specifications *(Page 12)*
- **Table 5.2:** Software Tools and Frameworks *(Page 13)*
- **Table 5.3:** Verification Testing Plan Matrix *(Page 13)*
- **Table 6.1:** Project Execution Timetable and Deliverables *(Page 14)*

---

\newpage

## ABSTRACT

Communication between individuals who are deaf or hard-of-hearing and the hearing population remains hindered by the widespread lack of sign language literacy among the general public. While American Sign Language (ASL) is a rich and structured linguistic medium, everyday public interactions at healthcare facilities, transport counters, and administrative desks frequently lack human interpreters. Existing technological interventions predominantly rely on expensive sensor-instrumented data gloves or complex multi-camera setups that are cost-prohibitive, cumbersome, and absent from mainstream web environments.

This synopsis presents **EchoSign**, an end-to-end, lightweight, web-accessible sign language recognition and speech synthesis system. EchoSign classifies static ASL fingerspelling gestures from 2D images and live camera feeds across 29 classes (letters A–Z, space, delete, and nothing) and vocalizes the translated output in real time. The system employs a deep Convolutional Neural Network (CNN) featuring double-convolution feature extraction blocks and dropout regularization, trained on a curated corpus of 20,300 images (700 images per class) derived from the ASL Alphabet dataset. To ensure deployment feasibility on cloud infrastructure and standard mobile/desktop browsers without requiring dedicated GPUs, the model is optimized via float16 quantization into TensorFlow Lite format, reducing storage footprint to 4.29 MB.

A key engineering contribution of this project is the alignment of image preprocessing between training and production inference: both stages utilize a deterministic center-square cropping algorithm and bilinear interpolation resampling via Pillow, eliminating spatial distortion and interpolation drift that typically degrade real-world webcam accuracy. On an independent held-out evaluation set of 2,030 samples, the quantized model achieves an overall classification accuracy of **96.75%**, with 28 out of 29 classes recognized correctly at confidences exceeding 92%. The serverless RESTful backend, built on Flask and hosted on Vercel, demonstrates an average inference latency of under 25 milliseconds, while the client interface leverages HTML5 Canvas region-of-interest guidance and the browser-native Web Speech API for seamless auditory output. EchoSign provides an accessible, private, zero-installation communication aid for inclusive daily interactions.

**Keywords:** American Sign Language, Convolutional Neural Networks, TensorFlow Lite, Edge Inference, Web Speech API, Assistive Technology, Image Preprocessing.

---

\newpage

# CHAPTER 1: INTRODUCTION

## 1.1 Background and Motivation
Communication is the foundation of educational, professional, and civic engagement. Over 70 million deaf individuals globally rely on sign language as their primary means of expression. In North America and various international communities, American Sign Language (ASL) serves as the primary linguistic medium for deaf and hard-of-hearing people. ASL possesses its own intricate morphology, phonology, and syntax, using combinations of handshapes, orientations, facial expressions, and spatial dynamics to convey meaning.

Despite its linguistic richness, fewer than 1% of the hearing population possesses working literacy in sign language. Consequently, deaf individuals routinely experience severe communication barriers when accessing essential services such as emergency triage, hospital consultations, educational lectures, public transit ticketing, and retail transactions. Certified human sign language interpreters are scarce and financially demanding, making full-time human translation unfeasible for casual, day-to-day encounters.

Recent breakthroughs in deep learning and computer vision have enabled machines to analyze complex visual data with high reliability. In particular, Convolutional Neural Networks (CNNs) have shown exceptional ability in extracting spatial hierarchies from digital imagery. However, most existing sign language research remains confined to academic laboratory settings or relies on specialized wearable sensors (such as flex-sensor data gloves and depth-sensing cameras) that cannot be integrated into a user's spontaneous digital workflow. There is an urgent practical demand for a cross-platform, zero-installation web application that runs directly in consumer browsers over inexpensive webcams to interpret fingerspelled signs into legible English text and spoken audio.

## 1.2 Overview of EchoSign
**EchoSign** is an AI-powered assistive web system designed to bridge the linguistic divide between sign language users and non-signers. The system accepts visual input from three distinct sources: static image file uploads (JPEG, PNG, WebP), live webcam video streams captured directly in the browser, and recorded video uploads.

The core of EchoSign comprises a custom-trained Convolutional Neural Network that classifies hand configurations into 29 distinct classes—encompassing the 26 standard English alphabet letters (A through Z) and 3 operational control gestures:
1. `space`: Inserts a word separation delimiter into the sentence composer.
2. `del`: Deletes the most recently added character to correct typographical errors.
3. `nothing`: Indicates an empty frame or resting hand posture, preventing spurious character insertions.

The system features an integrated client-side sentence composition buffer with temporal stabilization logic. As characters are recognized with high statistical confidence, they are appended to an editable text workspace. When an utterance is finalized, the platform engages the browser's native Web Speech API (`window.speechSynthesis`) to read the constructed English sentence aloud in natural spoken audio. The entire backend runs as a lightweight, serverless inference service deployable on minimal cloud infrastructure.

## 1.3 Objectives of the Project
The primary engineering and research objectives of the EchoSign project are:
1. **Model Formulation and Training:** To design, train, and validate a deep Convolutional Neural Network architecture capable of classifying 29 ASL fingerspelling categories with a target validation accuracy exceeding 95%.
2. **Preprocessing Pipeline Parity:** To construct an identical image preprocessing pipeline across both offline training and online inference phases using center-square cropping and bilinear interpolation, ensuring that aspect-ratio distortions do not corrupt real-time predictions.
3. **Model Compression and Edge Deployment:** To compress the trained Keras model via float16 quantization into an optimized TensorFlow Lite (`.tflite`) file under 5 MB, ensuring minimal memory consumption and sub-50 ms execution latencies on standard CPU environments.
4. **Interactive Multi-Input Web Application:** To develop a responsive, accessible web portal using Flask and Bootstrap 5 supporting image upload, interactive live camera processing with Region-of-Interest (ROI) alignment guides, and video analysis.
5. **Real-Time Speech Synthesis:** To incorporate client-side auditory vocalization of assembled text using the Web Speech API without external paid third-party voice APIs.
6. **Educational Support Tools:** To integrate an interactive ASL Alphabet Reference Guide displaying standardized hand postures and anatomical descriptions to serve as an educational resource for beginners.
7. **Rigorous Quality Verification:** To implement an automated verification suite confirming functional API correctness, preprocessing consistency, and classification reliability across all 29 target classes.

## 1.4 Scope of the Project
The functional scope of the initial EchoSign implementation is focused on **static ASL manual fingerspelling (the ASL alphabet)**. Fingerspelling is the standard component of sign language utilized to communicate names, technical terms, addresses, and concepts that do not possess dedicated root signs.

* **Boundary Limits:** The current release focuses on static gesture identification from single hand frames. The letters **J** and **Z**, which involve explicit trajectory motions in formal ASL, are evaluated via representative static pause postures accompanied by an automatic contextual advisory notice on the interface.
* **Grammar Scope:** The system transliterates fingerspelled signs into English letters and words; it does not attempt full semantic parsing of continuous multi-hand grammatical sign sentences.
* **Operating Environment:** The web platform operates over modern web browsers (Google Chrome, Mozilla Firefox, Microsoft Edge, Safari) supporting WebRTC camera permissions and HTML5 canvas manipulation, requiring no native executable downloads or proprietary external hardware.

---

\newpage

# CHAPTER 2: LITERATURE REVIEW

## 2.1 Review of Existing Gesture Recognition Techniques
Sign language recognition has been investigated through multiple engineering paradigms over the past three decades. These methodologies can be broadly categorized into four primary techniques:

### Technique 1: Sensor-Instrumented Wearable Data Gloves
Early gesture recognition research focused on physical sensors mounted on gloves worn by the user. These devices incorporate flex sensors along the finger joints to measure curvature, contact sensors at the fingertips to detect pinches, and 3-axis inertial measurement units (IMUs) on the back of the hand to track wrist pitch and roll.
* **Methodology:** Analog voltage changes across resistive flex sensors are digitized via microcontrollers (e.g., Arduino or STM32) and classified using threshold algorithms or shallow Support Vector Machines (SVMs).
* **Limitations:** While sensor gloves offer high spatial precision independent of ambient lighting, they require tedious manual calibration, suffer from mechanical wear and tear, and place an intrusive physical burden on the user. Furthermore, deaf individuals reject the requirement to carry and wear specialized hardware during spontaneous public encounters.

### Technique 2: Classical Computer Vision and Handcrafted Descriptors
Prior to the rise of deep learning, computer vision approaches relied on manual feature extraction. Researchers segmented hands using skin-color thresholding in the YCbCr or HSV color spaces, followed by edge extraction and morphological contour closing.
* **Methodology:** Features were extracted using mathematical descriptors such as Scale-Invariant Feature Transform (SIFT), Histogram of Oriented Gradients (HOG), and Hu Moments, followed by classification using K-Nearest Neighbors (KNN) or Random Forests.
* **Limitations:** These methods are extremely fragile in uncontrolled real-world environments. Variations in room illumination, skin tone diversity, and cluttered or moving backgrounds frequently cause segmentation failure, resulting in classification drop-offs below 70% in field settings.

### Technique 3: Deep Convolutional Neural Networks (CNNs)
Deep learning bypasses handcrafted feature extraction by learning hierarchical spatial representations directly from raw pixel matrices. Early convolutional layers extract low-level edges and corners, intermediate layers detect finger contours and knuckle joints, and deeper layers model complete hand silhouettes.
* **Methodology:** Feed-forward neural networks consisting of alternating convolutional, activation, and spatial pooling operations, regularized by dropout layers and trained end-to-end via backpropagation using categorical cross-entropy loss.
* **Advantages:** High resilience to background variations and lighting fluctuations when trained on sufficiently diverse image corpora.

### Technique 4: Hand Landmark Extraction (MediaPipe / OpenPose)
Frameworks such as Google MediaPipe Hands employ a two-stage pipeline: a palm detector localizes the hand boundary box across the entire image, after which a regression model predicts 21 3D coordinate keypoints corresponding to anatomical knuckles and finger tips.
* **Methodology:** The 21 landmark coordinate vectors are extracted and fed into dense feedforward networks or Long Short-Term Memory (LSTM) layers.
* **Limitations:** While computationally efficient on mobile devices, landmark regressors experience tracking failures during severe self-occlusions (such as closed-fist signs like 'E', 'M', 'N', 'S', and 'T' where fingers fold behind one another), causing misclassifications in fingerspelling alphabets where finger overlap is high. Direct CNN feature extraction preserves the global textural and shadow cues necessary to distinguish subtle knuckle positions.

## 2.2 Limitations of Existing Approaches
A critical review of published implementations and publicly available GitHub repositories reveals three chronic engineering deficiencies:
1. **Preprocessing Asymmetry:** Training pipelines frequently ingest cropped square images processed via OpenCV (`cv2.resize` with area interpolation), while the production web services ingest rectangular camera aspect ratios resized via Pillow (`PIL.Image.resize` with bilinear interpolation). This interpolation mismatch creates subtle pixel distortion that severely degrades production confidence.
2. **Computational Bloat:** Academic projects often deploy multi-gigabyte models (e.g., ResNet-152 or VGG-19) wrapped in unoptimized Python scripts. These models demand GPU acceleration, take minutes to load, and exceed the strict 250 MB execution size caps enforced by serverless cloud platforms like Vercel.
3. **Absence of End-to-End Assistive Integration:** Existing models are overwhelmingly presented as standalone Jupyter Notebooks without client interfaces, text composition buffers, or auditory feedback, limiting their real-world utility for non-technical users.

## 2.3 Comparative Summary of Existing Solutions

| Parameter / Feature | Wearable Sensor Gloves | Classical CV (HOG + SVM) | MediaPipe Landmarks + MLP | **EchoSign (Proposed)** |
|:---|:---:|:---:|:---:|:---:|
| **Hardware Requirement** | Custom flex sensor glove | Standard camera | Standard camera | **Standard consumer webcam** |
| **Physical Burden on User** | Severe (wearable hardware) | None | None | **None (Zero installation)** |
| **Lighting Sensitivity** | Impervious | Extremely high | Moderate | **Low (Data augmented CNN)** |
| **Handling of Finger Occlusions** | Good | Poor | Moderate to Poor | **High (Direct image CNN)** |
| **Model Size** | Microcontroller binary | < 10 MB | ~15 MB | **4.29 MB (TFLite Float16)** |
| **Inference Latency** | < 10 ms | 50–120 ms | 30–60 ms | **12–25 ms (CPU/Serverless)** |
| **Deployment Medium** | Embedded hardware | Native C++/Python | Web/Mobile SDK | **Web (Serverless REST API)** |
| **Built-in Speech Synthesis** | No | No | Rare | **Yes (Web Speech API)** |
| **End-to-End Accessibility** | Low | Low | Medium | **High (Responsive Web App)** |

---

\newpage

# CHAPTER 3: REAL-WORLD APPLICATIONS

## 3.1 Practical Applications of EchoSign
EchoSign is engineered as a zero-barrier assistive utility suited to several high-impact environments:

```
+-----------------------------------------------------------------------------------+
|                         REAL-WORLD APPLICATION DOMAINS                            |
+-----------------------------------------------------------------------------------+
|  1. Healthcare Outpatient Desks       |  2. Public Transit & Service Counters     |
|     - Patient intake & triage         |     - Ticketing inquiries                 |
|     - Symptom & medication spelling   |     - Information desk assistance         |
|     - Emergency reception check-in    |     - Administrative office queries       |
+---------------------------------------+-------------------------------------------+
|  3. Inclusive Educational Classrooms  |  4. Autonomous Sign Language Learning     |
|     - Peer-to-peer student dialogue   |     - Real-time gesture feedback          |
|     - Teacher-student communication   |     - Reference chart alignment           |
|     - Interactive spelling practice   |     - Confidence score validation         |
+-----------------------------------------------------------------------------------+
```

### 1. Healthcare Intake and Emergency Triage
In medical settings, prompt communication is vital. When a deaf patient arrives at an emergency clinic without an accompanying interpreter, front-desk staff can launch EchoSign on any clinic tablet or desktop browser. The patient can fingerspell their name, chief medical complaint, and known drug allergies. The system vocalizes the spelled words aloud to attending medical staff, preventing critical delays.

### 2. Public Transit and Civic Service Counters
Municipal service centers, railway ticket windows, and postal counters typically lack staff trained in sign language. Equipping service desks with a consumer tablet running EchoSign allows deaf citizens to independently communicate station names, document IDs, and transaction details without depending on written note-passing.

### 3. Inclusive Classroom Environments
In mainstream educational institutions with integrated classrooms, hearing instructors and peers frequently struggle to communicate with deaf students during laboratory sessions and informal discussions. EchoSign provides a real-time visual and auditory medium that promotes collaborative learning without requiring high-cost institutional setups.

### 4. Interactive Self-Learning Tool for ASL Students
Students learning American Sign Language frequently lack immediate validation when practicing fingerspelling postures at home. EchoSign functions as a personal practice coach: by showing signs to the webcam, students receive instant feedback on their posture accuracy, observing whether the predicted letter and confidence match the target alphabet chart.

## 3.2 Target User Demographics
1. **Primary Users (Deaf & Hard-of-Hearing Individuals):** Individuals who seek an autonomous, lightweight communication bridge for daily interactions with hearing persons who do not understand sign language.
2. **Secondary Users (Front-Line Service Staff & Public Personnel):** Healthcare receptionists, bank tellers, retail clerks, and transit operators who require an immediate translation interface to serve sign language users respectfully and efficiently.
3. **Tertiary Users (Sign Language Students & Educators):** Novice signers seeking real-time automated verification of their manual fingerspelling technique against standardized reference charts.

---

\newpage

# CHAPTER 4: INFERENCES DRAWN FROM LITERATURE

## 4.1 Research Gaps and Key Technical Inferences
Careful analysis of prior academic literature and deployed open-source systems highlights several technical findings that have directly governed the design of EchoSign:

1. **Inference 1: The Preprocessing Domain Gap Must Be Eliminated**  
   *Observation:* Standard computer vision training scripts read images using OpenCV (`cv2.imread`) in BGR format and downsample using `cv2.INTER_AREA`. Conversely, web application servers typically decode incoming HTTP base64 image payloads via Pillow (`PIL.Image`) in RGB format using bilinear or nearest-neighbor interpolation. At lower resolutions (e.g., 64×64), pixel intensity discrepancies between these resampling filters can alter decision boundaries by up to 20%, resulting in field misclassifications.  
   *Engineering Decision:* EchoSign enforces absolute preprocessing parity. Both training data ingestion and production inference utilize Pillow's deterministic bilinear resampling engine paired with center-square aspect-ratio preservation.

2. **Inference 2: Center-Square Cropping Preserves Natural Hand Geometry**  
   *Observation:* Direct non-uniform scaling of a standard 16:9 or 4:3 webcam frame to a 1:1 square model input (e.g., 64×64) compresses the hand horizontally or vertically. This geometric distortion warps the spatial relationship between fingers, causing critical confusion between tall vertical signs (e.g., 'B', 'D') and broad signs (e.g., 'C', 'O').  
   *Engineering Decision:* EchoSign introduces an algorithmic center-square cropping step that extracts $\min(W, H)$ from the center of the frame prior to resizing, maintaining hand shape proportions regardless of camera sensor aspect ratio.

3. **Inference 3: Serverless Constraints Demand Aggressive Quantization**  
   *Observation:* Modern web hosting architectures (such as Vercel and AWS Lambda) enforce strict memory ceilings (250 MB total package size) and cold-start timeout penalties. Full-precision TensorFlow Keras models exceed 25 MB and require heavyweight runtime dependencies, causing invocation timeouts.  
   *Engineering Decision:* The trained network is converted into an optimized TensorFlow Lite format with float16 parameter quantization. This achieves a 6× model compression (from 26.9 MB down to 4.29 MB) and enables execution via lightweight runtimes (`ai-edge-litert`), keeping invocation latencies under 25 ms.

## 4.2 Division of Two Research Paper Tracks
In accordance with the Department of Computer Science & Engineering guidelines for 5-member project teams, the technical contributions of EchoSign are formally partitioned into two distinct research tracks:

```
                                [ ECHOSIGN PROJECT TEAM ]
                                     (5 Students)
                                          |
                +-------------------------+-------------------------+
                |                                                   |
       [ RESEARCH TEAM 1 ]                                 [ RESEARCH TEAM 2 ]
          (2 Students)                                        (3 Students)
   - Nidhi Singh (2303491530068)                       - Rohit Kumar (2303491530090)
   - Yuvraj Singh (2303491530128)                      - Prashant Kumar Singh (2303491530075)
                |                                      - Komal Goswami (2303491530061)
                v                                                   |
    Research Paper Track 1                                          v
"Deep CNN Optimization, Bilinear                                Research Paper Track 2
 Resampling Parity, and Float16 Quantization            "Serverless RESTful Microservices, Real-Time
 for High-Accuracy ASL Alphabet Classification"          ROI Video Ingestion, and Web Speech Synthesis"
```

### Table 4.1: Two-Track Research Paper Division & Authorship

| Parameter | Research Track 1 (AI / Deep Learning Focus) | Research Track 2 (Systems & Cloud Deployment Focus) |
|:---|:---|:---|
| **Authors** | **Nidhi Singh** (2303491530068)<br>**Yuvraj Singh** (2303491530128) | **Rohit Kumar** (2303491530090)<br>**Prashant Kumar Singh** (2303491530075)<br>**Komal Goswami** (2303491530061) |
| **Research Domain** | Computer Vision & Neural Network Engineering | Distributed Systems & Assistive Human-Computer Interaction |
| **Core Technical Focus** | • Double-Conv deep CNN architecture design<br>• Preprocessing parity via Pillow bilinear interpolation<br>• Float16 model quantization and weight compression<br>• Per-class confusion matrix and precision-recall analysis | • Serverless RESTful architecture on Vercel<br>• In-browser ROI canvas frame extraction<br>• Temporal stabilization and buffer debounce algorithms<br>• Web Speech API integration and latency profiling |
| **Key Metric Evaluated** | 96.75% classification accuracy across 2,030 test images | Sub-25 ms backend inference latency; zero client installation |

---

\newpage

# CHAPTER 5: PROBLEM STATEMENT AND SOLUTION APPROACH

## 5.1 Problem Statement
Deaf and hard-of-hearing individuals face persistent communication barriers when interacting with the hearing majority who lack sign language knowledge. Existing computer vision solutions are either restricted to offline Python notebooks, rely on expensive specialized sensory hardware, or suffer severe accuracy degradation in production due to image resizing discrepancies between training and inference environments.

**Formal Engineering Problem:**  
*To engineer an accessible, zero-installation web translation platform that accepts single-frame and streaming webcam inputs of hand configurations, executes deep neural classification across 29 ASL classes with greater than 95% test accuracy in under 50 milliseconds, and synthesizes the translated output into natural English speech.*

## 5.2 Proposed Solution Architecture
EchoSign is architectured as a decoupled, three-tier cloud-native web system comprising the Client Presentation Layer, the Application Service Layer, and the Deep Inference Engine:

```
+-----------------------------------------------------------------------------------+
|                        1. CLIENT PRESENTATION LAYER                               |
|   - HTML5 / Bootstrap 5 Responsive UI (Desktop & Mobile Browser Support)          |
|   - WebRTC Camera Stream with 70% Center Region-of-Interest (ROI) Visual Guide    |
|   - HTML5 Canvas Frame Capture (Base64 JPEG Encoding)                             |
|   - Temporal Stabilizer (2-frame consecutive agreement filter)                    |
|   - Client-side Web Speech API (window.speechSynthesis for Vocalization)          |
+-----------------------------------------------------------------------------------+
                                       |
                   HTTP POST /api/predict (JSON Payload)
                                       v
+-----------------------------------------------------------------------------------+
|                        2. APPLICATION SERVICE LAYER                               |
|   - Lightweight Python Flask Web Server (WSGI / Vercel Serverless Handler)        |
|   - Base64 Payload Decoding & Image Header Validation (MIME Check)                 |
|   - Preprocessing Engine:                                                         |
|       * Aspect Ratio Check & Center-Square Cropping: min(W, H)                     |
|       * Pillow Resampling.BILINEAR Resize -> 64 x 64 pixels                       |
|       * Pixel Normalization -> Float32 Array [0.0, 1.0]                           |
+-----------------------------------------------------------------------------------+
                                       |
                   In-Memory Tensor Dispatch (Shape: 1x64x64x3)
                                       v
+-----------------------------------------------------------------------------------+
|                        3. DEEP INFERENCE ENGINE                                   |
|   - TensorFlow Lite Runtime (`ai-edge-litert` Engine)                             |
|   - Quantized Float16 Model (4.29 MB Storage Footprint)                           |
|   - 29-Class Softmax Probability Distribution Vector                              |
|   - Statistical Confidence Thresholding (Threshold = 0.50)                        |
|   - ASL Lexical Dictionary Lookup (Name, Semantic Meaning, Hand Shape Note)       |
+-----------------------------------------------------------------------------------+
```

## 5.3 Algorithmic and Mathematical Formulation

### 1. Aspect Ratio Preservation & Center-Square Crop
Given an incoming camera frame or uploaded image $\mathbf{I} \in \mathbb{R}^{H \times W \times 3}$, let $D = \min(W, H)$. The spatial bounding box coordinates for center-square cropping are defined as:
$$x_{\text{start}} = \left\lfloor \frac{W - D}{2} \right\rfloor, \quad y_{\text{start}} = \left\lfloor \frac{H - D}{2} \right\rfloor$$
The square sub-image $\mathbf{I}_{\text{crop}} \in \mathbb{R}^{D \times D \times 3}$ is extracted over:
$$\mathbf{I}_{\text{crop}} = \mathbf{I}[y_{\text{start}} : y_{\text{start}} + D, \; x_{\text{start}} : x_{\text{start}} + D]$$

### 2. Bilinear Interpolation Resampling
The cropped image $\mathbf{I}_{\text{crop}}$ is mapped to the target spatial dimension $64 \times 64$. For any coordinate $(x, y)$ in the target grid, the interpolated pixel intensity $f(x, y)$ is computed from the four nearest surrounding pixel coordinates $(x_1, y_1), (x_1, y_2), (x_2, y_1), (x_2, y_2)$ using:
$$f(x, y) \approx \frac{1}{(x_2 - x_1)(y_2 - y_1)} \begin{bmatrix} x_2 - x & x - x_1 \end{bmatrix} \begin{bmatrix} f(x_1, y_1) & f(x_1, y_2) \\ f(x_2, y_1) & f(x_2, y_2) \end{bmatrix} \begin{bmatrix} y_2 - y \\ y - y_1 \end{bmatrix}$$
Pixel intensities are subsequently scaled to the normalized unit interval:
$$\mathbf{X}_{\text{norm}} = \frac{f(x, y)}{255.0} \in [0.0, 1.0]^{1 \times 64 \times 64 \times 3}$$

### 3. Convolutional Feature Extraction and Softmax Classification
The input tensor is processed through sequential 2D convolutional filter banks:
$$\mathbf{Z}^{(l)} = \text{ReLU}\left( \mathbf{W}^{(l)} * \mathbf{A}^{(l-1)} + \mathbf{b}^{(l)} \right)$$
where $*$ denotes the discrete convolution operation, and $\text{ReLU}(z) = \max(0, z)$.

The final dense classification layer outputs unnormalized logits $\mathbf{z} \in \mathbb{R}^{29}$, which are converted into a probability vector $\mathbf{p}$ via the Softmax activation function:
$$p_i = \frac{e^{z_i}}{\sum_{j=1}^{29} e^{z_j}}, \quad \forall i \in \{1, 2, \dots, 29\}$$
The predicted category $\hat{y}$ and corresponding confidence score $C$ are obtained as:
$$\hat{y} = \arg\max_{i} (p_i), \quad C = \max_{i} (p_i)$$
If $C < 0.50$, the system flags a low-confidence warning on the user interface, prompting the user to adjust lighting or hand positioning.

## 5.4 Hardware and Software Requirements

### Table 5.1: Hardware Environment Specifications
| Environment Component | Development Hardware | Target Deployment Server | Minimum Client Device |
|:---|:---|:---|:---|
| **Processor (CPU)** | Intel Core i5 / AMD Ryzen 5 | Multi-tenant Serverless vCPU | Any dual-core mobile or desktop CPU |
| **System Memory (RAM)**| 8 GB DDR4 (minimum) | 1024 MB Execution Container | 2 GB System Memory |
| **Storage Capacity** | 256 GB SSD | < 50 MB Deployment Bundle | Standard browser storage |
| **Camera Sensor** | 720p HD integrated webcam | Not applicable (Server) | Standard front-facing webcam or phone camera |
| **Network Interface** | Broadband connection | High-speed Vercel Edge CDN | 3G / 4G / Wi-Fi internet connection |

### Table 5.2: Software Tools and Frameworks
| Layer | Tool / Technology | Version / Release | Role in EchoSign Project |
|:---|:---|:---|:---|
| **Programming Language**| Python | 3.12 | Primary backend scripting & ML training |
| **Deep Learning Library**| TensorFlow / Keras | 2.16+ / 2.21 | Model definition, training, and TFLite conversion |
| **Inference Runtime** | `ai-edge-litert` / TFLite | Latest | Serverless, lightweight CPU inference engine |
| **Image Processing** | Pillow (PIL) | 10.x | Aspect cropping, bilinear resizing, image decoding |
| **Numerical Computing** | NumPy | 1.26.x | Tensor manipulation and array operations |
| **Backend Framework** | Flask | 3.0.x | RESTful API routing and web application server |
| **Frontend Framework** | HTML5, CSS3, Bootstrap | 5.3.2 | Responsive, mobile-friendly user interface |
| **Styling & Icons** | Bootstrap Icons | 1.11.1 | Visual iconography and status indicators |
| **Speech Engine** | Web Speech API | W3C Standard | Client-side native text-to-speech vocalization |
| **Cloud Hosting** | Vercel Platform | Cloud Native | Serverless edge deployment and static asset CDN |

## 5.5 Testing and Quality Assurance Plan
To ensure software reliability, EchoSign incorporates a multi-tiered test suite:

### Table 5.3: Verification Testing Plan Matrix
| Test Domain | Target Module | Test Condition & Input Payload | Expected Metric / Behavior |
|:---|:---|:---|:---|
| **Preprocessing Test** | `src/preprocessing.py` | Rectangular image (1280×720) with non-square aspect | Yields perfectly square 64×64×3 tensor normalized to [0, 1] |
| **Model Verification** | `models/signbridge_model.tflite` | 2,030 held-out test images across 29 classes | Overall accuracy $\ge 95\%$; all classes correctly mapped |
| **Health API Test** | `GET /api/health` | Standard HTTP GET request | Status code 200; `model_loaded: true` |
| **Prediction API Test**| `POST /api/predict` | Valid base64 JPEG data payload | JSON response containing predicted label, confidence, meaning |
| **Boundary Test** | `POST /api/predict` | Corrupted base64 payload or non-image string | Graceful HTTP 400 error response without server crash |
| **Audio Synthesis Test**| Client Web Speech Engine | Multi-word constructed string in sentence buffer | Browser vocalizes English speech via system audio output |

---

\newpage

# CHAPTER 6: PROPOSED TIME-BOUND PROGRESS OF THE PROJECT

## 6.1 Project Development Schedule (Weeks 1 to 13)
The project execution is organized into structured, sequential phases over a 13-week academic duration:

```
+---------------------------------------------------------------------------------------+
|                       13-WEEK PROJECT ACTIVITY TIMETABLE                              |
+-----+----------------------------------+---------------+------------------------------+
| Wk  | Project Activity Description     | Duration      | Major Milestone Deliverable  |
+-----+----------------------------------+---------------+------------------------------+
| 1   | Problem Identification & Scope   | 1 Week        | Project Charter & Objectives |
| 2   | Literature Survey & Gaps         | 1 Week        | Comprehensive Review Matrix  |
| 3   | Dataset Acquisition & Audit      | 1 Week        | 20,300 Balanced Image Corpus |
| 4-5 | Preprocessing Pipeline & Parity  | 2 Weeks       | Pillow Cropping & Resampling |
| 6-7 | CNN Architecture & Training      | 2 Weeks       | 96.75% Accuracy Keras Model  |
| 8   | TFLite Quantization (Float16)    | 1 Week        | 4.29 MB Optimized Model File |
| 9   | Flask RESTful API Development    | 1 Week        | Tested Endpoint Services     |
| 10  | Frontend UI & Web Speech Setup   | 1 Week        | Responsive Client Portal     |
| 11  | Vercel Serverless Integration    | 1 Week        | Live Cloud Deployment        |
| 12  | Testing, Validation & Profiling  | 1 Week        | Complete Verification Suite  |
| 13  | Documentation & Research Papers  | 1 Week        | Final Report & 2 Submissions |
+-----+----------------------------------+---------------+------------------------------+
```

## 6.2 Team Member Responsibilities & Milestone Deliverables
In accordance with the 5-member team structure, responsibilities are clearly allocated:

1. **Nidhi Singh (2303491530068) — Lead Deep Learning Engineer (Research Team 1):**
   * Formulation and tuning of the deep Convolutional Neural Network architecture.
   * Implementation of regularized double-conv blocks, dropout layers, and softmax activation.
   * Primary author of Research Paper Track 1 (AI / Deep Learning methodology).

2. **Yuvraj Singh (2303491530128) — Machine Learning & Optimization Specialist (Research Team 1):**
   * Dataset curation, train/val/test stratified partitioning, and training evaluation.
   * Model quantization (float16) into TensorFlow Lite format and per-class confusion matrix analysis.
   * Co-author of Research Paper Track 1; model verification and benchmarking.

3. **Rohit Kumar (2303491530090) — Backend & Cloud Systems Architect (Research Team 2):**
   * Development of the Flask application, RESTful prediction endpoints, and error handling.
   * Cloud deployment configuration on Vercel serverless platform and rewrite routing.
   * Primary author of Research Paper Track 2 (Cloud Systems & Assistive HCI).

4. **Prashant Kumar Singh (2303491530075) — Computer Vision & Preprocessing Engineer (Research Team 2):**
   * Construction of the deterministic center-square cropping and Pillow bilinear resampling pipeline.
   * Validation of preprocessing symmetry between training data loaders and real-time API handlers.
   * Co-author of Research Paper Track 2; latency accounting and performance profiling.

5. **Komal Goswami (2303491530061) — Frontend UI/UX & Web Speech Engineer (Research Team 2):**
   * Design of the responsive Bootstrap 5 interface and WebRTC live camera integration with ROI guide box.
   * Implementation of the text composition buffer, temporal debounce stabilization, and Web Speech API synthesis.
   * Co-author of Research Paper Track 2; usability evaluation and interface testing.

---

\newpage

## CONCLUSION

The EchoSign project establishes a practical, high-accuracy, zero-installation solution for American Sign Language fingerspelling translation. By resolving the critical image preprocessing domain gap through deterministic center-square cropping and bilinear interpolation, and by compressing a double-convolution deep CNN into a 4.29 MB float16 TensorFlow Lite model, the system achieves an outstanding **96.75% test accuracy** while maintaining sub-25 ms inference latencies on standard CPU environments. 

The integration of real-time camera streaming with ROI alignment cues, an editable sentence construction workspace, and native client-side speech vocalization fulfills a pressing assistive need. This project demonstrates that state-of-the-art computer vision models can be deployed within serverless web constraints to provide practical, accessible, and privacy-preserving communication tools for the deaf and hard-of-hearing community.

---

\newpage

## BIBLIOGRAPHY / REFERENCES

1. **LeCun, Y., Bengio, Y., & Hinton, G. (2015).** Deep learning. *Nature*, 521(7553), 436–444.
2. **Akash Nagaraj. (2018).** ASL Alphabet Dataset. *Kaggle Datasets*, DOI: 10.34740/KAGGLE/DSV/26430.
3. **Goodfellow, I., Bengio, Y., & Courville, A. (2016).** *Deep Learning*. MIT Press, Cambridge, MA.
4. **Howard, A. G., et al. (2017).** MobileNets: Efficient convolutional neural networks for mobile vision applications. *arXiv preprint arXiv:1704.04861*.
5. **Lugaresi, C., et al. (2019).** MediaPipe: A framework for building perception pipelines. *arXiv preprint arXiv:1906.08172*.
6. **David, R., et al. (2021).** TensorFlow Lite: On-device machine learning framework. *IEEE Micro*, 41(4), 106–114.
7. **W3C Speech API Community Group. (2020).** Web Speech API Specification. *World Wide Web Consortium (W3C)*, W3C Draft Report.
8. **Rautaray, S. S., & Agrawal, A. (2015).** Vision based hand gesture recognition for human computer interaction: a survey. *Artificial Intelligence Review*, 43(1), 1–54.
9. **Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012).** ImageNet classification with deep convolutional neural networks. *Advances in Neural Information Processing Systems (NeurIPS)*, 25, 1097–1105.
10. **Kingma, D. P., & Ba, J. (2014).** Adam: A method for stochastic optimization. *arXiv preprint arXiv:1412.6980*.
11. **Srivastava, N., et al. (2014).** Dropout: a simple way to prevent neural networks from overfitting. *Journal of Machine Learning Research*, 15(1), 1929–1958.
12. **Grinberg, M. (2018).** *Flask Web Development: Developing Web Applications with Python* (2nd ed.). O'Reilly Media.
13. **IEEE Standards Association. (2017).** *IEEE Standard for Software and System Test Documentation* (IEEE Std 829-2017).
14. **Pressman, R. S., & Maxim, B. R. (2020).** *Software Engineering: A Practitioner's Approach* (9th ed.). McGraw-Hill Education.
