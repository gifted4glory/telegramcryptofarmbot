import requests
import json
from datetime import datetime, timedelta, timezone
import time  # Added import time
from colorama import Fore, Style  # Added import colorama
import os  # Added import os
import sys
import threading


def read_tokens():
    with open('spinner.txt', 'r') as file:
        return file.read().strip().split('\n')  # Read multiple tokens

def print_welcome_message():
    print(Fore.GREEN + Style.BRIGHT + "SpinnerCoin BOT")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_data(token):
    url = 'https://back.timboo.pro/api/init-data'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://spinner.timboo.pro',
        'priority': 'u=1, i',
        'referer': 'https://spinner.timboo.pro/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    data = {
        "initData": token
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        data = response.json()
        user = data.get('initData', {}).get('user', {})
        spinners = data.get('initData', {}).get('spinners', [])
        name = user.get('name')
        level = spinners[0].get('level') if spinners else None
        repair = spinners[0].get('endRepairTime') if spinners else None
        balance = user.get('balance')
        
        print(Fore.GREEN + f"[ Name ]: {name}" + Style.RESET_ALL)
        print(Fore.GREEN + f"[ Balance ]: {balance}" + Style.RESET_ALL)
        print(Fore.GREEN + f"[ Level ]: {level}" + Style.RESET_ALL)  # Green color for successfully retrieved data
        return data
    else:
        print(Fore.RED + "Token not found" + Style.RESET_ALL)  # Red color if data retrieval fails
        return None

def click_spinner(token, repair):
    url = 'https://back.timboo.pro/api/upd-data'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://spinner.timboo.pro',
        'priority': 'u=1, i',
        'referer': 'https://spinner.timboo.pro/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    data = {
        "initData": token,
        "data": {
            "clicks": 15,
            "isClose": None
        }
    }

    while True:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print(Fore.GREEN + "[ Clicking ]: Clicking..." + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "[ Clicking ]: Click complete..." + Style.RESET_ALL)
            break

    if repair:
        end_time = datetime.strptime(repair, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
        remaining_time = end_time - datetime.now(timezone.utc)
        hours, remainder = divmod(remaining_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        repair = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        print(f"{Fore.YELLOW}[ Repair ]: wait {repair}..." + Style.RESET_ALL)

def multi_thread_click_spinner(token, repair, num_threads=100):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=click_spinner, args=(token, repair))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()


def repair_spinner(token):
    url = 'https://back.timboo.pro/api/repair-spinner'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://spinner.timboo.pro',
        'priority': 'u=1, i',
        'referer': 'https://spinner.timboo.pro/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    data = {
        "initData": token
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        print(Fore.GREEN + "[ Repair ]: Spinner repair successful..." + Style.RESET_ALL)  # Green color for successful repair
    else:
        print(Fore.RED + "[ Repair ]: Spinner repair failed..." + Style.RESET_ALL)  # Red color for failed repair

def check_requirement(token, id_task):
    url = 'https://api.timboo.pro/check_requirement'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://spinner.timboo.pro',
        'priority': 'u=1, i',
        'referer': 'https://spinner.timboo.pro/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    data = {
        "initData": token,
        "requirementId": id_task
    }

    response = requests.post(url, headers=headers, json=data)
    time.sleep(2)
    
    try:
        result = response.json()
    except json.JSONDecodeError:
        if response.status_code == 500:
            print(Fore.RED + f"[ Clear Task ]: Server Error. Code {response}" + Style.RESET_ALL)
            return
        else:
            print(Fore.RED + f"[ Clear Task ]: JSON could not be decoded {response}" + Style.RESET_ALL)
        return

    # ... existing code ...
    if response.status_code == 200:
        if result.get('message') == "it's impossible to do the requirement 2 times":
            print(Fore.YELLOW + "[ Clear Task ]: Already Done" + Style.RESET_ALL)  # Yellow color if the task can be done twice

        elif not result.get('reward') and not result.get('success'):
            print(Fore.RED + f"[ Clear Task ]: No reward. {result.get('message')}" + Style.RESET_ALL)  # Red color if reward fails
        else:
            print(Fore.GREEN + f"[ Clear Task ]: Task successfully cleared | Reward {result.get('reward')} Points" + Style.RESET_ALL)  # Green color if reward succeeds
    else:
        print(Fore.RED + f"[ Clear Task ]: Requirement check failed. {result.get('message')}")

