import streamlit as st

# Set the page layout
st.set_page_config(page_title="Registration", page_icon=":pencil:", layout="wide")

# Custom CSS to style the form and make it visually appealing
st.markdown("""
<style>
   /* Hide Streamlit header and footer */
   #MainMenu {visibility: hidden;}
   footer {visibility: hidden;}
   header {visibility: hidden;}

   body {
       background-color: #e0f7fa;
   }
   .form-container {
       background-color: #ffffff;
       padding: 30px;
       border-radius: 50px;
       box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
       margin-top: 20px;
       animation: fadeIn 1s ease-in-out;
   }
   .form-container h1 {
       color: #ffffff;
       background-color: #9b59b6;
       text-align: center;
       margin-bottom: 20px;
       padding: 20px;
       border-radius: 10px;
       font-family: 'Arial', sans-serif;
       font-size: 32px;
       font-weight: bold;
       box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
   }
   .signup-form input {
       margin-bottom: 10px;
       width: 100%;
       padding: 12px;
       border-radius: 8px;
       border: 1px solid #ccc;
       font-size: 16px;
       transition: border-color 0.3s, box-shadow 0.3s;
   }
   .signup-form input:focus {
       border-color: #9b59b6;
       box-shadow: 0 0 8px rgba(155, 89, 182, 0.5);
   }
   .signup-form button {
       background-color: #007bff;
       color: white;
       padding: 12px;
       border: none;
       border-radius: 8px;
       cursor: pointer;
       width: 100%;
       font-size: 18px;
       transition: background-color 0.3s, transform 0.3s;
   }
   .signup-form button:hover {
       background-color: #0056b3;
       transform: scale(1.05);
   }
   .signup-form button:active {
       background-color: #004494;
   }
   .terms {
       margin-bottom: 15px;
   }
   .already-member {
       text-align: center;
       margin-top: 20px;
   }
    .already-member-container {
       text-align: center;
       margin-top: 20px;
       padding: 10px;
       background-color: #f1f1f1;
       border-radius: 8px;
       box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
   }
   .already-member a {
       color: #9b59b6;
       text-decoration: none;
       font-size: 16px;
   }
   .already-member a:hover {
       text-decoration: underline;
   }
   .already-member a:active {
       color: #0056b3;
   }
   .form-container h2 {
       color: #fff;
       background-color: #9b59b6;
       font-size: 28px;
       margin-bottom: 15px;
       text-align: center;
       padding: 10px;
       border-radius: 8px;
       box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
   }
   @keyframes fadeIn {
       from { opacity: 0; }
       to { opacity: 1; }
   }

    .stTextInput > div > div > input {
        border: 2px solid #9b59b6;
        padding: 10px;
        border-radius: 5px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #8e44ad;
        box-shadow: 0 0 8px rgba(142, 68, 173, 0.5);
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }

</style>
""", unsafe_allow_html=True)

# Form section with the heading
st.markdown('<div class="form-container"><h1>New User Registration</h1></div>', unsafe_allow_html=True)

# Adjust the columns
col1, col2 = st.columns([2, 1])

with col1:
    # Signup form
    with st.form(key="signup_form"):
        st.markdown('<h2>To Register, Please fill in Your Details!</h2>', unsafe_allow_html=True)
        first_name = st.text_input("First Name", help="Enter your first name")
        last_name = st.text_input("Last Name", help="Enter your last name")
        username = st.text_input("Your Username", help="Choose a unique username")
        email = st.text_input("Your Email", help="Enter your email address")
        password = st.text_input("Password", type="password", help="Choose a strong password")
        repeat_password = st.text_input("Repeat your password", type="password", help="Repeat your password")
        agree = st.checkbox("I agree to all statements in the Terms of service")
        # Form submit button
        st.markdown('<div class="signup-form">', unsafe_allow_html=True)
        if st.form_submit_button(label="Register"):
            if agree:
                st.success(f"Hi {first_name}, your registration is successful!")
            else:
                st.error("You need to agree to the Terms of Service")
        st.markdown('</div>', unsafe_allow_html=True)
    # Link to existing member login
    st.markdown('<div class="already-member-container"><div class="already-member"><a href="#">Already a member? LogIn!</a></div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Image section
with col2:
    # Provide the path to the image on your local machine
    image_path = "C:/Users/SRay5/OneDrive - Rockwell Automation, Inc/Desktop/TaxMaster/Frontend/Register.jpg"  # Replace with your actual image path
    st.image(image_path, caption="Register and become a member!", use_column_width=True)
