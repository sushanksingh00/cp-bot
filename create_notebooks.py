import os
import nbformat as nbf

def create_notebook(filename, cells):
    nb = nbf.v4.new_notebook()
    nb['cells'] = []
    
    for cell_type, content in cells:
        if cell_type == 'markdown':
            nb['cells'].append(nbf.v4.new_markdown_cell(content))
        elif cell_type == 'code':
            nb['cells'].append(nbf.v4.new_code_cell(content))
            
    with open(filename, 'w') as f:
        nbf.write(nb, f)
        
os.makedirs("notebooks", exist_ok=True)

# 01 Data Collection
create_notebook("notebooks/01_data_collection.ipynb", [
    ('markdown', '# Phase 2 & 3: Data Collection and Cleaning\nThis notebook demonstrates extracting the raw data from PostgreSQL and cleaning it.'),
    ('code', 'import sys, os\nsys.path.append(os.path.abspath(".."))\nfrom ml.data_collection import extract_raw_dataset\nfrom ml.cleaning import clean_data\nimport pandas as pd'),
    ('code', '# Extract Data\nraw_df = extract_raw_dataset("../ml/data/raw_dataset.csv")\nraw_df.head()'),
    ('code', '# Clean Data\nclean_df = clean_data("../ml/data/raw_dataset.csv", "../ml/data/cleaned_dataset.csv")\nclean_df.info()')
])

# 02 EDA
create_notebook("notebooks/02_eda.ipynb", [
    ('markdown', '# Phase 4: Exploratory Data Analysis\nAnswering key questions about CP Bot user performance.'),
    ('code', 'import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\ndf = pd.read_csv("../ml/data/cleaned_dataset.csv")\nfeatures_df = pd.read_csv("../ml/data/features.csv")\n\nsns.set_theme(style="whitegrid")'),
    ('markdown', '### Q1: How does problem difficulty affect solve probability?'),
    ('code', 'plt.figure(figsize=(10, 6))\nsns.histplot(data=df, x="problem_rating", hue="solved", multiple="stack", bins=20)\nplt.title("Problem Rating vs Solve Probability")\nplt.show()'),
    ('markdown', '### Q4: Does rating difference predict success?'),
    ('code', 'plt.figure(figsize=(10, 6))\nsns.boxplot(data=features_df, x="solved", y="rating_difference")\nplt.title("Rating Difference by Solve Outcome")\nplt.show()')
])

# 03 Feature Engineering
create_notebook("notebooks/03_feature_engineering.ipynb", [
    ('markdown', '# Phase 5: Feature Engineering\nSimulating the chronological generation of features.'),
    ('code', 'import sys, os\nsys.path.append(os.path.abspath(".."))\nfrom ml.features import generate_features'),
    ('code', '# Generate Features\nfeat_df = generate_features("../ml/data/cleaned_dataset.csv", "../ml/data/features.csv")\nfeat_df.head()')
])

# 04 Model Training
create_notebook("notebooks/04_model_training.ipynb", [
    ('markdown', '# Phase 6: Model Training\nTraining Logistic Regression, Random Forest, and XGBoost.'),
    ('code', 'import sys, os\nsys.path.append(os.path.abspath(".."))\nfrom ml.train import train_and_evaluate\n\nresults = train_and_evaluate("../ml/data/features.csv", "../ml/models")')
])

# 05 Model Evaluation
create_notebook("notebooks/05_model_evaluation.ipynb", [
    ('markdown', '# Phase 7 & 8: Model Evaluation and Explainability\nComparing models and explaining the best one.'),
    ('code', 'import pandas as pd\nimport joblib\nimport shap\nimport matplotlib.pyplot as plt\n\nmodel = joblib.load("../ml/models/best_model.pkl")\nprint(model)')
])

print("Notebooks created successfully.")
