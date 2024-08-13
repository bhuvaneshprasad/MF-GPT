import re
from PyPDF2 import PdfReader

reader = PdfReader("HDFC MF Factsheet -  June 2024.pdf")

def get_scheme_category(text):
    """
    Extracts and returns the Category of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Fund Category (string)
    """
    fund_category = None
    if 'FUND MANAGER' in text:
        fund_category_pattern = r'CATEGORY OF SCHEME\n([A-Z &-’]+FUND)?([A-Z &-’]+SCHEME)?'
        match = re.search(fund_category_pattern, text)
        if match:
            fund_category = match.group(1) or match.group(2)
        else:
            print("Something went wrong inside Fund Category")
        fund_category = fund_category.title()
    else:
        print("Not the first page of the scheme")
    return fund_category

def get_scheme_name(text):
    """
    Extracts and returns the list of all Fund names from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information. Content Page
    
    Returns:
    - Fund Names (string)
    """
    all_fund_names = []
    if 'CONTENTS' in text:
        fund_name_pattern = r"(HDFC[ a-zA-Z\d\-&’]+(Fund)?(saver)?([a-zA-Z -]+Plan)?)"
        match = re.findall(fund_name_pattern, text)
        if match:
            fund_names = match
            for j in range(len(fund_names)):
                all_fund_names.append(fund_names[j][0].replace("  ", " "))
    else:
        print("Not the first page of the scheme")
    return all_fund_names

def get_scheme_inception_date(text):
    """
    Extracts and returns the inception date of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Fund Inception Date (string)
    """
    fund_inception = []
    if 'FUND MANAGER' in text:
        fund_inception_pattern = r"INCEPTION DATE@?@?\n([a-zA-Z \d,]+)"
        match = re.search(fund_inception_pattern, text)
        if match:
            fund_inception = match.group(1)
    else:
        print("Not the first page of the scheme")
    return fund_inception

def get_closing_aum(text):
    """
    Extracts and returns the Closing AUM of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Fund's Closing AUM (string)
    """
    closing_aum = None
    if 'FUND MANAGER' in text:
        closing_aum_pattern = r"ASSETS UNDER MANAGEMENT ?J? ? ?\nAs on [a-zA-Z]+ \d{2}, \d{4}\n` ([\d., ]+)"
        match = re.search(closing_aum_pattern, text)
        if match:
            closing_aum = match.group(1).replace(" ","").strip()
    else:
        print("Not the first page of the scheme")
    return closing_aum

def get_avg_aum(text):
    """
    Extracts and returns the Avg. AUM of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Fund's Avg. AUM (string)
    """
    avg_aum = None
    if 'FUND MANAGER' in text:
        avg_aum_pattern = r"Average for Month of [a-zA-Z]+ \d{4}\n` ([\d., ]+)"
        match = re.search(avg_aum_pattern, text)
        if match:
            avg_aum = match.group(1).replace(" ","").strip()
    else:
        print("Not the first page of the scheme")
    return avg_aum

def get_expense_ratio(text):
    """
    Extracts and returns the Expense Ratio of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Fund's Expense Ratio (string) - Regular, Direct
    """
    expense_ratio = None
    if 'FUND MANAGER' in text:
        expense_ratio_pattern = r"TOTAL EXPENSE RATIO \(As on [a-zA-Z]+ \d{2}, \d{4}\) \nIncluding Additional Expenses and Goods and Service \nTax on Management Fees\nRegular: ([\d.]+%)[ ]+Direct: ([\d.]+%)"
        match = re.search(expense_ratio_pattern, text)
        if match:
            expense_ratio = match.group(1), match.group(2)
    else:
        print("Not the first page of the scheme")
    return expense_ratio

def get_total_turnover(text):
    """
    Extracts and returns the Total turnover of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Fund's Turnover (string)
    """
    portfolio_turnover = None
    if 'FUND MANAGER' in text:
        portfolio_turnover_pattern = r"Total Turnover ([\d. ]+%)"
        match = re.search(portfolio_turnover_pattern, text)
        if match:
            portfolio_turnover = match.group(1)
        elif 'Total Turnover' not in text:
            portfolio_turnover = "NA"
    else:
        print("Not the first page of the scheme")
    return portfolio_turnover

def get_ratios(text):
    """
    Extracts and returns the Risk Ratios of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Fund's Risk ratios (string)
    """
    ratios = None
    if 'FUND MANAGER' in text:
        ratios_pattern = r"Standard Deviation ([\d. ]+%)\nn Beta ([\d. ]+)\nn Sharpe Ratio[*] ([\d. ]+)"
        match = re.search(ratios_pattern, text)
        if match:
            ratios = f"Standard Deviation: {match.group(1)}, Portfolio Beta: {match.group(1)}, Sharpe Ratio: {match.group(1)}"
        elif 'Standard Deviation' not in text:
            ratios = "NA"
    else:
        print("Not the first page of the scheme")
    return ratios

