const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL ||
    "http://127.0.0.1:8000/api";

export interface AutoFixStatistics {
    rows_before: number;
    rows_after: number;
    columns_after: number;
    duplicates_removed: number;
    missing_values_fixed: number;
    outliers_capped: number;
    datatype_conversions: number;
    constant_columns_removed: number;
    remaining_missing_values: number;
    remaining_duplicates: number;
    output_file_name: string;
    output_file_size_bytes: number;
}

export interface AutoFixResponse {
    success: boolean;
    message: string;
    dataset_id: string;
    download_file: string;
    statistics: AutoFixStatistics;
}

export async function autoFixDataset(
    datasetId: string
): Promise<AutoFixResponse> {

    const response = await fetch(
        `${API_BASE_URL}/autofix/${datasetId}`,
        {
            method: "POST",
        }
    );

    if (!response.ok) {
        const error = await response.json();

        throw new Error(
            error.detail || "Auto Fix failed."
        );
    }

    return response.json();
}
export function downloadCleanedDataset(
    filename: string
) {

    window.open(
        `${API_BASE_URL}/download-cleaned/${filename}`,
        "_blank"
    );

}
export async function getCleanedDatasets() {

    const response = await fetch(
        `${API_BASE_URL}/cleaned-datasets`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to fetch cleaned datasets."
        );
    }

    return response.json();

}
