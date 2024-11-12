import requests
import time
from colorama import Fore, Style, init
import json

init(autoreset=True)

def print_welcome_message():
    print(Fore.GREEN + Style.BRIGHT + "Yescoin BOT!")

def load_tokens(file_path):
    with open(file_path, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

available_colors = [Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

def get_headers(token):
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.yescoin.gold',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.yescoin.gold/',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'token': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }

def collect_coin(token, amount):
    url = 'https://api.yescoin.gold/game/collectCoin'
    headers = get_headers(token)
    data = json.dumps(amount)
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            return result
        else:
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as e:
        print(f"Error collecting coin: {e}")
        return None

def fetch_account_info(token):
    try:
        url = 'https://api.yescoin.gold/account/getAccountInfo'
        headers = get_headers(token)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            return data
        else:
            return None
    except Exception as e:
        print(f"Error fetching account info: {e}")

def fetch_game_info(token):
    try:
        url = 'https://api.yescoin.gold/game/getGameInfo'
        headers = get_headers(token)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            return data
        else:
            return None
    except Exception as e:
        print(f"Error fetching game info: {e}")

def use_special_box(token):
    url = 'https://api.yescoin.gold/game/recoverSpecialBox'
    headers = get_headers(token)
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            print(f"{Fore.GREEN + Style.BRIGHT}\r[ Box ] : Activating...", flush=True)
            return True
        else:
            print(f"{Fore.RED + Style.BRIGHT}\r[ Box ] : Could not activate", flush=True)
            return False
    except Exception as e:
        print(f"{Fore.RED}\r[ Box ] : Error", flush=True)
        return False

def fetch_special_box_info(token):
    try:
        url = 'https://api.yescoin.gold/game/getSpecialBoxInfo'
        headers = get_headers(token)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            return data
        else:
            return None
    except Exception as e:
        print(f"Error fetching special box info: {e}")

def get_my_user_nick(token):
    try:
        url = 'https://api.yescoin.gold/account/getRankingList?index=1&pageSize=1&rankType=1&userLevel=1'
        headers = get_headers(token)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if 'myUserNick' in data['data'] and data['data']['myUserNick']:
            return data['data']['myUserNick']
        else:
            return "no nickname"
    except Exception as e:
        print(f"Error fetching user nickname: {e}")

def collect_from_special_box(token, box_type, coin_count):
    url = 'https://api.yescoin.gold/game/collectSpecialBoxCoin'
    headers = get_headers(token)
    data = json.dumps({"boxType": box_type, "coinCount": coin_count})
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            if result['data']['collectStatus']:
                print(f"{random.choice(available_colors) + Style.BRIGHT}\r[ Box ] : Collected {result['data']['collectAmount']} coins", flush=True)
                return True, result['data']['collectAmount']
            else:
                print(f"{Fore.RED + Style.BRIGHT}\r[ Box ] : No box", flush=True)
                return True, 0
        else:
            print(f"{Fore.RED + Style.BRIGHT}\r[ Box ] : Failed to collect coins: {result['message']}", flush=True)
            return False, 0
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}\r[ Box ] : Error: {e}", flush=True)
        return False, 0

def attempt_collect_special_box(token, box_type, initial_coin_count):
    coin_count = initial_coin_count
    while coin_count > 0:
        success, collected_amount = collect_from_special_box(token, box_type, coin_count)
        if success:
            return collected_amount
        coin_count -= 20
    print(f"{Fore.RED + Style.BRIGHT}\r[ Box ] : Could not collect after adjustments", flush=True)
    return 0

def fetch_account_build_info(token):
    try:
        url = 'https://api.yescoin.gold/build/getAccountBuildInfo'
        headers = get_headers(token)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            return data
        else:
            return None
    except Exception as e:
        print(f"Error fetching account build info: {e}")

def fetch_squad_info(token):
    url = 'https://api.yescoin.gold/squad/mySquad'
    headers = get_headers(token)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            return data
        else:
            return None
    except Exception as e:
        print(f"Error fetching squad info: {e}")
        return None

