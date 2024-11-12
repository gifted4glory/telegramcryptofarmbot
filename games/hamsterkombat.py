import requests
import json
import time
from datetime import datetime
from itertools import cycle
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Add a global variable to store the combo choice
auto_claim_daily_combo = None
combo_list = []

def load_tokens(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def get_headers(token):
    return {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Origin': 'https://hamsterkombat.io',
        'Referer': 'https://hamsterkombat.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
    }

def get_token(init_data_raw):
    url = 'https://api.hamsterkombat.io/auth/auth-by-telegram-webapp'
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'authorization': 'authToken is empty, store token null',
        'Origin': 'https://hamsterkombat.io',
        'Referer': 'https://hamsterkombat.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
        'accept': 'application/json',
        'content-type': 'application/json'
    }
    data = json.dumps({"initDataRaw": init_data_raw})
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()['authToken']
        elif response.status_code == 403:
            print(Fore.RED + Style.BRIGHT + "\rAccess denied. Status 403", flush=True)
        elif response.status_code == 500:
            print(Fore.RED + Style.BRIGHT + "\rInternal Server Error", flush=True)
        else:
            error_data = response.json()
            if "invalid" in error_data.get("error_code", "").lower():
                print(Fore.RED + Style.BRIGHT + "\rFailed to obtain token. Invalid initial data", flush=True)
            else:
                print(Fore.RED + Style.BRIGHT + f"\rFailed to obtain token. {error_data}", flush=True)
    except requests.exceptions.Timeout:
        print(Fore.RED + Style.BRIGHT + "\rFailed to obtain token. Request timed out", flush=True)
    except requests.exceptions.ConnectionError:
        print(Fore.RED + Style.BRIGHT + "\rFailed to obtain token. Connection error", flush=True)
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"\rFailed to obtain token. Error: {str(e)}", flush=True)
    return None

def authenticate(token):
    url = 'https://api.hamsterkombat.io/auth/me-telegram'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def sync_clicker(token):
    url = 'https://api.hamsterkombat.io/clicker/sync'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def claim_daily(token):
    url = 'https://api.hamsterkombat.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": "streak_days"})
    response = requests.post(url, headers=headers, data=data)
    return response

def upgrade(token, upgrade_type):
    url = 'https://api.hamsterkombat.io/clicker/buy-boost'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": upgrade_type, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response

def tap(token, max_taps, available_taps):
    url = 'https://api.hamsterkombat.io/clicker/tap'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"count": max_taps, "availableTaps": available_taps, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response

def list_tasks(token):
    url = 'https://api.hamsterkombat.io/clicker/list-tasks'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def exchange(token):
    url = 'https://api.hamsterkombat.io/clicker/select-exchange'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"exchangeId": 'okx'})
    response = requests.post(url, headers=headers, data=data)
    return response

def claim_cipher(token, cipher_text):
    url = 'https://api.hamsterkombat.io/clicker/claim-daily-cipher'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"cipher": cipher_text})
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        try:
            return response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "Failed to parse JSON from response.", flush=True)
            return None
    elif response.status_code == 400:
        try:
            return response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "Failed to parse JSON from response.", flush=True)
            return None
    elif response.status_code == 500:
        print(Fore.RED + Style.BRIGHT + f"Failed to claim cipher, Internal Server Error", flush=True)
        return response
    else:
        print(Fore.RED + Style.BRIGHT + f"Failed to claim cipher, status code: {response.status_code}", flush=True)
        return None

def check_task(token, task_id):
    url = 'https://api.hamsterkombat.io/clicker/check-task'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"taskId": task_id})
    response = requests.post(url, headers=headers, data=data)
    return response

def cek_booster(token):
    url = 'https://api.hamsterkombat.io/clicker/boosts-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    return response

