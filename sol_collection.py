import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

def fetch_daily_solution(date: str) -> dict:
    """
    Fetches the daily Letter Boxed solution from the website.
    
    Args:
        date (str): The date in the format 'YYYY/MM/DD'
        
    Returns:
        dict: A dictionary containing the letter square and the solution.
    """
    url = f"https://letterboxedanswers.com/{date.replace('-', '/')}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data for {date}. Status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    letter_square = extract_letter_square(soup)
    solution = extract_solution(soup)
    
    if letter_square and solution:
        return {"date": date, "letter_square": letter_square, "solution": solution}
    else:
        print(f"Failed to extract solution for {date}.")
        return None

def extract_letter_square(soup: BeautifulSoup) -> list:
    """
    Extracts the letter square from the HTML soup.
    
    Args:
        soup (BeautifulSoup): Parsed HTML of the page.
        
    Returns:
        list: A list of letter square sides.
    """
    square_element = soup.find_all('span', class_='fjalet')

    if square_element:
        letters = [span.get_text().strip() for span in square_element[:4]]
        return [list(letters[i]) for i in range(4)]
    return None

def extract_solution(soup: BeautifulSoup) -> list:
    """
    Extracts the solution from the HTML soup.
    
    Args:
        soup (BeautifulSoup): Parsed HTML of the page.
        
    Returns:
        list: A list of solution words.
    """
    solution_element = soup.find_all('span', class_='fjalet')
    
    if solution_element and len(solution_element) > 4:
        solution_words = [span.get_text().strip() for span in solution_element[4:]]
        return solution_words
    return None

def save_solution(data: dict, output_file: str):
    """
    Saves the collected data into a JSON file.
    
    Args:
        data (dict): The solution data to save.
        output_file (str): The file to save the data into.
    """
    with open(output_file, 'a') as file:
        json.dump(data, file)
        file.write('\n')

def collect_data(start_date: str, end_date: str, output_file: str):
    """
    Collects solutions between a date range and saves them to a file.
    
    Args:
        start_date (str): Start date in the format 'YYYY-MM-DD'.
        end_date (str): End date in the format 'YYYY-MM-DD'.
        output_file (str): Path to the file where data should be saved.
    """
    current_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        print(f"Fetching solution for {date_str}...")
        data = fetch_daily_solution(date_str)
        if data:
            save_solution(data, output_file)
        current_date += timedelta(days=1)

if __name__ == "__main__":
    start_date = '2020-12-09'
    end_date = '2024-10-12'
    output_file = 'letterboxed_solutions.json'
    
    collect_data(start_date, end_date, output_file)
