import requests
import curses
import re

def check_cve(cve_id, stdscr):
    stdscr.scrollok(True)  
    while True:
        if not re.match(r'^CVE-\d{4}-\d{4}$', cve_id):
            stdscr.addstr(3, 0, "Error: Please enter a valid CVE ID in the format 'CVE-Year-Number', e.g., 'CVE-2021-12345'")
            stdscr.refresh()
            stdscr.addstr(4, 0, "Try again:")
            stdscr.refresh()
            cve_id = get_input(stdscr, 4, len("Try again: ")) 
            stdscr.refresh()             
            continue

        url = f"https://cve.circl.lu/api/cve/{cve_id}"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            cve_data = response.json()
            if cve_data is not None:
                stdscr.addstr(0, 0, f"Vulnerability: {cve_data['id']}")
                stdscr.addstr(2, 0, f"Description: {cve_data['summary']}")
                stdscr.refresh()
                break  
            else:
                stdscr.clear()         
                stdscr.addstr(0, 0, f"Error: No information found for CVE {cve_id}.")
                stdscr.refresh()
        except requests.exceptions.HTTPError as err:
            stdscr.clear()  
            stdscr.addstr(0, 0, f"HTTP Error: {err}")
            stdscr.refresh()
        except requests.exceptions.ConnectionError:
            stdscr.clear()  
            stdscr.addstr(0, 0, "Error: Connection error. Please check your internet connection.")
            stdscr.refresh()
        except requests.exceptions.RequestException as e:
            stdscr.clear()  
            stdscr.addstr(0, 0, f"Error: {e}. Failed to retrieve information for CVE {cve_id}.")
            stdscr.refresh()
        except KeyError:
            stdscr.clear()  
            stdscr.addstr(0, 0, f"Error: No information found for CVE {cve_id}.")
            stdscr.refresh()
        
        cve_id = get_input(stdscr, 3, 0)

def get_input(stdscr, row, col):
    curses.echo()  
    input_str = stdscr.getstr(row, col).decode('utf-8')
    curses.noecho()  
    return input_str
