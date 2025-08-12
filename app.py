import streamlit as st
from chatbot import ask_samvidhan
from scenario_advisor import get_scenario_based_response
import os

st.set_page_config(
    page_title="Samvidhan AI",
    page_icon="📜",
    layout="wide"
)

st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #2E3A8C; }
    .subheader { font-size: 1.5rem; color: #3949AB; }
    .scenario-box { 
        background-color: #E3F2FD; 
        padding: 20px; 
        border-radius: 10px; 
        margin: 20px 0; 
        border: 1px solid #BBDEFB;
        color: #000000 !important;
    }
    .scenario-box p, .scenario-box div {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Samvidhan Chatbot", "Scenario-based Response"])

# ---------- TAB 1 ----------
with tab1:
    st.markdown('<p class="main-header">📜 Samvidhan Chatbot</p>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Ask questions about the Constitution of India</p>', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query = st.chat_input("Ask me about the Constitution...")

    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ask_samvidhan(query)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# ---------- TAB 2 ----------
with tab2:
    st.markdown('<p class="main-header">⚖️ Scenario-based Legal Analysis</p>', unsafe_allow_html=True)
    
    # Add some example scenarios
    st.markdown("### Example Scenarios:")
    examples = [
        "A state government passes a law restricting online speech criticizing its ministers, citing maintenance of public order. Is this constitutional?",
        "A private school refuses admission based on religion. What does the Constitution say?",
        "Government wants to acquire private land for highway. What are the constitutional provisions?"
    ]
    
    selected_example = st.selectbox("Choose an example or write your own:", ["Write your own..."] + examples)
    
    if selected_example != "Write your own...":
        scenario = st.text_area("Describe your legal scenario", value=selected_example, height=200)
    else:
        scenario = st.text_area("Describe your legal scenario", height=200)
    
    if st.button("Analyze Scenario"):
        if scenario.strip():
            with st.spinner("Analyzing..."):
                try:
                    response = get_scenario_based_response(scenario)
                    # Display response without HTML styling that might cause issues
                    st.markdown("### Constitutional Analysis:")
                    st.write(response)  # Using st.write instead of styled HTML
                    
                except Exception as e:
                    st.error(f"Error analyzing scenario: {str(e)}")
        else:
            st.warning("Please enter a scenario to analyze.")

# ---------- SIDEBAR ----------
with st.sidebar:
    st.image("https://api.placeholder.com/120/120", width=120)
    st.markdown("### Samvidhan AI")
    st.markdown("This AI assistant helps with:")
    st.markdown("- Constitutional Q&A")
    st.markdown("- Scenario-based legal analysis")
    st.markdown("- Article & Schedule references")
    st.markdown("- Plain language explanations")
    
    st.markdown("---")
    st.markdown("### Quick Test")
    if st.button("Test Scenario Function"):
        test_scenario = "A citizen wants to know their fundamental rights under the Constitution."
        with st.spinner("Testing..."):
            try:
                test_response = get_scenario_based_response(test_scenario)
                st.success("✅ Scenario function working!")
                st.text_area("Test Response:", test_response, height=100)
            except Exception as e:
                st.error(f"❌ Function error: {str(e)}")