def use_booster(token):
    url = 'https://api.hamsterkombat.io/clicker/buy-boost'
    headers = get_headers(token)
    headers['accept'] = 'application/json'
    headers['content-type'] = 'application/json'
    data = json.dumps({"boostId": "BoostFullAvailableTaps", "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    return response

def read_upgrade_list(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def get_available_upgrades(token):
    url = 'https://api.hamsterkombat.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        try:
            upgrades = response.json()['upgradesForBuy']
            return upgrades
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Upgrade Mining ] : Failed to parse JSON from response.", flush=True)
            return []
    else:
        print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Mining ] : Failed to obtain upgrade list: Status {response.status_code}", flush=True)
        return []

def buy_upgrade(token, upgrade_id, upgrade_name):
    url = 'https://api.hamsterkombat.io/clicker/buy-upgrade'
    headers = get_headers(token)
    data = json.dumps({"upgradeId": upgrade_id, "timestamp": int(time.time())})
    time.sleep(3)
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        try:
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade Mining ] : Upgrade {upgrade_name} successfully purchased.", flush=True)
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Upgrade Mining ] : Failed to parse JSON during upgrade.", flush=True)
    else:
        try:
            error_response = response.json()
            if error_response.get('error_code') == 'INSUFFICIENT_FUNDS':
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Mining ] : Not enough money hahaha :D", flush=True)
                return 'insufficient_funds'
            elif error_response.get('error_code') == 'UPGRADE_COOLDOWN':
                cooldown_seconds = error_response.get('cooldownSeconds', 0)
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Mining ] : Upgrade {upgrade_name} is still cooling down. Remaining {cooldown_seconds} seconds.", flush=True)
                return {'cooldown': True, 'cooldown_seconds': cooldown_seconds}
            else:
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Mining ] : Upgrade failed {upgrade_name}: {error_response}", flush=True)
                return {'error': True, 'message': error_response}
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade Mining ] : Failed to parse JSON from response. Status: {response.status_code}", flush=True)
            return {'error': True, 'status_code': response.status_code}

def get_available_upgrades_combo(token):
    url = 'https://api.hamsterkombat.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        try:
            upgrades = response.json()['upgradesForBuy']
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Combo ] : Upgrade list successfully obtained.", flush=True)
            return upgrades
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Daily Combo ] : Failed to parse JSON from response.", flush=True)
            return []
    else:
        print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Failed to obtain upgrade list: Status {response.status_code}", flush=True)
        return []

def buy_upgrade_combo(token, upgrade_id):
    url = 'https://api.hamsterkombat.io/clicker/buy-upgrade'
    headers = get_headers(token)
    data = json.dumps({"upgradeId": upgrade_id, "timestamp": int(time.time())})
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        try:
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Combo ] : Combo {upgrade_id} successfully purchased.", flush=True)
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + "\r[ Daily Combo ] : Failed to parse JSON during upgrade.", flush=True)
        return response
    else:
        try:
            error_response = response.json()
            if error_response.get('error_code') == 'INSUFFICIENT_FUNDS':
                print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Not enough money.", flush=True)
                return 'insufficient_funds'
            else:
                return error_response
        except json.JSONDecodeError:
            print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Failed to parse JSON from response. Status: {response.status_code}", flush=True)
            return None

def check_and_upgrade(token, upgrade_id, required_level):
    upgrades = get_available_upgrades_combo(token)
    if upgrades:
        for upgrade in upgrades:
            if upgrade['id'] == upgrade_id and upgrade['level'] < required_level + 1:
                print(Fore.CYAN + Style.BRIGHT + f"[ Daily Combo ] : Upgrading {upgrade_id}", flush=True)
                req_level_total = required_level + 1
                for _ in range(req_level_total - upgrade['level']):
                    result = buy_upgrade_combo(token, upgrade_id)
                    if isinstance(result, dict) and 'error_code' in result and result['error_code'] == 'UPGRADE_NOT_AVAILABLE':
                        needed_upgrade = result['error_message'].split(':')[-1].strip().split()
                        needed_upgrade_id = needed_upgrade[1]
                        needed_upgrade_level = int(needed_upgrade[-1])
                        print(Fore.YELLOW + Style.BRIGHT + f"\r[ Daily Combo ] : Trying to buy {needed_upgrade_id} level {needed_upgrade_level}", flush=True)
                        if check_and_upgrade(token, needed_upgrade_id, needed_upgrade_level):
                            print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Combo ] : Successfully upgraded {needed_upgrade_id} to level {needed_upgrade_level}. Retrying upgrade {upgrade_id}.", flush=True)
                            continue
                        else:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Failed to upgrade {needed_upgrade_id} to level {needed_upgrade_level}", flush=True)
                            return False
                    elif result == 'insufficient_funds':
                        print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Not enough coins to upgrade {upgrade_id}", flush=True)
                        return False
                    elif result.status_code != 200:
                        print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Upgrade failed for {upgrade_id} with errors: {result}", flush=True)
                        return False
                print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Combo ] : Upgrade {upgrade_id} successfully leveled to {required_level}", flush=True)
                return True
    return False

