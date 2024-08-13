import re
from PyPDF2 import PdfReader

reader = PdfReader("icici_amc_factsheet.pdf")

def extract_fund_name(text):
    """
    Extracts the fund/scheme name from the given text based on predefined patterns.

    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - fund_name (string): Name of the fund/scheme.
    """
    fund_name = "NA"
    if 'Fund Managers' in text:
        scheme_name_pattern = r"(ICICI [a-zA-Z\d /(/)&-.]+? (Fund|FOF)\b(?:\n?|$))[ ]?"
        match = re.search(scheme_name_pattern, text)
        
        if match:
            fund_name = match.group(1).strip()
            
            # Check if fund_name contains 'Retirement Fund'
            if 'Retirement Fund' in fund_name:
                retirement_scheme_pattern = r"(ICICI [a-zA-Z\d /(/)&-.]+? Fund(?:\n?|$)[ ]?[- a-zA-Z ]+Plan|ICICI [a-zA-Z\d /(/)&-. ]+? FOF(?:\n?|$)[ ]?[- a-zA-Z ]+Plan)"
                match = re.search(retirement_scheme_pattern, text)
                
                if match:
                    fund_name = match.group(1).strip()
                else:
                    print("Something went wrong inside retirement fund")
    else:
        print("Not the first page of the scheme")
    return fund_name

def extract_inception_dates(text):
    """
    Extracts and returns the inception date(s) from the given pages based on predefined patterns.

    Parameters:
    - text (str): The text containing scheme information.

    Returns:
    - inception_date (string/tuple)
    """
    inception_date = "NA"
    inception_date_pattern = (
        r"Inception/ ?Allotment date ?:[ \n]+(?:[a-zA-Z :]+(\d{2}-[a-zA-Z]+-(?:\d{2}|\d{4}))?\n)?"
        r"[a-zA-Z :]*(\d{2}-[a-zA-Z]+-(?:\d{2}|\d{4}))"
    )
    if 'Fund Managers' in text:
        matches = re.findall(inception_date_pattern, text)
        if matches:
            inception_date = matches[0][1] if matches[0][0] == '' else matches[0]
        else:
            print("Something went wrong inside inception dates")
    else:
        print("Not the first page of the scheme")
    return inception_date

def extract_closing_aum(text):
    """
    Extracts and returns the Closing AUM of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Cloaing AUM (string)
    """
    closing_aum = "NA"
    closing_aum_pattern = (r"Closing AUM as on \d\d-[a-zA-Z ]+-\d\d ?: Rs\. ([\d,.]+)")
    if 'Fund Managers' in text:
        match = re.search(closing_aum_pattern, text)
        if match:
            closing_aum = match.group(1)
        else:
            print("Something went wrong inside Closing AUM")
    else:
        print("Not the first page of the scheme")
    return closing_aum

def extract_avg_aum(text):
    """
    Extracts and returns the Average Monthly AUM of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Average Monthly AUM (string)
    """
    avg_monthly_aum = "NA"
    avg_aum_pattern = (r"Monthly AAUM as on \d\d-[a-zA-Z ]+-\d\d :[ ]+Rs\. ([\d,.]+)")
    if 'Fund Managers' in text:
        match = re.search(avg_aum_pattern, text)
        if match:
            avg_monthly_aum = match.group(1)
        else:
            print("Something went wrong inside Average Monthly AUM")
    else:
        print("Not the first page of the scheme")
    return avg_monthly_aum

