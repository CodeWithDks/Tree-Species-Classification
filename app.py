import streamlit as st
import requests
from PIL import Image
import base64
import os
import json
from datetime import datetime

# === PAGE CONFIG ===
st.set_page_config(
    page_title="Tree Species Classifier",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === CUSTOM CSS FOR RESPONSIVE DESIGN ===
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .header-container {
        background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #2E8B57;
    }
    
    .confidence-high {
        color: #2E8B57;
        font-weight: bold;
    }
    
    .confidence-medium {
        color: #FFA500;
        font-weight: bold;
    }
    
    .confidence-low {
        color: #FF6B6B;
        font-weight: bold;
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
        gap: 1rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    
    .social-link {
        background: #2E8B57;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-decoration: none;
        font-size: 0.9rem;
        transition: background 0.3s;
    }
    
    .social-link:hover {
        background: #228B22;
        color: white;
    }
    
    .upload-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px dashed #2E8B57;
    }
    
    .info-box {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #2E8B57;
    }
    
    @media (max-width: 768px) {
        .developer-info {
            flex-direction: column;
            align-items: center;
        }
        
        .social-link {
            width: 200px;
            text-align: center;
        }
        
        .header-container {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# === LOAD API KEY FROM SECRETS ===
def load_api_key():
    try:
        return st.secrets["plantnet"]["api_key"]
    except:
        st.error("⚠️ API key not found. Please configure secrets.toml file.")
        st.stop()

API_KEY = load_api_key()
API_URL = "https://my-api.plantnet.org/v2/identify/all"

# === HEADER ===
st.markdown("""
<div class="header-container">
    <h1>🌿 Tree Species Classification</h1>
    <p style="font-size: 1.2rem; margin-top: 1rem;">
        AI-powered tool for identifying trees and plants
    </p>
    <p style="font-size: 1rem; opacity: 0.9;">
        Upload clear images of leaves, flowers, or bark for accurate species identification
    </p>
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
    
    st.header("🔧 Settings")
    max_results = st.slider("Max Results", 1, 10, 5)
    show_details = st.checkbox("Show Detailed Info", True)

# === MAIN CONTENT ===
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.subheader("📤 Upload Images")
    
    image1 = st.file_uploader(
        "Primary Image (Required)", 
        type=["jpg", "jpeg", "png"],
        help="Upload a clear image of the plant part you want to identify"
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
        help="Upload another angle or part of the same plant for better accuracy"
    )
    
    if image2:
        st.image(image2, caption="Secondary Image", use_column_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# === INFO BOX ===
st.markdown("""
<div class="info-box">
    <strong>💡 Pro Tip:</strong> For best identification results, upload images of different plant parts 
    (leaves, flowers, bark, fruit) from the same plant. This helps the AI make more accurate predictions.
</div>
""", unsafe_allow_html=True)

# === CLASSIFICATION BUTTON ===
if image1:
    if st.button("🔍 Identify Plant Species", type="primary", use_container_width=True):
        
        def process_image(uploaded_file, filename):
            """Process and save uploaded image"""
            img = Image.open(uploaded_file)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            # Resize large images for better API performance
            if img.size[0] > 1024 or img.size[1] > 1024:
                img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
            img.save(filename, format="PNG", optimize=True)
            return open(filename, "rb")
        
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
                return f"🟢 {score}% (High Confidence)"
            elif score >= 40:
                return f"🟡 {score}% (Medium Confidence)"
            else:
                return f"🔴 {score}% (Low Confidence)"
        
        # Create images directory
        os.makedirs("images", exist_ok=True)
        
        # Process images
        file1 = process_image(image1, "images/img1.png")
        files = [("images", ("img1.png", file1, "image/png"))]
        
        if image2:
            file2 = process_image(image2, "images/img2.png")
            files.append(("images", ("img2.png", file2, "image/png")))
        
        params = {"api-key": API_KEY}
        
        with st.spinner("🔍 Analyzing images with AI... Please wait"):
            try:
                response = requests.post(API_URL, files=files, params=params, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    results = result.get("results", [])
                    
                    if results:
                        st.success("✅ Classification Complete!")
                        
                        # Display results
                        st.subheader(f"🌱 Top {min(len(results), max_results)} Results:")
                        
                        for i, r in enumerate(results[:max_results]):
                            species = r.get("species", {})
                            name = species.get("scientificNameWithoutAuthor", "Unknown Species")
                            common = species.get("commonNames", [])
                            score = round(r.get("score", 0) * 100, 2)
                            family = species.get("family", {}).get("scientificNameWithoutAuthor", "Unknown Family")
                            genus = species.get("genus", {}).get("scientificNameWithoutAuthor", "Unknown Genus")
                            
                            confidence_class = get_confidence_class(score)
                            
                            st.markdown(f"""
                            <div class="result-card">
                                <h3>#{i+1} {name}</h3>
                                <p class="{confidence_class}">
                                    {format_confidence(score)}
                                </p>
                                <p><strong>🏷️ Common Names:</strong> {', '.join(common[:3]) if common else 'Not available'}</p>
                                <p><strong>👨‍🔬 Scientific Classification:</strong></p>
                                <ul>
                                    <li><strong>Family:</strong> {family}</li>
                                    <li><strong>Genus:</strong> {genus}</li>
                                    <li><strong>Species:</strong> {name}</li>
                                </ul>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Show additional info if enabled
                        if show_details and len(results) > 0:
                            st.subheader("📊 Analysis Summary")
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Total Matches", len(results))
                            
                            with col2:
                                highest_score = max([r.get("score", 0) * 100 for r in results])
                                st.metric("Best Match", f"{highest_score:.1f}%")
                            
                            with col3:
                                avg_score = sum([r.get("score", 0) * 100 for r in results]) / len(results)
                                st.metric("Average Confidence", f"{avg_score:.1f}%")
                            
                            # Show timestamp
                            st.info(f"🕐 Analysis completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    else:
                        st.warning("🤔 No species matches found. Try uploading clearer images or different plant parts.")
                
                else:
                    st.error(f"❌ API Error {response.status_code}: {response.text}")
                    
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timeout. Please try again.")
            except requests.exceptions.RequestException as e:
                st.error(f"🌐 Network error: {str(e)}")
            except Exception as e:
                st.error(f"💥 Unexpected error: {str(e)}")
            finally:
                # Clean up files
                file1.close()
                if image2:
                    file2.close()
                # Remove temporary files
                try:
                    os.remove("images/img1.png")
                    if image2:
                        os.remove("images/img2.png")
                except:
                    pass

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
    <p style="margin-top: 1rem; color: #666; font-size: 0.9rem;">
        🌿 Powered by advanced AI and image recognition | Built with Streamlit
    </p>
</div>
""", unsafe_allow_html=True)