from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
from datetime import datetime

def create_driver(wait_seconds: int = 30):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument(r"--user-data-dir=C:\Users\admin\selenium_chrome_profile")
    options.add_argument("--profile-directory=Default")  # or "Profile 1", "Profile 2", etc.
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, wait_seconds)
    return driver, wait

def select_datasets(driver: webdriver.Chrome, wait: WebDriverWait):
    driver.get("https://tke.axionray.com/workspace/683851f685f19b4445d29bb8/explore/investigate")
    # Dataset Selection
    toggle = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'input.MuiSwitch-input[aria-label="Deselect All Datasets"]')
    ))
    if toggle.is_selected():
        toggle.click()
        print("Toggle turned OFF.")
    else:
        print("Toggle already OFF.")
    qcr_dataset_el = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[value="QCR"]')))  
    qcr_dataset_el.click()

    next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next')]")))
    next_btn.click()
    time.sleep(1)

def primary_issue_id_filter_select(driver: webdriver.Chrome, wait: WebDriverWait):
    # The First Filter
    primary_issue_id_source = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '[data-testid="customAttributes.Primary Issue ID Ax_Primary Issue ID_QCR"]')
    ))

    primary_issue_id_target = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '[data-testid="drop-area-filter-new-and"]')
    ))

    actions = ActionChains(driver)
    actions.drag_and_drop(primary_issue_id_source, primary_issue_id_target).perform()
    time.sleep(2)

def primary_issue_id_filter_apply_at_first_filter(driver: webdriver.Chrome, wait: WebDriverWait, primary_issue_id: str):
    options_btn = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, '[data-testid="multiple-selector-button"]')
    ))
    options_btn.click()
    time.sleep(1)
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "search")))
    search_box.send_keys(primary_issue_id)
    time.sleep(2)
    checkbox_selector = f'[data-testid="multiple-selector-options-{primary_issue_id}"]'
    option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, checkbox_selector)))
    option.click()
    ActionChains(driver).move_by_offset(30,30).click().perform()
    time.sleep(2)

def part_number_filter_select(driver: webdriver.Chrome, wait: WebDriverWait):
       # The Second Filter
    part_number_source = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '[data-testid="customAttributes.Part Number Ax_Part Number_QCR"]')
    ))

    part_number_target = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '[data-testid="drop-area-filter-new-and"]')
    ))

    actions = ActionChains(driver)
    actions.drag_and_drop(part_number_source, part_number_target).perform()

    time.sleep(2)
def qcr_id_filter_select(driver: webdriver.Chrome, wait: WebDriverWait):
    # The QCR ID is the second Filter
    source = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '[data-testid="eventId_EOX QCR Id_QCR"]')
    ))

    target = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '[data-testid="drop-area-filter-new-and"]')
    ))

    actions = ActionChains(driver)
    actions.drag_and_drop(source, target).perform()
    time.sleep(2)

def qcr_id_filter_apply_at_thrid_filter(driver: webdriver.Chrome, wait: WebDriverWait, qcr_id: str):
    options_btn = wait.until(
    lambda d: d.find_elements(By.CSS_SELECTOR, '[data-testid="multiple-selector-button"]')[2]
    if len(d.find_elements(By.CSS_SELECTOR, '[data-testid="multiple-selector-button"]')) > 2
    else False
    )
    options_btn.click()
    time.sleep(1)
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "search")))
    search_box.send_keys(str(qcr_id))
    time.sleep(3)
    # select 

    select_all = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="selectAll-button"]')))
    select_all.click()
    time.sleep(1)

    ActionChains(driver).move_by_offset(30, 30).click().perform()
    time.sleep(1)


def part_number_filter_apply_at_second_filter(driver: webdriver.Chrome, wait: WebDriverWait, part_number: str):
    part_number = [num.strip() for num in part_number.split(',')]
    for part_number in part_number:
        print("Part Number: ", part_number, "is selected")
        options_btn = wait.until(
            lambda d: d.find_elements(By.CSS_SELECTOR, '[data-testid="multiple-selector-button"]')[1]
            if len(d.find_elements(By.CSS_SELECTOR, '[data-testid="multiple-selector-button"]')) > 1
            else False
        )
        options_btn.click()
        time.sleep(1)
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "search")))
        search_box.send_keys(part_number)
        time.sleep(2)
        checkbox_selector = f'[data-testid="multiple-selector-options-{part_number}"]'
        option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, checkbox_selector)))
        option.click()
        ActionChains(driver).move_by_offset(30,30).click().perform()
        time.sleep(2)

