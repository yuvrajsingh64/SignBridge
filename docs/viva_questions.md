# SignBridge — Comprehensive Viva Voce Questions & Answers

> **Project**: SignBridge — AI-Powered Sign Language to English Translator  
> **Domains**: Python, Computer Vision, Convolutional Neural Networks, Deep Learning, Preprocessing, Model Evaluation, Flask Backend, Web APIs, Accessibility & Ethics  
> **Total Questions**: 48 Questions with Detailed Academic Answers  

---

## Table of Contents
1. [Python Fundamentals & Scientific Computing (Q1 – Q5)](#1-python-fundamentals--scientific-computing)
2. [Deep Learning & Convolutional Neural Networks (Q6 – Q15)](#2-deep-learning--convolutional-neural-networks)
3. [Computer Vision & OpenCV (Q16 – Q21)](#3-computer-vision--opencv)
4. [Image Preprocessing & Data Augmentation (Q22 – Q27)](#4-image-preprocessing--data-augmentation)
5. [Dataset Splitting & Validation Methodology (Q28 – Q31)](#5-dataset-splitting--validation-methodology)
6. [Overfitting, Regularization & Optimization (Q32 – Q36)](#6-overfitting-regularization--optimization)
7. [Model Evaluation & Classification Metrics (Q37 – Q41)](#7-model-evaluation--classification-metrics)
8. [Flask Backend & RESTful Architecture (Q42 – Q45)](#8-flask-backend--restful-architecture)
9. [Real-Time Webcam & Frontend Integration (Q46 – Q48)](#9-real-time-webcam--frontend-integration)

---

## 1. Python Fundamentals & Scientific Computing

### Q1: Why was Python chosen as the primary programming language for the SignBridge project?
**Answer:** Python is the de facto industry standard for artificial intelligence and machine learning due to its extensive ecosystem of mature, high-performance libraries such as TensorFlow, Keras, OpenCV, NumPy, and scikit-learn. Python's clear syntax accelerates rapid prototyping and modular development. Furthermore, Python provides robust web microframeworks like Flask, enabling seamless unification of backend machine learning inference pipelines with frontend user interfaces without language-bridging overhead.

### Q2: What role does NumPy play in the image preprocessing and inference pipeline?
**Answer:** In computer vision, images are fundamentally multidimensional numerical matrices (tensors). OpenCV and PIL decode images into NumPy `ndarray` structures where spatial dimensions, color channels, and batch sizes are manipulated. In SignBridge, NumPy is utilized for pixel normalization (casting uint8 `[0, 255]` to float32 `[0.0, 1.0]`), array reshaping and dimension expansion (`np.expand_dims` to create batch dimensions `(1, 64, 64, 3)`), argmax extraction (`np.argmax` on output probability distributions), and saving evaluation test splits as binary `.npy` archives.

### Q3: How does Python manage memory when loading large image datasets, and how is out-of-memory (OOM) prevented?
**Answer:** Loading tens of thousands of raw uncompressed images directly into memory as dense float32 arrays can easily exhaust system RAM. SignBridge mitigates this by:
1. Providing a configurable `max_per_class` sampling threshold during experimentation.
2. Downscaling image resolutions from 200×200 to 64×64 pixels before array conversion, reducing per-image memory footprint by ~90%.
3. Utilizing TensorFlow's `tf.data.Dataset` pipeline with batch generators and prefetching (`tf.data.AUTOTUNE`), which streams images in manageable minibatches (batch size 32) during training rather than materializing the full augmented dataset in memory simultaneously.

### Q4: Explain the singleton pattern used in `src/predictor.py` and why it is critical for web applications.
**Answer:** Loading a deep learning model from disk into memory involves parsing network graphs, allocating tensor buffers, and loading millions of floating-point weights, which is computationally expensive (often taking 2–5 seconds). If a model were loaded inside the Flask route handler on every incoming HTTP request, latency would be catastrophic and server memory would be depleted rapidly. The singleton pattern in `get_predictor()` ensures that `SignPredictor` initializes and loads `signbridge_model.keras` exactly once upon server startup. Subsequent prediction requests reuse the cached in-memory model instance.

### Q5: What is the difference between shallow copying and deep copying in Python, and where is this relevant in SignBridge?
**Answer:** A shallow copy creates a new compound object but inserts references into it to the objects found in the original, whereas a deep copy constructs a new object and recursively inserts copies of the objects found in the original. In `src/dictionary.py`, the `lookup()` function returns `ASL_DICTIONARY[label].copy()`. Returning a copy rather than the direct dictionary reference ensures that mutation of prediction responses by caller functions cannot contaminate the core dictionary definition.

---

## 2. Deep Learning & Convolutional Neural Networks

### Q6: What is a Convolutional Neural Network (CNN), and why is it superior to traditional Multi-Layer Perceptrons (MLPs) for image recognition?
**Answer:** A CNN is a specialized deep neural network designed for grid-structured data like images. Unlike MLPs that flatten images into 1D vectors—discarding 2D spatial relationships and requiring massive numbers of weights that lead to overfitting—CNNs exploit spatial locality through convolutional filters. Key advantages include:
1. **Local receptive fields**: Neurons detect localized features (edges, textures, contours) rather than connecting to every pixel.
2. **Parameter sharing (weight sharing)**: The same filter slides across the entire image, drastically reducing trainable parameters.
3. **Translation equivariance**: If a hand sign shifts slightly within the frame, feature maps preserve the activation pattern.

### Q7: Describe the architectural layers used in the SignBridge CNN model.
**Answer:** The SignBridge model consists of an input layer accepting `(64, 64, 3)` tensors, followed by three sequential convolutional blocks:
- **Block 1**: Two Conv2D layers (32 filters, 3×3 kernel, same padding), Batch Normalization, ReLU activation, 2×2 MaxPooling, and 0.25 Dropout.
- **Block 2**: Two Conv2D layers (64 filters, 3×3 kernel, same padding), Batch Normalization, ReLU activation, 2×2 MaxPooling, and 0.25 Dropout.
- **Block 3**: Two Conv2D layers (128 filters, 3×3 kernel, same padding), Batch Normalization, ReLU activation, 2×2 MaxPooling, and 0.25 Dropout.
- **Classifier**: GlobalAveragePooling2D, Dense layer (256 units), Batch Normalization, ReLU activation, 0.5 Dropout, and a final Dense output layer with 29 units and Softmax activation.

### Q8: What is the role of the activation function, and why is ReLU preferred in hidden layers?
**Answer:** Without non-linear activation functions, any composition of linear convolutional and dense layers simplifies mathematically into a single linear transformation, preventing the network from learning complex non-linear decision boundaries. The Rectified Linear Unit ($\text{ReLU}(z) = \max(0, z)$) is preferred in hidden layers because:
1. It is computationally efficient (a simple threshold at zero).
2. It mitigates the vanishing gradient problem encountered with sigmoid or tanh functions during backpropagation, as its derivative is 1 for all positive inputs.
3. It induces sparse activations, promoting efficient representation learning.

### Q9: How does the Softmax activation function work in the final output layer?
**Answer:** The Softmax function converts unnormalized real-valued logits $z_i$ produced by the final dense layer into a normalized probability distribution across the $K=29$ classes:
$$\sigma(z)_i = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}$$
The resulting outputs satisfy two essential mathematical properties: every probability is bounded in $(0, 1)$, and the sum of all class probabilities equals 1.0. This allows the highest-probability class to be identified via $\text{argmax}$ and interpreted as the model's confidence score.

### Q10: Why did SignBridge adopt GlobalAveragePooling2D instead of a Flatten layer before the dense classifier?
**Answer:** A conventional `Flatten` layer vectorizes the feature map $(H \times W \times C)$ into a massive 1D vector. For example, flattening an $8 \times 8 \times 128$ tensor yields 8,192 features, requiring millions of weights in the subsequent dense layer, which increases memory consumption and susceptibility to overfitting. `GlobalAveragePooling2D` computes the spatial average of each feature map, outputting a compact 128-dimensional vector (one scalar per filter). This enforces structural correspondence between feature maps and categories while dramatically shrinking parameter count.

### Q11: What is the receptive field of a neuron in a CNN?
**Answer:** The receptive field is the specific spatial subregion of the input image that directly influences the activation of a particular neuron in a deep layer. In initial layers with 3×3 filters, the receptive field is small (3×3 pixels), capturing primitive edges. As feature maps undergo consecutive convolutions and pooling operations, deeper neurons integrate signals over wider areas of the input image, allowing them to detect composite structures such as fingers, palm orientation, and complete hand silhouettes.

### Q12: Why are two consecutive 3×3 convolutions used in each block instead of a single 5×5 convolution?
**Answer:** Stacking two consecutive 3×3 convolutional layers achieves the exact same effective receptive field as a single 5×5 convolution ($3 + (3 - 1) = 5$). However, using two 3×3 layers provides two major benefits:
1. **Fewer parameters**: A single 5×5 filter with $C$ channels has $25C^2$ weights, whereas two 3×3 filters have $2 \times (9C^2) = 18C^2$ weights—a 28% parameter reduction.
2. **Greater non-linearity**: Two layers allow two separate non-linear activation functions (ReLUs) rather than one, increasing representational capacity.

### Q13: What loss function is used in SignBridge, and why was it chosen over Categorical Crossentropy?
**Answer:** SignBridge employs **Sparse Categorical Crossentropy**. Both Categorical Crossentropy and Sparse Categorical Crossentropy compute the exact same mathematical loss:
$$\mathcal{L} = -\sum_{i=1}^{K} y_i \log(\hat{y}_i)$$
However, Categorical Crossentropy requires ground-truth labels to be one-hot encoded vectors of shape `(N, 29)`, which increases memory allocation. Sparse Categorical Crossentropy accepts integer scalar class labels `(N,)` directly, computing index-based negative log likelihood efficiently without generating intermediate sparse one-hot matrices.

### Q14: Explain the Adam optimizer and why it is well-suited for training this model.
**Answer:** Adam (Adaptive Moment Estimation) combines the advantages of AdaGrad (which adapts learning rates to sparse features) and RMSprop (which handles non-stationary objectives). It maintains exponentially decaying moving averages of past gradients (first moment $m_t$, indicating momentum) and past squared gradients (second moment $v_t$, indicating uncentered variance):
$$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}, \quad \theta_{t+1} = \theta_t - \frac{\alpha}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$
Adam provides adaptive per-parameter learning rate scaling, rapid convergence, and robustness to noisy gradients, making it ideal for visual classification tasks.

### Q15: How does backpropagation calculate weight updates in convolutional layers?
**Answer:** Backpropagation applies the mathematical chain rule of calculus to compute the partial derivative of the scalar loss function $\mathcal{L}$ with respect to every trainable kernel weight and bias:
$$\frac{\partial \mathcal{L}}{\partial W_{i,j}} = \sum_{x}\sum_{y} \frac{\partial \mathcal{L}}{\partial z_{x,y}} \cdot a_{x+i, y+j}$$
where $z$ is the linear activation and $a$ is the input from the preceding layer. The optimizer then adjusts weights in the direction of steepest descent: $W \leftarrow W - \alpha \frac{\partial \mathcal{L}}{\partial W}$.

---

## 3. Computer Vision & OpenCV

### Q16: What color space does OpenCV use by default, and why is color conversion necessary before feeding images to the CNN?
**Answer:** OpenCV decodes image files into NumPy arrays using the **BGR** (Blue-Green-Red) color channel ordering by default. However, Matplotlib, PIL, and standard web technologies (HTML canvas, CSS, JPEG/PNG decoders) expect **RGB** (Red-Green-Blue) ordering. If an image is processed in BGR without conversion, the red and blue channels are inverted. Because neural networks learn color-specific distribution weights during training on RGB data, failing to convert BGR to RGB via `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` causes massive feature degradation during inference.

### Q17: Which interpolation algorithm is used for image downscaling in SignBridge, and why?
**Answer:** SignBridge specifies `cv2.INTER_AREA` for downscaling images from 200×200 (or webcam resolution 640×480) down to the model input dimensions of 64×64. Unlike `INTER_NEAREST` (which introduces severe aliasing and jagged edges) or `INTER_LINEAR` / `INTER_CUBIC` (which sample discrete pixel coordinates and can produce moiré patterns when downsampling), `INTER_AREA` resamples pixels using pixel area relation, computing weighted averages over pixel neighborhoods. This preserves continuous edge structures and suppresses high-frequency noise.

### Q18: How does SignBridge handle webcam video frame extraction?
**Answer:** In the browser-based live recognition interface, the client accesses the webcam using the HTML5 `navigator.mediaDevices.getUserMedia()` API. Video frames are rendered onto an offscreen `<canvas>` element at 1500 ms intervals. The canvas converts the image into a compressed Base64 JPEG data URL (`canvas.toDataURL('image/jpeg', 0.8)`), which is transmitted asynchronously via HTTP POST `fetch()` to `/api/predict`. This client-side sampling prevents flooding the server with continuous 30 FPS streams.

### Q19: What computer vision challenges exist in recognizing ASL signs from an unconstrained webcam?
**Answer:** Key computer vision challenges include:
1. **Variable illumination**: Shadows, underexposure, or backlighting alter color distributions and hand boundary contrast.
2. **Complex background clutter**: Background objects matching human skin tones create false-positive contour activations.
3. **Scale and distance variation**: Hands positioned closer to or further from the camera exhibit different pixel area sizes.
4. **Motion blur**: Rapid hand transitions between signs cause blurred boundaries.
5. **Morphological diversity**: Variations in finger proportions, skin tones, and subtle articulation angles across different users.

### Q20: How does OpenCV handle video decoding in the optional video upload endpoint?
**Answer:** The `/api/predict-video` endpoint accepts uploaded video files (`.mp4`, `.avi`, `.webm`), validates their file size and container integrity, and opens them using `cv2.VideoCapture(temp_path)`. The video's frame rate ($\text{FPS}$) and frame count are extracted to enforce maximum duration constraints (30 seconds). Frames are extracted at discrete intervals (every 0.5 seconds), preprocessed through the standard inference pipeline, and analyzed sequentially.

### Q21: What is the difference between image classification and object detection?
**Answer:** Image classification assigns a single categorical label to an entire image (e.g., "This image represents sign 'A'"). Object detection (e.g., YOLO, SSD) simultaneously solves two problems: localization (predicting bounding box coordinates $[x, y, w, h]$ around one or more objects) and classification of each detected region. SignBridge utilizes image classification under the assumption that the user's hand occupies the primary central focus of the frame.

---

## 4. Image Preprocessing & Data Augmentation

### Q22: What preprocessing steps are applied to an image before it reaches the CNN?
**Answer:** The SignBridge preprocessing pipeline (`src/preprocessing.py`) executes five deterministic steps:
1. **Format decoding**: Decodes raw bytes, PIL images, or file paths into a NumPy array.
2. **Channel standardization**: Converts grayscale (`shape[2]==1`) or RGBA (`shape[2]==4`) to 3-channel RGB.
3. **Spatial resizing**: Standardizes dimensions to $64 \times 64$ pixels using `cv2.INTER_AREA`.
4. **Normalization**: Scales integer pixel values in $[0, 255]$ by dividing by $255.0$, producing float32 values in $[0.0, 1.0]$.
5. **Batch dimension expansion**: Adds a leading axis via `np.expand_dims(img, axis=0)` to convert shape `(64, 64, 3)` to `(1, 64, 64, 3)`.

### Q23: Why is pixel normalization to $[0.0, 1.0]$ mathematically necessary?
**Answer:** Raw pixel values range from 0 to 255. Feeding large input magnitudes into a neural network with randomly initialized small weights causes unnormalized intermediate activations to explode. This leads to large gradients that destabilize backpropagation, causing erratic weight oscillations or saturated activations where gradients vanish. Normalizing to $[0.0, 1.0]$ centers feature variances, standardizes condition numbers of the Hessian matrix, and enables smooth, stable gradient descent convergence.

### Q24: What is data augmentation, and which augmentation techniques are implemented in SignBridge?
**Answer:** Data augmentation is a regularization technique that synthetically expands the diversity of training data by applying label-preserving transformations to images during training. SignBridge implements Keras preprocessing layers:
- `RandomRotation(0.1)`: Rotates images up to $\pm 10\%$ ($\pm 36^\circ$), simulating natural hand orientation tilt.
- `RandomZoom(0.1)`: Zooms in/out by up to $10\%$, simulating varying distances from the camera.
- `RandomBrightness(0.1)`: Adjusts luminance by up to $\pm 10\%$, simulating differing ambient lighting.
- `RandomFlip("horizontal")`: Simulates opposite-hand orientation (used judiciously).

### Q25: Why must horizontal flipping be handled with caution in American Sign Language datasets?
**Answer:** In ASL, certain signs are asymmetrical and lateral-specific. While some static alphabet letters retain their identity when executed with the left versus right hand, horizontal flipping can invert directional finger orientation. In real-world multi-sign datasets, flipping can inadvertently transform one sign into another or produce anatomically unnatural poses. For alphabet recognition, left-hand vs. right-hand signing requires careful consideration.

### Q26: Why must the exact same preprocessing pipeline be applied to both training and inference data?
**Answer:** Supervised machine learning algorithms operate under the fundamental assumption that training data and production inference data are independent and identically distributed ($\text{i.i.d.}$). If the training data was normalized to $[0.0, 1.0]$ while inference inputs are passed as raw $[0, 255]$ integers, the model receives inputs that are orders of magnitude outside the activation distributions it learned, causing completely invalid predictions.

### Q27: How does SignBridge validate incoming image files for security and integrity?
**Answer:** The `validate_image_file()` utility in `src/preprocessing.py` performs rigorous multi-layer validation:
1. **Filename & extension check**: Verifies presence of allowed extensions (`.jpg`, `.jpeg`, `.png`, `.webp`).
2. **Payload size check**: Rejects empty files ($0$ bytes) and enforces a 10 MB maximum upload ceiling to prevent denial-of-service memory exhaustion.
3. **Header & bitstream verification**: Loads image bytes using PIL's `Image.open(io.BytesIO(content))` and calls `img.verify()`. This confirms valid image headers and decodable data, preventing corrupted files or polyglot exploit payloads from crashing OpenCV decoders.

---

## 5. Dataset Splitting & Validation Methodology

### Q28: How is the dataset split, and what are the specific proportions used in SignBridge?
**Answer:** The dataset is split using a three-way partition:
1. **Test set (10%)**: Held out completely before training begins; never seen by the model or hyperparameter tuning.
2. **Validation set (20% of remaining data, ~18% overall)**: Evaluated at the end of each epoch to monitor generalization and trigger early stopping.
3. **Training set (~72% overall)**: Used by gradient descent to update convolutional and dense weights.

### Q29: What is stratified splitting, and why is it essential for multi-class sign language datasets?
**Answer:** Stratified sampling (`stratify=labels` in `train_test_split`) ensures that the relative frequency distribution of every target class in each split mirrors the exact class proportions of the overall dataset. Because SignBridge classifies 29 distinct categories, random non-stratified partitioning could inadvertently underrepresent minority or difficult classes in the validation or test sets, skewing metric reliability.

### Q30: Why is a separate test set required in addition to a validation set?
**Answer:** While the validation set is not used directly for backpropagation weight updates, it is used by engineers to select hyperparameters (learning rate, layer depth, dropout rates) and by callbacks (`EarlyStopping`, `ReduceLROnPlateau`) to pick the best epoch checkpoint. Consequently, subtle optimistic bias (validation data leakage) leaks into the validation evaluation. The completely isolated test set provides an unbiased, objective evaluation of real-world generalization performance.

### Q31: How are dynamic signs like 'J' and 'Z' handled in the dataset, and what are the academic implications?
**Answer:** In genuine ASL, 'J' involves tracing a J-curve in the air using the pinky finger, and 'Z' involves tracing a Z-path with the index finger. The Kaggle ASL Alphabet dataset captures these dynamic signs as still 2D photographs of the concluding or characteristic hand posture. Academically, static 2D image classification cannot model temporal trajectory or kinematic velocity. SignBridge transparently flags these signs with `is_dynamic=True` and surfaces an explanatory note to users rather than claiming full dynamic translation.

---

## 6. Overfitting, Regularization & Optimization

### Q32: What is overfitting, and what symptoms indicate that a CNN is overfitting?
**Answer:** Overfitting occurs when a neural network learns statistical noise, idiosyncrasies, and specific background artifacts in the training dataset rather than true invariant sign features. Symptoms include:
- Training loss continues to decrease monotonically while validation loss plateaus and begins increasing.
- Training accuracy approaches near-perfect levels (e.g., 99%) while validation accuracy remains stagnant at significantly lower levels (e.g., 82%).
- High variance when tested on new real-world images from unseen users.

### Q33: How does Dropout mitigate overfitting in deep neural networks?
**Answer:** Dropout randomly deactivates a predefined fraction $p$ (e.g., $p=0.25$ in conv blocks, $p=0.5$ in dense classifier) of neuron activations during each forward training pass, setting their values to zero. This prevents co-adaptation—a phenomenon where neurons rely excessively on the presence of specific other neurons to correct their errors. Instead, each neuron must learn robust, redundant features. At inference time, Dropout is disabled, and activations are scaled by $(1-p)$ to compute an ensemble prediction.

### Q34: What is Batch Normalization, and how does it stabilize training?
**Answer:** Batch Normalization normalizes the activations of an intermediate layer across the current minibatch to have zero mean and unit variance, followed by learnable scale ($\gamma$) and shift ($\beta$) parameters:
$$\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}, \quad y_i = \gamma \hat{x}_i + \beta$$
Batch Normalization mitigates internal covariate shift (the continuous drift in layer input distributions as upstream weights change), allows significantly higher learning rates, acts as a mild regularizer, and prevents activation values from collapsing into saturated regions.

### Q35: How does the `EarlyStopping` callback work in SignBridge?
**Answer:** `EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)` tracks the validation loss after each training epoch. If validation loss fails to improve for 5 consecutive epochs (the patience parameter), training halts prematurely. Crucially, `restore_best_weights=True` rewinds the model weights back to the epoch that achieved the absolute minimum validation loss, discarding overfitted weights from subsequent epochs.

### Q36: What is the purpose of the `ReduceLROnPlateau` callback?
**Answer:** During initial epochs, a relatively large learning rate ($\alpha = 0.001$) is desirable for rapid traversal of the loss landscape. However, as the model approaches a local minimum, large gradient steps can overshoot the minimum and oscillate. `ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6)` automatically cuts the learning rate in half whenever validation loss plateaus for 3 epochs, enabling fine-grained weight convergence into deeper loss valleys.

---

## 7. Model Evaluation & Classification Metrics

### Q37: Define Precision, Recall, and F1-score in the context of ASL sign recognition.
**Answer:**
- **Precision**: Out of all images the model predicted as sign 'A', what proportion were actually sign 'A'?
  $$\text{Precision} = \frac{TP}{TP + FP}$$
- **Recall (Sensitivity)**: Out of all actual instances of sign 'A' in the dataset, what proportion did the model correctly identify?
  $$\text{Recall} = \frac{TP}{TP + FN}$$
- **F1-Score**: The harmonic mean of precision and recall, balancing false positives and false negatives:
  $$\text{F1} = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

### Q38: Why is accuracy alone insufficient for evaluating a multi-class model?
**Answer:** Overall accuracy simply measures total correct predictions divided by total samples. If a dataset has class imbalances, a naive model can achieve deceptive overall accuracy while completely failing on difficult or underrepresented categories. Furthermore, accuracy treats all misclassifications uniformly, masking whether errors are concentrated among specific confusing class pairs (such as visually similar hand shapes like 'M', 'N', and 'S').

### Q39: What is a Confusion Matrix, and what insights does it provide for SignBridge?
**Answer:** A Confusion Matrix is an $N \times N$ matrix (where $N=29$) where rows represent ground-truth classes and columns represent model-predicted classes. Diagonal cells represent correct classifications ($TP$), while off-diagonal cells indicate specific pairwise confusions ($FP$ and $FN$). In SignBridge, the confusion matrix reveals morphological ambiguities—for instance, whether closed-fist signs with subtle thumb variations ('A', 'E', 'S', 'T') or two-finger upright signs ('U', 'V', 'K', 'R') are frequently misclassified as one another.

### Q40: What is weighted averaging versus macro averaging in scikit-learn's classification report?
**Answer:**
- **Macro Average**: Computes the metric (precision, recall, F1) independently for each of the 29 classes and takes the unweighted arithmetic mean. This treats all classes equally, highlighting poor performance on minority classes.
- **Weighted Average**: Computes the metric for each class and weights the average by the support (number of true instances) of each class. This reflects overall dataset performance proportional to class prevalence.

### Q41: How does SignBridge implement confidence scoring and threshold-based warnings?
**Answer:** When the CNN executes a forward pass, the Softmax layer outputs 29 class probabilities. The highest probability value ($\max P$) represents the model's prediction confidence. In `src/predictor.py`:
- If $\text{confidence} \ge 0.70$: Classified as high-confidence; rendered with a green progress bar.
- If $0.50 \le \text{confidence} < 0.70$: Classified as moderate confidence; rendered in yellow with a caution warning.
- If $\text{confidence} < 0.50$: Classified as low-confidence (`is_confident = False`); displays an alert advising the user to reposition their hand or improve lighting.

---

## 8. Flask Backend & RESTful Architecture

### Q42: What is the architectural role of Flask in SignBridge?
**Answer:** Flask serves as the lightweight WSGI web backend, decoupling the browser client from machine learning execution. Its responsibilities include:
1. Serving static frontend assets (HTML, CSS, JS, Bootstrap icons).
2. Exposing RESTful API endpoints (`/api/predict`, `/api/predict-video`, `/api/health`, `/api/dictionary`).
3. Managing upload security, payload size enforcement, and temporary file lifecycle.
4. Marshalling between web formats (Base64 data URLs, multipart forms) and NumPy/TensorFlow tensor representations.
5. Formatting model predictions, top-5 candidates, and dictionary descriptions into consistent JSON responses.

### Q43: How does the `/api/predict` endpoint handle dual-mode input (file upload vs. webcam Base64)?
**Answer:** The endpoint inspects the incoming HTTP request headers:
- If `request.is_json` is true, it extracts the `image` key containing a Base64-encoded string from the webcam canvas, strips the `data:image/jpeg;base64,` prefix, and decodes the payload into raw bytes via `base64.b64decode()`.
- If `multipart/form-data` is detected, it accesses `request.files['image']`, validates the file wrapper using `validate_image_file()`, and reads the byte stream directly.
Both branches feed identical byte streams into `predictor.predict(image_bytes)`, ensuring a single unified inference code path.

### Q44: What HTTP status codes are used across the SignBridge API and why?
**Answer:**
- `200 OK`: Request succeeded, prediction JSON payload returned.
- `400 Bad Request`: Client error (missing file, invalid image format, corrupt bitstream, unparsable JSON).
- `404 Not Found`: Requested endpoint or asset does not exist.
- `413 Payload Too Large`: Uploaded file exceeds the 10 MB limit (`MAX_CONTENT_LENGTH`).
- `500 Internal Server Error`: Unhandled server-side exception (sanitized to avoid leaking local paths).
- `503 Service Unavailable`: Model is not loaded or weights are missing from disk.

### Q45: How are temporary video files safely managed during video prediction?
**Answer:** When a video is uploaded to `/api/predict-video`, Flask saves it to the `uploads/` directory with a cryptographically unique identifier (`uuid.uuid4().hex + ".mp4"`) to prevent filename collisions or directory traversal exploits. The frame extraction and prediction logic executes inside a `try...finally` block. In the `finally` clause, `os.path.exists()` checks for the temporary video file and removes it via `os.remove()`, ensuring no lingering video files accumulate on server disk storage.

---

## 9. Real-Time Webcam & Frontend Integration

### Q46: How does SignBridge implement prediction stabilization (temporal smoothing) in the webcam feed?
**Answer:** Continuous webcam recognition can produce flickering predictions if individual frames fluctuate due to noise or transitional hand movements. In `static/js/app.js`, SignBridge implements a consecutive-frame stability counter:
```javascript
if (data.label === state.lastCameraLabel) {
    state.stableCount++;
} else {
    state.lastCameraLabel = data.label;
    state.stableCount = 1;
}
if (state.stableCount === state.stabilityThreshold && data.is_confident) {
    addDetection(data);
}
```
A sign is only committed to the detection history and auto-added to text if the model predicts the exact same label across multiple consecutive samples with sufficient confidence.

### Q47: How is the Web Speech API integrated for English text-to-speech synthesis?
**Answer:** SignBridge leverages the browser's native `window.speechSynthesis` interface, eliminating any reliance on external or paid cloud APIs. When the user clicks "Speak Text":
1. Any active speech is canceled via `window.speechSynthesis.cancel()`.
2. A new `SpeechSynthesisUtterance(text)` object is instantiated with properties `lang = 'en-US'`, `rate = 0.9`, and `pitch = 1.0`.
3. Event listeners on `onstart` and `onend` toggle the play/stop UI buttons.
4. The utterance is spoken using `window.speechSynthesis.speak(utterance)`.

### Q48: What are the ethical and practical limitations of SignBridge that should be discussed in a viva examination?
**Answer:** Candidates should emphasize three fundamental truths:
1. **Fingerspelling vs. Natural Sign Language**: SignBridge recognizes the manual ASL alphabet (fingerspelling). Fingerspelling represents less than 10% of natural ASL discourse, which relies on lexical signs, facial expressions, body posture, and non-manual grammatical markers.
2. **Grammar gap**: Sequentially concatenating recognized letters produces English words, not grammatically structured ASL (which possesses its own topic-comment syntax and spatial morphology).
3. **Safety boundary**: SignBridge is an educational and technological demonstration of computer vision. It is **not** a certified communication tool and must never be deployed as an autonomous substitute for certified human ASL interpreters in medical, legal, educational, or emergency environments.
