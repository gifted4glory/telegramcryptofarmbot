import requests
import time
from colorama import Fore, Style, init
import json
from datetime import datetime, timedelta, timezone
import argparse
import json

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://sexyzbot.pxlvrs.io',
    'priority': 'u=1, i',
    'referer': 'https://sexyzbot.pxlvrs.io/',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def get_user_data(query_data):
    url = 'https://api-clicker.pixelverse.xyz/api/users'
    headers['initdata'] = query_data
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Will trigger error if status is not 200
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Your query is incorrect")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def get_progress(query_data):
    url = 'https://api-clicker.pixelverse.xyz/api/mining/progress'
    headers['initdata'] = query_data
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Will trigger error if status is not 200
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Your query is incorrect")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def get_pets_data(query_data):
    url = 'https://api-clicker.pixelverse.xyz/api/pets'
    headers['initdata'] = query_data
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Will trigger error if status is not 200
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Your query is incorrect")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def claim_balance(query_data):
    url = 'https://api-clicker.pixelverse.xyz/api/mining/claim'
    headers['initdata'] = query_data
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Will trigger error if status is not 200
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Your query is incorrect")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

start_time = datetime.now()
def calculate_time_difference(last_buy_time_str):
    last_buy_time = datetime.strptime(last_buy_time_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
    current_time = datetime.now(timezone.utc)
    time_diff = current_time - last_buy_time
    hours, remainder = divmod(time_diff.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"{Fore.MAGENTA+Style.BRIGHT}\r[ Buy Pet ] : In {int(hours)} hours {int(minutes)} minutes", flush=True)

def animated_loading(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(f"\rWaiting for the next request to complete. {frame} - Remaining {remaining_time} seconds         ", end="", flush=True)
            time.sleep(0.25)
    print("\rWaiting for the next request to complete.                           ", flush=True)

def print_welcome_message():
    print(Fore.GREEN + Style.BRIGHT + "Pixelverse BOT!")
    current_time = datetime.now()
    up_time = current_time - start_time
    days, remainder = divmod(up_time.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    # print(Fore.CYAN + Style.BRIGHT + f"Bot up time: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds\n\n")

def upgrade_pet_if_needed(query_data, max_level):
    pets_data = get_pets_data(query_data)
    if pets_data:
        for pet in pets_data['data']:
            current_level = pet['userPet']['level']
            if current_level < max_level:
                pet_id = pet['userPet']['id']
                upgrade_url = f'https://api-clicker.pixelverse.xyz/api/pets/user-pets/{pet_id}/level-up'
                try:
                    headers['initdata'] = query_data
                    upgrade_response = requests.post(upgrade_url, headers=headers)
                    upgrade_response.raise_for_status()
                    print(f"{Fore.GREEN+Style.BRIGHT}\r[ Upgrade Pet ] : Successfully upgraded {pet['name']} to Lv. {current_level + 1}", flush=True)
                except requests.RequestException as e:
                    print(f"{Fore.RED+Style.BRIGHT}\r[ Upgrade Pet ] : Failed to upgrade pet {pet['name']}: {str(e)}", flush=True)
            print(f"{Fore.GREEN+Style.BRIGHT}\r[ Upgrade Pet ] : {pet['name']} is at level {max_level}", flush=True)
    else:
        print(f"{Fore.RED+Style.BRIGHT}\r[ Upgrade Pet ] : Could not fetch pet data", flush=True)

def check_daily_rewards(query_data):
    url = 'https://api-clicker.pixelverse.xyz/api/daily-rewards'
    headers['initdata'] = query_data
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        total_claimed = data['totalClaimed']
        day = data['day']
        reward_amount = data['rewardAmount']
        todays_reward_available = data['todaysRewardAvailable']
        status_claim = "Not Claimed" if todays_reward_available else "Already Claimed"
        print(f"{Fore.MAGENTA+Style.BRIGHT}\r[ Daily Reward ] : Day {day} Amount {reward_amount} | Status: {status_claim} | Total Claimed: {total_claimed}", flush=True)
        if todays_reward_available:
            print(f"{Fore.MAGENTA+Style.BRIGHT}\r[ Daily Reward ] : Claiming...", end="", flush=True)
            claim_daily_reward(query_data)
        return data
    except Exception as e:
        print(f"{Fore.RED+Style.BRIGHT}\r[ Daily Reward ] : Error: {e}")
        return None

def claim_daily_reward(query_data):
    url = 'https://api-clicker.pixelverse.xyz/api/daily-rewards/claim'
    headers['initdata'] = query_data
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        day = data['day']
        amount = data['amount']
        print(f"{Fore.MAGENTA+Style.BRIGHT}\r[ Daily Reward ] : Claimed | Day {day} | Amount: {amount}", flush=True)
        return data
    except Exception as e:
        print(f"{Fore.RED+Style.BRIGHT}\r[ Daily Reward ] : Error: {e}", flush=True)
        return None

def claim_daily_combo(query_data, user_input_order):
    try:
        headers['initdata'] = query_data
        response = requests.get(url="https://api-clicker.pixelverse.xyz/api/cypher-games/current", headers=headers)
        if response.status_code == 200:
            data = response.json()
            combo_id = data.get('id')
            options = data.get('availableOptions')
            json_data = {options[i-1]['id']: user_input_order.index(i) for i in user_input_order}
            print(f"{Fore.CYAN+Style.BRIGHT}\r[ Daily Combo ] : Submitting answer...", flush=True)
            headers['initdata'] = query_data
            response = requests.post(url=f"https://api-clicker.pixelverse.xyz/api/cypher-games/{combo_id}/answer", json=json_data, headers=headers)
            if response.status_code != 400:
                data = response.json()
                amount = data.get("rewardAmount")
                percent = data.get("rewardPercent")
                print(f"{Fore.CYAN+Style.BRIGHT}\r[ Daily Combo ] : Claimed {amount} | {percent}%", flush=True)
            else:
                response = response.json()
                print(f"{Fore.RED+Style.BRIGHT}\r[ Daily Combo ] : Failed to claim {response['message']}", flush=True)
                return None
        else:
            response = response.json()
            if "BadRequestException" in response['code']:
                print(f"{Fore.RED+Style.BRIGHT}\r[ Daily Combo ] : You have already played the cipher game today", flush=True)
            else:
                print(f"{Fore.RED+Style.BRIGHT}\r[ Daily Combo ] : Could not fetch data", flush=True)
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def main():
    auto_upgrade_pet = 'n'  # Set to 'n' by default without asking the user
    if auto_upgrade_pet == 'y':
        max_level_pet = 10  # Set to 10 by default without asking the user

    auto_daily_combo = 'n'  # Set to 'n' by default without asking the user
    if auto_daily_combo == 'y':
        user_input = input("Enter the daily combo order (separate by commas, e.g., 1,4,3,2): ")
        user_input_order = [int(x.strip()) for x in user_input.split(',')]

    while True:
        print_welcome_message()
        try:
            try:
                with open('pixel.txt', 'r') as file:
                    queries = file.readlines()
                for query_data in queries:
                    query_data = query_data.strip()
                    user_response = get_user_data(query_data)
                    if user_response:
                        username = user_response.get('username', "No username")
                        clicks_count = "{:,.0f}".format(user_response.get('clicksCount', 0)).replace(',', '.')
                        pet = user_response.get('pet', {})
                        level_up_price = "{:,.0f}".format(pet.get('levelUpPrice', 0)).replace(',', '.')
                        pet_details = f"Level: {pet.get('level', 'N/A')} | Energy: {pet.get('energy', 'N/A')} | Lv. Up Price: {level_up_price}"
                        print(f"{Fore.BLUE+Style.BRIGHT}\n========[{Fore.WHITE + Style.BRIGHT} {username} {Fore.BLUE + Style.BRIGHT}]========")
                        print(f"{Fore.GREEN+Style.BRIGHT}[ Balance ] : {clicks_count}")
                        print(f"{Fore.YELLOW+Style.BRIGHT}[ Active Pet ] : {pet_details}")
                        print(f"{Fore.YELLOW+Style.BRIGHT}\r[ Pets ] : Fetching pet data...", end="", flush=True)
                        pets_data = get_pets_data(query_data)
                        if pets_data:
                            try:
                                for pet in pets_data['data']:
                                    pet_level = pet['userPet']['level']
                                    print(f"{Fore.YELLOW+Style.BRIGHT}\r[ Pets ] : {pet['name']} | Lv. {pet_level}", flush=True)
                            except KeyError as e:
                                print(f"{Fore.RED+Style.BRIGHT}\r[ Pets ] : An error occurred: {str(e)}", flush=True)
                        else:
                            print(f"{Fore.RED+Style.BRIGHT}\r[ Pets ] : Could not fetch pet data         ", flush=True)
                        if auto_upgrade_pet == 'y':
                            print(f"{Fore.YELLOW+Style.BRIGHT}\r[ Upgrade Pet ] : Upgrading pet", end="", flush=True)
                            upgrade_pet_if_needed(query_data, max_level=max_level_pet)
                        cek_progress = get_progress(query_data)
                        if cek_progress:
                            data = cek_progress
                            max_coin = "{:,.0f}".format(data['maxAvailable']).replace(',', '.')
                            can_claim = "{:,.0f}".format(data['currentlyAvailable']).replace(',', '.')
                            min_claim = "{:,.0f}".format(data['minAmountForClaim']).replace(',', '.')
                            full_claim = datetime.strptime(data['nextFullRestorationDate'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%H hours %M minutes")
                            restore_speed = data['restorationPeriodMs']
                            print(f"{Fore.CYAN+Style.BRIGHT}[ Progress ] : Maximum claim: {max_coin} | Minimum claim: {min_claim}")
                            print(f"{Fore.CYAN+Style.BRIGHT}[ Progress ] : Can claim: {can_claim} | Full claim: {full_claim}")
                            print(f"{Fore.CYAN+Style.BRIGHT}[ Progress ] : Restoration speed: {restore_speed}")
                            print(f"{Fore.YELLOW+Style.BRIGHT}\r[ Claim ] : Claiming...", end="", flush=True)
                            claim = claim_balance(query_data)
                            if claim:
                                claimed_amount = claim.get('claimedAmount', 0)
                                amount = "{:,.0f}".format(claimed_amount).replace(',', '.')
                                print(f"{Fore.GREEN+Style.BRIGHT}\r[ Claim ] : Claimed {amount}     ", flush=True)
                            else:
                                if 'message' in claim and claim['message'] == "There is currently no claim available for this user":
                                    print(f"{Fore.RED+Style.BRIGHT}\r[ Claim ] : Not time to claim yet", flush=True)
                                else:
                                    print(f"{Fore.RED+Style.BRIGHT}\r[ Claim ] : Error {claim}", flush=True)
                        else:
                            print(f"{Fore.RED + Style.BRIGHT}[ Progress ] : Could not check progress status {cek_progress}")
                        print(Fore.MAGENTA + Style.BRIGHT + f"\r[ Daily Reward ] : Checking...", end="", flush=True)
                        check_daily_rewards(query_data)
                        if auto_daily_combo == 'y':
                            print(Fore.CYAN + Style.BRIGHT + f"\r[ Daily Combo ] : Checking...", end="", flush=True)
                            claim_daily_combo(query_data, user_input_order)
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}\n======= Incorrect Query =======")
                animated_loading(300)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        except Exception as e:
            print(f"Error Burst: {str(e)}")

if __name__ == "__main__":
    main()
