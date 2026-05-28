from pathlib import Path
import pandas as pd


def check_gene_consistency(files):
    """
    Checks whether all RNA-seq sample files contain:

    - the same number of genes
    - the same gene set
    - the same gene order

    Parameters
    ----------
    files : list
        List of file paths.

    Returns
    -------
    bool
        True if all files are consistent.
    """

    reference_df = pd.read_csv(files[0], sep="\t")

    reference_genes = reference_df["Gene ID"].tolist()

    print(f"Reference file: {Path(files[0]).name}")
    print(f"Total genes: {len(reference_genes)}\n")

    all_consistent = True

    for file in files[1:]:

        df = pd.read_csv(file, sep="\t")

        current_genes = df["Gene ID"].tolist()

        same_gene_count = len(reference_genes) == len(current_genes)

        same_gene_set = set(reference_genes) == set(current_genes)

        same_gene_order = reference_genes == current_genes

        print(f"{Path(file).name}")
        print(f"Same gene count: {same_gene_count}")
        print(f"Same gene set: {same_gene_set}")
        print(f"Same gene order: {same_gene_order}\n")

        if not (
            same_gene_count
            and same_gene_set
            and same_gene_order
        ):
            all_consistent = False

    return all_consistent