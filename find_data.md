# HAR Privacy Analyzer & Rule Generator

This command-line tool analyzes `.har` files to find where personal or sensitive data is being transmitted. It then allows you to interactively inspect these requests and automatically generate importable rules for [HTTP Toolkit](https://httptoolkit.com/) to block or modify this traffic.

This is primarily designed for app privacy analysis, security research, and quality assurance testing.

## Features

*   **Sensitive Data Discovery**: Scans entire HAR files for any number of specified data strings (e.g., email, name, device IDs).
*   **Interactive Analysis**: Presents a clean, numbered list of all findings for easy review.
*   **Detailed Context**: View the exact location (URL, Request Body, etc.) and a pretty-printed JSON snippet for any finding.
*   **Powerful Filtering**: Narrow your search to specific HTTP methods (e.g., `POST`, `GET`).
*   **Automatic Rule Generation**: Creates HTTP Toolkit compatible `.json` rule files from your selected findings.
*   **Flexible Blocking Actions**: Choose how to block traffic:
    1.  Close the connection (hard block).
    2.  Return a `403 Forbidden` error.
    3.  Pause the request for manual inspection and modification.
*   **Safe by Default**: Generated rule files automatically include a "pass-through" rule to ensure non-blocked traffic continues to work correctly.

## Requirements

*   **Python 3.x**: The script is written in Python and uses standard libraries, so no external packages need to be installed with `pip`.

## How to Run

1.  Save the script as `analyze_har.py` (or any other `.py` name).
2.  Open a terminal or command prompt.
3.  Navigate to the directory where you saved the script.
4.  Run the script using the command structure below.

### Command-Line Arguments

| Argument     | Required? | Description                                                                                             | Example                                             |
| :----------- | :-------- | :------------------------------------------------------------------------------------------------------ | :-------------------------------------------------- |
| `har_file`   | **Yes**   | The path to the `.har` file you want to analyze.                                                        | `session.har`                                       |
| `--data`     | **Yes**   | One or more pieces of data to search for. Separate multiple items with spaces.                         | `--data my.email@test.com b7a42a43bb5cdeba`         |
| `--method`   | No        | (Optional) Filters the search to only include specific HTTP methods. Case-insensitive.                | `--method POST` or `--method GET PUT`               |

