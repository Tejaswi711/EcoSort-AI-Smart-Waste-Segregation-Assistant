import os
import json

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from prompt import SYSTEM_PROMPT


# Load environment variables
load_dotenv()

# Get API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Create OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


# Page configuration
st.set_page_config(
    page_title="EcoSort AI",
    page_icon="🌱",
    layout="centered"
)


# Application title
st.title("🌱 EcoSort AI")

st.subheader("Smart Waste Segregation Assistant")

st.write(
    "Enter a waste item and EcoSort AI will identify "
    "the suitable waste category, recommended bin, "
    "disposal method, and sustainability tip."
)


# Waste item input
waste_item = st.text_input(
    "Enter the waste item",
    placeholder="Example: plastic bottle"
)


# Analyze button
if st.button("Analyze Waste"):

    if waste_item.strip() == "":
        st.warning("Please enter a waste item.")

    elif not OPENAI_API_KEY:
        st.error("OpenAI API key is not configured.")

    else:

        with st.spinner("Analyzing waste..."):

            try:

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Analyze this waste item: {waste_item}"
                            )
                        }
                    ],
                    temperature=0.2
                )

                result = response.choices[0].message.content

                data = json.loads(result)

                st.success("Analysis Complete!")

                st.markdown("## ♻️ Waste Analysis")

                # Waste category
                st.markdown("### ♻️ Waste Category")
                st.write(data["waste_category"])

                # Recommended bin
                st.markdown("### 🗑️ Recommended Bin")
                st.write(data["recommended_bin"])

                # Disposal method
                st.markdown("### 🔄 Disposal Method")
                st.write(data["disposal_method"])

                # Sustainability tip
                st.markdown("### 🌱 Sustainability Tip")
                st.write(data["sustainability_tip"])

                # Safety note
                st.markdown("### ⚠️ Safety Note")
                st.write(data["safety_note"])

                st.info(
                    "🌍 Responsible AI: AI-generated recommendations "
                    "may vary depending on local waste-management rules."
                )

            except json.JSONDecodeError:
                st.error(
                    "The AI response was not in the expected format. "
                    "Please try again."
                )

            except Exception as e:
                st.error(f"Error: {e}")