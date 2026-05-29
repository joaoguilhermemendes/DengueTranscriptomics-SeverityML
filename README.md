# Dengue Transcriptomic Analysis

![Status](https://img.shields.io/badge/status-in%20development-yellow)

Use public RNA-seq gene expression data from dengue patients to explore transcriptomic patterns associated with dengue severity by exploratory bioinformatics and computational analysis.

---

This project was created as a practical learning experience in:
- transcriptomic data analysis
- RNA-seq preprocessing
- exploratory data analysis (EDA)
- dimensionality reduction
- bioinformatics workflows

The dataset used in this project is the NCBI GEO `GSE279208`, which contains transcriptomic data from healthy controls and dengue patients with different clinical conditions.

## Tools and Libraries

Python (Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn) and Jupyter Notebook
 
## Project Structure

```text
01_Data_Collection.ipynb
02_Data_Cleaning.ipynb
03_Exploratory_Data_Analysis.ipynb
(In development...)
```

## Current Workflow

```text
Raw GEO sample files
↓
Data cleaning and preprocessing
↓
Log transformation
↓
Exploratory visualization and PCA
↓
(In development...)
```

## Current Analyses

* TPM preprocessing and cleaning
* Log-transformation
* Boxplots and density plots
* Correlation heatmaps
* PCA visualization and potential outlier identification

## Next Steps

* Differential gene expression analysis
* Volcano plots
* Functional enrichment analysis
* Clustering and machine learning approaches