def get_benchmark(text):
    """
    Extracts and returns the Benchmark of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Fund's Benchmark (string)
    """
    benchmark = None
    if 'FUND MANAGER' in text:
        benchmark_pattern = r"BENCHMARK INDEX:[ ]+\n([a-zA-Z &%\+\(\)\d:\n-]+)\n#?"
        match = re.search(benchmark_pattern, text)
        if match:
            benchmark = match.group(1)
    else:
        print("Not the first page of the scheme")
    return benchmark

def get_riskometer(text, next_page_text='', next_to_next_page_text='', third_page_text=''):
    """
    Extracts and returns the Riskometer of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Fund's Riskometer (string)
    """
    riskometer = None
    if 'FUND MANAGER' in text:
        if 'FUND MANAGER' not in next_page_text:
            text+=next_page_text
        if 'FUND MANAGER' not in next_to_next_page_text:
            text+=next_to_next_page_text
        riskometer_pattern = r"Investors understand that their principal will be at\n([a-z ]+)\n"
        match = re.search(riskometer_pattern, text)
        if match:
            riskometer = match.group(1)
        else:
            text+=third_page_text
            riskometer_pattern = r"Investors understand that their principal will be at\n([a-z ]+)\n"
            match = re.search(riskometer_pattern, text)
            riskometer = match.group(1)
        riskometer = riskometer.replace("ris k", "risk").title()
    else:
        print("Not the first page of the scheme")
    return riskometer

def get_fund_managers(text):
    """
    Extracts and returns the Fund Managers from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Fund Managers (string)
    """
    fund_managers = None
    if 'FUND MANAGER' in text:
        fund_managers_pattern = r"\n([a-zA-Z ]+)\n(\([a-zA-Z .\n]+\))? ?(\([a-zA-Z ]+\d+ ?, \d{4}\))[ ]+\n(Total Experience: [a-zA-Z \d]+)?"
        match = re.findall(fund_managers_pattern, text)
        if match:
            fund_managers = match
            fund_managers = [''.join(filter(None, fund_manager)).replace(")", ") ").replace("  ", " ") for fund_manager in fund_managers]
    else:
        print("Not the first page of the scheme")
    return fund_managers

def get_residual_maturity(text):
    """
    Extracts and returns the Maturity period of the Fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Residual Maturity (string)
    """
    residual_maturity = None
    if 'FUND MANAGER' in text:
        residual_maturity_pattern = r"Residual Maturity \*[ ]+([\d.]+ years)|Residual Maturity \*[ ]+([\d.]+ days)"
        match = re.search(residual_maturity_pattern, text)
        if match:
            residual_maturity = match.group(1) or match.group(2)
        elif 'Residual Maturity' not in text:
            residual_maturity = None
    else:
        print("Not the first page of the scheme")
    return residual_maturity

def get_macaulay_duration(text):
    """
    Extracts and returns the Macaulay Duration of the Fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Macaulay Duration (string)
    """
    macaulay_duration = None
    if 'FUND MANAGER' in text:
        macaulay_duration_pattern = r"Macaulay Duration \*[ ]+([\d. ]+ years?)|Macaulay Duration \*[ ]+([\d. ]+ days)"
        match = re.search(macaulay_duration_pattern, text)
        if match:
            macaulay_duration = match.group(1) or match.group(2)
        elif 'Macaulay Duration' not in text:
            macaulay_duration = None
    else:
        print("Not the first page of the scheme")
    return macaulay_duration

def get_modified_duration(text):
    """
    Extracts and returns the Modified Duration of the Fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Modified Duration (string)
    """
    modified_duration = None
    if 'FUND MANAGER' in text:
        modified_duration_pattern = r"Modified Duration \*[ ]+([\d. ]+ years?)|Modified Duration \*[ ]+([\d. ]+ days)"
        match = re.search(modified_duration_pattern, text)
        if match:
            modified_duration = match.group(1) or match.group(2)
        elif 'Modified Duration' not in text:
            modified_duration = None
    else:
        print("Not the first page of the scheme")
    return modified_duration

def get_annualised_ytm(text):
    """
    Extracts and returns the Annualized Portfolio YTM of the Fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Annualized Portfolio YTM (string)
    """
    annualised_ytm = None
    if 'FUND MANAGER' in text:
        annualised_ytm_pattern = r"Annualized Portfolio YTM# \*[ ]+([\d. ]+%)"
        match = re.search(annualised_ytm_pattern, text)
        if match:
            annualised_ytm = match.group(1).replace(" ", "")
        elif 'Annualized Portfolio YTM' not in text:
            annualised_ytm = None
    else:
        print("Not the first page of the scheme")
    return annualised_ytm

def get_scheme_obj(text):
    """
    Extracts and returns the Investment Objectives the Fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Investment Objectives (string)
    """
    scheme_obj = None
    if 'FUND MANAGER' in text:
        scheme_obj_pattern = r"INVESTMENT OBJECTIVE[ ]+:([a-zA-Z \+\(\)\d.\/\n&,-]+realized.)"
        match = re.search(scheme_obj_pattern, text)
        if match:
            scheme_obj = match.group(1).strip()
    else:
        print("Not the first page of the scheme")
    return scheme_obj

