import pandas as pd
from langchain_ollama import OllamaLLM  # Correct import for Ollama
from langchain.prompts import PromptTemplate

# Initialize Ollama model
llm = OllamaLLM(model="llama3.2:latest")

# Define a prompt template for energy analysis
prompt = PromptTemplate(
    input_variables=["data_summary"],
    template="Analyze the following energy data and suggest optimizations: {data_summary}"
)

# Use the new chaining syntax instead of LLMChain
chain = prompt | llm

# Load the dataset
data = pd.read_csv("/Users/rajin/Developer/UNI/SEM10-MACHINE-LEARNING-PROJECT/Collection/extracted/energy_iter9.csv")

# Generate a summary from the latest row of the dataset
latest_data = data.tail(1).iloc[0]  # Get the latest row of data
data_summary = f"""
Peak generation was {latest_data['DayPeakGen(MW)']}MW during the day and {latest_data['EveningPeakGen(MW)']}MW in the evening.
Maximum demand reached {latest_data['MaxDemand(MW)']}MW. Temperature was {latest_data['Temp(C)']}°C.
Is it a holiday: {'Yes' if latest_data['IsHoliday'] == 1 else 'No'}.
"""

# Run the chain with the new .invoke() method
response = chain.invoke({"data_summary": data_summary})
print("Energy Analysis:\n", response)