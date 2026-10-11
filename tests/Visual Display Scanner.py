import tkinter as tk
import time

def display_test():
    print("[!] Instructions:")
    print(" - Click Left Mouse Button or press SPACE to switch colors.")
    print(" - Press ESC to exit the test early.")
    print(" - Look for dead (black) pixels on white and stuck (colored) pixels on black.\n")

    # Base colors to expose any type of dead/stuck pixels
    colors = ['white', 'black', 'red', 'green', 'blue']
    current_idx = 0

    # Initialize the base window
    root = tk.Tk()
    root.title("Matrix Dead Pixel Test")
    
    # Make it fullscreen, remove borders, and hide the cursor
    root.attributes("-fullscreen", True)
    root.config(cursor="none")
    root.configure(bg=colors[current_idx])

    # Function to cycle through colors
    def next_color(event=None):
        nonlocal current_idx
        current_idx += 1
        if current_idx >= len(colors):
            root.destroy()  # Exit if colors are exhausted
        else:
            root.configure(bg=colors[current_idx])

    # Function for emergency exit
    def exit_test(event=None):
        root.destroy()

    # Bind actions to inputs
    root.bind("<Button-1>", next_color)  # Left Click
    root.bind("<space>", next_color)     # Spacebar
    root.bind("<Return>", next_color)    # Enter
    root.bind("<Escape>", exit_test)     # Esc

    # Run the window loop (Python pauses here until window is closed)
    root.mainloop()

    return "--- DISPLAY TEST ---\nStatus: Completed visually by user.\n"

if __name__ == "__main__":
    display_test()