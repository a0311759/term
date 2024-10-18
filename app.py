import streamlit as st
import subprocess
import os

# Initialize session state to keep track of command history and current directory
if 'current_dir' not in st.session_state:
    st.session_state.current_dir = os.getcwd()

if 'command_history' not in st.session_state:
    st.session_state.command_history = ""

# Display the current directory at the top
st.write(f"**Current Directory**: {st.session_state.current_dir}")

# Input field for user to enter a command
command = st.text_input("Enter a command (e.g., ls, cd, mkdir, etc.):", key="input_box")

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
            output = f"Changed directory to: {st.session_state.current_dir}\n"
        else:
            # Execute the command using subprocess in the current directory
            result = subprocess.run(command, shell=True, cwd=st.session_state.current_dir, capture_output=True, text=True)
            
            # Capture the command output
            output = result.stdout if result.stdout else result.stderr if result.stderr else "Command executed with no output\n"

        # Append the command and output to the command history
        st.session_state.command_history += f"$ {command}\n{output}\n"

    except Exception as e:
        st.session_state.command_history += f"An error occurred: {e}\n"

# Display the full command history as a scrollable text area (terminal-like behavior)
st.text_area("Terminal", st.session_state.command_history, height=400)

# Reset the command input after each submission to stay at the bottom
st.text_input("Enter a command (e.g., ls, cd, mkdir, etc.):", key="input_box_2")
