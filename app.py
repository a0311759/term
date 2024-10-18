import streamlit as st
import subprocess
import os

# Initialize session state for storing the current working directory
if 'current_dir' not in st.session_state:
    st.session_state.current_dir = os.getcwd()

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
            st.write(f"Changed directory to: {st.session_state.current_dir}")
        else:
            # Execute the command using subprocess in the current directory
            result = subprocess.run(command, shell=True, cwd=st.session_state.current_dir, capture_output=True, text=True)
            
            # Display the result
            if result.stdout:
                st.text_area("Output:", result.stdout, height=300)
            if result.stderr:
                st.text_area("Error:", result.stderr, height=300)

    except Exception as e:
        st.error(f"An error occurred: {e}")
      
