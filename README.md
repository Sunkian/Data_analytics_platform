# Natural Language to SQL with Llama 3 70B

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