def save_as_asg(driver: webdriver.Chrome, wait: WebDriverWait, title: str):
    # Click the Save as
    save_as_btn = wait.until(EC.element_to_be_clickable((By.ID, "event-analytics-button-create-group")))
    save_as_btn.click()
    time.sleep(1)
    title_input = wait.until(EC.element_to_be_clickable((By.ID, "title")))
    title_input.send_keys(title)

def submit_asg(driver: webdriver.Chrome, wait: WebDriverWait):
    create_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="save group button"]')))
    create_btn.click()
    time.sleep(3)
    wait.until(EC.element_to_be_clickable((By.ID, "claim-analytics-tab-0-overview")))

def is_existing_asg(driver: webdriver.Chrome, wait: WebDriverWait):
    try:
        link_el = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.MuiChip-root.MuiChip-clickable'))
        )
        href = link_el.get_attribute("href")
        label = link_el.text
        return href, label
    except:
        return False
def qcr_id_filter_apply_at_second_filter(driver: webdriver.Chrome, wait: WebDriverWait, qcr_id: str):
    options_btn = wait.until(
    lambda d: d.find_elements(By.CSS_SELECTOR, '[data-testid="multiple-selector-button"]')[1]
    if len(d.find_elements(By.CSS_SELECTOR, '[data-testid="multiple-selector-button"]')) > 1
    else False
    )
    options_btn.click()
    time.sleep(1)
    search_box = wait.until(EC.element_to_be_clickable((By.ID, "search")))
    search_box.send_keys(str(qcr_id))
    time.sleep(3)
    # select 
    select_all = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="selectAll-button"]')))
    select_all.click()
    time.sleep(1)

    ActionChains(driver).move_by_offset(30, 30).click().perform()
    time.sleep(1)

def add_description(driver: webdriver.Chrome, wait: WebDriverWait, description: str):
    overview_tab = wait.until(EC.element_to_be_clickable((By.ID, "claim-analytics-tab-0-overview")))
    overview_tab.click()
    time.sleep(2)
    description_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[contenteditable="true"]')))
    description_input.send_keys(description)
    time.sleep(1)

    ActionChains(driver).move_by_offset(0, -200).click().perform()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[normalize-space()='Saved!']"))
        )
        print("Description saved successfully.")
    except:
        print("Saved indicator not found; proceeding assuming autosave on blur.")

