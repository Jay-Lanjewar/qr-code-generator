import streamlit as st
import os
import tempfile
import io
import contextlib

from main import generate_qr_code, ERROR_CORRECTION_LEVELS

# -------------------------------------------------
# Page configuration
# -------------------------------------------------
st.set_page_config(page_title="QR Code Generator", page_icon="🔲")
st.title("🔲 QR Code Generator")

# -------------------------------------------------
# Session state (THIS prevents duplicate QRs)
# -------------------------------------------------
if "qr_image" not in st.session_state:
    st.session_state.qr_image = None

# -------------------------------------------------
# Sidebar inputs
# -------------------------------------------------
st.sidebar.header("Customization")

ec_choice = st.sidebar.selectbox(
    "Error Correction Level",
    options=list(ERROR_CORRECTION_LEVELS.keys()),
    index=1
)

box_size = st.sidebar.slider(
    "Box Size",
    min_value=1,
    max_value=50,
    value=10
)

fill_color = st.sidebar.color_picker(
    "Fill Color",
    "#000000"
)

back_color = st.sidebar.color_picker(
    "Background Color",
    "#FFFFFF"
)

# -------------------------------------------------
# Main input
# -------------------------------------------------
data = st.text_input(
    "Enter Data (Text or URL)",
    placeholder="https://example.com"
)

# -------------------------------------------------
# Generate button
# -------------------------------------------------
if st.button("Generate QR Code"):
    if not data.strip():
        st.warning("Please enter some text or a valid URL to generate a QR code.")
    else:
        # Create temp file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            temp_path = tmp_file.name

        stderr_capture = io.StringIO()

        try:
            with contextlib.redirect_stderr(stderr_capture):
                generate_qr_code(
                    data=data,
                    filename=temp_path,
                    error_correction=ERROR_CORRECTION_LEVELS[ec_choice],
                    box_size=box_size,
                    border=4,
                    fill_color=fill_color,
                    back_color=back_color
                )

            # Read QR image into memory
            with open(temp_path, "rb") as f:
                st.session_state.qr_image = f.read()

            st.success("QR Code generated successfully!")

        except SystemExit:
            error_message = stderr_capture.getvalue()
            st.error(f"Generation failed:\n{error_message}")

        except Exception as e:
            st.error(f"Unexpected error: {e}")

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

# -------------------------------------------------
# Display QR (ONLY ONCE)
# -------------------------------------------------
if st.session_state.qr_image:
    st.image(
        st.session_state.qr_image,
        caption="Generated QR Code"
    )

    st.download_button(
        label="Download PNG",
        data=st.session_state.qr_image,
        file_name="qr_code.png",
        mime="image/png"
    )
