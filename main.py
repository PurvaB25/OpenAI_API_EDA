import openai
import pandas as pd
import os
from messages import initial_messages

# Set your OpenAI API key
openai.api_key = "sk-proj-eX1GCPhH4RSXjkB12X9aT3BlbkFJf30CtDoAAs8MpFZjefOu"

# Define the path to the CSV file within your project directory
csv_file_path = os.path.join("/Users/purvabadve/PycharmProjects/EDA_OpenAI/venv/lib/data", "youtube.csv")

def read_csv_file(file_path):
    """
    Read a CSV file and return a DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        return str(e)

def summarize_dataframe(df):
    """
    Summarize the DataFrame to include in the conversation.
    """
    summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "dtypes": df.dtypes.to_dict(),
        "head": df.head(5).to_dict(orient="records"),  # Limit to first 5 rows
        "missing_values": df.isnull().sum().to_dict(),
        "unique_rows": len(df.drop_duplicates())
    }
    return summary

# Read the CSV file into a DataFrame using the predefined csv_file_path
dataframe = read_csv_file(csv_file_path)

if isinstance(dataframe, pd.DataFrame):
    print("CSV file loaded successfully.")
else:
    print(f"Error loading CSV file: {dataframe}")
    exit()

# Summarize the DataFrame
dataframe_summary = summarize_dataframe(dataframe)

# Add the DataFrame summary to the initial messages
initial_messages.append({
    "role": "user",
    "content": f"Here is the summary of the data:\n\n"
               f"Number of Rows: {dataframe_summary['rows']}\n"
               f"Number of Columns: {dataframe_summary['columns']}\n"
               f"Column Names: {dataframe_summary['column_names']}\n"
               f"Data Types: {dataframe_summary['dtypes']}\n"
               f"First Few Rows: {dataframe_summary['head']}\n"
               f"Missing Values: {dataframe_summary['missing_values']}\n"
               f"Unique Rows: {dataframe_summary['unique_rows']}\n\n"
               "Please provide the steps to clean and analyze this data."
})

while True:
    # Get user input
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chat.")
        break

    # Add the user input to the messages
    initial_messages.append({"role": "user", "content": user_input})

    # Create a chat completion using the specified model and parameters
    completion = openai.chat.completions.create(
        model="gpt-4",
        messages=initial_messages,
        max_tokens=300,
        temperature=0.3,
    )

    # Extract the assistant's response
    assistant_message = completion.choices[0].message.content

    # Print the assistant's response
    print(f"Assistant: {assistant_message}")

    # Add the assistant's response to the messages
    initial_messages.append({"role": "assistant", "content": assistant_message})