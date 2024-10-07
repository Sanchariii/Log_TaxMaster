import streamlit as st
from PIL import Image
import base64
# Page Configuration
st.set_page_config(page_title="TaxMaster", page_icon=":moneybag:", layout="wide")
# CSS styling with dynamic class application
st.markdown(f"""
<style>
/* Navbar styling */
.header {{
  background-color: #E5E4E2;
  padding: 10px 50px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 30px;
  box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
  position: fixed;
  top: 50px;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  z-index: 999;
}}
.nav {{
  display: flex;
  gap: 30px;
}}
.nav-link {{
  color: #4a4a4a;
  font-weight: 500;
  text-decoration: none;
  font-size: 18px;
}}
.nav-link:hover {{
  color: #BF40BF;
}}
.nav-link.active {{
  color: #BF40BF;
  font-weight: 600;
}}
.nav-link.contacts {{
  text-decoration: underline;
}}
.cta-buttons {{
  display: flex;
  gap: 15px;
}}
.cta-button {{
  padding: 10px 20px;
  border-radius: 25px;
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
}}
.cta-button.signup {{
  background-color: black;
  color: white;
}}
.cta-button.login {{
  background-color: transparent;
  color: black;
}}
body {{
  padding-top: 130px;
}}
.hero {{
  display: flex;
  justify-content: space-between;
  padding: 50px 100px;
}}
.hero-text {{
  max-width: 600px;
}}
.hero-text h1 {{
  font-size: 55px;
  line-height: 1.2;
  font-weight: 700;
  display: flex;
  align-items: center;
}}
.hero-text img.favicon {{
  width: 40px;
  height: 40px;
  margin-right: 15px;
}}
.hero-text p {{
  font-size: 18px;
  color: #6c757d;
  margin-top: 20px;
}}
.hero-buttons {{
  margin-top: 30px;
}}
.hero-button {{
  padding: 12px 30px;
  border-radius: 30px;
  font-size: 16px;
  text-decoration: none;
  font-weight: 500;
  margin-right: 20px;
}}
.hero-button.get-started {{
  background-color: #CF9FFF;
  color: white;
}}
.hero-button.explore-more {{
  background-color: #e0e0e0;
  color: black;
}}
.responsive-hero-image {{
  width: 500px;
  height: auto;
  border-radius: 8px;
}}
.favicon {{
  width: 30px;
  height: auto;
  margin-right: 10px;
  vertical-align: middle;
}}
</style>
""", unsafe_allow_html=True)
# Navbar with dynamic styling and scroll-based highlighting
st.markdown("""
<div class="header">
<div class="nav">
<a href="#home" class="nav-link" id="home-link">Home</a>
<a href="#why" class="nav-link" id="why-link">Why Use TaxMaster?</a>
<a href="#contacts" class="nav-link" id="contacts-link">Contacts</a>
<a href="#learn-more" class="nav-link" id="learn-more-link">Learn More</a>
</div>
<div class="cta-buttons">
<a href="/?page=signup" class="cta-button signup">Register</a>
<a href="/?page=login" class="cta-button login">Log In</a>
</div>
</div>
""", unsafe_allow_html=True)
# Load your local image
favicon_path = "C:/Users/SRay5/OneDrive - Rockwell Automation, Inc/Desktop/TaxMaster/Templates/tax_favicon.jpg"
def get_base64_image(image_path):
   with open(image_path, "rb") as img_file:
       return base64.b64encode(img_file.read()).decode()
favicon_base64 = get_base64_image(favicon_path)
# Hero Section
st.markdown(f"""
<div id="home" class="hero">
<div class="hero-text">
<h1>
<img src="data:image/png;base64,{favicon_base64}" alt="Favicon" class="favicon"/>
          Welcome To TaxMaster!
</h1>
<p>Simplify Your Taxes, Maximize Your Refunds.</p>
<div class="hero-buttons">
<a href="#getstarted" class="hero-button get-started">Get Started</a>
<a href="#explore" class="hero-button explore-more">Explore More</a>
</div>
</div>
<div class="hero-image">
<img src="https://media.istockphoto.com/id/1364117721/vector/online-tax-filing-concept-businessman-filling-tax-form-documents-online-vector-illustration.jpg?s=612x612&w=0&k=20&c=ode3rxpIjUSBD-zROmt7pf5rmYX6FwLakG3jGzKhMwk=" alt="Hero Image" class="responsive-hero-image">
</div>
</div>
""", unsafe_allow_html=True)
# Section 1 - Why Use TaxMaster
st.markdown("""
<div id="why" style="padding: 50px; background-color: #F8F9FA; border-radius: 10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.1);">
<h2 style="color: #4A4A4A; font-weight: 700; font-size: 36px; margin-bottom: 20px;">Why Use TaxMaster?</h2>
<p style="font-size: 20px; color: #333333; line-height: 1.6;"><strong style="color: #BF40BF;">Tax!!!</strong> What's the first thing that comes to your mind when you hear the word "TAX"? Money, right? But how much?</p>
<p style="font-size: 18px; color: #555555;">This is a complicated question.</p>
<p style="font-size: 18px; color: #555555;">To know how much, you need to study our income tax rules and deal with a number of lengthy calculations.</p>
<p style="font-size: 18px; color: #555555;">Well, don't be intimidated by those lengthy calculations because <strong>TaxMaster</strong> is here for the rescue!</p>
<p style="font-size: 18px; color: #555555;">TaxMaster is a web-based portal for tax calculation that allows users of any age group to calculate their taxes based on their income without facing complexity.</p>
<ul style="font-size: 18px; color: #555555;">
<li>Accurate tax calculations</li>
<li>Solutions to minimize your taxes</li>
<li>Maximum privacy and security</li>
</ul>
<p style="font-size: 18px; color: #555555;">TaxMaster is here to simplify your tax experience!</p>
</div>
""", unsafe_allow_html=True)
# Section 2 - Contacts
st.markdown("""
<div id="contacts" style='padding: 50px; text-align: center; background-color: #E5E4E2; border-radius: 10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.1);'>
<h2 style="color: #4A4A4A; font-weight: 700; font-size: 36px;">Contact Us</h2>
<p style="font-size: 20px; color: #333333; line-height: 1.6;">For more information, please reach out to us at:</p>
<p style="font-size: 22px; font-weight: bold; color: #BF40BF;">sanchari.ray@rockwellautomation.com</p>
</div>
""", unsafe_allow_html=True)
# Section 3 - Learn More
st.markdown("""
<div id="learn-more" style="padding: 50px; background: linear-gradient(135deg, #CF9FFF 0%, #E5E4E2 100%); border-radius: 10px; box-shadow: 0px 4px 12px rgba(0,0,0,0.1);">
<h2 style="color: #4A4A4A; font-weight: 700; font-size: 36px;">Learn More</h2>
<p style="font-size: 20px; color: #333333; line-height: 1.6;">Discover how <strong>TaxMaster</strong> can help simplify your taxes and save you time.</p>
<p style="font-size: 18px; color: #555555;">Maximize your returns with our simple-to-use tools and enjoy a hassle-free experience!</p>
</div>
""", unsafe_allow_html=True)