def create_asg_eox(*, csv_path: str, output_path: str, qcr_id_col: str, primary_issue_id_col: str, part_number_col: str, title_col: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, dtype=str)

    for col in [qcr_id_col, primary_issue_id_col, part_number_col, title_col]:
        if col not in df.columns:
            raise ValueError(f"Column {col} is not in the input CSV file.")

    driver, wait = create_driver()
    driver.get("https://tke.axionray.com/")
    input('Login and navigate to the ASG Creation page. And Press Enter to continue...')
    ActionChains(driver).move_by_offset(30,30).click().perform()
    time.sleep(1)

    df_list = []

    for _, row in df.iterrows():
        try:
            if pd.notna(row[part_number_col]) and pd.notna(row[primary_issue_id_col]):
                select_datasets(driver, wait)
                primary_issue_id_filter_select(driver, wait)
                primary_issue_id_filter_apply_at_first_filter(driver, wait, str(row[primary_issue_id_col]))
                part_number_filter_select(driver, wait)
                part_number_filter_apply_at_second_filter(driver, wait, str(row[part_number_col]))
                save_as_asg(driver, wait, row[title_col])
                submit_asg(driver, wait)
                if is_existing_asg(driver, wait):
                    row_details = {
                        'qcr_id': row[qcr_id_col],
                        'primary_issue_id': row[primary_issue_id_col],
                        'part_number': row[part_number_col],
                        'title': row[title_col],
                        'parent_href': is_existing_asg(driver, wait)[0],
                        'parent_label': is_existing_asg(driver, wait)[1],
                        'status': 'Created with Primary Issue ID, Part Number and QCR ID',
                        'success': True
                    }
                    select_datasets(driver, wait)
                    primary_issue_id_filter_select(driver, wait)
                    primary_issue_id_filter_apply_at_first_filter(driver, wait, str(row[primary_issue_id_col]))
                    part_number_filter_select(driver, wait)
                    part_number_filter_apply_at_second_filter(driver, wait, str(row[part_number_col]))
                    qcr_id_filter_select(driver, wait)
                    qcr_id_filter_apply_at_thrid_filter(driver, wait, str(row[qcr_id_col]))
                    save_as_asg(driver, wait, row[title_col])
                    submit_asg(driver, wait)
                    time.sleep(1)
                    if is_existing_asg(driver, wait):
                        row_details = {
                        'qcr_id': row[qcr_id_col],
                        'primary_issue_id': row[primary_issue_id_col],
                        'part_number': row[part_number_col],
                        'title': row[title_col],
                        'parent_href': is_existing_asg(driver, wait)[0],
                        'parent_label': is_existing_asg(driver, wait)[1],
                        'status': 'Parent ASG already exists, need manual creation',
                        'success': FalseSocial 
                        }
                        df_list.append(row_details)
                        continue

                    # Add the Description Logic Here
                    row_details['status'] = 'Created with Primary Issue ID, Part Number and QCR ID, but the description is not added'
                    df_list.append(row_details)
                    description = f"Parent QCR ID {row_details['parent_label']} -> {row_details['parent_href']}"
                    add_description(driver, wait, description)
                    df_list.pop()
                    row_details['status'] = 'Created with Primary Issue ID, Part Number and QCR ID, and the description is added'
                    df_list.append(row_details)

                else:
                    df_list.append({
                        'qcr_id': row[qcr_id_col],
                        'primary_issue_id': row[primary_issue_id_col],
                        'part_number': row[part_number_col],
                        'title': row[title_col],
                        'status': 'created',
                        'success': True
                    })
            elif pd.notna(row[qcr_id_col]) and pd.notna(row[primary_issue_id_col]):
                select_datasets(driver, wait)
                primary_issue_id_filter_select(driver, wait)
                primary_issue_id_filter_apply_at_first_filter(driver, wait, str(row[primary_issue_id_col]))
                qcr_id_filter_select(driver, wait)
                qcr_id_filter_apply_at_second_filter(driver, wait, str(row[qcr_id_col]))
                save_as_asg(driver, wait, row[title_col])
                submit_asg(driver, wait)
                if is_existing_asg(driver, wait):
                    df_list.append({
                        'qcr_id': row[qcr_id_col],
                        'primary_issue_id': row[primary_issue_id_col],
                        'part_number': row[part_number_col],
                        'title': row[title_col],
                        'parent_href': is_existing_asg(driver, wait)[0],
                        'parent_label': is_existing_asg(driver, wait)[1],
                        'status': 'existing, need manual creation'
                    })
                else:
                    df_list.append({
                        'qcr_id': row[qcr_id_col],
                        'primary_issue_id': row[primary_issue_id_col],
                        'part_number': row[part_number_col],
                        'title': row[title_col],
                        'status': 'created',
                        'success': True
                    })
            else:
                df_list.append({
                    'qcr_id': row[qcr_id_col],
                    'primary_issue_id': row[primary_issue_id_col],
                    'part_number': row[part_number_col],
                    'title': row[title_col],
                    'status': 'no part number or qcr id or primary issue id',
                    'success': False
                })
        except Exception as e:
            df_list.append({
                'qcr_id': row[qcr_id_col],
                'primary_issue_id': row[primary_issue_id_col],
                'part_number': row[part_number_col],
                'title': row[title_col],
                'status': f'error: {e}',
                'success': False
            })
            continue
    driver.quit()
    output = pd.DataFrame(df_list)
    if output_path:
        output_path = output_path.replace('.csv', '')
        try:
            output.to_csv(f'{output_path}{datetime.now().strftime("%d_%m_%y_%H_%M_%S")}.csv', index=False)
        except Exception as e:
            print(f"Error saving output to {output_path}: {e}")
            output.to_csv(f'asg_creation_result_{datetime.now().strftime("%d_%m_%y_%H_%M_%S")}.csv', index=False)
    else:
        output.to_csv(f'asg_creation_result_{datetime.now().strftime("%d_%m_%y_%H_%M_%S")}.csv', index=False)
    return output


# if __name__ == "__main__":
#     df = pd.read_csv("Triage ASG Creation Mar 09 2026 - Test Records.csv")
#     df = create_asg(df, 'qcr_id', 'primary_issue_id', 'part_number', 'title')
#     df.to_csv(f'asg_creation_result_{datetime.now().strftime("%d_%m_%y_%H_%M_%S")}.csv', index=False)