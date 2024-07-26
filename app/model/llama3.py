from transformers import pipeline

def load_llama_model():
    return pipeline('text2text-generation', model="meta-llama/Meta-Llama-3-70B")

def query_model(question):
    model = load_llama_model()
    sql_query = model(question)[0]['generated_text']
    return sql_query

if __name__ == '__main__':
    question = "You are a powerful text-to-SQL model. Give me a simple SQL code."
    sql_query = query_model(question)
    print("Natural Language Question:", question)
    print("Generated SQL Query:", sql_query)
