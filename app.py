import streamlit as st
from stegano import lsb
from PIL import Image
import tempfile

st.set_page_config(page_title="Steganography Tool")

st.title("Steganography Tool")

uploaded_file = st.file_uploader("Open Image", type=["png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Selected Image", use_column_width=True)

    message = st.text_area("Enter Secret Message")
    password = st.text_input("Enter Secret Key", type="password")

    if st.button("Hide Data"):
        if password == "1234":
            if message == "":
                st.error("Please enter a message")
            else:
                uploaded_file.seek(0)
                temp = tempfile.NamedTemporaryFile(delete=False)
                temp.write(uploaded_file.read())
                temp.close()

                secret = lsb.hide(temp.name, message)
                secret.save("hidden.png")

                with open("hidden.png", "rb") as file:
                    st.download_button("Download Image", file, file_name="secret.png")
        else:
            st.error("Wrong Secret Key")

    if st.button("Show Data"):
        if password == "1234":
            uploaded_file.seek(0)
            temp = tempfile.NamedTemporaryFile(delete=False)
            temp.write(uploaded_file.read())
            temp.close()

            revealed = lsb.reveal(temp.name)

            if revealed:
                st.text_area("Hidden Message", revealed)
            else:
                st.warning("No hidden message found")
        else:
            st.error("Wrong Secret Key")