def extract_min_investment(text):
    """
    Extracts and returns the Minimum Investment of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Minimum Investment (string)
    """
    min_investment = "NA"
    if 'Fund Managers' in text:
        min_investment_pattern = (r"Application Amount for fr ?esh Subscription[ *]?:\n(a\)[ a-zA-Z&:]+[ \d,/-]+[A-Za-z.]+[ \d,/-]+ \(?[a-zA-Z .\d]+\)\nb\)) [a-zA-Z :.]+[ \d,/-]+ \(?[a-zA-Z .\d]+\)|Application Amount for fr ?esh Subscription[ *#]+?:\n(Rs.[ \d,/-]+ \(?[a-zA-Z .\d/-]+\)?(?: thereafter)?)"
    )
        match = re.search(min_investment_pattern, text)
        if match:
            min_investment = match.group(2)
            if min_investment is None:
              min_investment_pattern = r"Application Amount for fr ?esh Subscription[ *]?:\n(a\)[ a-zA-Z&:]+[ \d,/-]+[A-Za-z.]+[ \d,/-]+ \(?[a-zA-Z .\d]+\)\nb\) [a-zA-Z :.]+[ \d,/-]+ \(?[a-zA-Z .\d]+\))"
              match = re.search(min_investment_pattern, text)
              min_investment = match.group(1).replace("\n", " ")
        else:
            print("Something went wrong inside Minimum Investment")
    else:
        print("Not the first page of the scheme")
    if min_investment != "NA":
        try:
            min_investment = min_investment.replace("R s", "Rs").replace("Re. ", "Re.").replace("Rs. ", "Rs.").replace("/-", "").replace("/ -", "").replace("Rs ", "Rs.").strip()
        except:
            print("*******************")
            print(min_investment)
            print("*******************")
            min_investment = min_investment
    return min_investment

def extract_investment_horizon(text):
    """
    Extracts and returns the Minimum Investment of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Minimum Investment (string)
    """
    inv_horizon = "NA"
    if 'Fund Managers' in text:
        inv_horizon_pattern = (r"Indicative Investment Horiz ?on ?: (\d+ [a-zA-Z &]+ above)?(\d+ [a-zA-Z &]+ more)?(\d+ Years)?([\d a-zA-Z]+Days)?")
        match = re.search(inv_horizon_pattern, text)
        if match:
            inv_horizon = match.group(1) or match.group(2) or match.group(3) or match.group(4)
        else:
            inv_horizon = "NA"
    else:
        print("Not the first page of the scheme")
    return inv_horizon

def extract_expense_ratio(text):
    """
    Extracts and returns the Expense of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Expense Ratio (string) - Regular, Direct
    """
    expense_ratio = "NA"
    if 'Fund Managers' in text:
        expense_ratio_pattern = (r"Total Expense Ratio @@ :\nOther : ([\d.]+% p ?. a.)\nDirect : ([\d.]+% p ?. a.)")
        match = re.search(expense_ratio_pattern, text)
        if match:
            expense_ratio = match.group(1).replace("p. a.", "p.a.").replace("p . a.", "p.a."), match.group(2).replace("p. a.", "p.a.").replace("p . a.", "p.a.")
        else:
            print("Something went wrong inside Expense Ratio")
    else:
        print("Not the first page of the scheme")
    return expense_ratio

def extract_no_of_folios_in_scheme(text):
    """
    Extracts and returns the No. of folios in the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - No. of Folios (string)
    """
    no_of_folios_in_scheme = "NA"
    if 'Fund Managers' in text:
        no_of_folios_in_scheme_pattern = (r"No. of folios [\n]?in the Scheme :[\n]?([ \d,]+)")
        match = re.search(no_of_folios_in_scheme_pattern, text)
        if match:
            no_of_folios_in_scheme = match.group(1)
        else:
            print("Something went wrong inside Expense Ratio")
    else:
        print("Not the first page of the scheme")
    return no_of_folios_in_scheme

def extract_avg_div_yield(text):
    """
    Extracts and returns the Average Dividend Yield of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Average Dividend Yield (string)
    """
    avg_div_yeild = "NA"
    if 'Fund Managers' in text:
        avg_div_yeild_pattern = (r"Average Dividend Yield :\n([\d.]+)")
        match = re.search(avg_div_yeild_pattern, text)
        if match:
            avg_div_yeild = match.group(1)
        elif 'Average Dividend' not in text:
            avg_div_yeild = "NA"
        else:
            print("Something went wrong inside Average Dividend Yield")
    else:
        print("Not the first page of the scheme")
    return avg_div_yeild

