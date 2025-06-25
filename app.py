import streamlit as st
import openai

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Lensrentals Product Verifier")

query = st.text_input("Enter product name or MPN")

if st.button("Verify"):
    if not query:
        st.warning("Please enter a product name or MPN.")
    else:
        with st.spinner("Verifying..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a product verifier for Lensrentals. Confirm product details and availability."
                        },
                        {
                            "role": "user",
                            "content": f"Verify this product: {query}"
                        }
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                result = response.choices[0].message.content
                st.success("Verification result:")
                st.write(result)

            except Exception as e:
                st.error(f"An error occurred: {e}")
