import csv
from apps.langchain_bot.context.vectors_store_sentence_transformer import DocumentRetriever

# Initialize the DocumentRetriever
retriever = DocumentRetriever()

# Input and output file paths
input_csv = './data/data_for_embedding/final/embedding_dataset_question_table_description_label.csv'
output_csv = './data/data_for_embedding/Top_3_Table_Names.csv'

# Read the questions from the input CSV
with open(input_csv, 'r') as infile:
    reader = csv.reader(infile)
    next(reader)  # Skip the header row
    seen = set()
    questions = []
    for row in reader:
        question = row[0].strip()
        if question and question not in seen:
            seen.add(question)
            questions.append(question)  # Maintain order while removing duplicates

# Prepare to write results
with open(output_csv, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Question', 'Top_3_Table_Names'])  # Write header

    for question in questions:
        # Retrieve the top 3 similar table names for the question
        top_k = retriever.find_top_k_similar(question, k=3)
        table_names = ', '.join([k['Table_Name'] for k in top_k])

        # Write the question and corresponding table names to the output file
        writer.writerow([question, table_names])

print(f"Results have been written to {output_csv}")
