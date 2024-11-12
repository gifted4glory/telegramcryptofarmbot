import requests
import time
from colorama import Fore, Style, init
import json
from datetime import datetime, timedelta, timezone
import argparse
import urllib.parse

def parse_arguments():
    parser = argparse.ArgumentParser(description='TimeFarm BOT')
    parser.add_argument('--task', type=str, choices=['y', 'n'], default='y', help='Request Task (y/n)')
    parser.add_argument('--upgrade', type=str, choices=['y', 'n'], default='n', help='Automatic Upgrade (y/n)')
    args = parser.parse_args()

    if args.task is None:
        task_input = input("Would you like to automatically request tasks? (y/n, default n): ").strip().lower()
        args.task = task_input if task_input in ['y', 'n'] else 'n'
    
    if args.upgrade is None:
        upgrade_input = input("Would you like to automatically upgrade the hours? (y/n, default n): ").strip().lower()
        args.upgrade = upgrade_input if upgrade_input in ['y', 'n'] else 'n'

    return args

args = parse_arguments()
check_task_enable = args.task
check_upgrade_enable = args.upgrade

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'text/plain;charset=UTF-8',
    'origin': 'https://tg-tap-miniapp.laborx.io',
    'priority': 'u=1, i',
    'referer': 'https://tg-tap-miniapp.laborx.io/',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def get_access_token_and_info(query_data):
    url = 'https://tg-bot-tap.laborx.io/api/v1/auth/validate-init'
    try:
        response = requests.post(url, headers=headers, data=query_data)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Parsing Error: Your request is invalid")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def check_farming(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/farming/info'
    headers['authorization'] = f'Bearer {token}'
    response = requests.get(url, headers=headers)
    return response.json()

def start_farming(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/farming/start'
    headers['authorization'] = f'Bearer {token}'
    response = requests.post(url, headers=headers, json={})
    return response.json()

def finish_farming(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/farming/finish'
    headers['authorization'] = f'Bearer {token}'
    response = requests.post(url, headers=headers, json={})
    return response.json()

def check_task(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/tasks'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def submit_task(token, task_id):
    url = f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/submissions'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json={})
    return response.json()

def claim_task(token, task_id):
    url = f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/claims'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json={})
    return response.json()

start_time = datetime.now()

def upgrade_level(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/me/level/upgrade'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://tg-tap-miniapp.laborx.io',
        'referer': 'https://tg-tap-miniapp.laborx.io/',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.post(url, headers=headers)
    return response.json()

def auto_upgrade(token):
    while True:
        response = upgrade_level(token)
        if 'error' in response:
            if response['error']['message'] == "Insufficient balance":
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade ] : Insufficient balance for upgrade.", flush=True)
                break
            elif response['error']['message'] == "Forbidden":
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade ] : Upgrade error.", flush=True)
            elif response['error']['message'] == "Reached maximum level":
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade ] : Maximum level reached.", flush=True)
                break
            else:
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade ] : Upgrade error. {response['error']['message']}", flush=True)
                break
        else:
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade ] : Upgrade successful, continuing..", flush=True)

