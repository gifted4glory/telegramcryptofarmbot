import requests
import time
from colorama import init, Fore, Style
import json
from datetime import datetime, timezone
import argparse
import urllib.parse
import random
from requests.structures import CaseInsensitiveDict

init(autoreset=True)

start_time = datetime.now() 

def parse_arguments():
    parser = argparse.ArgumentParser(description='Blum BOT')
    parser.add_argument('--task', type=str, choices=['y', 'n'], default='y', help='Check and Claim Task (y/n)')
    parser.add_argument('--reff', type=str, choices=['y', 'n'], default='y', help='Do you want to claim ref? (y/n, default n)')
    args = parser.parse_args()

    if args.task is None:
        task_input = input("Do you want to check and claim task? (y/n, default n): ").strip().lower()
        args.task = task_input if task_input in ['y', 'n'] else 'n'

    if args.reff is None:
        reff_input = input("Do you want to claim ref? (y/n, default n): ").strip().lower()
        args.reff = reff_input if reff_input in ['y', 'n'] else 'n'

    return args

def check_tasks(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }

    try:
        response = requests.get('https://game-domain.blum.codes/api/v1/tasks', headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            for task in tasks:
                title = task['title']
                if task['status'] == 'CLAIMED':
                    print(f"{Fore.CYAN+Style.BRIGHT}Task {title} claimed | Status: {task['status']} | Reward: {task['reward']}")
                elif task['status'] == 'NOT_STARTED':
                    print(f"{Fore.YELLOW+Style.BRIGHT}Starting Task: {task['title']}")
                    start_task(token, task['id'], title)
                    claim_task(token, task['id'], title)
                else:
                    print(f"{Fore.CYAN+Style.BRIGHT}Task already started: {task['title']} | Status: {task['status']} | Reward: {task['reward']}")
        else:
            print(f"{Fore.RED+Style.BRIGHT}\nFailed to get tasks")
    except:
        print(f"{Fore.RED+Style.BRIGHT}\nFailed to get tasks {response.status_code} ")

def start_task(token, task_id, title):
    url = f'https://game-domain.blum.codes/api/v1/tasks/{task_id}/start'
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            print(f"{Fore.GREEN+Style.BRIGHT}\nTask {title} started")
        else:
            print(f"{Fore.RED+Style.BRIGHT}\nFailed to start task {title}")
        return
    except:
        print(f"{Fore.RED+Style.BRIGHT}\nFailed to start task {title} {response.status_code} ")

def claim_task(token, task_id, title):
    print(f"{Fore.YELLOW+Style.BRIGHT}\nClaiming task {title}")
    url = f'https://game-domain.blum.codes/api/v1/tasks/{task_id}/claim'
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            print(f"{Fore.CYAN+Style.BRIGHT}\nTask {title} claimed")
        else:
            print(f"{Fore.RED+Style.BRIGHT}\nFailed to claim task {title}")
    except:
        print(f"{Fore.RED+Style.BRIGHT}\nFailed to claim task {title} {response.status_code} ")

def get_new_token(query_id):
    import json
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://telegram.blum.codes",
        "priority": "u=1, i",
        "referer": "https://telegram.blum.codes/"
    }
    data = json.dumps({"query": query_id})
    url = "https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"

    for attempt in range(3):
        print(f"\r{Fore.YELLOW+Style.BRIGHT}Getting token...", end="", flush=True)
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            print(f"\r{Fore.GREEN+Style.BRIGHT}Token successfully created", end="", flush=True)
            response_json = response.json()
            return response_json['token']['refresh']
        else:
            print(response.json())
            print(f"\r{Fore.RED+Style.BRIGHT}Failed to get token, attempt {attempt + 1}", flush=True)

    print(f"\r{Fore.RED+Style.BRIGHT}Failed to get token after 3 attempts.", flush=True)
    return None

