import streamlit as st
import requests
from PIL import Image
import base64
import os
import json
from datetime import datetime
import io

# === PAGE CONFIG ===
st.set_page_config(
    page_title="Tree Species Classifier",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === ENHANCED CUSTOM CSS FOR MOBILE RESPONSIVENESS ===
st.markdown("""
<style>
    .main {
        padding: 0.5rem;
    }
    
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .header-container {
        background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
        color: white;
    }
    
    .header-container h1 {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .header-container p {
        margin: 0.5rem 0;
    }
    
    .result-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #2E8B57;
        word-wrap: break-word;
    }
    
    .result-card h3 {
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        line-height: 1.3;
        color: #2E8B57;
    }
    
    .result-card p {
        margin: 0.5rem 0;
        line-height: 1.4;
        font-size: 0.9rem;
    }
    
    .result-card ul {
        margin: 0.5rem 0;
        padding-left: 1.2rem;
    }
    
    .result-card li {
        margin: 0.3rem 0;
        font-size: 0.9rem;
        line-height: 1.3;
    }
    
    .confidence-high {
        color: #2E8B57;
        font-weight: bold;
        font-size: 1rem;
    }
    
    .confidence-medium {
        color: #FFA500;
        font-weight: bold;
        font-size: 1rem;
    }
    
    .confidence-low {
        color: #FF6B6B;
        font-weight: bold;
        font-size: 1rem;
    }
    
    .footer {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 2rem;
        text-align: center;
        border-top: 3px solid #2E8B57;
    }
    
    .developer-info {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    
    .social-link {
        background: #2E8B57;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-decoration: none;
        font-size: 0.8rem;
        transition: background 0.3s;
        display: inline-block;
    }
    
    .social-link:hover {
        background: #228B22;
        color: white;
    }
    
    .camera-section {
        background: #f0f8f0;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #4CAF50;
        text-align: center;
    }
    
    .camera-button {
        background: #4CAF50;
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-size: 1rem;
        cursor: pointer;
        margin: 0.5rem;
        transition: background 0.3s;
    }
    
    .camera-button:hover {
        background: #45a049;
    }
    
    .tab-button {
        background: #e8f5e8;
        color: #2E8B57;
        border: 2px solid #2E8B57;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 0.2rem;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.3s;
    }
    
    .tab-button.active {
        background: #2E8B57;
        color: white;
    }
    
    .tab-button:hover {
        background: #2E8B57;
        color: white;
    }
    
    .info-box {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #2E8B57;
        font-size: 0.9rem;
    }
    
    .error-box {
        background: #ffebee;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #f44336;
        color: #c62828;
    }
    
    .warning-box {
        background: #fff3e0;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #ff9800;
        color: #e65100;
    }
    
    .species-name {
        font-weight: bold;
        color: #2E8B57;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .common-names {
        font-style: italic;
        color: #666;
        margin-bottom: 0.5rem;
    }
    
    /* Mobile-specific styles */
    @media (max-width: 768px) {
        .main {
            padding: 0.3rem;
        }
        
        .header-container {
            padding: 1rem;
        }
        
        .header-container h1 {
            font-size: 1.5rem;
        }
        
        .header-container p {
            font-size: 0.9rem;
        }
        
        .result-card {
            padding: 0.8rem;
            margin: 0.5rem 0;
        }
        
        .result-card h3 {
            font-size: 1rem;
        }
        
        .result-card p, .result-card li {
            font-size: 0.8rem;
        }
        
        .developer-info {
            flex-direction: column;
            align-items: center;
        }
        
        .social-link {
            width: 150px;
            text-align: center;
            font-size: 0.8rem;
            padding: 0.4rem 0.8rem;
        }
        
        .camera-section {
            padding: 0.8rem;
        }
        
        .camera-button {
            width: 100%;
            padding: 0.6rem 1rem;
            font-size: 0.9rem;
        }
        
        .tab-button {
            width: 48%;
            margin: 0.1rem;
            padding: 0.4rem 0.8rem;
            font-size: 0.8rem;
        }
        
        .info-box {
            padding: 0.8rem;
            font-size: 0.8rem;
        }
        
        /* Fix for Streamlit columns on mobile */
        .element-container {
            width: 100% !important;
        }
        
        /* Better spacing for mobile */
        .stButton > button {
            width: 100%;
            margin: 0.5rem 0;
        }
        
        /* Sidebar adjustments */
        .sidebar .sidebar-content {
            padding: 1rem 0.5rem;
        }
    }
    
    /* Extra small devices */
    @media (max-width: 480px) {
        .header-container h1 {
            font-size: 1.3rem;
        }
        
        .result-card h3 {
            font-size: 0.9rem;
        }
        
        .result-card p, .result-card li {
            font-size: 0.75rem;
        }
        
        .confidence-high, .confidence-medium, .confidence-low {
            font-size: 0.9rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# === ENHANCED ERROR HANDLING FOR API KEY ===
@st.cache_data
def load_api_key():
    """Load API key with better error handling"""
    try:
        if hasattr(st, 'secrets') and "plantnet" in st.secrets and "api_key" in st.secrets["plantnet"]:
            return st.secrets["plantnet"]["api_key"]
        else:
            st.error("⚠️ API key not found in secrets. Please configure your PlantNet API key in secrets.toml")
            st.markdown("""
            <div class="error-box">
                <strong>Configuration Required:</strong><br>
                1. Create a secrets.toml file in your project root<br>
                2. Add your PlantNet API key:<br>
                <code>[plantnet]<br>api_key = "your_api_key_here"</code>
            </div>
            """, unsafe_allow_html=True)
            st.stop()
    except Exception as e:
        st.error(f"❌ Error loading API key: {str(e)}")
        st.stop()

# Try to load API key
try:
    API_KEY = load_api_key()
    API_URL = "https://my-api.plantnet.org/v2/identify/all"
except:
    st.error("⚠️ Unable to initialize the application. Please check your configuration.")
    st.stop()

# === HEADER ===
st.markdown("""
<div class="header-container">
    <h1>🌿 Tree Species Classification</h1>
    <p>AI-powered tool for identifying trees and plants</p>
    <p>Upload clear images of leaves, flowers, or bark for accurate species identification</p>
</div>
""", unsafe_allow_html=True)

# === SIDEBAR ===
with st.sidebar:
    st.header("📋 Instructions")
    st.markdown("""
    **For best results:**
    - 📸 Use clear, well-lit photos
    - 🍃 Focus on leaves, flowers, or bark
    - 📏 Capture details up close
    - 🌅 Avoid shadows and blur
    - 📱 Multiple angles help accuracy
    """)
    
    st.header("📷 Camera Tips")
    st.markdown("""
    **When using camera:**
    - 🎯 Hold steady and focus
    - 💡 Ensure good lighting
    - 🔍 Get close to the plant
    - 📐 Keep the subject centered
    - 🚫 Avoid moving while capturing
    """)
    
    st.header("🔧 Settings")
    max_results = st.slider("Max Results", 1, 10, 5)
    show_details = st.checkbox("Show Detailed Info", True)

# === MAIN CONTENT ===
# Create tabs for different input methods
st.markdown("""
<div style="text-align: center; margin: 1rem 0;">
    <h3>🎯 Choose Your Input Method</h3>
</div>
""", unsafe_allow_html=True)

# Create input method selection
input_method = st.radio(
    "Select how you want to provide images:",
    ["📤 Upload Images", "📷 Take Real-time Photos"],
    horizontal=True,
    label_visibility="collapsed"
)

if input_method == "📤 Upload Images":
    # Original upload functionality
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.subheader("📤 Upload Images")
        
        image1 = st.file_uploader(
            "Primary Image (Required)", 
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of the plant part you want to identify",
            key="upload_primary"
        )
        
        if image1:
            st.image(image1, caption="Primary Image", use_column_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.subheader("📤 Additional Image")
        
        image2 = st.file_uploader(
            "Secondary Image (Optional)", 
            type=["jpg", "jpeg", "png"],
            help="Upload another angle or part of the same plant for better accuracy",
            key="upload_secondary"
        )
        
        if image2:
            st.image(image2, caption="Secondary Image", use_column_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

else:  # Camera mode
    # Real-time camera functionality
    st.markdown("""
    <div class="info-box">
        <strong>📷 Camera Mode:</strong> Take real-time photos using your device's camera. 
        Make sure to allow camera permissions when prompted.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="camera-section">', unsafe_allow_html=True)
        st.subheader("📷 Primary Photo")
        
        camera_image1 = st.camera_input(
            "Take a primary photo of the plant",
            help="Point your camera at the plant and click to capture",
            key="camera_primary"
        )
        
        if camera_image1:
            st.image(camera_image1, caption="Primary Photo", use_column_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="camera-section">', unsafe_allow_html=True)
        st.subheader("📷 Additional Photo")
        
        camera_image2 = st.camera_input(
            "Take an additional photo (optional)",
            help="Capture another angle or part of the same plant",
            key="camera_secondary"
        )
        
        if camera_image2:
            st.image(camera_image2, caption="Additional Photo", use_column_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Set images based on camera input
    image1 = camera_image1
    image2 = camera_image2

# === INFO BOX ===
if input_method == "📤 Upload Images":
    st.markdown("""
    <div class="info-box">
        <strong>💡 Pro Tip:</strong> For best identification results, upload images of different plant parts 
        (leaves, flowers, bark, fruit) from the same plant. This helps the AI make more accurate predictions.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="info-box">
        <strong>📸 Camera Tips:</strong> 
        • Hold your device steady while taking photos<br>
        • Ensure good lighting for clear images<br>
        • Get close to the plant for detailed shots<br>
        • Take photos of different parts (leaves, flowers, bark) for better accuracy
    </div>
    """, unsafe_allow_html=True)

# === ENHANCED CLASSIFICATION LOGIC ===
if image1:
    if st.button("🔍 Identify Plant Species", type="primary", use_container_width=True):
        
        def process_image(uploaded_file, filename):
            """Process and save uploaded image with error handling"""
            try:
                # Handle both uploaded files and camera input
                if hasattr(uploaded_file, 'read'):
                    # For camera input or file upload
                    image_data = uploaded_file.read()
                    img = Image.open(io.BytesIO(image_data))
                else:
                    # For regular file uploads
                    img = Image.open(uploaded_file)
                
                # Handle different image modes
                if img.mode in ("RGBA", "P"):
                    # Create a white background for transparency
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode == "RGBA":
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background
                
                # Resize large images for better API performance
                max_size = 1024
                if img.size[0] > max_size or img.size[1] > max_size:
                    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                # Save with optimization
                img.save(filename, format="JPEG", quality=85, optimize=True)
                return open(filename, "rb")
                
            except Exception as e:
                st.error(f"❌ Error processing image: {str(e)}")
                return None
        
        def get_confidence_class(score):
            """Get confidence level class for styling"""
            if score >= 70:
                return "confidence-high"
            elif score >= 40:
                return "confidence-medium"
            else:
                return "confidence-low"
        
        def format_confidence(score):
            """Format confidence score with emoji"""
            if score >= 70:
                return f"🟢 {score:.1f}% (High Confidence)"
            elif score >= 40:
                return f"🟡 {score:.1f}% (Medium Confidence)"
            else:
                return f"🔴 {score:.1f}% (Low Confidence)"
        
        def safe_get(dictionary, key, default="Not available"):
            """Safely get value from dictionary with fallback"""
            try:
                value = dictionary.get(key, default)
                return value if value else default
            except:
                return default
        
        # Create images directory with error handling
        try:
            os.makedirs("images", exist_ok=True)
        except Exception as e:
            st.error(f"❌ Error creating images directory: {str(e)}")
            st.stop()
        
        # Process images
        try:
            file1 = process_image(image1, "images/img1.jpg")
            if file1 is None:
                st.error("❌ Failed to process the primary image. Please try a different image.")
                st.stop()
                
            files = [("images", ("img1.jpg", file1, "image/jpeg"))]
            
            file2 = None
            if image2:
                file2 = process_image(image2, "images/img2.jpg")
                if file2 is not None:
                    files.append(("images", ("img2.jpg", file2, "image/jpeg")))
                else:
                    st.warning("⚠️ Secondary image could not be processed. Continuing with primary image only.")
            
            params = {"api-key": API_KEY}
            
            with st.spinner("🔍 Analyzing images with AI... This may take a few moments"):
                # Show different messages based on input method
                if input_method == "📷 Take Real-time Photos":
                    st.info("📸 Processing your camera photos...")
                else:
                    st.info("📤 Processing your uploaded images...")
                    
                try:
                    response = requests.post(
                        API_URL, 
                        files=files, 
                        params=params, 
                        timeout=45  # Increased timeout
                    )
                    
                    if response.status_code == 200:
                        try:
                            result = response.json()
                            results = result.get("results", [])
                            
                            if results and len(results) > 0:
                                st.success("✅ Classification Complete!")
                                
                                # Display results with enhanced formatting
                                st.subheader(f"🌱 Top {min(len(results), max_results)} Results:")
                                
                                for i, r in enumerate(results[:max_results]):
                                    try:
                                        species = r.get("species", {})
                                        score = round(r.get("score", 0) * 100, 2)
                                        
                                        # Safely extract species information
                                        scientific_name = safe_get(species, "scientificNameWithoutAuthor", "Unknown Species")
                                        common_names = species.get("commonNames", [])
                                        family_info = species.get("family", {})
                                        genus_info = species.get("genus", {})
                                        
                                        family_name = safe_get(family_info, "scientificNameWithoutAuthor", "Unknown Family")
                                        genus_name = safe_get(genus_info, "scientificNameWithoutAuthor", "Unknown Genus")
                                        
                                        confidence_class = get_confidence_class(score)
                                        
                                        # Format common names
                                        common_names_str = "Not available"
                                        if common_names and len(common_names) > 0:
                                            # Take first 3 common names
                                            common_names_str = ', '.join(common_names[:3])
                                        
                                        st.markdown(f"""
                                        <div class="result-card">
                                            <h3>#{i+1} {scientific_name}</h3>
                                            <p class="{confidence_class}">
                                                {format_confidence(score)}
                                            </p>
                                            <div class="common-names">
                                                <strong>🏷️ Common Names:</strong> {common_names_str}
                                            </div>
                                            <p><strong>👨‍🔬 Scientific Classification:</strong></p>
                                            <ul>
                                                <li><strong>Family:</strong> {family_name}</li>
                                                <li><strong>Genus:</strong> {genus_name}</li>
                                                <li><strong>Species:</strong> {scientific_name}</li>
                                            </ul>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        
                                    except Exception as e:
                                        st.error(f"❌ Error processing result #{i+1}: {str(e)}")
                                        continue
                                
                                # Show additional info if enabled
                                if show_details and len(results) > 0:
                                    st.subheader("📊 Analysis Summary")
                                    
                                    try:
                                        col1, col2, col3 = st.columns(3)
                                        
                                        with col1:
                                            st.metric("Total Matches", len(results))
                                        
                                        with col2:
                                            highest_score = max([r.get("score", 0) * 100 for r in results if r.get("score", 0) > 0])
                                            st.metric("Best Match", f"{highest_score:.1f}%")
                                        
                                        with col3:
                                            valid_scores = [r.get("score", 0) * 100 for r in results if r.get("score", 0) > 0]
                                            if valid_scores:
                                                avg_score = sum(valid_scores) / len(valid_scores)
                                                st.metric("Average Confidence", f"{avg_score:.1f}%")
                                            else:
                                                st.metric("Average Confidence", "N/A")
                                        
                                        # Show timestamp
                                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        st.info(f"🕐 Analysis completed at {timestamp}")
                                        
                                    except Exception as e:
                                        st.warning(f"⚠️ Could not generate analysis summary: {str(e)}")
                            
                            else:
                                st.markdown("""
                                <div class="warning-box">
                                    <strong>🤔 No species matches found.</strong><br>
                                    This could be due to:<br>
                                    • Image quality issues<br>
                                    • Unusual plant species<br>
                                    • Unclear plant parts<br><br>
                                    Try uploading clearer images or different plant parts.
                                </div>
                                """, unsafe_allow_html=True)
                                
                        except json.JSONDecodeError:
                            st.error("❌ Invalid response from API. Please try again.")
                        except Exception as e:
                            st.error(f"❌ Error processing API response: {str(e)}")
                    
                    elif response.status_code == 401:
                        st.error("🔑 Invalid API key. Please check your PlantNet API key configuration.")
                    elif response.status_code == 429:
                        st.error("⏱️ API rate limit exceeded. Please wait a moment before trying again.")
                    elif response.status_code == 413:
                        st.error("📸 Image file too large. Please use smaller images (max 5MB).")
                    else:
                        st.error(f"❌ API Error {response.status_code}: {response.text}")
                        
                except requests.exceptions.Timeout:
                    st.error("⏱️ Request timeout. The API is taking too long to respond. Please try again.")
                except requests.exceptions.ConnectionError:
                    st.error("🌐 Connection error. Please check your internet connection and try again.")
                except requests.exceptions.RequestException as e:
                    st.error(f"🌐 Network error: {str(e)}")
                except Exception as e:
                    st.error(f"💥 Unexpected error during API call: {str(e)}")
                    
        except Exception as e:
            st.error(f"💥 Error during image processing: {str(e)}")
            
        finally:
            # Clean up files safely
            try:
                if 'file1' in locals() and file1:
                    file1.close()
                if 'file2' in locals() and file2:
                    file2.close()
                    
                # Remove temporary files
                for filename in ["images/img1.jpg", "images/img2.jpg"]:
                    if os.path.exists(filename):
                        os.remove(filename)
                        
            except Exception as e:
                # Silent cleanup - don't bother user with cleanup errors
                pass

else:
    # Show different messages based on input method
    if input_method == "📷 Take Real-time Photos":
        st.info("📸 Please take at least one photo using your camera to start the identification process.")
    else:
        st.info("👆 Please upload at least one image to start the identification process.")

# === FOOTER ===
st.markdown("""
<div class="footer">
    <h3>👨‍💻 Developed by Deepak Singh</h3>
    <p>Full Stack Developer & AI Enthusiast</p>
    <div class="developer-info">
        <a href="https://www.linkedin.com/in/deepaksinghai" target="_blank" class="social-link">
            💼 LinkedIn
        </a>
        <a href="https://github.com/CodeWithDks" target="_blank" class="social-link">
            🐙 GitHub
        </a>
        <a href="https://relaxed-trifle-359674.netlify.app" target="_blank" class="social-link">
            🌐 Portfolio
        </a>
    </div>
    <p style="margin-top: 1rem; color: #666; font-size: 0.8rem;">
        🌿 Powered by advanced AI and image recognition | Built with Streamlit
    </p>
</div>
""", unsafe_allow_html=True)