# Natural Language to SQL with Llama 3 70B

## Task

The goal is to design, implement, and evaluate a system that uses the Llama 3 70B model to translate natural language questions about business data into SQL queries.

1. Design and implement a solution using the Llama 3 70B model to convert natural language questions into SQL queries. Consider that this would work in a production environment.

2. Create a demonstration of your solution's capabilities. This should include handling various types of questions and database complexities you think are relevant.

3. Develop a method to evaluate the performance and effectiveness of your solution.

4. Prepare a report discussing your approach, the challenges you encountered, and your ideas
for further improvements or research directions.


## Approach

A small draft of the proposed architecture can be found in the 'images/Graph.png'.

Challenges : 
- First of all, the Llama3 70B model as it is is a big LLM, very hard to deploy at the Edge. 
Two approaches can be explored from there.
A Cloud solution to host it (on a AWS endpoint for example) seemed to be the fastest, most practical solution especially for a production environment.
However, techniques like quantization, model compression/distillation (transfering knowledge from a large, expensive model to a smaller one) can be applied in order to reduce the size of the model while preserving its capabilities. 
Alternative models can be chosen to run locally, like the latests Llama3.1 8B.
Also, the Llama3 70B model being outdated, the new 3.1 70B can be used here.

- Another challenge was to find the right prompt to call the model. The prompt had to be designed in such way that the models would understand perfectly the query: this involed telling the model about the chosen database's architecture (Schema, Tables, etc), giving it an elaborate context window. Techniques to find the appropriate prompts have been investigated intensively the past few years. Also, I got inspired here by multiple sources.



## How to use

1. Create a virtual environment:

```sh
conda create -n platform python=3.11
```

2. Activate the venv:

```sh
conda activate platform
```

3. Updata pip and Install the requirements: 

```sh
python3.11 -m pip install --upgrade pip
pip3 install -r requirements.txt
```

4. Make sure your database is active

5. Run the Flask API
```sh
run flask_api.py
```

6. Run the Streamlit app
```sh
streamlit run streamlit_platform.py
```

