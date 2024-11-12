import requests
import time
from colorama import Fore, Style, init
import json
from datetime import datetime, timedelta, timezone
import argparse
import urllib.parse
import random

# Function to parse user data from data.txt file
def parse_user_data(file_path):
    user_data_list = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if "user=" in line:
                user_data_encoded = line.split('user=')[1].split('&')[0]
                user_data_json = urllib.parse.unquote(user_data_encoded)
                user_data = json.loads(user_data_json)
                user_data_list.append((line.strip(), user_data))
    return user_data_list

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://tgapp.matchain.io',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://tgapp.matchain.io/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
}

def get_token(line, user_data):
    payload = {
        "uid": user_data["id"],
        "first_name": user_data["first_name"],
        "last_name": user_data["last_name"],
        "username": user_data.get("username", ""),
        "tg_login_params": line
    }
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/user/login'
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Your query is incorrect")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def get_profile(user_data, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/user/profile'
    headers['Authorization'] = token
    payload = {"uid": user_data["id"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Invalid token")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def get_farming_reward(user_data, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/reward'
    headers['Authorization'] = token
    payload = {"uid": user_data["id"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Invalid token")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None
    
def get_ref_reward(user_data, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/invite/balance'
    headers['Authorization'] = token
    payload = {"uid": user_data["id"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Invalid token")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def claim_ref_reward(user_data, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/invite/claim'
    headers['Authorization'] = token
    payload = {"uid": user_data["id"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Invalid token")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def claim_farming_reward(user_data, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/claim'
    headers['Authorization'] = token
    payload = {"uid": user_data["id"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Invalid token")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def start_farming(user_data, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/farming'
    headers['Authorization'] = token
    payload = {"uid": user_data["id"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Invalid token")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def get_task(user_data, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/task/list'
    headers['Authorization'] = token
    payload = {"uid": user_data["id"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Invalid token")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def complete_task(user_data,task_name, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/task/complete'
    headers['Authorization'] = token
    payload = {
            "uid": user_data["id"],
            "type": task_name
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Invalid token")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def claim_task(user_data,task_name, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/task/claim'
    headers['Authorization'] = token
    payload = {
            "uid": user_data["id"],
            "type": task_name
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Invalid token")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def check_ticket(token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/game/rule'
    headers['Authorization'] = token

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Invalid token")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def play_game(token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/game/play'
    headers['Authorization'] = token
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Invalid token")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def claim_game(game_id,point, token):
    url = 'https://tgapp-api.matchain.io/api/tgapp/v1/game/claim'
    headers['Authorization'] = token
    payload = {
        "game_id": game_id,
        "point": point
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Invalid token")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def calculate_default_score(rule):
    big_fire_count = 0
    small_fire_count = 0
    magnifier_count = 0
    bomb_count = 0
    total_score = 0

    for level in rule:
        for key, objects in level.items():
            for obj in objects:
                if obj['objectType'] == 'bigFire':
                    big_fire_count += 1
                    total_score += obj['score']
                elif obj['objectType'] == 'smallFire':
                    small_fire_count += 1
                    total_score += obj['score']
                elif obj['objectType'] == 'magnifier':
                    magnifier_count += 1
                elif obj['objectType'] == 'bomb':
                    bomb_count += 1

    return big_fire_count, small_fire_count, magnifier_count, bomb_count, total_score

def animated_loading(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(f"\rWaiting for the next claim time {frame} - Remaining {remaining_time} seconds         ", end="", flush=True)
            time.sleep(0.25)
    print("\rNext claim time completed.                            ", flush=True)

start_time = datetime.now()

user_data_list = parse_user_data('match.txt')

def format_balance(balance):
    if balance < 1000:
        return str(balance)
    return f"{balance // 1000}"

def convert_ts(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds

def main():
    auto_clear_task = 'y'
    auto_play_game = 'y'
  
    if auto_play_game == "Y":
        print(Fore.YELLOW + Style.BRIGHT + f"Select Score: ")
        print(Fore.YELLOW + Style.BRIGHT + f"1. Default Score")
        print(Fore.YELLOW + Style.BRIGHT + f"2. Maximum Score")
        print(Fore.YELLOW + Style.BRIGHT + f"3. Random Score")
        while True:
            try:
                select_score = '2'
                if 1 <= select_score <= 3:
                    break
                else:
                    print(Fore.RED + Style.BRIGHT + "Input should be between 1 and 3.")
            except ValueError:
                print(Fore.RED + Style.BRIGHT + "Input should be a number.")

    while True:
        print_welcome_message()
        try:
            for line, user_data in user_data_list:
                print(Fore.CYAN + Style.BRIGHT + f"Getting token", end="\r", flush=True)
                time.sleep(1)
                get_token_response = get_token(line, user_data)

                if get_token_response is not None:
                    print(Fore.GREEN + Style.BRIGHT + f"Token obtained!", end="\r", flush=True)
                    token = get_token_response['data'].get('token')
                    nickname = get_token_response['data']['user'].get('nickname', 'Unknown')
                    print(Fore.CYAN + Style.BRIGHT + f"============= [ Account {nickname} ] =============", flush=True)
                    profile = get_profile(user_data, token)
                    if profile is None or 'data' not in profile:
                        print(Fore.RED + Style.BRIGHT + f"[ Profile ]: Data for {nickname} could not be retrieved!")
                        time.sleep(5)
                        continue
                    else:
                        balance = profile['data'].get('Balance', 0)
                        invite_count = profile['data'].get('invite_count', 0)
                        balance_view = format_balance(balance)
                        print(Fore.CYAN + Style.BRIGHT + f"[ Balance ]: {balance_view}")
                        print(Fore.CYAN + Style.BRIGHT + f"[ Total Invites ]: {invite_count}")

                    farming_balance = get_farming_reward(user_data, token)
                    if farming_balance is None or 'data' not in farming_balance:
                        print(Fore.RED + Style.BRIGHT + f"[ Farming ]: Data for {nickname} could not be retrieved!")
                    else:
                        claim_balance = int(format_balance(farming_balance['data']['reward']))  # Convert to integer
                        claim_in = farming_balance.get('data', {}).get('next_claim_timestamp')
                        ts = datetime.now().timestamp() * 1000
                        time_remaining = max(0, claim_in - ts)

                        second = int(time_remaining / 1000)
                        hours, minutes, seconds = convert_ts(second)
                        print(Fore.GREEN + Style.BRIGHT + f"[ Farming ]: Reward {claim_balance} Points")
                        print(Fore.GREEN + Style.BRIGHT + f"[ Farming ]: Claim time {hours} Hours {minutes} Minutes")

                        if claim_balance > 0 or time_remaining == 0:
                            print(Fore.GREEN + Style.BRIGHT + f"[ Farming ]: Claiming {claim_balance} Points", end="\r", flush=True)
                            claim_farming = claim_farming_reward(user_data, token)
                            if claim_farming:
                                print(Fore.GREEN + Style.BRIGHT + f"[ Farming ]: Claimed {claim_balance} Points              ", flush=True)
                                print(Fore.GREEN + Style.BRIGHT + f"[ Farming ]: Starting farming..", end="\r", flush=True)
                                start_farming_response = start_farming(user_data, token)
                                if start_farming_response:
                                    print(Fore.GREEN + Style.BRIGHT + f"[ Farming ]: Farming started!           ", flush=True)
                                else:
                                    print(Fore.RED + Style.BRIGHT + f"[ Farming ]: Farming could not start!           ", flush=True)
                            else:
                                print(Fore.RED + Style.BRIGHT + f"[ Farming ]: Claim failed")
                        elif claim_balance == 0 or time_remaining == 0:
                            print(Fore.GREEN + Style.BRIGHT + f"[ Farming ]: Starting farming..", end="\r", flush=True)
                            start_farming_response = start_farming(user_data, token)
                            if start_farming_response:
                                print(Fore.GREEN + Style.BRIGHT + f"[ Farming ]: Farming started!           ", flush=True)
                            else:
                                print(Fore.RED + Style.BRIGHT + f"[ Farming ]: Farming could not start!           ", flush=True)
                        else:
                            print(Fore.YELLOW + Style.BRIGHT + f"[ Farming ]: Still farming         ")

                        print(Fore.YELLOW + Style.BRIGHT + f"[ Ref Balance ]: Checking..", end="\r", flush=True)
                        time.sleep(2)
                        check_ref_balance = get_ref_reward(user_data,token)
                        if check_ref_balance is None or 'data' not in farming_balance:
                            print(Fore.RED + Style.BRIGHT + f"[ Ref Balance ]: Data for {nickname} could not be retrieved!", flush=True)
                        else:
                            balance = check_ref_balance['data'].get('balance', 0)
                            balance_view = format_balance(balance)
                            print(Fore.GREEN + Style.BRIGHT + f"[ Ref Balance ]: Reward {balance_view} Points          ", flush=True)
                            if int(balance_view) > 0:
                                claim_ref = claim_ref_reward(user_data,token)
                                if claim_ref:
                                    balance_claim = claim_ref.get('data')
                                    balance_claim_view = format_balance(balance_claim)
                                    print(Fore.GREEN + Style.BRIGHT + f"[ Ref Balance ]: Claimed {balance_claim_view} Points            ", flush=True)
                                else:
                                    print(Fore.RED + Style.BRIGHT + f"[ Ref Balance ]: Ref balance claim failed!          ", flush=True)

                        if auto_clear_task == "Y":
                            print(Fore.GREEN + Style.BRIGHT + f"[ Task ]: Checking..", end="\r", flush=True)
                            get_task_list = get_task(user_data, token)
                            if get_task_list:
                                task_list = get_task_list.get('data', [])
                                for task in task_list:
                                    if not task['complete']:
                                        print(Fore.GREEN  + f"[ Task ]: Completing task {task['name']}", end="\r" , flush=True)
                                        time.sleep(1)
                                        complete_task_result = complete_task(user_data,task['name'],token)   
                                        if complete_task_result:
                                            result = complete_task_result.get('data', False)
                                            if result:
                                                print(Fore.GREEN + Style.BRIGHT + f"[ Task ]: Claiming task {task['name']}               ", flush=True)
                                                time.sleep(1)
                                                claim_task_result = claim_task(user_data,task['name'],token)
                                                if claim_task_result:
                                                    print(f"{Fore.GREEN+Style.BRIGHT}[ Task ]: Task completed and claimed {task['name']}               " , flush=True)
                                                else:
                                                    print(f"{Fore.RED+Style.BRIGHT}[ Task ]: Task claim failed {task['name']}                  ", flush=True)
                                            else:
                                                 print(f"{Fore.RED+Style.BRIGHT}[ Task ]: Task claim failed {task['name']}                  ", flush=True)
                                        else:
                                            print(f"{Fore.RED+Style.BRIGHT}[ Task ]: Task not completed {task['name']}            ", flush=True)
                            else:
                                print(f"{Fore.RED+Style.BRIGHT}[ Task ]: Task list could not be retrieved          ", flush=True)
                        print(Fore.GREEN + Style.BRIGHT + f"[ Game ]: Checking ticket..", end="\r", flush=True)
                        time.sleep(2)
                        ticket_response = check_ticket(token)
                        
                        if ticket_response:
                            total_ticket = ticket_response.get('data', {}).get('game_count')
                            print(Fore.CYAN + Style.BRIGHT + f"[ Game ]: {total_ticket} Ticket            " , flush=True)

                            if auto_play_game == "Y":
                                while total_ticket > 0:
                                    print(Fore.YELLOW + Style.BRIGHT + f"[ Game ]: Playing game..", end="\r", flush=True)
                                    time.sleep(2)
                                    get_game_id = play_game(token)

                                    if get_game_id:
                                        game_id = get_game_id.get('data', {}).get('game_id')
                                        if game_id:
                                            if select_score == 1: # default score
                                                print(Fore.YELLOW + Style.BRIGHT + f"[ Game ]: Default Score Selected       ", flush=True)
                                                rule = ticket_response.get('data', {}).get('rule', [])
                                                big_fire_count, small_fire_count, magnifier_count, bomb_count, total_score = calculate_default_score(rule)
                                                print(f"[ Game ]: You won {big_fire_count} Big Fires, {small_fire_count} Small Fires, {magnifier_count} Magnifiers")
                                                print(f"[ Game ]: {bomb_count} bombs prevented")
                                                max_score = total_score
                                            elif select_score == 2: # maximum score
                                                print(Fore.YELLOW + Style.BRIGHT + f"[ Game ]: Maximum Score Selected       ", flush=True)
                                                max_score = 100
                                            else: # random score
                                                print(Fore.YELLOW + Style.BRIGHT + f"[ Game ]: Random Score Selected       ", flush=True)
                                                max_score = random.randint(50, 100)
                                            game_result = claim_game(game_id, max_score, token)
                                            
                                            if game_result.get('code') == 200:
                                                 print(Fore.GREEN + Style.BRIGHT + f"[ Game ]: Game played successfully | Score: {max_score} Points     ", flush=True)
                                                 time.sleep(2)
                                            else:
                                                 print(Fore.RED + Style.BRIGHT + f"[ Game ]: Game could not be played    ", flush=True)
                                                 time.sleep(2)

                                            check_remaining_tickets = check_ticket(token)
                                            total_ticket = check_remaining_tickets.get('data', {}).get('game_count')  # Update total_ticket
                                            if total_ticket > 0:
                                                 print(Fore.CYAN + Style.BRIGHT + f"[ Game ]: Still {total_ticket} Tickets left      " , flush=True)
                                                 print(Fore.CYAN + Style.BRIGHT + f"[ Game ]: Playing game again" , end="\r", flush=True)
                                                 time.sleep(2)
                                                 continue
                                            else:
                                                 print(Fore.CYAN + Style.BRIGHT + f"[ Game ]: No more tickets left        " , flush=True)
                                                 break
                                    else:
                                        print(Fore.RED + Style.BRIGHT + f"[ Game ]: Game could not be played            ", flush=True)

                        else:
                            print(f"{Fore.RED+Style.BRIGHT}[ Game ]: Ticket could not be retrieved            ", flush=True)
                else:
                    print(Fore.RED + Style.BRIGHT + f"Could not log into account {get_token_response}")
                    time.sleep(2)
                    continue

            print(Fore.BLUE + Style.BRIGHT + f"\n==========ALL ACCOUNTS PROCESSED==========\n", flush=True)
            animated_loading(300)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            time.sleep(5)
        except KeyboardInterrupt:
            print(f"\n{Fore.RED+Style.BRIGHT}Process forcibly stopped by you!")
            break

def print_welcome_message():
    print(Fore.GREEN + Style.BRIGHT + "MatchQuest BOT")
    current_time = datetime.now()
    up_time = current_time - start_time
    days, remainder = divmod(up_time.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    # print(Fore.CYAN + Style.BRIGHT + f"Bot uptime: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds\n\n")

if __name__ == "__main__":
    main()