def join_squad(token, squad_link):
    url = 'https://api.yescoin.gold/squad/joinSquad'
    headers = get_headers(token)
    data = json.dumps({"squadTgLink": squad_link})
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            return result
        else:
            return None
    except Exception as e:
        print(f"Error joining squad: {e}")
        return None

def recover_coin_pool(token):
    url = 'https://api.yescoin.gold/game/recoverCoinPool'
    headers = get_headers(token)
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Recovery ] : Successful", flush=True)
            return True
        else:
            print(f"{Fore.RED + Style.BRIGHT}\r[ Recovery ] : Failed", flush=True)
            return False
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}\r[ Recovery ] : Error: {e}", flush=True)
        return False

def fetch_task_list(token):
    url = 'https://api.yescoin.gold/task/getCommonTaskList'
    headers = get_headers(token)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tasks = response.json()
        if tasks['code'] == 0:
            return tasks['data']
        else:
            print(f"{Fore.RED + Style.BRIGHT}\r[ Task ] : Could not fetch task list: {tasks['message']}", flush=True)
            return None
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}Error: {e}")
        return None

def finish_task(token, task_id):
    url = 'https://api.yescoin.gold/task/finishTask'
    headers = get_headers(token)
    data = json.dumps(task_id)
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            print(f"{Fore.GREEN + Style.BRIGHT}\r[ Task ] : Task {task_id} completed. Bonus: {result['data']['bonusAmount']}", flush=True)
            return True
        else:
            print(f"{Fore.RED + Style.BRIGHT}\r[ Task ] : Task {task_id} could not be completed: {result['message']}", flush=True)
            return False
    except Exception as e:
        print(f"{Fore.RED + Style.BRIGHT}\r[ Task ] : Error: {e}", flush=True)
        return False

def process_tasks(token):
    tasks = fetch_task_list(token)
    if tasks:
        for task in tasks:
            if task['taskStatus'] == 0:
                finish_task(token, task['taskId'])
            else:
                print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Task ] : Task already completed", flush=True)

import random

def upgrade_level(token, current_level, target_level, upgrade_type):
    url = 'https://api.yescoin.gold/build/levelUp'
    headers = get_headers(token)
    data = json.dumps(upgrade_type)
    if upgrade_type == '1':
        upgrade_type_name = 'Multiple Earnings'
    else:
        upgrade_type_name = 'Refill Rate'
    while current_level < target_level:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            current_level += 1
            print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Upgrade ] : {upgrade_type_name} upgraded to level {current_level}", flush=True)
        else:
            print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Upgrade ] : Upgrade failed: {result['message']}", flush=True)
            break

    if current_level == target_level:
        print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Upgrade ] : {upgrade_type_name} already at level {current_level}", flush=True)

