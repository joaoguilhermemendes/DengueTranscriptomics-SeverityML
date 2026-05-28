import pandas as pd


def load_metadata():
    """
    Creates and returns the sample metadata dataframe.

    Returns
    -------
    pd.DataFrame
        Metadata dataframe containing:
        - sample_id
        - group
        - severity
    """

    metadata = {
        "sample_id": [
            "HCB1-21",
            "HCB2-21",
            "HCB3-21",
            "HCB4-21",
            "HCB5-21",
            "HCB6-21",
            "HCB7-21",
            "HCB8-21",
            "HCB9-21",
            "HCB10-21",
            "HCB11-21",

            "PTB1-21",
            "PTB1-22",
            "PTB2-21",
            "PTB2-22",
            "PTB3-21",
            "PTB3-22",
            "PTB4-21",
            "PTB5-21",
            "PTB6-21",
            "PTB7-21",
            "PTB8-21",
            "PTB9-21",
            "PTB10-21",
            "PTB11-21",
            "PTB12-21",
            "PTB13-21"
        ],

        "group": [
            *["control"] * 11,
            *["dengue"] * 16
        ],

        "severity": [
            *["healthy"] * 11,

            "severe",
            "warning",
            "warning",
            "warning",
            "warning",
            "warning",
            "warning",
            "warning",
            "warning",
            "warning",
            "warning",
            "severe",
            "warning",
            "warning",
            "severe",
            "warning"
        ]
    }

    metadata_df = pd.DataFrame(metadata)

    return metadata_df


if __name__ == "__main__":

    metadata_df = load_metadata()

    print(metadata_df.head())

    metadata_df.to_csv(
        "../../data/processed/sample_metadata.csv",
        index=False
    )

    print("\nMetadata saved successfully!")