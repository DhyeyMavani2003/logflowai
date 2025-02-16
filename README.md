# TreeHacks 2025 Project

Welcome to the TreeHacks 2025 repository! This project demonstrates advanced capabilities ranging from deep learning using PyTorch to hybrid data operations via an InterSystems IRIS vector store, alongside large-scale log/data analytics using HDFS trace benchmarks.

## Table of Contents

- [Project Overview](#project-overview)
- [Neural Network Architecture](#neural-network-architecture)
- [Dataset and Preprocessing](#dataset-and-preprocessing)
- [Model Architecture](#model-architecture)
- [Training and Evaluation](#training-and-evaluation)
- [Deployment with FastAPI](#deployment-with-fastapi)
- [Database and Vector Store Architecture](#database-and-vector-store-architecture)
- [IRIS Vector Store Overview](#iris-vector-store-overview)
- [Document Ingestion and Similarity Search](#document-ingestion-and-similarity-search)
- [HDFS Trace Bench Data](#hdfs-trace-bench-data)
- [Quickstart](#quickstart)
- [Project Structure](#project-structure)
- [Dependencies and Installation](#dependencies-and-installation)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project integrates multiple components:

- **Neural Network Architecture:** A deep learning model built in PyTorch, trained on CSV files (including preprocessed HDFS trace benchmarks) to predict outcomes based on historical data.
- **Database Architecture:** An IRIS vector store is employed for advanced document storage and similarity searches using SQL-backed operations.
- **HDFS Trace Bench Data:** Large-scale HDFS trace benchmarks provide performance metrics and error patterns, offering rich data for analytics and model training.

## Neural Network Architecture

The model is implemented in PyTorch, using data loaded from several CSV files including standard splits (train, val, test) and benchmark data. A custom CSVDataset processes numerical features and converts targets into tensors.

## Dataset and Preprocessing

- Data is sourced from multiple CSV files:
    - Standard splits: train.csv, val.csv, test.csv
    - Benchmark dataset: rowNumberResult.csv (contains performance metrics from HDFS traces)
- Preprocessing involves cleaning data, extracting numerical features, and preparing tensors for model input.

## Model Architecture

The neural network (encapsulated in the Net class) includes:

- **Input Layer:** Accepts a dynamic set of features.
- **Four Hidden Layers:**
    - Layer 1: Linear (input → 128) → BatchNorm → ReLU → Dropout (0.3)
    - Layer 2: Linear (128 → 64) → BatchNorm → ReLU → Dropout (0.3)
    - Layer 3: Linear (64 → 32) → BatchNorm → ReLU → Dropout (0.3)
    - Layer 4: Linear (32 → 16) → BatchNorm → ReLU → Dropout (0.3)
- **Output Layer:** A final linear layer producing a single output, transformed via sigmoid activation to yield probabilities.

## Training and Evaluation

- **Loss Function:** Utilizes nn.BCEWithLogitsLoss() to handle raw logits.
- **Optimizer:** Adam optimizer with a learning rate typically set to 0.001.
- **Metrics:** Tracks training loss, accuracy, True Positive Rate (TPR), and True Negative Rate (TNR).
- **Model Saving:** The trained weights are saved as model.pth for deployment and inference.

## Deployment with FastAPI

- A FastAPI server (app.py) is set up to load the trained model and serve predictions via a /predict endpoint.
- The endpoint expects JSON input (a list of feature values) and returns the predicted probability and class.

## Database and Vector Store Architecture

This project leverages an advanced vector store implemented with the InterSystems IRIS driver:

- **Vectorized Document Storage:** Documents are embedded and stored in a persistent SQL table.
- **Robust Search and Reconnection:** The IRIS-based retriever supports similarity searches, ensuring persistent connections to the vector store.

## IRIS Vector Store Overview

Documents are transformed into embeddings and stored within the IRIS vector store. This allows for efficient similarity searches and analytical queries using SQL-based operations.

## Document Ingestion and Similarity Search

- **Ingestion:** Demonstrated in notebooks like langchain_demo.ipynb, where documents are processed and embedded.
- **Search:** The embedded vectors are used to perform similarity searches, facilitating quick retrieval of related documents.

## HDFS Trace Bench Data

The project incorporates HDFS trace benchmarks, particularly through files like rowNumberResult.csv, which contains measurements and performance metrics. These benchmarks are used for:

- Analyzing performance characteristics.
- Feeding relevant metrics into the neural network.
- Enriching the document store for similarity queries.

## Quickstart

1. **Clone the Repository:**
        ```bash
        git clone https://github.com/yourusername/treehacks-2025.git
        cd treehacks-2025
        ```

2. **Set Up the Environment:**
        ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate
        ```

3. **Install Dependencies:**
        ```bash
        pip install -r requirements.txt
        ```

4. **Run Data Preprocessing and Training:**
        ```bash
        python preprocess.py
        python train.py
        ```

5. **Start the FastAPI Server:**
        ```bash
        uvicorn app:app --reload
        ```

6. **Open and Run the Notebooks:** Explore Jupyter notebooks such as:
        - main.ipynb for training and evaluation.
        - langchain_demo.ipynb for document ingestion and similarity search features.

## Project Structure

```
treehacks-2025/
├── .env                      # Environment configuration
├── Apps/                    # Demos (e.g., simpleFlask demo)
├── data/                    # Datasets (HDFS logs, reviews, etc.)
├── demo/                    # Jupyter notebooks:
│   ├── iris_notebook_container.ipynb
│   ├── IRISDatabaseOperationsUsingSQL.ipynb
│   ├── langchain_demo.ipynb
│   └── llama_demo.ipynb
├── iris-env/                # Python virtual environment for IRIS operations
├── neural-network/          # Neural network training, evaluation, and FastAPI deployment:
│   ├── main.ipynb           # Primary notebook
│   ├── app.py               # FastAPI server
│   ├── train.py             # Model training script
│   ├── preprocess.py        # Data preprocessing script
│   └── model.pth            # Saved model weights
├── CSV Files:               # Data splits and HDFS benchmark file:
│   ├── train.csv
│   ├── val.csv
│   ├── test.csv
│   └── rowNumberResult.csv
└── requirements.txt         # Python dependencies list
```

## Dependencies and Installation

Key dependencies include:

- **PyTorch:** For deep learning model construction and training.
- **FastAPI and Uvicorn:** For deploying the inference API.
- **Pandas & NumPy:** For data manipulation.
- **scikit-learn:** For data splitting and metric computation.
- **InterSystems IRIS driver:** For vector store operations.

Install them via:
```bash
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests. For major changes, open an issue to discuss your ideas before proceeding.

## License

This project is licensed under the MIT License.
