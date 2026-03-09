# Usage Guide

## Modules

The `triage_asg_creator` package provides two modules for different QCR datasets:

| Function | Dataset | Workspace |
|---|---|---|
| `create_legacy_qcr_asg` | Legacy QCR | `68d297b0131207fba5b42844` |
| `create_eox_qcr_asg` | EOX QCR | `683851f685f19b4445d29bb8` |

Both functions share the same signature and behavior — only the target workspace and filter element selectors differ.

## Function Signature

```python
create_legacy_qcr_asg(
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
| `output_path` | `str` | Path for the output CSV (timestamp is appended). Pass `None` to use a default name. |
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
from triage_asg_creator import create_legacy_qcr_asg

result = create_legacy_qcr_asg(
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
from triage_asg_creator import create_eox_qcr_asg

result = create_eox_qcr_asg(
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
from triage_asg_creator import create_legacy_qcr_asg

result = create_legacy_qcr_asg(
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

1. Run the function. A Chrome window opens.
2. **Log in to TKE AxionRay** in the browser.
3. Return to the terminal/notebook and press **Enter**.
4. The automation processes each CSV row and creates ASGs.
5. Results are saved to the output path (or a timestamped default) and returned as a DataFrame.

## Output Status Values

| Status | Meaning |
|---|---|
| `created` | ASG created successfully |
| `existing, need manual creation` | A duplicate ASG was detected; manual intervention required |
| `Parent ASG already exists, need manual creation` | Both the broad and specific ASG already exist |
| `Created with Primary Issue ID, Part Number and QCR ID, and the description is added` | Duplicate detected, narrower ASG created with description linking to parent |
| `no part number or qcr id or primary issue id` | Row skipped due to missing required data |
| `error: <message>` | An exception occurred during processing |
