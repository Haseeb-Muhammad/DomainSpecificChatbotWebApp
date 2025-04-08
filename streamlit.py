import DomainSpecificChatbotWebApp.frontend.streamlit as st
import time
import random
import requests

BACKEND_URL = 'http://0.0.0.0:8000'

# Set page configuration
st.set_page_config(
    page_title="Knowledge Assistant",
    page_icon="📚",
    layout="wide"
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "contexts" not in st.session_state:
    st.session_state.contexts = {}

# Mock function to simulate RAG retrieval (replace with actual implementation)
def get_rag_response(query):
    response = requests.post(BACKEND_URL, json={"question": query})
    data = response.json()

    if "error" in data:
        return "Error occurred: " + data["error"], {}
    return data["response"], data["context"]

# Custom CSS
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #e6f7ff;
        border-left: 5px solid #1890ff;
    }
    .chat-message.assistant {
        background-color: #f6f6f6;
        border-left: 5px solid #722ed1;
    }
    .context-box {
        background-color: #fffbe6;
        border: 1px solid #ffe58f;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📚 Knowledge Assistant")
st.markdown("Ask questions about books, documents, and more. I'll provide answers with relevant context.")

# Sidebar for additional options
with st.sidebar:
    st.header("Settings")
    st.markdown("Configure your assistant preferences")
    
    search_depth = st.slider("Search Depth", min_value=1, max_value=10, value=3,
                          help="Controls how extensively the system searches for relevant content")
    
    confidence_threshold = st.slider("Confidence Threshold", min_value=0.0, max_value=1.0, value=0.7, step=0.05,
                                  help="Minimum confidence level for including retrieved context")
    
    st.divider()
    st.subheader("About")
    st.markdown("""
    This assistant uses Retrieval-Augmented Generation (RAG) to provide answers based on your document library.
    Responses include source information for verification.
    """)

# Main chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show context for assistant messages
            if message["role"] == "assistant" and i in st.session_state.contexts:
                context = st.session_state.contexts[i]
                with st.expander("View Source", expanded=False):
                    st.markdown(f"**Book:** {context['book_name']}")
                    st.markdown(f"**Page:** {context['page_number']}")
                    st.markdown("**Relevant Context:**")
                    st.markdown(f"> {context['content']}")

# Chat input
if prompt := st.chat_input("Ask a question..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from RAG system
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        context_placeholder = st.empty()
        
        with st.status("Searching knowledge base...", expanded=True) as status:
            st.write("Retrieving relevant documents...")
            time.sleep(0.5)
            st.write("Analyzing context...")
            time.sleep(0.5)
            st.write("Generating response...")
            
            # Call RAG function (placeholder)
            response_text, context = get_rag_response(prompt)
            status.update(label="Done!", state="complete", expanded=False)
        
        # Display response
        message_placeholder.markdown(response_text)
        
        # Display context in an expander
        with st.expander("View Source", expanded=False):
            st.markdown(f"**Book:** {context['book_name']}")
            st.markdown(f"**Page:** {context['page_number']}")
            st.markdown("**Relevant Context:**")
            st.markdown(f"> {context['content']}")
    
    # Save assistant response and context
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    st.session_state.contexts[len(st.session_state.messages) - 1] = context
    
# Add a footer
st.divider()
st.caption("Knowledge Assistant powered by RAG technology")
