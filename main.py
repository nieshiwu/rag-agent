import os
import sys
import time
import subprocess
import threading
from langfuse.callback import CallbackHandler
from dotenv import load_dotenv

# Load environment variables explicitly at the start
load_dotenv()
langfuse_handler = CallbackHandler()


def start_mock_server():
    """Starts the mock server in a separate process."""
    print("Starting mock knowledge base server...")
    # Using sys.executable to ensure we use the same python interpreter
    # Run as module to resolve imports correctly
    # Updated path to src.api.mock_server
    process = subprocess.Popen([sys.executable, "-m", "src.api.mock_server"], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    time.sleep(2) # Give it a moment to start
    return process

def main():
    print("Initializing Agentic RAG System...")
    
    # Start Mock Server
    server_process = start_mock_server()
    
    try:
        # Import here to avoid issues if dependencies are missing during initial setup
        # Updated import path to src.core.agent
        from src.core.agent import create_rag_agent
        from src.core.callbacks import AgentCallbackHandler # Import Callback Handler
        # from langfuse.callback import CallbackHandler # Moved up
        
        agent_executor = create_rag_agent()

        print("\n=== Agent Ready ===")
        print("Try asking about 'finance report', 'AI models', or 'weather'.")
        print("Type 'exit' to quit.\n")
        
        while True:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            try:
                print("\nAgent processing...")
                # Use LangGraph input format: list of messages
                # Pass callback handler to invoke config
                from langchain_core.messages import HumanMessage
                response = agent_executor.invoke(
                    {"messages": [HumanMessage(content=user_input)]},
                    config={"callbacks": [AgentCallbackHandler(), langfuse_handler]}
                )
                
                # --- Visualization is now handled by AgentCallbackHandler in real-time ---

                # Check available keys in response for debugging if needed
                if 'messages' in response:
                    # Handle case where response is a list of messages (LangGraph/new LangChain behavior)
                    messages = response['messages']
                    if messages and hasattr(messages[-1], 'content'):
                         print(f"\nAgent: {messages[-1].content}\n")
                    else:
                         print(f"\nAgent (Raw Messages): {messages}\n")
                else:
                    # Fallback for other potential return keys like 'return_values' or raw string
                    print(f"\nAgent (Debug): {response}\n")
            except Exception as e:
                print(f"Error: {e}")
                
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        print("Flushing Langfuse traces...")
        langfuse_handler.langfuse.flush()
        print("Terminating mock server...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    main()