def extract_annual_portfolio_turnover(text):
    """
    Extracts and returns the Annual Portfolio Turnover of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Annual Portfolio Turnover (string)
    """
    annual_portfolio_turnover = "NA"
    if 'Fund Managers' in text:
        annual_portfolio_turnover_pattern = (r"Annual P ?ortfolio [\n]?Turnover Ratio : \nEquity - ([\d.]+ times)")
        match = re.search(annual_portfolio_turnover_pattern, text)
        if match:
            annual_portfolio_turnover = match.group(1)
        elif 'Annual P' not in text:
            annual_portfolio_turnover = "NA"
        else:
            print("Something went wrong inside Annual Portfolio Turnover")
    else:
        print("Not the first page of the scheme")
    return annual_portfolio_turnover

def extract_ratios(text):
    """
    Extracts and returns the Ratios of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Ratios (string) - Standard Deviation, Sharpe Ratio, Portfolio Beta
    """
    std_dev = sharpe_ratio = portfolio_beta = "NA"
    if 'Fund Managers' in text:
        std_dev_pattern = (r"Std Dev[ \n]+?\(Annualised\) : \n([-\d.]+%)")
        sharpe_ratio_pattern = (r"Sharpe[ \n]+?Ratio : \n([-\d.]+)")
        portfolio_beta_pattern = (r"Portfolio[ \n]+?Beta : \n([-\d.]+)")
        std_dev_match = re.search(std_dev_pattern, text)
        sharpe_ratio_match = re.search(sharpe_ratio_pattern, text)
        portfolio_beta_match = re.search(portfolio_beta_pattern, text)
        if std_dev_match and sharpe_ratio_match and portfolio_beta_match:
            std_dev = std_dev_match.group(1) or "NA"
            sharpe_ratio = sharpe_ratio_match.group(1) or "NA"
            portfolio_beta = portfolio_beta_match.group(1) or "NA"
        elif 'Std Dev' not in text:
            std_dev = "NA"
            sharpe_ratio = "NA"
            portfolio_beta = "NA"
        else:
            print("Something went wrong inside Ratios")
    else:
        print("Not the first page of the scheme")
    return f"Standard Ratio: {std_dev}, Sharpe Ratio: {sharpe_ratio}, Portfolio Beta: {portfolio_beta}"

def extract_fund_category(text):
    """
    Extracts and returns the fund category from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Fund Category (string)
    """
    fund_category = "NA"
    if 'Fund Managers' in text:
        fund_category_pattern = r"[\n]?S?i?z?e?(Size)?(Quantitativ ?e Indicators)? ?([a-zA-z \(\)]+)Category"
        match = re.search(fund_category_pattern, text)
        if match:
            fund_category = match.group(3)
            if 'Flexi' in fund_category:
                fund_category = 'Flexi Cap'
            elif 'Sectoral' in fund_category:
                fund_category = 'Sectoral Fund'
            elif 'Thematic' in fund_category:
                fund_category = 'Thematic Fund'
            elif 'EL SS' in fund_category:
                fund_category = 'ELSS - Equity Linked Savings Scheme'
            elif 'Multi Asset Allocation' in fund_category:
                fund_category = 'Multi Asset Allocation Fund'
            elif 'F OF' in fund_category:
                fund_category = 'FOF - Fund Of Funds'
            elif 'Overnight' in fund_category:
                fund_category = 'Overnight Fund'
            elif 'Liquid' in fund_category:
                fund_category = 'Liquid Fund'
            elif 'Money Mar' in fund_category:
                fund_category = 'Money Market Fund'
            elif 'Ultra Short' in fund_category:
                fund_category = 'Ultra Short Duration Fund'
            elif 'Low Dur' in fund_category:
                fund_category = 'Low Duration Fund'
            elif fund_category == 'hort Duration Fund':
                fund_category = 'Short Duration Fund'
            elif 'Medium to Long' in fund_category:
                fund_category = 'Medium to Long Duration Fund'
            elif 'Corporate Bond' in fund_category:
                fund_category = 'Corporate Bond Fund'
            elif 'Long Dur' in fund_category:
                fund_category = 'Long Duration Fund'
            elif 'olution oriented scheme' in fund_category:
                fund_category = 'Solution oriented scheme'
            elif 'Closed Ended' in fund_category:
                fund_category = 'Closed Ended'
            elif 'Constant Dur' in fund_category:
                fund_category = 'Gilt Fund with 10-year Constant Duration'
            elif 'Other Scheme' in fund_category:
                fund_category = 'FOF - Fund Of Funds'
            fund_category = fund_category.replace("F und", "Fund").replace("C ap", "Cap").strip()
        else:
            print("Something went wrong inside Annual Portfolio Turnover")
    else:
        print("Not the first page of the scheme")
    return fund_category

