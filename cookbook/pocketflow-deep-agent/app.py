import streamlit as st
# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Pocket Flow × Streamlit: Chat + (mock) web tool", page_icon="💬")

# Init session state (persist across reruns) — recommended pattern in Streamlit
# Docs: st.chat_message / st.chat_input / st.session_state
if "shared" not in st.session_state:
    st.session_state.shared = make_empty_shared()
if "flow" not in st.session_state:
    st.session_state.flow = build_flow(FakeWebSearchAPI())

st.title("Pocket Flow × Streamlit")
st.caption("Chat with a Router + (mock) Web Search tool. Use `/web your query` to force search.")

# Show history
for msg in st.session_state.shared["history"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_text = st.chat_input("Type a message… (tip: try `/web pocket flow streamlit`)")
if user_text:
    # Record user message and run the flow
    st.session_state.shared["last_user_message"] = user_text
    st.session_state.shared["history"].append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    # Run the flow (Router → WebSearch or Chat)
    st.session_state.flow.run(st.session_state.shared)

    # Render assistant reply immediately from shared
    assistant_reply = st.session_state.shared["assistant_last_message"]
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

# Sidebar: debug + controls
with st.sidebar:
    st.subheader("Flow Debug")
    st.write(f"Last route: **{st.session_state.shared.get('route','')}**")
    st.write("Tool metrics:")
    st.json(st.session_state.shared["tools"], expanded=False)

    if st.button("🔁 Reset conversation"):
        st.session_state.shared = make_empty_shared()
        st.rerun()