def convert_to_qa(fund_info, fs_date):
    qa_format = ""
    questions_answers = {
        f"What is the investment objective of {fund_info['fund_name']}?": f"The investment objective of {fund_info['fund_name']} is {fund_info['fund_objective']}.",
        f"When was {fund_info['fund_name']} launched?": f"{fund_info['fund_name']} was launched on {fund_info['inception']}.",
        f"What is the closing AUM of {fund_info['fund_name']}?": f"As of {fs_date}, the closing AUM of {fund_info['fund_name']} is {fund_info['closing_aum']}.",
        f"What is the average AUM of {fund_info['fund_name']}?": f"As of {fs_date}, the average AUM of {fund_info['fund_name']} is {fund_info['average_aum']}.",
        f"What is the minimum first investment for {fund_info['fund_name']}?": f"As of {fs_date}, the minimum first investment for {fund_info['fund_name']} is {fund_info['minimum_first_investment']}.",
        f"What is the minimum additional investment for {fund_info['fund_name']}?": f"As of {fs_date}, the minimum additional investment for {fund_info['fund_name']} is {fund_info['minimum_additional_investment']}.",
        f"What is the expense ratio of {fund_info['fund_name']}?": f"As of {fs_date}, the expense ratio of {fund_info['fund_name']} is {fund_info['expense_ratio'][0]} for Regular Plan and {fund_info['expense_ratio'][1]} for Direct Plan.",
        f"What is the portfolio turnover of {fund_info['fund_name']}?": f"The portfolio turnover of {fund_info['fund_name']} is {fund_info['portfolio_turnover']} in {fs_date}.",
        f"What are the ratios of {fund_info['fund_name']}?": f"As of {fs_date}, the risk ratios of {fund_info['fund_name']} are {fund_info['ratios']}.",
        f"What category does {fund_info['fund_name']} belong to?": f"{fund_info['fund_name']} belongs to the {fund_info['fund_category']} category.",
        f"What is the benchmark of {fund_info['fund_name']}?": f"The benchmark of {fund_info['fund_name']} is {fund_info['fund_benchmark']}.",
        f"What is the riskometer rating of {fund_info['fund_name']}?": f"The riskometer rating of {fund_info['fund_name']} is {fund_info['riskometer']}.",
        f"Who are the fund managers of {fund_info['fund_name']}?": f"As of {fs_date}, the fund managers of {fund_info['fund_name']} are {fund_info['fund_managers']}.",
        f"What is the average maturity of {fund_info['fund_name']}?": f"As of {fs_date}, the average maturity of {fund_info['fund_name']} is {fund_info['average_maturity']}.",
        f"What is the modified duration of {fund_info['fund_name']}?": f"As of {fs_date}, the modified duration of {fund_info['fund_name']} is {fund_info['modified_duration']}.",
        f"What is the Macaulay duration of {fund_info['fund_name']}?": f"As of {fs_date}, the Macaulay duration of {fund_info['fund_name']} is {fund_info['macaulay_duration']}.",
        f"What is the annualised yield to maturity (YTM) of {fund_info['fund_name']}?": f"As of {fs_date}, the annualised yield to maturity (YTM) of {fund_info['fund_name']} is {fund_info['annualised_ytm']}."
    }

    for question, answer in questions_answers.items():
        if ("None" or "NA") not in answer:
            qa_format += f"Question: {question}\nAnswer: {answer}\n\n"

    return qa_format

pages = reader.pages[7:103]
text = pages[0].extract_text()
fs_date_match = re.search(r"AS ON ([a-zA-Z]+) \d{2}, (\d{4})", text)
fs_date = fs_date_match.group(1).title() + " " + fs_date_match.group(2)
not_found = 0
total = 0
j = 0
for i, page in enumerate(pages):
    text = page.extract_text()
    if i < len(pages)-3:
        next_page_text = pages[i+1].extract_text()
        next_to_next_page_text = pages[i+2].extract_text()
        third_page_text = pages[i+3].extract_text()
    if 'FUND MANAGER' in text:
        fund_info = {
            "fund_name": get_scheme_name(reader.pages[6:7][0].extract_text())[j],
            "fund_objective": get_scheme_obj(text),
            "inception": get_scheme_inception_date(text),
            "closing_aum": get_closing_aum(text),
            "average_aum": get_avg_aum(text),
            "minimum_first_investment": "Rs.100",
            "minimum_additional_investment": "Any amount after the first investment of Rs.100.",
            "expense_ratio": get_expense_ratio(text),
            "portfolio_turnover": get_total_turnover(text),
            "ratios": get_ratios(text),
            "fund_category": get_scheme_category(text),
            "fund_benchmark": get_benchmark(text),
            "riskometer": get_riskometer(text, next_page_text, next_to_next_page_text, third_page_text),
            "fund_managers": get_fund_managers(text),
            "average_maturity": get_residual_maturity(text),
            "modified_duration": get_modified_duration(text),
            "macaulay_duration": get_macaulay_duration(text),
            "annualised_ytm": get_annualised_ytm(text)
            }
        qa_text = convert_to_qa(fund_info, fs_date)
        j+=1

        # Save to text file
        with open('hdfc_fund_qa.txt', 'a') as f:
            f.write(qa_text)