def auto_upgrade(token, spinner_id):
    url = 'https://back.timboo.pro/api/upgrade-spinner'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://spinner.timboo.pro',
        'priority': 'u=1, i',
        'referer': 'https://spinner.timboo.pro/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    
    data = {
        "initData": token,
        "spinnerId": spinner_id
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        print(Fore.GREEN + "[ Upgrade ]: " + result.get("message", "Message not received") + Style.RESET_ALL)  # Green color for successful upgrade
    else:
        print(Fore.RED + "[ Upgrade ]: Spinner upgrade failed" + Style.RESET_ALL)  # Red color for failed upgrade

def def_rocket(token, spinner_id):
    url = 'https://back.timboo.pro/api/rocket-activate'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://spinner.timboo.pro',
        'priority': 'u=1, i',
        'referer': 'https://spinner.timboo.pro/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }
    
    data = {
        "initData": token,
        "spinnerId": spinner_id
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        print(Fore.GREEN + "[ Rocket ]: Rocket Successfully Activated!" + Style.RESET_ALL)  # Green color if rocket is active
    else:
        print(Fore.RED + "[ Rocket ]: Rocket not found!" + Style.RESET_ALL)  # Red color if rocket is inactive

def claim_daily(token):
    url = 'https://api.timboo.pro/open_box'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://spinner.timboo.pro',
        'priority': 'u=1, i',
        'referer': 'https://spinner.timboo.pro/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }
    
    data = {
        "initData": token,
        "boxId": 8
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        print(Fore.GREEN + f"[ Daily Claim ]: Daily claim successful! Reward: {result.get('reward_text')}" + Style.RESET_ALL)  # Green color for successful daily claim
    else:
        print(Fore.RED + "[ Daily Claim ]: Daily claim not found" + Style.RESET_ALL)  # Red color for failed daily claim

def def_fullhp(token, spinner_id):
    url = 'https://back.timboo.pro/api/fullhp-activate'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://spinner.timboo.pro',
        'priority': 'u=1, i',
        'referer': 'https://spinner.timboo.pro/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }
    
    data = {
        "initData": token,
        "spinnerId": spinner_id
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        print(Fore.GREEN + "[ FullHP ]: " + result.get("message", "Message not received") + Style.RESET_ALL)  # Green color for successful Full HP
    elif response.status_code == 400:
        print(Fore.RED + "[ FullHP ]: Full HP not found" + Style.RESET_ALL)  # Red color if Full HP is not found
    else:
        print(Fore.RED + "[ FullHP ]: Full HP could not be activated" + Style.RESET_ALL)  # Red color if Full HP is not activated

def main():
    print_welcome_message()
    # Add auto upgrade question
    auto_upgrade_spinner = 'n'
    # Add rocket activation question
    activate_rocket = 'y'
    # Add Full HP activation question
    activate_fullhp = 'y'
    # Add auto reward claim question
    auto_claim_reward = 'y'
    # Add daily reward claim question
    auto_claim_daily = 'y'
    
    while True:
        tokens = read_tokens()  # Read all tokens from the file
        for index, token in enumerate(tokens):
            print(f"{Fore.CYAN+Style.BRIGHT}============== [  Account {index + 1}  ] ==============" + Style.RESET_ALL)  # Print account name
            data = get_data(token)
            if data:
                spinners = data.get('initData', {}).get('spinners', [])
                if spinners:
                    spinner_id = spinners[0].get('id')
                    if auto_upgrade_spinner == 'e':
                        auto_upgrade(token, spinner_id)  # Call auto_upgrade function if 'e' is answered
                repair = spinners[0].get('endRepairTime') if spinners else None
                repair_spinner(token)
                
                if activate_fullhp == 'e':
                    def_fullhp(token, spinner_id)  # Call def_fullhp function if 'e' is answered
                if activate_rocket == 'e':
                    def_rocket(token, spinner_id)
                    multi_thread_click_spinner(token, repair)  # Start multi-threaded click_spinner after rocket is activated
                else:
                    click_spinner(token, repair)
                if auto_claim_daily == 'e':
                    claim_daily(token)  # Call claim_daily function if 'e' is answered
                if auto_claim_reward == 'e':
                    for i in range(1, 110):
                        check_requirement(token, i)  # Call check_requirement function if 'e' is answered

                click_spinner(token, repair)
                
        for i in range(360, 0, -1):
            sys.stdout.write(f"\r{Fore.CYAN+Style.BRIGHT}============ Completed, wait {i} seconds.. ============")
            sys.stdout.flush()
            time.sleep(1)
        print()  # Print a new line after countdown is complete

        # Clear console after countdown is complete
        clear_console()
        time.sleep(5)  # Add a 5-second delay before restarting the loop

if __name__ == "__main__":
    main()
