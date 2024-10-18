import streamlit as st
import subprocess
import os

# Initialize session state to keep track of command history and current directory
if 'current_dir' not in st.session_state:
    st.session_state.current_dir = os.getcwd()

if 'command_history' not in st.session_state:
    st.session_state.command_history = []

# Function to display the command history as paragraphs
def display_command_history():
    for entry in st.session_state.command_history:
        st.markdown(f"**$ {entry['command']}**")
        st.markdown(f"{entry['output']}")

# Display the current command history (scrollable)
display_command_history()

# Input field for user to enter a command, fixed at the bottom
command = st.text_input("Enter a command:", key="input_box")

# If a command is entered
if command:
    try:
        # Split the command to handle 'cd' separately
        command_parts = command.split()

        if command_parts[0] == 'cd':
            # Change the directory
            new_dir = command_parts[1] if len(command_parts) > 1 else os.path.expanduser("~")
            os.chdir(new_dir)
            st.session_state.current_dir = os.getcwd()
            output = f"Changed directory to: {st.session_state.current_dir}"
        else:
            # Execute the command using subprocess in the current directory
            result = subprocess.run(command, shell=True, cwd=st.session_state.current_dir, capture_output=True, text=True)
            
            # Capture the command output
            output = result.stdout if result.stdout else result.stderr if result.stderr else "Command executed with no output"

        # Append the command and output to the command history
        st.session_state.command_history.append({'command': command, 'output': output})

    except Exception as e:
        st.session_state.command_history.append({'command': command, 'output': f"An error occurred: {e}"})

    # Reset the command input field after each submission
    st.experimental_rerun()

# Fix the input field at the bottom with some custom CSS
st.markdown(
    """
    <style>
    .stTextInput {
        position: fixed;
        bottom: 0;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True
)