def animated_loading(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(f"\rWaiting for next request time {frame} - Remaining {remaining_time} seconds         ", end="", flush=True)
            time.sleep(0.25)
    print("\rNext request time completed.                            ", flush=True)     

def print_welcome_message():
    print(Fore.GREEN + Style.BRIGHT + "Timefarm BOT!")
    current_time = datetime.now()
    up_time = current_time - start_time
    days, remainder = divmod(up_time.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    # print(Fore.CYAN + Style.BRIGHT + f"Bot uptime: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")

def extract_user_details(query_line):
    parts = query_line.split('&')
    user_info_encoded = [part for part in parts if part.startswith('user=')][0]
    user_info_encoded = user_info_encoded.split('=')[1]
    user_info_json = urllib.parse.unquote(user_info_encoded)
    user_info = json.loads(user_info_json)
    return user_info.get('username', "No Username"), user_info.get('first_name', "No First Name"), user_info.get('last_name', "No Last Name")

def main():
    while True:
        print_welcome_message()
        try:
            with open('timefarm.txt', 'r') as file:
                queries = file.readlines()
            
            for query_data in queries:
                username, first_name, last_name = extract_user_details(query_data.strip())

                query_data = query_data.strip()
                auth_response = get_access_token_and_info(query_data)
                token = auth_response['token']

                balance_info = auth_response['balanceInfo']

                print(Fore.CYAN + Style.BRIGHT + f"\n===== [ {first_name} {last_name} | {username} ] =====")
                print(Fore.YELLOW + Style.BRIGHT + f"[ Balance ] : {int(balance_info['balance']):,}".replace(',', '.'))
                if check_upgrade_enable == 'y':
                    print(Fore.YELLOW + Style.BRIGHT + f"\r[ Upgrade ] : Upgrading hours..", end="", flush=True)
                    auto_upgrade(token)
                if check_task_enable == 'y':
                    print(Fore.YELLOW + Style.BRIGHT + f"\r[ Task ] : Checking ...", end="", flush=True)
                    tasks = check_task(token)
      
                    if tasks:
                        for task in tasks:
                            if task.get('submission', {}).get('status') == 'CLAIMED':
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Task ] : {task['title']} | Claimed                                               ", flush=True)
                            elif task.get('submission', {}).get('status') == 'COMPLETED':
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Task ] : {task['title']} claiming task", flush=True)
                                response = claim_task(token, task['id'])
                                if response is not None:
                                    if 'error' in response:
                                        if response['error']['message'] == "Failed to claim reward":
                                            print(Fore.RED + Style.BRIGHT + f"\r[ Task ] : Task claim: {task['title']} | Already claimed", end="", flush=True)
                                    else:
                                        print(Fore.GREEN + Style.BRIGHT + f"\r[ Task ] : Task claim: {task['title']} | Claimed", flush=True)    
                            
                            else:
                                print(f"\r[ Task ] : Submitting task: {task['title']}", end="", flush=True)
                                if task.get('submission', {}).get('status') == 'SUBMITTED':
                                    print(Fore.YELLOW + Style.BRIGHT + f"\r[ Task ] : Task submission: {task['title']} | Already Submitted", flush=True)
                                else:
                                    response = submit_task(token, task['id'])
                                    if response is not None:
                                        if 'error' in response:
                                            print(Fore.RED + Style.BRIGHT + f"\r[ Task ] : Task submission: {task['title']} | {response['error']['message']}", end="", flush=True)
                                        else:
                                            print(Fore.GREEN + Style.BRIGHT + f"\r[ Task ] : Task submission: {task['title']} | Submitted", flush=True)
                                    time.sleep(3)
                                print(f"\r[ Task ] : Claiming task: {task['title']}", end="", flush=True)
                                response = claim_task(token, task['id'])
                                if response is not None:
                                    if 'error' in response:
                                        if response['error']['message'] == "Failed to claim reward":
                                            print(Fore.RED + Style.BRIGHT + f"\r[ Task ] : Task claim: {task['title']} | Reward claim failed / already claimed", end="", flush=True)
                                    else:
                                        print(Fore.GREEN + Style.BRIGHT + f"\r[ Task ] : Task claim: {task['title']} | Claimed", flush=True)
                print(Fore.YELLOW + Style.BRIGHT + f"\r[ Farming ] : Checking ...", end="", flush=True)
                time.sleep(2)
                farming_response = finish_farming(token)
                if farming_response is not None:
                    if 'error' in farming_response:
                        if farming_response['error']['message'] == "Too early to finish farming":

                            check_farming_response = check_farming(token)
                            if check_farming_response:
                                started_at = datetime.fromisoformat(check_farming_response['activeFarmingStartedAt'].replace('Z', '+00:00')).astimezone(timezone.utc)
                                duration_sec = check_farming_response['farmingDurationInSec']
                                end_time = started_at + timedelta(seconds=duration_sec)
                                time_now = datetime.now(timezone.utc)

                                remaining_time = end_time - time_now
                                if remaining_time.total_seconds() > 0:
                                    hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                                    minutes, _ = divmod(remainder, 60)
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Farming ] : Farming can be claimed in {int(hours)} hours {int(minutes)} minutes", flush=True)
                                else:
                                    print(Fore.GREEN + Style.BRIGHT + f"\r[ Farming ] : Farming can be claimed now", flush=True)
                        elif farming_response['error']['message'] == "Farming not started":
                            print(Fore.YELLOW + Style.BRIGHT + f"\r[ Farming ] : Starting farming..", end="", flush=True)
                            time.sleep(2)
                            start_farming_response = start_farming(token)
                            if start_farming_response is not None:
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Farming ] : Started | Reward: {int(start_farming_response['farmingReward']):,}".replace(',', '.'), flush=True)
                            else:
                                if 'error' in start_farming_response:
                                    if start_farming_response['error']['message'] == "Farming already started":
                                        print(Fore.RED + Style.BRIGHT + f"\r[ Farming ] : Farming already started", flush=True)
                                else:
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Farming ] : Unable to start farming", flush=True)
                        else:
                            print(f"\r[ Farming ] : {farming_response['error']['message']}", flush=True)
                    else:
                        print(Fore.GREEN + Style.BRIGHT + f"\r[ Farming ] : Claimed | Balance: {int(farming_response['balance']):,}".replace(',', '.'), flush=True)
                        print(Fore.YELLOW + Style.BRIGHT + f"\r[ Farming ] : Checking farming..", end="", flush=True)
                        time.sleep(2)
                        check_farming_response = check_farming(token)
                        if check_farming_response is not None:
                            if check_farming_response['activeFarmingStartedAt'] is None:
                                print(Fore.RED + Style.BRIGHT + f"\r[ Farming ] : Farming not started", flush=True)
                                print(Fore.YELLOW + Style.BRIGHT + f"\r[ Farming ] : Starting farming..", end="", flush=True)
                                time.sleep(2)
                                start_farming_response = start_farming(token)
                                if start_farming_response is not None:
                                    print(Fore.GREEN + Style.BRIGHT + f"\r[ Farming ] : Started | Reward: {int(start_farming_response['farmingReward']):,}".replace(',', '.'), flush=True)
                                else:
                                    if 'error' in start_farming_response:
                                        if start_farming_response['error']['message'] == "Farming already started":
                                            print(Fore.RED + Style.BRIGHT + f"\r[ Farming ] : Farming already started", flush=True)
                                    else:
                                        print(Fore.RED + Style.BRIGHT + f"\r[ Farming ] : Unable to start farming", flush=True)
                            else:
                                print(Fore.YELLOW + Style.BRIGHT + f"\r[ Farming ] : Farming already started", flush=True)                              
                else:
                    print(Fore.RED + Style.BRIGHT + f"\r[ Farming ] : Farming check failed", flush=True)
                    continue

            print(Fore.BLUE + Style.BRIGHT + f"\n==========ALL ACCOUNTS PROCESSED==========\n",  flush=True)    
            animated_loading(300)            
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
