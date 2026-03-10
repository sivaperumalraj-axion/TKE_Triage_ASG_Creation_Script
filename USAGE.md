# Usage Guide

## Modules

The `triage_asg_creator` package provides two functions for different QCR datasets:

| Function | Dataset | Workspace ID |
|---|---|---|
| `create_asg_legacy_with_predetermined_filters` | Legacy QCR | `68d297b0131207fba5b42844` |
| `create_asg_eox_with_predetermined_filters` | EOX QCR | `683851f685f19b4445d29bb8` |

Both functions share the same signature and behavior — only the target workspace and filter element selectors differ.

## Function Signature

```python
create_asg_legacy_with_predetermined_filters(
    *,
    csv_path: str,
    output_path: str,
    qcr_id_col: str,
    primary_issue_id_col: str,
    part_number_col: str,
    title_col: str,
) -> pd.DataFrame
```

All arguments are **keyword-only**.

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `csv_path` | `str` | Path to the input CSV file |
| `output_path` | `str` | Path for the output CSV (timestamp is appended automatically). Pass `None` to use a default name in the current directory. |
| `qcr_id_col` | `str` | Column name in the CSV that contains QCR IDs |
| `primary_issue_id_col` | `str` | Column name for Primary Issue IDs |
| `part_number_col` | `str` | Column name for Part Numbers |
| `title_col` | `str` | Column name for ASG titles |

### Returns

A `pd.DataFrame` with the creation results for each row.

---

## Examples

### Legacy QCR

```python
from triage_asg_creator import create_asg_legacy_with_predetermined_filters

result = create_asg_legacy_with_predetermined_filters(
    csv_path="Triage ASG Creation Mar 09 2026 (Legacy)- Test Records.csv",
    output_path="output/legacy_result.csv",
    qcr_id_col="qcr_id",
    primary_issue_id_col="primary_issue_id",
    part_number_col="part_number",
    title_col="title",
)
```

**Expected CSV columns:** `qcr_id`, `primary_issue_id`, `part_number`, `title`

Sample input:

```csv
primary_issue_id,part_number,qcr_id,title
11.2.1,,338384,QCR ID: 338384 | Missing Selector Tape and Mounting Brackets
11.1.1,"905081-H06-42, 461XR004",338391,QCR ID: 338391 | Stripped Thread on Center Opening Hanger Plate
```

### EOX QCR

```python
from triage_asg_creator import create_asg_eox_with_predetermined_filters

result = create_asg_eox_with_predetermined_filters(
    csv_path="EOX QCR update_05_03_26 - ASG.csv",
    output_path="output/eox_result.csv",
    qcr_id_col="QCR Id",
    primary_issue_id_col="Primary Issue ID",
    part_number_col="Part Number Ax",
    title_col="Title",
)
```

**Expected CSV columns:** `QCR Id`, `Primary Issue ID`, `Part Number Ax`, `Title`

Sample input:

```csv
QCR Id,Primary Issue ID,Part Number Ax,Title
338165,11.2.1,"8000815546, 8000865927, 8000866014",QCR ID: 338165 | GPCR Fixture Issue Kit Incomplete
338122,9.0.4,,QCR ID: 338122 | CIB-2 Board Ethernet Ports Defective
```

### Using in a Jupyter Notebook

```python
from triage_asg_creator import create_asg_legacy_with_predetermined_filters

result = create_asg_legacy_with_predetermined_filters(
    csv_path="input.csv",
    output_path=None,
    qcr_id_col="qcr_id",
    primary_issue_id_col="primary_issue_id",
    part_number_col="part_number",
    title_col="title",
)

# Inspect the results inline
result
```

---

## Workflow

1. Call the function. A Chrome window opens automatically.
2. **Log in to TKE AxionRay** in the browser.
3. Return to the terminal/notebook and press **Enter** to start the automation.
4. The script processes each CSV row and creates ASGs based on available data.
5. Results are saved to the output path (or a timestamped default) and returned as a DataFrame.

---

## Filter Logic

The function chooses which filters to apply based on which columns have data:

| Priority | Condition | Filters Applied |
|---|---|---|
| 1 | Primary Issue ID + Part Number + QCR ID all present | Primary Issue ID, Part Number (with duplicate detection and QCR ID refinement) |
| 2 | Primary Issue ID + Part Number present | Primary Issue ID, Part Number |
| 3 | Primary Issue ID + QCR ID present | Primary Issue ID, QCR ID |
| — | None of the above | Row skipped |

### Duplicate Detection (Case 1 only)

When all three fields are present, the function first creates an ASG with Primary Issue ID + Part Number. If a parent ASG already exists (duplicate detected):

1. A second, narrower ASG is created with all three filters (Primary Issue ID + Part Number + QCR ID).
2. A description is added linking back to the parent ASG.

If the first submission succeeds but no duplicate is detected, the result is checked:
- If submitted successfully but without proper filters, it is flagged for deletion.
- If submission failed, it is flagged for manual creation.

---

## Output Status Values

| Status | Success | Meaning |
|---|---|---|
| `created` | `True` | ASG created successfully |
| `Created with Primary Issue ID, Part Number and QCR ID, and the description is added` | `True` | Duplicate detected, narrower ASG created with description linking to parent |
| `Created with Primary Issue ID, Part Number and QCR ID, but the description is not added` | `False` | Narrower ASG created but description failed |
| `Created. But the ASG is trash. Need too delete it.` | `False` | Submission completed but without proper duplicate handling; needs deletion |
| `Need to create the ASG manually.` | `False` | Submission did not complete; manual creation required |
| `no title` | `False` | Row skipped because the title column is empty |
| `no part number or qcr id or primary issue id` | `False` | Row skipped due to insufficient filter data |
| `error: <message>` | `False` | An exception occurred during processing |