def extract_benchmark(text):
    """
    Extracts and returns the fund's Benchmark from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Benchmark (string)
    """
    benchmark = "NA"
    if 'Fund Managers' in text:
        benchmark_pattern = r"Riskometer\n\(([a-zA-z \d\:\(\)\+&\-%\n]+)\)|\((NYSE Arca Gold Miners Index and\nthe S&P Oil & Gas Exploration &\nProduction Select Industry Index)\)?|\((Domestic price of gold as derived \nfrom the LBMA AM fixing prices.)\)?|\((Domestic price of silver as derived \nfrom the LBMA AM fixing prices.)\)?"
        match = re.search(benchmark_pattern, text)
        if match:
            benchmark = match.group(1) or match.group(2) or match.group(3) or match.group(4)
        elif 'Riskometer' not in text:
            benchmark = "NA"
        else:
            print("Something went wrong inside Benchmark")
    else:
        print("Not the first page of the scheme")
    return benchmark

def extract_riskometer(text, next_page_text=''):
    """
    Extracts and returns the fund's Risk from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Riskmoeter (string)
    """
    riskometer = "NA"
    if 'Fund Managers' in text:
        if 'Fund Manager' not in next_page_text:
            text+=next_page_text
        riskometer_pattern = r"riskometer is at \n([a-zA-z ]+)risk|principal \nwill be at ([a-zA-Z]+)[ ]+risk"
        match = re.search(riskometer_pattern, text)
        if match:
            riskometer = match.group(1) or match.group(2)
        elif 'riskometer' not in text:
            riskometer = "NA"
        else:
            print("Something went wrong inside Benchmark")
    else:
        print("Not the first page of the scheme")
    return riskometer

def extract_fund_managers(text):
    """
    Extracts and returns the Fund Managers from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Fund Managers (string)
    """
    fund_managers = "NA"
    if 'Fund Managers' in text:
        # TO DO: include Sharmila D'mello full name and exp. --> try: ’
        fund_managers_pattern = r"Fund Managers\*?\*? : ? ?\n([a-zA-Z :\(\),\d&''.\n]+\n?)(Indicative)?"
        match = re.search(fund_managers_pattern, text)
        if match:
            fund_managers = match.group(1)
            if 'Indicative' in fund_managers:
                fund_managers = fund_managers.split("Indicative")[0]
            if 'Total Expense Ration' in fund_managers:
                fund_managers = fund_managers.split("Total Expense ratio")[0]
        else:
            print("Something went wrong inside Fund Managers")
    else:
        print("Not the first page of the scheme")
    return fund_managers.replace("\n", "")

def extract_min_addl_investment(text):
    """
    Extracts and returns Min. Addl. Investment of the Fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Min. Additional Investment (string)
    """
    min_addl_investment = "NA"
    if 'Fund Managers' in text:
        min_addl_investment_pattern = r"Min\.Addl\.Investment ?[*]? :\n(Rs\. ?[ \d,\/-]+(?: [&a-zA-Z .\d\(\)\/-]+))"
        match = re.search(min_addl_investment_pattern, text)
        if match:
            min_addl_investment = match.group(1)
            if ')' in min_addl_investment:
                min_addl_investment = min_addl_investment.split(")")[0] + ")"
            if 'Exit' in min_addl_investment:
                min_addl_investment = min_addl_investment.split("Exit")[0] + ")"
            if 'Other' in min_addl_investment:
                min_addl_investment = min_addl_investment.split("Other")[0] + ")"
            min_addl_investment = min_addl_investment.replace("Rs. ", "Rs.").replace("Re. ", "Re.").replace("/-", "").replace("/ -", "").replace("R s.", "Rs.")
    else:
        print("Not the first page of the scheme")
    return min_addl_investment

