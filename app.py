import streamlit as st
import time
import json
import os
import requests
from ghost import chat_with_ghost, OLLAMA_URL

# ==============================
# CONFIG & INITIALIZATION
# ==============================

st.set_page_config(
    page_title="Ghost Terminal AI",
    page_icon="👻",
    layout="centered"
)

MEMORY_FILE = "ghost_memory.json"

# Load / Save Persistent Memory
def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_memory(history):
    with open(MEMORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

if "messages" not in st.session_state:
    st.session_state.messages = load_memory()

# Check Ollama Connection
def check_ollama_status():
    try:
        res = requests.get("http://localhost:11434/", timeout=2)
        return res.status_code == 200
    except Exception:
        return False

# ==============================
# CUSTOM STYLING (MATRIX TERMINAL)
# ==============================

st.markdown("""
<style>
/* Background aplikasi utama & sidebar */
.stApp, header[data-testid="stHeader"] {
    background-color: #080D0A !important;
}

[data-testid="stSidebar"] {
    background-color: #0D1410 !important;
    border-right: 1px solid #1E3A2B !important;
}

/* Mengubah warna teks sidebar */
[data-testid="stSidebar"] * {
    color: #39FF88 !important;
    font-family: 'Courier New', Courier, monospace !important;
}

/* Memperbaiki tata letak & kontras chat message */
[data-testid="stChatMessage"] {
    background-color: transparent !important;
    padding: 0.5rem !important;
}

[data-testid="stChatMessageContent"] {
    background-color: #0E1A14 !important;
    border: 1px solid #1E3A2B !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
}

/* Teks balasan & pesan di dalam chat bubble */
[data-testid="stChatMessageContent"] p {
    color: #39FF88 !important;
    font-family: 'Courier New', Courier, monospace !important;
    font-size: 15px !important;
    margin: 0 !important;
}

/* ============================================== */
/* FIXING INPUT BOX BACKGROUND & TEXT CONTRAST    */
/* ============================================== */

/* Paksa container bawah & seluruh wrapper input berlatar hijau tua gelap */
[data-testid="stBottom"], 
[data-testid="stBottom"] > div,
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] div[data-baseweb="input"],
[data-testid="stChatInput"] div[data-baseweb="base-input"] {
    background-color: #0E1A14 !important;
    border-color: #1E3A2B !important;
}

/* Paksa area input ketik teks berlatar gelap & font hijau neon terang */
[data-testid="stChatInput"] textarea {
    background-color: #0E1A14 !important;
    color: #00FF66 !important;
    -webkit-text-fill-color: #00FF66 !important; /* Mencegah override browser */
    font-family: 'Courier New', Courier, monospace !important;
    font-size: 16px !important;
    font-weight: bold !important;
}

/* Teks placeholder ("Enter your message...") */
[data-testid="stChatInput"] textarea::placeholder {
    color: #5A8C69 !important;
    -webkit-text-fill-color: #5A8C69 !important;
}

/* Tombol kirim (panah) */
[data-testid="stChatInput"] button {
    color: #00FF66 !important;
    background-color: #15291E !important;
    border: 1px solid #1E3A2B !important;
}

/* ASCII Art & Status */
.ghost-ascii {
    color: #39FF88 !important;
    font-size: 11px;
    line-height: 1.1;
    text-align: center;
    white-space: pre;
    margin-bottom: 15px;
}
.status-online {
    color: #39FF88 !important;
    font-weight: bold;
}
.status-offline {
    color: #FF4D4D !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# SIDEBAR CONTROL PANEL
# ==============================

st.sidebar.title("👻 GHOST CONTROL")
is_online = check_ollama_status()

if is_online:
    st.sidebar.markdown("STATUS: <span class='status-online'>● ONLINE</span>", unsafe_allow_html=True)
else:
    st.sidebar.markdown("STATUS: <span class='status-offline'>● OFFLINE (Ollama disconnect)</span>", unsafe_allow_html=True)

st.sidebar.write("MODEL: QWEN 2.5 (7B)")
st.sidebar.markdown("---")

if st.sidebar.button("🗑️ CLEAR MEMORY"):
    st.session_state.messages = []
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
    st.rerun()

# ==============================
# MAIN TERMINAL INTERFACE
# ==============================

ghost_ascii_art = """
  .-.
 (o.o)  GHOST TERMINAL v1.1
  |=|   --------------------
 /   \\  "I am watching..."
"""
st.markdown(f"<pre class='ghost-ascii'>{ghost_ascii_art}</pre>", unsafe_allow_html=True)

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
if prompt := st.chat_input("Enter your message..."):
    # Render user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Render Ghost response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if not is_online:
            full_response = "ERR: Cannot establish connection to Ollama local instance."
            message_placeholder.markdown(full_response)
        else:
            message_placeholder.markdown("GHOST: Thinking...")
            
            # Format history for Ollama API
            api_history = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages[:-1]
            ]
            
            response_text = chat_with_ghost(prompt, api_history)
            
            # Typing effect
            full_response = ""
            for char in response_text:
                full_response += char
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.015)
            
            message_placeholder.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        save_memory(st.session_state.messages)