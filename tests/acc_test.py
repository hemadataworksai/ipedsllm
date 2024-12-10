import os
import csv
from apps.langchain_bot.context.vectors_store_sentence_transformer import DocumentRetriever

# Initialize the DocumentRetriever
retriever = DocumentRetriever()

# Input and output paths
input_csv = './data/data_for_embedding/final/embedding_dataset_question_table_description_label.csv'
sql_scripts_path = './data/sql_scripts'
output_csv = './data/data_for_embedding/accuracy_results.csv'

# Helper function to extract true tables from SQL files
def get_true_tables(sql_dir):
    true_tables = {}
    for filename in os.listdir(sql_dir):
        if filename.endswith('.sql'):
            table_name = filename[:-4]  # Remove ".sql" to get the table name
            true_tables[table_name] = True
    return true_tables

# Get the true table names
true_tables = get_true_tables(sql_scripts_path)

# Read the questions from the input CSV
with open(input_csv, 'r') as infile:
    reader = csv.reader(infile)
    next(reader)  # Skip the header row
    questions = [row[0].strip() for row in reader if row[0].strip()]

# Evaluate accuracy
total_questions = len(questions)
correct_matches = 0
results = []

for question in questions:
    # Retrieve the top 3 similar table names for the question
    top_k = retriever.find_top_k_similar(question, k=3)
    retrieved_tables = [k['Table_Name'] for k in top_k]

    # Check how many retrieved tables are in the true tables
    matches = sum(1 for table in retrieved_tables if table in true_tables)
    correct_matches += matches

    # Store the result
    results.append({
        'Question': question,
        'Retrieved_Tables': ', '.join(retrieved_tables),
        'Matches': matches
    })

# Calculate accuracy
accuracy = correct_matches / (total_questions * 3) * 100  # Top 3 tables per question

# Save results to a CSV
with open(output_csv, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Question', 'Retrieved_Tables', 'Matches'])  # Write header
    for result in results:
        writer.writerow([result['Question'], result['Retrieved_Tables'], result['Matches']])

print(f"Accuracy: {accuracy:.2f}%")
print(f"Detailed results have been saved to {output_csv}")