def extract_top_5_stock_holdings(text, next_page_text=''):
    """
    Extracts and returns the Top 5 Stock Holings of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Top 5 Stock Holdings (string)
    """
    top_5_holdings = "NA"
    if 'Fund Managers' in text:
        text+=next_page_text
        top_5_holdings_pattern = r"Top 5 Stock Holdings\n([a-zA-z .&'\(\)]+) ([\d.]+%)\n([a-zA-z .&'\(\)]+) ([\d.]+%)\n([a-zA-z .&'\(\)]+) ([\d.]+%)\n([a-zA-z .&'\(\)]+) ([\d.]+%)\n([a-zA-z .&'\(\)]+) ([\d.]+%)"
        match = re.search(top_5_holdings_pattern, text)
        if match:
            first_comp = match.group(1) + f" ({match.group(2)})"
            second_comp = match.group(3) + f" ({match.group(4)})"
            third_comp = match.group(5) + f" ({match.group(6)})"
            fourth_comp = match.group(7) + f" ({match.group(8)})"
            fifth_comp = match.group(9) + f" ({match.group(10)})"
            top_5_holdings = [first_comp, second_comp, third_comp, fourth_comp, fifth_comp]
        elif 'Top 5 holdings' not in text:
            top_5_holdings = "NA"
        else:
            print("Something went wrong inside Top 5 Stock Holdings")
    else:
        print("Not the first page of the scheme")
    return ", ".join(top_5_holdings)

def extract_top_5_sector_holdings(text, next_page_text=''):
    """
    Extracts and returns the Top 5 Sector Holings of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Top 5 Sector Holdings (string)
    """
    top_5_sectors = "NA"
    if 'Fund Managers' in text:
        text+=next_page_text
        top_5_sectors_pattern = r"Top 5 Sector Holdings\n([a-zA-z ,.&'\(\)]+) ([\d.]+%)\n([a-zA-z ,.&'\(\)]+) ([\d.]+%)\n([a-zA-z ,.&'\(\)]+) ([\d.]+%)\n([a-zA-z ,.&'\(\)]+) ([\d.]+%)\n([a-zA-z ,.&'\(\)]+) ([\d.]+%)"
        match = re.search(top_5_sectors_pattern, text)
        if match:
            first_sec = match.group(1) + f"({match.group(2)})"
            second_sec = match.group(3) + f"({match.group(4)})"
            third_sec = match.group(5) + f"({match.group(6)})"
            fourth_sec = match.group(7) + f"({match.group(8)})"
            fifth_sec = match.group(9) + f"({match.group(10)})"
            top_5_sectors = [first_sec, second_sec, third_sec, fourth_sec, fifth_sec]
        elif 'Top 5 holdings' not in text:
            top_5_sectors = "NA"
        else:
            print("Something went wrong inside Top 5 Sector Holdings")
    else:
        print("Not the first page of the scheme")
    return ", ".join(top_5_sectors)

def extract_average_maturity(text):
    """
    Extracts and returns the Average Maturity of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Average Maturity (string)
    """
    average_maturity = "NA"
    if 'Fund Managers' in text:
        average_maturity_pattern = r"Average Maturity ?:? ?\n([ \d.]+ Years)|Average Maturity ?:? ?\n([ \d.]+ Day ?s)"
        match = re.search(average_maturity_pattern, text)
        if match:
            average_maturity = match.group(1) or match.group(2).replace("Day s", "Days")
        elif 'Average Maturity' not in text:
            average_maturity = "NA"
        else:
            print("Something went wrong inside Average Maturity")
    else:
        print("Not the first page of the scheme")
    return average_maturity