def claim_daily_combo(token):
    url = 'https://api.hamsterkombat.io/clicker/claim-daily-combo'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Origin': 'https://hamsterkombat.io',
        'Referer': 'https://hamsterkombat.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print(Fore.GREEN + Style.BRIGHT + "\r[ Daily Combo ] : Daily combo successfully claimed.", flush=True)
        return response.json()
    else:
        error_response = response.json()
        if error_response.get('error_code') == 'DAILY_COMBO_DOUBLE_CLAIMED':
            print(Fore.YELLOW + Style.BRIGHT + "\r[ Daily Combo ] : Already claimed", flush=True)
        else:
            print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Failed. {response}", flush=True)
        return error_response
    
def check_combo_purchased(token):
    url = 'https://api.hamsterkombat.io/clicker/upgrades-for-buy'
    headers = get_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        purchased_combos = data.get('dailyCombo', {}).get('upgradeIds', [])
        return purchased_combos
    else:
        print(Fore.RED + Style.BRIGHT + f"Failed to obtain combo status. Status: {response.status_code}", flush=True)
        return None

# Define the variables that are referenced but not defined in the script
ask_cipher = 'n'  # Default value for asking cipher
cipher_text = "default_cipher"  # Default cipher text
cek_task_list = 'n'  # Default value for checking task list
auto_upgrade_passive = 'n'  # Default value for auto-upgrade passive

# If the auto upgrade passive is 'n', set a default max price
if auto_upgrade_passive == 'n':
    max_price = 1500000  # Default max price

# Define a function to print a welcome message
def print_welcome_message():
    print(Fore.GREEN + Style.BRIGHT + "Hamster Kombat BOT!")

# MAIN CODE
cek_task_dict = {}
claimed_ciphers = set()

