# Triage ASG Creation Automation

Automates the creation of Analytic Sub Groups (ASGs) on the [TKE AxionRay](https://tke.axionray.com/) platform using Selenium. Reads QCR records from a CSV file, applies the appropriate filters on the web UI, and creates ASGs for each row.

## Project Structure

```
Triage_AGS_Creation_Automation/
├── triage_asg_creator/          # Main package
│   ├── __init__.py              # Exports both creation functions
│   ├── legacy_qcr.py            # ASG creation for the Legacy QCR dataset
│   └── eox_qcr.py               # ASG creation for the EOX QCR dataset
├── output/                      # Generated result CSVs
├── USAGE.md                     # Detailed usage guide with examples
├── README.md
└── .gitignore
```

## Prerequisites

- **Python 3.8+**
- **Google Chrome** installed
- **ChromeDriver** matching your Chrome version (managed automatically by `selenium` 4.x)
- A valid TKE AxionRay account with access to the target workspace

### Python Dependencies

```
selenium
pandas
```

Install with:

```bash
pip install selenium pandas
```

## Quick Start

```python
from triage_asg_creator import create_asg_legacy_with_predetermined_filters

create_asg_legacy_with_predetermined_filters(
    csv_path="your_input.csv",
    output_path="output/result.csv",
    qcr_id_col="qcr_id",
    primary_issue_id_col="primary_issue_id",
    part_number_col="part_number",
    title_col="title",
)
```

See [USAGE.md](USAGE.md) for full details, CSV formats, and examples for both modules.

## Input CSV Format

The input CSV must contain columns that map to these four required fields:

| Field | Description | Required |
|---|---|---|
| QCR ID | The QCR ID (e.g. `338165`) | Yes |
| Primary Issue ID | Primary Issue ID code (e.g. `11.2.1`) | Yes |
| Part Number | Comma-separated part numbers (e.g. `8001339599, 8000723386`). Leave blank if not applicable. | No |
| Title | ASG title (e.g. `QCR ID: 338160 \| Incorrect EMT Fittings`) | Yes |

## How It Works

The script determines which filters to apply based on which columns have data for each row:

### Case 1: Primary Issue ID + Part Number + QCR ID (all three present)

1. Navigates to the Investigate page and selects the appropriate dataset.
2. Applies **Primary Issue ID** and **Part Number** filters.
3. Saves the ASG with a light submit (no wait for overview tab).
4. If a **parent ASG already exists** (duplicate detected), creates a second, more specific ASG by additionally filtering on **QCR ID**, then adds a description referencing the parent.
5. If no duplicate but submission didn't complete, logs the row for manual creation.

### Case 2: Primary Issue ID + Part Number (no QCR ID)

1. Applies **Primary Issue ID** and **Part Number** filters.
2. Saves and submits the ASG.

### Case 3: Primary Issue ID + QCR ID (no Part Number)

1. Applies **Primary Issue ID** and **QCR ID** filters.
2. Saves and submits the ASG.

### Rows with missing data

- Rows without a **title** are skipped with status `no title`.
- Rows that lack sufficient filter columns are logged with status `no part number or qcr id or primary issue id`.

## Output CSV Format

| Column | Description |
|---|---|
| `qcr_id` | QCR ID from input |
| `primary_issue_id` | Primary Issue ID from input |
| `part_number` | Part Number(s) from input |
| `title` | ASG title from input |
| `parent_href` | URL of the parent/existing ASG (if duplicate detected) |
| `parent_label` | Label of the parent/existing ASG (if duplicate detected) |
| `status` | Creation result (see [USAGE.md](USAGE.md) for all possible values) |
| `success` | `True` if created successfully, `False` otherwise |

## Notes

- The script uses a **persistent Chrome profile** (`selenium_chrome_profile`) so login sessions are preserved across runs.
- All UI interactions include `time.sleep()` pauses to account for varying page load times.
- If a row fails, the error is captured in the output CSV `status` column and the script continues to the next row.
- All CSV columns are read as strings (`dtype=str`) to prevent numeric values from gaining decimal suffixes.