def extract_modified_duration(text):
    """
    Extracts and returns the Modified Duration of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Modified Duration (string)
    """
    modified_duration = "NA"
    if 'Fund Managers' in text:
        modified_duration_pattern = r"Modified Dur ?ation ?:? ?\n([ \d.]+ Years)|Modified Dur ?ation ?:? ?\n([ \d.]+ Day ?s)"
        match = re.search(modified_duration_pattern, text)
        if match:
            modified_duration = match.group(1) or match.group(2).replace("Day s", "Days")
        elif 'Modified Dur' not in text:
            modified_duration = "NA"
        else:
            print("Something went wrong inside Modified Duration")
    else:
        print("Not the first page of the scheme")
    return modified_duration

def extract_macaulay_duration(text):
    """
    Extracts and returns the Macaulay Duration of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Macaulay Duration (string)
    """
    macaulay_duration = "NA"
    if 'Fund Managers' in text:
        macaulay_duration_pattern = r"Macaulay Dur ?ation ?:? ?\n([ \d.]+ Years)|Macaulay Dur ?ation ?:? ?\n([ \d.]+ Day ?s)"
        match = re.search(macaulay_duration_pattern, text)
        if match:
            macaulay_duration = match.group(1) or match.group(2).replace("Day s", "Days")
        elif 'Macaulay Dur' not in text:
            macaulay_duration = "NA"
        else:
            print("Something went wrong inside Macaulay Duration")
    else:
        print("Not the first page of the scheme")
    return macaulay_duration

def extract_annualised_ytm(text):
    """
    Extracts and returns the Annualised Portfolio YTM of the fund from the given pages based on predefined patterns.
    
    Parameters:
    - text (str): The text containing scheme information.
    
    Returns:
    - Annualised Portfolio YTM (string)
    """
    annualised_ytm = "NA"
    if 'Fund Managers' in text:
        annualised_ytm_pattern = r"Annualised P ortfolio YTM[*]? ?:? ?\n([ \d.]+%)"
        match = re.search(annualised_ytm_pattern, text)
        if match:
            annualised_ytm = match.group(1)
        elif 'Annualised P' not in text:
            annualised_ytm = "NA"
        else:
            print("Something went wrong inside Annualised Portfolio YTM")
    else:
        print("Not the first page of the scheme")
    return annualised_ytm

