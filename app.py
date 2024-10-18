import streamlit as st
import subprocess
import os

# Initialize session state for storing the current working directory and output history
if 'current_dir' not in st.session_state:
    st.session_state.current_dir = os.getcwd()

if 'output_history' not in st.session_state:
    st.session_state.output_history = ""

# Display the current directory
st.write(f"**Current Directory**: {st.session_state.current_dir}")

# Input field for user to enter a command
command = st.text_input("Enter a command (e.g., ls, cd, mkdir, etc.):")

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
            st.session_state.output_history += f"\nChanged directory to: {st.session_state.current_dir}\n"
        else:
            # Execute the command using subprocess in the current directory
            result = subprocess.run(command, shell=True, cwd=st.session_state.current_dir, capture_output=True, text=True)
            
            # Append the result to output history
            if result.stdout:
                st.session_state.output_history += f"\n{result.stdout}\n"
            if result.stderr:
                st.session_state.output_history += f"\nError: {result.stderr}\n"

    except Exception as e:
        st.session_state.output_history += f"\nAn error occurred: {e}\n"

# Display the output history in paragraphs
st.write(st.session_state.output_history)