def main():
    tokens = load_tokens('yescoin.txt')
    while True:
        print_welcome_message()
        for index, token in enumerate(tokens):
            nickname = get_my_user_nick(token)
            print(f"{Fore.BLUE + Style.BRIGHT}\n[{Fore.WHITE + Style.BRIGHT} Account {index + 1} | {nickname} {Fore.BLUE + Style.BRIGHT}]")
            print(f"{random.choice(available_colors)+Style.BRIGHT}[ Squad ] : Fetching...", flush=True)
            squad_info = fetch_squad_info(token)
            if squad_info and squad_info['data']['isJoinSquad']:
                squad_title = squad_info['data']['squadInfo']['squadTitle']
                squad_members = squad_info['data']['squadInfo']['squadMembers']
                print(f"{random.choice(available_colors)+Style.BRIGHT}[ Squad ] : {squad_title} | {squad_members} Members")
            else:
                print(f"{Fore.YELLOW + Style.BRIGHT}[ Squad ] : Not joined. Joining Fridibuck.", flush=True)
                time.sleep(3)
                join_result = join_squad(token, "t.me/fridibuck")
                if join_result:
                    print(f"{random.choice(available_colors) + Style.BRIGHT}[ Squad ] : Welcome Pemulung {nickname} - Fridibuck!", flush=True)
                else:
                    print(f"{random.choice(available_colors) + Style.BRIGHT}[ Squad ] : Could not join Fridibuck.", flush=True)

            print(f"{random.choice(available_colors)+Style.BRIGHT}[ Balance ] : Fetching...", flush=True)
            balance = fetch_account_info(token)
            if balance is None:
                print(f"{Fore.RED}[ Balance ] : Could not fetch balance", flush=True)
                continue
            else:
                balance = balance.get('data', {}).get('currentAmount', 0)
                balance = f"{balance:,}".replace(',', '.')
                print(f"{random.choice(available_colors) + Style.BRIGHT}[ Balance ] : {balance}", flush=True)

            print(f"{random.choice(available_colors)+Style.BRIGHT}[ Game Info ] : Fetching...", flush=True)
            game_info = fetch_account_build_info(token)
            if game_info is None:
                print(f"{Fore.RED}[ Game Info ] : Could not fetch data", flush=True)
                continue
            else:
                special_box_left_recovery_count = game_info['data'].get('specialBoxLeftRecoveryCount', 0)
                coin_pool_left_recovery_count = game_info['data'].get('coinPoolLeftRecoveryCount', 0)
                single_coin_value = game_info['data'].get('singleCoinValue', 0)
                single_coin_level = game_info['data'].get('singleCoinLevel', 0)
                coin_pool_recovery_speed = game_info['data'].get('coinPoolRecoverySpeed', 0)
                print(f"{random.choice(available_colors)+Style.BRIGHT}[ Power-up ] : Box {special_box_left_recovery_count} | Recovery {coin_pool_left_recovery_count}", flush=True)
                print(f"{random.choice(available_colors)+Style.BRIGHT}[ Multiple Earnings ] : Level {single_coin_value}", flush=True)
                print(f"{random.choice(available_colors)+Style.BRIGHT}[ Coin Limit ] : Level {single_coin_level}", flush=True)
                print(f"{random.choice(available_colors)+Style.BRIGHT}[ Refill Rate ] : Level {coin_pool_recovery_speed}", flush=True)

            if cek_task_enable == 'y':
                print(f"{random.choice(available_colors)+Style.BRIGHT}[ Task ] : Completing task...", flush=True)
                process_tasks(token)

            time.sleep(2)

            if upgrade_multi_enable == 'y':
                print(f"{random.choice(available_colors)+Style.BRIGHT}[ Upgrade ] : Upgrading Multiple Earnings...", flush=True)
                upgrade_level(token, single_coin_value, max_level, '1')

            time.sleep(2)

            if upgrade_fill_enable == 'y':
                print(f"{random.choice(available_colors)+Style.BRIGHT}[ Upgrade ] : Upgrading Refill Rate...", flush=True)
                upgrade_level(token, coin_pool_recovery_speed, max_level, '2')

            print(f"{random.choice(available_colors)+Style.BRIGHT}[ Game Info ] : Fetching...", flush=True)
            collect_info = fetch_game_info(token)
            if collect_info is None:
                print(f"{Fore.RED}[ Game Info ] : Could not fetch data", flush=True)
                continue
            else:
                single_coin_value = collect_info['data'].get('singleCoinValue', 0)
                coin_pool_left_count = collect_info['data'].get('coinPoolLeftCount', 0)
                print(f"{random.choice(available_colors) + Style.BRIGHT}[ Remaining Coins ] : {coin_pool_left_count}", flush=True)

                print(f"{random.choice(available_colors)+Style.BRIGHT}[ Collecting ] : Collecting coins...", flush=True)
                if coin_pool_left_count > 0:
                    amount = coin_pool_left_count // single_coin_value
                    collect_result = collect_coin(token, amount)
                    if collect_result and collect_result.get('code') == 0:
                        collected_amount = collect_result['data']['collectAmount']
                        print(f"{random.choice(available_colors) + Style.BRIGHT}[ Collecting ] : Collected {collected_amount} coins", flush=True)
                    else:
                        print(f"{random.choice(available_colors)+Style.BRIGHT}[ Collecting ] : Could not collect coins", flush=True)

            print(f"{random.choice(available_colors)+Style.BRIGHT}[ Box ] : Activating...", flush=True)
            if game_info and game_info['data'].get('specialBoxLeftRecoveryCount', 0) > 0:
                if use_special_box(token):
                    print(f"{random.choice(available_colors)+Style.BRIGHT}[ Box ] : Collecting...", flush=True)
                    collected_amount = attempt_collect_special_box(token, 2, 240)
            else:
                print(f"{random.choice(available_colors)+Style.BRIGHT}[ Box ] : No box", flush=True)

            time.sleep(2)

            print(f"{random.choice(available_colors)+Style.BRIGHT}[ Recovery ] : Recovering...", flush=True)
            game_info = fetch_account_build_info(token)
            if game_info and game_info['data'].get('coinPoolLeftRecoveryCount', 0) > 0:
                if recover_coin_pool(token):
                    collect_info = fetch_game_info(token)
                    if collect_info:
                        coin_pool_left_count = collect_info['data'].get('coinPoolLeftCount', 0)
                        if coin_pool_left_count > 0:
                            amount = coin_pool_left_count // game_info['data'].get('singleCoinValue', 1)
                            collect_result = collect_coin(token, amount)
                            if collect_result and collect_result.get('code') == 0:
                                collected_amount = collect_result['data']['collectAmount']
                                print(f"{Fore.GREEN + Style.BRIGHT}[ Collecting ] : Collected {collected_amount} coins", flush=True)
                            else:
                                print(f"{Fore.RED + Style.BRIGHT}[ Collecting ] : Could not collect coins", flush=True)
            else:
                print(f"{random.choice(available_colors)+Style.BRIGHT}[ Recovery ] : No recovery", flush=True)

            time.sleep(2)

            print(f"{random.choice(available_colors)+Style.BRIGHT}[ Free Box ] : Collecting...", flush=True)
            collected_amount = attempt_collect_special_box(token, 1, 200)

            time.sleep(2)

        print(f"\n{random.choice(available_colors)+Style.BRIGHT}========={Fore.WHITE+Style.BRIGHT}All accounts processed{Fore.GREEN+Style.BRIGHT}=========", flush=True)
        import sys
        wait_time = 15
        for seconds in range(wait_time, 0, -1):
            sys.stdout.write(f"\r{Fore.CYAN}Waiting for next request: {Fore.CYAN}{Fore.WHITE}{seconds // 60} minutes {Fore.WHITE}{seconds % 60} seconds")
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write("\rTime for next request!\n")

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Blum BOT')
    parser.add_argument('--task', type=str, choices=['y', 'n'], default= 'y', help='Check and request task (y/n)')
    parser.add_argument('--multi', type=str, choices=['y', 'n'],default= 'n', help='Upgrade Multiple Earnings (y/n)')
    parser.add_argument('--fill', type=str, choices=['y', 'n'], default= 'n',help='Upgrade Refill Rate (y/n)')
    parser.add_argument('--max-level', type=int, help='Maximum level for upgrade (default: 5)')

    args = parser.parse_args()

    if args.task is None:
        task_input = input("Do you want to check and request task? (y/n, default n): ").strip().lower()
        args.task = task_input if task_input in ['y', 'n'] else 'n'

    if args.multi is None:
        multi_input = input("Do you want to upgrade Multiple Earnings? (y/n, default n): ").strip().lower()
        args.multi = multi_input if multi_input in ['y', 'n'] else 'n'

    if args.fill is None:
        fill_input = input("Do you want to upgrade Refill Rate? (y/n, default n): ").strip().lower()
        args.fill = fill_input if fill_input in ['y', 'n'] else 'n'

    if (args.multi == 'y' or args.fill == 'y') and args.max_level is None:
        max_level_input = input("Enter maximum level for upgrade (default: 5): ").strip()
        args.max_level = int(max_level_input) if max_level_input else 5
    elif args.max_level is None:
        args.max_level = 5

    return args

args = parse_arguments()
cek_task_enable = args.task
upgrade_multi_enable = args.multi
upgrade_fill_enable = args.fill
max_level = args.max_level

if __name__ == '__main__':
    main()
