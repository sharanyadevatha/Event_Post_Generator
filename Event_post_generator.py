import streamlit as st
import openai
from openai import OpenAI
import io

st.title("📣 Event Post Generator")
st.write("Create platform-specific posts for your event!")

# --- Input Fields ---
api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")
event_description = st.text_area("📌 Describe your event")

st.write("## 🎯 Choose Platforms")
selected_platforms = {
    "LinkedIn": st.checkbox("LinkedIn"),
    "WhatsApp": st.checkbox("WhatsApp"),
    "Twitter": st.checkbox("Twitter"),
}

# Initialize session state to store results
if "posts" not in st.session_state:
    st.session_state.posts = {}

# Generate posts when button is clicked
if st.button("Generate Posts"):
    if not api_key or not event_description:
        st.warning("Please enter both the API key and the event description.")
    elif not any(selected_platforms.values()):
        st.warning("Please select at least one platform.")
    else:
        try:
            client = OpenAI(api_key=api_key)

            def generate_post(platform, tone_instructions, extra_constraints=""):
                prompt = f"""
You are a social media content writer. Write a post for {platform}.
Event: {event_description}
Tone: {tone_instructions}
{extra_constraints}
Make sure the content is engaging and platform-appropriate.
"""
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                content = response.choices[0].message.content.strip()
                if platform.lower() == "twitter":
                    content = content[:280]
                return content

            st.session_state.posts = {}  # Reset previous posts

            if selected_platforms["LinkedIn"]:
                st.session_state.posts["LinkedIn"] = generate_post(
                    "LinkedIn",
                    "Professional yet exciting. Highlight opportunities and impact."
                )

            if selected_platforms["WhatsApp"]:
                st.session_state.posts["WhatsApp"] = generate_post(
                    "WhatsApp",
                    "Friendly and casual. Imagine you’re sharing it with a close group of friends."
                )

            if selected_platforms["Twitter"]:
                st.session_state.posts["Twitter"] = generate_post(
                    "Twitter",
                    "Informative and hyped. Use hashtags and emojis where appropriate.",
                    "Limit the post to 280 characters."
                )

        except Exception as e:
            st.error(f"Error: {e}")

# Display stored posts and allow download
if st.session_state.posts:
    for platform, content in st.session_state.posts.items():
        st.subheader(f"📢 {platform} Post")
        st.code(content)
        st.caption(f"Character count: {len(content)}")
        st.download_button(
            label=f"⬇️ Download {platform} Post",
            data=content,
            file_name=f"{platform.lower()}_post.txt",
            mime="text/plain",
            key=f"download_{platform}"
        )