def get_user_info(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.get('https://gateway.blum.codes/v1/user/me', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        result = response.json()
        if result['message'] == 'Token is invalid':
            print(f"{Fore.RED+Style.BRIGHT}Invalid token, getting a new token...")
            new_token = get_new_token()
            if new_token:
                print(f"{Fore.GREEN+Style.BRIGHT}New token obtained, trying again...")
                return get_user_info(new_token)
            else:
                print(f"{Fore.RED+Style.BRIGHT}Failed to get new token.")
                return None
        else:
            print(f"{Fore.RED+Style.BRIGHT}Failed to get user information")
            return None

def get_balance(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    for attempt in range(3):
        try:
            response = requests.get('https://game-domain.blum.codes/api/v1/user/balance', headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"\r{Fore.RED+Style.BRIGHT}Failed to get balance, attempt {attempt + 1}", flush=True)
        except requests.exceptions.ConnectionError as e:
            print(f"\r{Fore.RED+Style.BRIGHT}Connection failed, trying again {attempt + 1}", flush=True)
        except Exception as e:
            print(f"\r{Fore.RED+Style.BRIGHT}Error: {str(e)}", flush=True)
        except:
            print(f"\r{Fore.RED+Style.BRIGHT}Failed to get balance, trying again {attempt + 1}", flush=True)
    print(f"\r{Fore.RED+Style.BRIGHT}Failed to get balance after 3 attempts.", flush=True)
    return None

def play_game(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'content-length': '0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response = requests.post('https://game-domain.blum.codes/api/v1/game/play', headers=headers)
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print(f"{Fore.RED+Style.BRIGHT}Failed to play game due to connection issues: {e}")
    except Exception as e:
        print(f"{Fore.RED+Style.BRIGHT}Failed to play game due to error: {e}")
    return None

def claim_game(token, game_id, points):
    url = "https://game-domain.blum.codes/api/v1/game/claim"
    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json, text/plain, */*"
    headers["accept-language"] = "en-US,en;q=0.9"
    headers["authorization"] = "Bearer " + token
    headers["content-type"] = "application/json"
    headers["origin"] = "https://telegram.blum.codes"
    headers["priority"] = "u=1, i"
    headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    data = '{"gameId":"' + game_id + '","points":' + str(points) + '}'

    try:
        resp = requests.post(url, headers=headers, data=data)
        return resp
    except requests.exceptions.ConnectionError as e:
        print(f"{Fore.RED+Style.BRIGHT}Failed to claim game reward due to connection issues: {e}")
    except Exception as e:
        print(f"{Fore.RED+Style.BRIGHT}Failed to claim game reward due to error: {e}")
    return None

def claim_balance(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response = requests.post('https://game-domain.blum.codes/api/v1/farming/claim', headers=headers)
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print(f"{Fore.RED+Style.BRIGHT}Failed to claim balance due to connection issues: {e}")
    except Exception as e:
        print(f"{Fore.RED+Style.BRIGHT}Failed to claim balance due to error: {e}")
    return None

def start_farming(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response = requests.post('https://game-domain.blum.codes/api/v1/farming/start', headers=headers)
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print(f"{Fore.RED+Style.BRIGHT}Failed to start farming due to connection issues: {e}")
    except Exception as e:
        print(f"{Fore.RED+Style.BRIGHT}Failed to start farming due to error: {e}")
    return None

def refresh_token(old_refresh_token):
    url = 'https://gateway.blum.codes/v1/auth/refresh'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'origin': 'https://telegram.blum.codes',
        'referer': 'https://telegram.blum.codes/'
    }
    data = {
        'refresh': old_refresh_token
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"{Fore.RED+Style.BRIGHT}Failed to refresh token for: {old_refresh_token}")
            return None
    except requests.exceptions.ConnectionError as e:
        print(f"{Fore.RED+Style.BRIGHT}Failed to refresh token due to connection issues: {e}")
    except Exception as e:
        print(f"{Fore.RED+Style.BRIGHT}Failed to refresh token due to error: {e}")
    return None

def check_balance_friend(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response = requests.get('https://gateway.blum.codes/v1/friends/balance', headers=headers)
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print(f"{Fore.RED+Style.BRIGHT}Failed to get friend's balance due to connection issues: {e}")
    except Exception as e:
        print(f"{Fore.RED+Style.BRIGHT}Failed to get friend's balance due to error: {e}")
    return None

def claim_balance_friend(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response = requests.post('https://gateway.blum.codes/v1/friends/claim', headers=headers)
        return response.json()
    except requests.exceptions.ConnectionError as e:
        print(f"{Fore.RED+Style.BRIGHT}Failed to claim friend's balance due to connection issues: {e}")
    except Exception as e:
        print(f"{Fore.RED+Style.BRIGHT}Failed to claim friend's balance due to error: {e}")
    return None

def check_daily_reward(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'content-length': '0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site'
    }
    try:
        response = requests.post('https://game-domain.blum.codes/api/v1/daily-reward?offset=-420', headers=headers, timeout=10)
        if response.status_code == 400:
            try:
                return response.json()
            except json.JSONDecodeError:
                if response.text == "OK":
                    return response.text
                return None
        else:
            try:
                return response.json()
            except json.JSONDecodeError:
                print(f"{Fore.RED+Style.BRIGHT}Json Error: {response.text}")
                return None
            return None
    except requests.exceptions.Timeout:
        print(f"\r{Fore.RED+Style.BRIGHT}Failed to claim daily reward: Timeout")
    except requests.exceptions.RequestException as e:
        return response.json()
      
    return None

def print_welcome_message():
    print(Fore.GREEN + Style.BRIGHT + "Blum BOT")
    current_time = datetime.now()
    up_time = current_time - start_time
    days, remainder = divmod(up_time.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

checked_tasks = {}

args = parse_arguments()
cek_task_enable = args.task
claim_ref_enable = args.reff
with open('blum.txt', 'r') as file:
    query_ids = file.read().splitlines()
while True:
    try:
        print_welcome_message()

        for query_id in query_ids:
            token = get_new_token(query_id) 
            user_info = get_user_info(token)
            if user_info is None:
                continue
            print(f"{Fore.BLUE+Style.BRIGHT}\r\n==================[{Fore.WHITE+Style.BRIGHT}{user_info['username']}{Fore.BLUE+Style.BRIGHT}]==================")
            print(f"\r{Fore.YELLOW+Style.BRIGHT}Fetching Information....", end="", flush=True)
            balance_info = get_balance(token)
            if balance_info is None:
                print(f"\r{Fore.RED+Style.BRIGHT}Failed to fetch balance information", flush=True)
                continue
            else:
                available_balance_before = balance_info['availableBalance']
                balance_before = f"{float(available_balance_before):,.0f}".replace(",", ".")
                print(f"\r{Fore.YELLOW+Style.BRIGHT}[Balance]: {balance_before}", flush=True)
                print(f"{Fore.MAGENTA+Style.BRIGHT}[Game Tickets]: {balance_info['playPasses']}")

                farming_info = balance_info.get('farming')

                if farming_info:
                    end_time_ms = farming_info['endTime']
                    end_time_s = end_time_ms / 1000.0
                    end_utc_date_time = datetime.fromtimestamp(end_time_s, timezone.utc)
                    current_utc_time = datetime.now(timezone.utc)
                    time_difference = end_utc_date_time - current_utc_time
                    hours_remaining = int(time_difference.total_seconds() // 3600)
                    minutes_remaining = int((time_difference.total_seconds() % 3600) // 60)
                    farming_balance = farming_info['balance']
                    farming_balance_formatted = f"{float(farming_balance):,.0f}".replace(",", ".")
                    print(f"{Fore.RED+Style.BRIGHT}[Claim Balance]: {hours_remaining} hours {minutes_remaining} minutes | Balance: {farming_balance_formatted}")

                    if hours_remaining < 0:
                        print(f"\r{Fore.GREEN+Style.BRIGHT}[Claim Balance]: Claiming balance...", end="", flush=True)
                        claim_response = claim_balance(token)
                        if claim_response:
                            print(f"\r{Fore.GREEN+Style.BRIGHT}[Claim Balance]: Claimed: {claim_response['availableBalance']}                ", flush=True)
                            print(f"\r{Fore.GREEN+Style.BRIGHT}[Claim Balance]: Starting farming...", end="", flush=True)
                            start_response = start_farming(token)
                            if start_response:
                                print(f"\r{Fore.GREEN+Style.BRIGHT}[Claim Balance]: Farming started.", flush=True)
                            else:
                                print(f"\r{Fore.RED+Style.BRIGHT}[Claim Balance]: Failed to start farming", start_response.status_code, flush=True)
                        else:
                            print(f"\r{Fore.RED+Style.BRIGHT}[Claim Balance]: Failed to claim", claim_response.status_code, flush=True)
                else:
                    print(f"\n{Fore.RED+Style.BRIGHT}[Claim Balance]: Failed to fetch farming information", flush=True)
                    print(f"\r{Fore.GREEN+Style.BRIGHT}[Claim Balance]: Claiming balance...", end="", flush=True)
                    claim_response = claim_balance(token)
                    if claim_response:
                        print(f"\r{Fore.GREEN+Style.BRIGHT}[Claim Balance]: Claimed               ", flush=True)
                        print(f"\r{Fore.GREEN+Style.BRIGHT}[Claim Balance]: Starting farming...", end="", flush=True)
                        start_response = start_farming(token)
                        if start_response:
                            print(f"\r{Fore.GREEN+Style.BRIGHT}[Claim Balance]: Farming started.", flush=True)
                        else:
                            print(f"\r{Fore.RED+Style.BRIGHT}[Claim Balance]: Failed to start farming", start_response.status_code, flush=True)
                    else:
                        print(f"\r{Fore.RED+Style.BRIGHT}[Claim Balance]: Failed to claim", claim_response.status_code, flush=True)

            print(f"\r{Fore.CYAN+Style.BRIGHT}[Daily Reward]: Checking daily reward...", end="", flush=True)
            daily_reward_response = check_daily_reward(token)
            if daily_reward_response is None:
                print(f"\r{Fore.RED+Style.BRIGHT}[Daily Reward]: Failed to check daily reward", flush=True)
            else:
                if daily_reward_response.get('message') == 'same day':
                    print(f"\r{Fore.CYAN+Style.BRIGHT}[Daily Reward]: Daily reward already claimed today", flush=True)
                elif daily_reward_response.get('message') == 'OK':
                    print(f"\r{Fore.CYAN+Style.BRIGHT}[Daily Reward]: Daily reward successfully claimed!", flush=True)
                else:
                    print(f"\r{Fore.RED+Style.BRIGHT}[Daily Reward]: Failed to check daily reward. {daily_reward_response}", flush=True)

            if cek_task_enable == 'y':
                if query_id not in checked_tasks or not checked_tasks[query_id]:
                    print(f"\r{Fore.YELLOW+Style.BRIGHT}Checking tasks...\n", end="", flush=True)
                    check_tasks(token)
                    checked_tasks[query_id] = True

            print(f"\r{Fore.YELLOW+Style.BRIGHT}[Ref Balance]: Checking ref balance...", end="", flush=True)
            if claim_ref_enable == 'y':
                friend_balance = check_balance_friend(token)
                if friend_balance:
                    if friend_balance['canClaim']:
                        print(f"\r{Fore.GREEN+Style.BRIGHT}Ref Balance: {friend_balance['amountForClaim']}", flush=True)
                        print(f"\n\r{Fore.GREEN+Style.BRIGHT}Claiming Ref balance.....", flush=True)
                        claim_friend_balance = claim_balance_friend(token)
                        if claim_friend_balance:
                            claimed_amount = claim_friend_balance['claimBalance']
                            print(f"\r{Fore.GREEN+Style.BRIGHT}[Ref Balance]: Successfully claimed total: {claimed_amount}", flush=True)
                        else:
                            print(f"\r{Fore.RED+Style.BRIGHT}[Ref Balance]: Failed to claim ref balance", flush=True)
                    else:
                        can_claim_at = friend_balance.get('canClaimAt')
                        if can_claim_at:
                            claim_time = datetime.fromtimestamp(int(can_claim_at) / 1000)
                            current_time = datetime.now()
                            time_diff = claim_time - current_time
                            hours, remainder = divmod(int(time_diff.total_seconds()), 3600)
                            minutes, seconds = divmod(remainder, 60)
                            print(f"{Fore.RED+Style.BRIGHT}\r[Ref Balance]: Claim in {hours} hours {minutes} minutes", flush=True)
                        else:
                            print(f"{Fore.RED+Style.BRIGHT}\r[Ref Balance]: False", flush=True)
                else:
                    print(f"{Fore.RED+Style.BRIGHT}\r[Ref Balance]: Failed to check ref balance", flush=True)
            else:
                print(f"\r{Fore.YELLOW+Style.BRIGHT}[Ref Balance]: Skipped!", flush=True)

            available_colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

            while balance_info['playPasses'] > 0:
                print(f"{Fore.CYAN+Style.BRIGHT}[Play Game]: Playing game...")
                game_response = play_game(token)
                print(f"\r{Fore.CYAN+Style.BRIGHT}[Play Game]: Checking game...", end="", flush=True)
                time.sleep(1)
                claim_response = claim_game(token, game_response['gameId'], random.randint(1500, 2000))
                if claim_response is None:
                    print(f"\r{Fore.RED+Style.BRIGHT}[Play Game]: Failed to claim game, retrying...", flush=True)
                while True:
                    if claim_response.text == '{"message":"game session not finished"}':
                        time.sleep(1)
                        random_color = random.choice(available_colors)
                        print(f"\r{random_color+Style.BRIGHT}[Play Game]: Game session not finished.. retrying", flush=True)
                        claim_response = claim_game(token, game_response['gameId'], random.randint(1500, 2000))
                        if claim_response is None:
                            print(f"\r{Fore.RED+Style.BRIGHT}[Play Game]: Failed to claim game, retrying...", flush=True)
                    elif claim_response.text == '{"message":"game session not found"}':
                        print(f"\r{Fore.RED+Style.BRIGHT}[Play Game]: Game session not found", flush=True)
                        break
                    elif 'message' in claim_response and claim_response['message'] == 'Token is invalid':
                        print(f"{Fore.RED+Style.BRIGHT}[Play Game]: Token is invalid, getting new token...")
                        token = get_new_token(query_id)
                        continue
                    else:
                        print(f"\r{Fore.YELLOW+Style.BRIGHT}[Play Game]: Game claimed: {claim_response.text}", flush=True)
                        break

                balance_info = get_balance(token)
                if balance_info is None:
                    print(f"\r{Fore.RED+Style.BRIGHT}[Play Game]: Failed to get ticket information", flush=True)
                else:
                    available_balance_after = balance_info['availableBalance']
                    before = float(available_balance_before)
                    after = float(available_balance_after)
                    total_balance = after - before
                    print(f"\r{Fore.YELLOW+Style.BRIGHT}[Play Game]: You Got Total {total_balance} From Playing Game", flush=True)
                    before = balance_info['playPasses']
                    print(f"\r{Fore.YELLOW+Style.BRIGHT}[Play Game]: You Have {before} play passes left", flush=True)

            end_color = random.choice(available_colors)
            print(f"{end_color+Style.BRIGHT}\nComplete", flush=True)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\r\nProgram has been terminated by user")
        break
    except Exception as e:
        print(f"\r\nUnknown Error: {e}")
        continue
