import requests

def check_cve(cve_id):
    while True:
        if not cve_id.startswith("CVE-"):
            print("Error: Please enter a valid CVE ID in the format 'CVE-Year-Number', e.g., 'CVE-2021-12345'")
            cve_id = input("Enter CVE ID to check for vulnerabilities: ")
            continue

        url = f"https://cve.circl.lu/api/cve/{cve_id}"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            cve_data = response.json()
            print(f"Vulnerability: {cve_data['id']}")
            print(f"Description: {cve_data['summary']}")
            break  
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error: {err}")
        except requests.exceptions.ConnectionError:
            print("Error: Connection error. Please check your internet connection.")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}. Failed to retrieve information for CVE {cve_id}.")
        except KeyError:
            print(f"Error: No information found for CVE {cve_id}.")
        
        cve_id = input("Enter CVE ID to check for vulnerabilities: ")  
