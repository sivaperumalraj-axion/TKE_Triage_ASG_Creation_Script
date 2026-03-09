# Triage ASG Creation Automation

Automates the creation of Analytic Sub Groups (ASGs) on the [TKE AxionRay](https://tke.axionray.com/) platform using Selenium. Reads QCR records from a CSV file, applies the appropriate filters on the web UI, and creates ASGs for each row.

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

## Input CSV Format

The input CSV must contain the following columns:

| Column | Description | Required |
|---|---|---|
| `qcr_id` | The QCR ID (e.g. `338165`) | Yes |
| `primary_issue_id` | Primary Issue ID code (e.g. `11.2.1`) | Yes |
| `part_number` | Comma-separated part numbers (e.g. `8001339599, 8000723386`). Leave blank if not applicable. | No |
| `title` | ASG title (e.g. `QCR ID: 338160 \| Incorrect EMT Fittings`) | Yes |

Example:

```csv
part_number,qcr_id,title,primary_issue_id
"8001339599, 8000723386",338160,QCR ID: 338160 | Incorrect EMT Fittings Provided in Kit 8001339599,11.2.3
```

## Usage

1. Update the input CSV filename in `main.py` (bottom of the file) to point to your data:

   ```python
   df = pd.read_csv("your_input_file.csv")
   df = create_asg(df, 'qcr_id', 'primary_issue_id', 'part_number', 'title')
   ```

2. Run the script:

   ```bash
   python main.py
   ```

3. A Chrome window will open. **Log in to TKE AxionRay manually**, then return to the terminal and press **Enter** to start the automation.

4. The script will iterate through each CSV row and create ASGs automatically.

5. Results are saved to the `output/` folder as a timestamped CSV (e.g. `asg_creation_result_mar_09_03_26_15_34_44.csv`).

## How It Works

The script handles two cases per row based on available data:

### Case 1: Part Number is present

1. Navigates to the Investigate page and selects the **QCR** dataset.
2. Drags **Primary Issue ID** into the filter area and applies the value.
3. Drags **Part Number** into the filter area and applies each comma-separated value.
4. Saves the ASG with the given title.
5. If a **parent ASG already exists** (duplicate detected), it creates a second, more specific ASG by additionally filtering on **QCR ID**, then adds a description referencing the parent ASG.

### Case 2: Only QCR ID is present (no Part Number)

1. Navigates to the Investigate page and selects the **QCR** dataset.
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
| `status` | Creation result: `created`, `existing, need manual creation`, or `error: <message>` |

## Key Functions

| Function | Purpose |
|---|---|
| `create_driver()` | Initializes Chrome with a persistent user profile |
| `select_datasets()` | Navigates to the workspace and selects the QCR dataset |
| `primary_issue_id_filter_select()` | Drags Primary Issue ID into the filter panel |
| `primary_issue_id_filter_apply_at_first_filter()` | Searches and selects a Primary Issue ID value |
| `part_number_filter_select()` | Drags Part Number into the filter panel |
| `part_number_filter_apply_at_second_filter()` | Searches and selects each part number value |
| `qcr_id_filter_select()` | Drags QCR ID into the filter panel |
| `qcr_id_filter_apply_at_second_filter()` | Applies QCR ID as the 2nd filter |
| `qcr_id_filter_apply_at_thrid_filter()` | Applies QCR ID as the 3rd filter |
| `save_as_asg()` | Opens the save dialog and enters the ASG title |
| `submit_asg()` | Clicks the create/save button |
| `is_existing_asg()` | Checks if a duplicate ASG chip/link appeared after submission |
| `add_description()` | Switches to Overview tab, types a description, and waits for autosave |
| `create_asg()` | Main orchestrator that loops through the DataFrame and coordinates all steps |

## Notes

- The script uses a **persistent Chrome profile** (`selenium_chrome_profile`) so login sessions are preserved across runs.
- All UI interactions include `time.sleep()` pauses to account for varying page load times.
- If a row fails, the error is captured in the output CSV `status` column and the script continues to the next row.
