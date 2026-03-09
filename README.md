# Triage ASG Creation Automation

Automates the creation of Analytic Sub Groups (ASGs) on the [TKE AxionRay](https://tke.axionray.com/) platform using Selenium. Reads QCR records from a CSV file, applies the appropriate filters on the web UI, and creates ASGs for each row.

## Project Structure

```
Triage_AGS_Creation_Automation/
├── triage_asg_creator/          # Main package
│   ├── __init__.py              # Exports create_legacy_qcr_asg, create_eox_qcr_asg
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
from triage_asg_creator import create_legacy_qcr_asg

create_legacy_qcr_asg(
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

Each module handles two cases per row based on available data:

### Case 1: Part Number is present

1. Navigates to the Investigate page and selects the appropriate dataset.
2. Drags **Primary Issue ID** into the filter area and applies the value.
3. Drags **Part Number** into the filter area and applies each comma-separated value.
4. Saves the ASG with the given title.
5. If a **parent ASG already exists** (duplicate detected), it creates a second, more specific ASG by additionally filtering on **QCR ID**, then adds a description referencing the parent ASG.

### Case 2: Only QCR ID is present (no Part Number)

1. Navigates to the Investigate page and selects the appropriate dataset.
2. Drags **Primary Issue ID** into the filter area and applies the value.
3. Drags **QCR ID** into the filter area and applies the value.
4. Saves the ASG with the given title.

### Rows with missing data

Rows that lack both `part_number` and `qcr_id` (or `primary_issue_id`) are skipped and logged with a status of `no part number or qcr id or primary issue id`.

## Output CSV Format

| Column | Description |
|---|---|
| `qcr_id` | QCR ID from input |
| `primary_issue_id` | Primary Issue ID from input |
| `part_number` | Part Number(s) from input |
| `title` | ASG title from input |
| `parent_href` | URL of the parent/existing ASG (if duplicate detected) |
| `parent_label` | Label of the parent/existing ASG (if duplicate detected) |
| `status` | Creation result (see USAGE.md for all possible values) |
| `success` | `True` if created successfully, `False` otherwise |

## Notes

- The script uses a **persistent Chrome profile** (`selenium_chrome_profile`) so login sessions are preserved across runs.
- All UI interactions include `time.sleep()` pauses to account for varying page load times.
- If a row fails, the error is captured in the output CSV `status` column and the script continues to the next row.
- All CSV columns are read as strings (`dtype=str`) to prevent numeric values from gaining decimal suffixes.
