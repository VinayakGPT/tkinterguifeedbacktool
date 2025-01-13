import tkinter as tk
from tkinter import scrolledtext, StringVar
import openai
import json
import time 

openai.api_key = "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"

prob_mapping = {
    "Triangle Type": "6-triangle-type",
    "Tetrahedral": "3-tetrahedral",
    "Smallest Prime - Type 1": "13-smallest-prime_1",
    "Smallest Prime - Type 2": "13-smallest-prime_2",
    "Count Primes": "11-count-primes",
    "Find Duplicates": "18-find-duplicates",
    "Recursive Pattern": "22-recursive-pattern",
}

def save_feedback(feedback_data):
    with open('feedbackGPT4Turbo.json', 'w') as f:
        json.dump(feedback_data, f, indent=4)

def selectfile():
    prob_alias = selected_problem.get()
    problem_name = prob_mapping.get(prob_alias)

    if problem_name is None:
        output_text.insert(tk.END, "Invalid problem selection!\n")
        return
    
    with open('data.json', 'r') as f:
        data = json.load(f)
        
    prob_data = data.get(problem_name, [])
    incorrect_solution = prob_data[0]
    instructor_solution = prob_data[1]
    all_manual_test_cases = prob_data[2]
    failing_manual_test_cases = prob_data[3]
    passing_manual_test_cases = prob_data[4]
    all_llm_test_cases = prob_data[5]
    failing_llm_test_cases = prob_data[6]
    passing_llm_test_cases = prob_data[7]
    problem_statement = prob_data[8]
    combination = [choice1.get(), choice2.get(), choice3.get(), choice4.get(), choice5.get(), choice6.get(), choice7.get(), choice8.get()]
    
    prompt = ""
    if combination[0]:
        prompt = f"Incorrect Solution:\n{incorrect_solution}\nModel Solution:\n{instructor_solution}\n"
    prompt += "Assume you are a teaching assistant, provide a description of the differences between the correct and incorrect solutions. "
    prompt += "The output should report the logical distinction between them, not structural or identifier differences. "
    prompt += "Check if the incorrect solution uses a different approach from the correct solution. "
    prompt += "Summarise the output in 2-3 lines highlighting the logical errors in the incorrect program. "
    
    for i in combination[1:]:
        if i != 0:
            prompt += " Use the additional information described below:"
            break
    
    if combination[1]:
        prompt += f"\nProblem Statement:\n{problem_statement}"
    if combination[2]:
        prompt += f"\nAll Manual Test Cases:\n{all_manual_test_cases}"
    if combination[3]:
        prompt += f"\nManual Test Cases failed by Incorrect solution:\n{failing_manual_test_cases}"
    if combination[4]:
        prompt += f"\nManual Test Cases passed by Incorrect solution:\n{passing_manual_test_cases}"
    if combination[5]:
        prompt += f"\nAll LLM-generated Test Cases:\n{all_llm_test_cases}"
    if combination[6]:
        prompt += f"\nLLM-generated Test Cases failed by Incorrect solution:\n{failing_manual_test_cases}"
    if combination[7]:
        prompt += f"\nLLM-generated Test Cases passed by Incorrect solution:\n{passing_llm_test_cases}"
        
    start_time = time.time()
    
    chat_completion = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
            "role": "user",
            "content": f"{prompt}\n"
        }
    ],
    temperature=1,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    
    end_time = time.time()
    time_taken = end_time - start_time
    
    reply = chat_completion.choices[0].message.content
    feedback_data = {
        "problem_statement": problem_statement,
        "incorrect_solution": incorrect_solution,
        "instructor_solution": instructor_solution,
        "all_manual_test_cases": all_manual_test_cases,
        "failing_manual_test_cases": failing_manual_test_cases,
        "passing_manual_test_cases": passing_manual_test_cases,
        "all_llm_test_cases": all_llm_test_cases,
        "failing_llm_test_cases": failing_llm_test_cases,
        "passing_llm_test_cases": passing_llm_test_cases,
        "prompt": prompt,
        "analysis": reply.strip(),
        "time_taken": time_taken
    }
    save_feedback(feedback_data)
    output_text.insert(tk.END, f"\n Prompt:\n{prompt}\n")
    output_text.insert(tk.END, f"\n Analysis:\n{reply.strip()}\n")
    output_text.insert(tk.END, f"\nTime taken: {time_taken:.2f} seconds\n")

def reset():
    selected_problem.set("")
    choice1.set(0)
    choice2.set(0)
    choice3.set(0)
    choice4.set(0)
    choice5.set(0)
    choice6.set(0)
    choice7.set(0)
    choice8.set(0)
    output_text.delete(1.0, tk.END)

root = tk.Tk()
root.title("PEM Enhancement Tool")

problem_label1 = tk.Label(root, text="Select problem:")
problem_label1.pack()

selected_problem = StringVar()
selected_problem.set("")  

problems = [
    'Triangle Type',
    'Tetrahedral',
    'Smallest Prime - Type 1',
    'Smallest Prime - Type 2',
    'Count Primes',
    'Find Duplicates',
    'Recursive Pattern',
]
radio_frame1 = tk.Frame(root)
radio_frame1.pack(pady=10)

for problem in problems:
    tk.Radiobutton(radio_frame1, text=problem, variable=selected_problem, value=problem).pack(anchor=tk.W) 

choice1 = tk.IntVar()
choice2 = tk.IntVar()
choice3 = tk.IntVar()
choice4 = tk.IntVar()
choice5 = tk.IntVar()
choice6 = tk.IntVar()
choice7 = tk.IntVar()
choice8 = tk.IntVar()

problem_label2 = tk.Label(root, text="Select combination:")
problem_label2.pack()
checkbox_frame = tk.Frame(root)
checkbox_frame.pack(pady=10)

tk.Checkbutton(checkbox_frame, text="Incorrect and model solution", variable=choice1).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Add problem statement", variable=choice2).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Add all manual test cases", variable=choice3).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Add failing manual test cases", variable=choice4).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Add passing manual test cases", variable=choice5).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Add all LLM-generated test cases", variable=choice6).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Add failing LLM-generated test cases", variable=choice7).pack(anchor=tk.W)
tk.Checkbutton(checkbox_frame, text="Add passing LLM-generated test cases", variable=choice8).pack(anchor=tk.W)

analyze_button = tk.Button(root, text="Analyse", command=selectfile)
analyze_button.pack(pady=5)
reset_button = tk.Button(root, text="Reset", command=reset)
reset_button.pack(pady=5)
output_text = scrolledtext.ScrolledText(root, width=60, height=20)
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()