def convert_to_qa(fund_info, fs_date):
    qa_format = ""
    questions_answers = {
        f"When was {fund_info['fund_name']} launched?": f"{fund_info['fund_name']} was launched on {fund_info['inception']}.",
        f"What is the closing AUM of {fund_info['fund_name']}?": f"As of {fs_date}, the closing AUM of {fund_info['fund_name']} is {fund_info['closing_aum']}.",
        f"What is the average AUM of {fund_info['fund_name']}?": f"As of {fs_date}, the average AUM of {fund_info['fund_name']} is {fund_info['average_aum']}.",
        f"What is the minimum first investment for {fund_info['fund_name']}?": f"As of {fs_date}, the minimum first investment for {fund_info['fund_name']} is {fund_info['minimum_first_investment']}.",
        f"What is the minimum additional investment for {fund_info['fund_name']}?": f"As of {fs_date}, the minimum additional investment for {fund_info['fund_name']} is {fund_info['minimum_additional_investment']}.",
        f"What is the investment horizon for {fund_info['fund_name']}?": f"The investment horizon for {fund_info['fund_name']} is {fund_info['investment_horizon']}.",
        f"What is the expense ratio of {fund_info['fund_name']}?": f"As of {fs_date}, the expense ratio of {fund_info['fund_name']} is {fund_info['expense_ratio'][0]} for Regular Plan and {fund_info['expense_ratio'][1]} for Direct Plan.",
        f"How many folios are there in the scheme {fund_info['fund_name']}?": f"As of {fs_date}, there are {fund_info['no_of_folios_in_scheme']} folios in the scheme {fund_info['fund_name']}.",
        f"What is the average dividend yield of {fund_info['fund_name']}?": f"As of {fs_date}, the average dividend yield of {fund_info['fund_name']} is {fund_info['average_dividend_yield']}.",
        f"What is the portfolio turnover of {fund_info['fund_name']}?": f"The portfolio turnover of {fund_info['fund_name']} in {fs_date} is {fund_info['portfolio_turnover']}.",
        f"What are the Standard deviation, Sharpe ratio and Portfolio beta of {fund_info['fund_name']}?": f"As of {fs_date}, the risk ratios of {fund_info['fund_name']} are {fund_info['ratios']}.",
        f"What category does {fund_info['fund_name']} belong to?": f"{fund_info['fund_name']} belongs to the {fund_info['fund_category']} category.",
        f"What is the benchmark of {fund_info['fund_name']}?": f"The benchmark of {fund_info['fund_name']} is {fund_info['fund_benchmark']}.",
        f"What is the riskometer rating of {fund_info['fund_name']}?": f"The riskometer rating of {fund_info['fund_name']} is {fund_info['riskometer']}.",
        f"Who are the fund managers of {fund_info['fund_name']}?": f"As of {fs_date}, the fund managers of {fund_info['fund_name']} are {fund_info['fund_managers']}.",
        f"What are the top 5 stock holdings of {fund_info['fund_name']}?": f"As of {fs_date}, the top 5 stock holdings of {fund_info['fund_name']} are {fund_info['top_5_stock_holdings']}.",
        f"What are the top 5 sector holdings of {fund_info['fund_name']}?": f"As of {fs_date}, the top 5 sector holdings of {fund_info['fund_name']} are {fund_info['top_5_sector_holdings']}.",
        f"What is the average maturity of {fund_info['fund_name']}?": f"As of {fs_date}, the average maturity of {fund_info['fund_name']} is {fund_info['average_maturity']}.",
        f"What is the modified duration of {fund_info['fund_name']}?": f"As of {fs_date}, the modified duration of {fund_info['fund_name']} is {fund_info['modified_duration']}.",
        f"What is the Macaulay duration of {fund_info['fund_name']}?": f"As of {fs_date}, the Macaulay duration of {fund_info['fund_name']} is {fund_info['macaulay_duration']}.",
        f"What is the annualised yield to maturity (YTM) of {fund_info['fund_name']}?": f"As of {fs_date}, the annualised yield to maturity (YTM) of {fund_info['fund_name']} is {fund_info['annualised_ytm']}."
    }

    for question, answer in questions_answers.items():
        if "NA" not in answer:
            qa_format += f"Question: {question}\nAnswer: {answer.replace("  ", '')}\n\n"

    return qa_format

pages = reader.pages[13:97]
text = pages[0].extract_text()
fs_date_match = re.search(r'as on ([a-zA-Z]+) \d{2}, (\d{4})', text)
fs_date = fs_date_match.group(1) + " " + fs_date_match.group(2)
for i, page in enumerate(pages):
    text = page.extract_text()
    if 'Fund Manager' in text:
        fund_info = {
        "fund_name": extract_fund_name(text),
        "inception": extract_inception_dates(text),
        "closing_aum": extract_closing_aum(text),
        "average_aum": extract_avg_aum(text),
        "minimum_first_investment": extract_min_investment(text),
        "minimum_additional_investment": extract_min_addl_investment(text),
        "investment_horizon": extract_investment_horizon(text),
        "expense_ratio": extract_expense_ratio(text),
        "no_of_folios_in_scheme": extract_no_of_folios_in_scheme(text),
        "average_dividend_yield": extract_avg_div_yield(text),
        "portfolio_turnover": extract_annual_portfolio_turnover(text),
        "ratios": extract_ratios(text),
        "fund_category": extract_fund_category(text),
        "fund_benchmark": extract_benchmark(text),
        "riskometer": extract_riskometer(text),
        "fund_managers": extract_fund_managers(text),
        "top_5_stock_holdings": extract_top_5_stock_holdings(text),
        "top_5_sector_holdings": extract_top_5_sector_holdings(text),
        "average_maturity": extract_average_maturity(text),
        "modified_duration": extract_modified_duration(text),
        "macaulay_duration": extract_macaulay_duration(text),
        "annualised_ytm": extract_annualised_ytm(text)
        }
        
        qa_text = convert_to_qa(fund_info, fs_date)
        
        # Save to text file
        with open('fund_qa.txt', 'a') as f:
            f.write(qa_text)