combo_upgraded = {}
def main():
    global cek_task_dict, claimed_ciphers, auto_claim_daily_combo, combo_list, combo_upgraded
    
    print_welcome_message()
    print(Fore.GREEN + Style.BRIGHT + "Starting Hamster Kombat....\n\n")
    init_data = load_tokens('hamster.txt')
    token_cycle = cycle(init_data)

    token_dict = {}
    while True:
        init_data_raw = next(token_cycle)
        token = token_dict.get(init_data_raw)
        
        if token:
            print(Fore.GREEN + Style.BRIGHT + f"\n\n\rUsing an existing token...", end="", flush=True)
        else:
            print(Fore.GREEN + Style.BRIGHT + f"\n\n\rObtaining tokens...", end="", flush=True)

            token = get_token(init_data_raw)
            if token:
                token_dict[init_data_raw] = token
                print(Fore.GREEN + Style.BRIGHT + f"\n\n\rToken successfully obtained", flush=True)
            else:
                print(Fore.RED + Style.BRIGHT + f"\n\n\rMoving to the next account\n\n", flush=True)
                continue

        if init_data_raw not in combo_upgraded:
            combo_upgraded[init_data_raw] = False

        response = authenticate(token)
   
        if response.status_code == 200:

            user_data = response.json()
            username = user_data.get('telegramUser', {}).get('username', 'Username Empty')
            firstname = user_data.get('telegramUser', {}).get('firstName', 'Empty')
            lastname = user_data.get('telegramUser', {}).get('lastName', 'Empty')
            
            print(Fore.GREEN + Style.BRIGHT + f"\r\n[{Fore.WHITE + Style.BRIGHT} {username} | {firstname} {lastname} {Fore.GREEN + Style.BRIGHT}]")

            print(Fore.GREEN + f"\rRetrieving user information...", end="", flush=True)
            response = sync_clicker(token)
            if response.status_code == 200:
                clicker_data = response.json()['clickerUser']
                print(Fore.YELLOW + Style.BRIGHT + f"\r[ Level ] : {clicker_data['level']}          ", flush=True)
                print(Fore.YELLOW + Style.BRIGHT + f"[ Total Earned ] : {int(clicker_data['totalCoins'])}")
                print(Fore.YELLOW + Style.BRIGHT + f"[ Coin ] : {int(clicker_data['balanceCoins'])}")
                print(Fore.YELLOW + Style.BRIGHT + f"[ Energy ] : {clicker_data['availableTaps']}")
                boosts = clicker_data['boosts']
                boost_max_taps_level = boosts.get('BoostMaxTaps', {}).get('level', 0)
                boost_earn_per_tap_level = boosts.get('BoostEarnPerTap', {}).get('level', 0)
                
                print(Fore.CYAN + Style.BRIGHT + f"[ Energy Level] : {boost_max_taps_level}")
                print(Fore.CYAN + Style.BRIGHT + f"[ Tap Level ] : {boost_earn_per_tap_level}")
                print(Fore.CYAN + Style.BRIGHT + f"[ Exchange ] : {clicker_data['exchangeId']}")
                if clicker_data['exchangeId'] == None:
                    print(Fore.GREEN + '\rSetting exchange to OKX..', end="", flush=True)
                    exchange_set = exchange(token)

                    if exchange_set.status_code == 200:
                        print(Fore.GREEN + Style.BRIGHT +'\rSuccessfully set exchange to OKX', flush=True)
                    else:
                        print(Fore.RED + Style.BRIGHT +'\rFailed to set exchange', flush=True)
                print(Fore.CYAN + Style.BRIGHT + f"[ Passive Earnings ] : {clicker_data['earnPassivePerHour']}\n")
                
                print(Fore.GREEN + f"\r[ Tap Status ] : Tapping...", end="", flush=True)

                response = tap(token, clicker_data['maxTaps'], clicker_data['availableTaps'])
                if response.status_code == 200:
                    print(Fore.GREEN + Style.BRIGHT + "\r[ Tap Status ] : Tapped", flush=True)
                    print(Fore.CYAN + Style.BRIGHT + f"\r[ Booster ] : Checking booster...", end="", flush=True)
                    response = cek_booster(token)
                    if response.status_code == 200:
                        booster_info = response.json()['boostsForBuy']
                        for boost in booster_info:
                            if boost['id'] == 'BoostFullAvailableTaps':
                                stock = boost['maxLevel'] - boost['level']
                                cooldown = boost['cooldownSeconds'] // 60
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Booster ] : Stock {stock} | Cooldown {cooldown} minutes", flush=True)
                        if cooldown == 0:
                            print(Fore.GREEN + Style.BRIGHT + f"\r[ Boosted ] : Activating booster..", end="", flush=True)
                            response = use_booster(token)
                            if response.status_code == 200:
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Boosted ] : Booster activated", flush=True)   
                            elif response.status_code == 400:
                                error_info = response.json()
                                if error_info.get('error_code') == 'BOOST_COOLDOWN':
                                    cooldown_seconds = int(error_info.get('error_message').split()[-2])
                                    cooldown_minutes = cooldown_seconds // 60
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Boosted ] : Booster on cooldown for {cooldown_minutes} minutes", flush=True)
                                else:
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Boosted ] : Booster activation failed", flush=True)
                            else:
                                print(Fore.RED + Style.BRIGHT + f"\r[ Boosted ] : Booster activation failed", flush=True)
                    else:
                        print(Fore.RED + Style.BRIGHT + "\r[ Booster ] : Tap Status : Tap failed", flush=True)
                else:
                    print(Fore.RED + Style.BRIGHT + "\r[ Tap Status ] : Tap failed", flush=True)

                print(Fore.GREEN + f"\r[ Daily Login ] : Checking...", end="", flush=True)

                time.sleep(1)
                response = claim_daily(token)
                if response.status_code == 200:
                    daily_response = response.json()['task']
                    if daily_response['isCompleted']:
                        print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Login ] Days {daily_response['days']} | Completed", flush=True)
                    else:
                        print(Fore.RED + Style.BRIGHT + f"\r[ Daily Login ] Days {daily_response['days']} | Not yet time to claim daily", flush=True)
                else:
                    print(Fore.RED + Style.BRIGHT + f"\r[ Daily Login ] Daily check failed {response.status_code}", flush=True)
                
                if ask_cipher == 'y':
                    if token not in claimed_ciphers:
                        print(Fore.GREEN + Style.BRIGHT + f"\r[ Claim Cipher ] : Claiming cipher...", end="", flush=True)
                        response = claim_cipher(token, cipher_text)
                        try:
                            if response.status_code == 200:
                                bonuscoins = response.json()['dailyCipher']['bonusCoins']
                                print(Fore.GREEN + Style.BRIGHT + f"\r[ Claim Cipher ] : Cipher successfully claimed | {bonuscoins} bonus coins", flush=True)
                                claimed_ciphers.add(token)
                            else:
                                error_info = response.json()
                                if error_info.get('error_code') == 'DAILY_CIPHER_DOUBLE_CLAIMED':
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Claim Cipher ] : Cipher already claimed", flush=True)
                                else:
                                    print(Fore.RED + Style.BRIGHT + f"\r[ Claim Cipher ] : Failed to claim cipher: {error_info.get('error_message', 'No error message')}", flush=True)
                        except json.JSONDecodeError:
                            print(Fore.RED + Style.BRIGHT + "\r[ Claim Cipher ] : Failed to parse JSON from response.", flush=True)
                        except Exception as e:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Claim Cipher ] : An error occurred: {str(e)}", flush=True)
                    else:
                        print(Fore.RED + Style.BRIGHT + f"\r[ Claim Cipher ] : Cipher previously claimed.", flush=True)

                if auto_claim_daily_combo == 'y' and not combo_upgraded[init_data_raw]:
                    cek = claim_daily_combo(token)
                    if cek.get('error_code') != 'DAILY_COMBO_DOUBLE_CLAIMED':
                        purchased_combos = check_combo_purchased(token)
                        if purchased_combos is None:
                            print(Fore.RED + Style.BRIGHT + "\r[ Daily Combo ] : Failed to obtain combo status. Will try again with the next account.", flush=True)
                        else:
                            for combo in combo_list:
                                if combo in purchased_combos:
                                    print(Fore.GREEN + Style.BRIGHT + f"\r[ Daily Combo ] : {combo} purchased.", flush=True)
                                else:
                                    print(Fore.GREEN + f"\r[ Daily Combo ] : Buying {combo}", flush=True)
                                    result = buy_upgrade_combo(token, combo)
                                    if result == 'insufficient_funds':
                                        print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Failed to purchase {combo} due to insufficient funds", flush=True)
                                    elif 'error_code' in result and result['error_code'] == 'UPGRADE_NOT_AVAILABLE':
                                        upgrade_details = result['error_message'].split(':')[-1].strip().split()
                                        upgrade_key = upgrade_details[1]
                                        upgrade_level = int(upgrade_details[-1])
                                        print(Fore.RED + Style.BRIGHT + f"\r[ Daily Combo ] : Failed to purchase {combo} due to requirement {upgrade_key} level {upgrade_level}", flush=True)    
                                        result = check_and_upgrade(token, upgrade_key, upgrade_level)
                            combo_upgraded[init_data_raw] = True
                            required_combos = set(combo_list)
                            purchased_combos = set(check_combo_purchased(token))
                            if purchased_combos == required_combos:
                                print(Fore.GREEN + Style.BRIGHT + "\r[ Daily Combo ] : All combos purchased, trying to claim daily combo.", end="" ,flush=True)
                                claim_daily_combo(token)
                            else:
                                print(Fore.YELLOW + Style.BRIGHT + f"\r[ Daily Combo ] : Error. Unpurchased combo: {required_combos - purchased_combos}", flush=True)
                                combo_upgraded[init_data_raw] = False
                                continue
                
                print(Fore.GREEN + f"\r[ Task List ] : Checking...", end="", flush=True)
                if cek_task_list == 'y':
                    if token not in cek_task_dict:
                        cek_task_dict[token] = False
                    if not cek_task_dict[token]:
                        response = list_tasks(token)
                        cek_task_dict[token] = True
                        if response.status_code == 200:
                            tasks = response.json()['tasks']
                            all_completed = all(task['isCompleted'] or task['id'] == 'invite_friends' for task in tasks)
                            if all_completed:
                                print(Fore.GREEN + Style.BRIGHT + "\r[ Task List] : All tasks claimed\n", flush=True)
                            else:
                                for task in tasks:
                                    if not task['isCompleted']:
                                        print(Fore.YELLOW + Style.BRIGHT + f"\r[ Task List ] : Claiming {task['id']}...", end="", flush=True)
                                        response = check_task(token, task['id'])
                                        if response.status_code == 200 and response.json()['task']['isCompleted']:
                                            print(Fore.GREEN + Style.BRIGHT + f"\r[ Task List ] : Claimed {task['id']}\n", flush=True)
                                        else:
                                            print(Fore.RED + Style.BRIGHT + f"\r[ Task List ] : Claim Failed {task['id']}\n", flush=True)
                        else:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Task List ] : Failed to obtain task list {response.status_code}\n", flush=True)
                else:
                    print(Fore.GREEN + f"\r[ Task List ] : Skipped...", end="", flush=True)

                if auto_upgrade_passive == 'y':
                    print(Fore.GREEN + f"\r[ Upgrade Minning ] : Checking...", end="", flush=True)

            else:
                print(Fore.RED + Style.BRIGHT + f"\r Failed to obtain user info {response.status_code}", flush=True)
        elif response.status_code == 401:
            error_data = response.json()
            if error_data.get("error_code") == "NotFound_Session":
                print(Fore.RED + Style.BRIGHT + f"=== [ Invalid Token {token} ] ===")
                token_dict.pop(init_data_raw, None)
                token = None
            else:
                print(Fore.RED + Style.BRIGHT + "Authentication failed with unknown error")
        else:
            print(Fore.RED + Style.BRIGHT + f"Error with status code: {response.status_code}")
            token = None
            
        time.sleep(1)

if __name__ == "__main__":
    main()
