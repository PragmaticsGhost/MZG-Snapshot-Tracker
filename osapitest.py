import requests
import json
import time
import datetime
import os


loop = True

while loop:

    
    walletID = input("Please enter the Wallet ID you would like to query the OpenSea API about:\n")
    contractID = input("Please enter the Contract ID you would like to query:\n")
    snapshotDate = input("Please enter the snapshot date you are wishing to check eligibility for in unix time.\n")
    correctedDate = datetime.datetime.fromtimestamp(int(snapshotDate)).strftime('%Y-%m-%d %H:%M:%S')
    print(correctedDate)

    walletLength = len(walletID)
    wallet1stchars = walletID[0:2]
    print("Requested Wallet ID is:" + walletID + ", is this correct?\n")
    time.sleep(0.3)
    answer = input("Y/N?:\n") 

    if answer == "Y":

        if walletLength == 42 : 

            if wallet1stchars == "0x" :

                print("Wallet ID appears to be valid.\n")
                time.sleep(0.3)
                print("Querying OpenSea & Etherscan APIs for Wallet info...\n")
                time.sleep(0.3)

                responseOS = requests.get(f"https://api.opensea.io/api/v1/collections?asset_owner={walletID}&limit=300")
                responseES = requests.get(f"https://api.etherscan.io/api?module=account&action=tokennfttx&contractaddress={contractID}&address={walletID}&page=1&offset=100&startblock=12051523&endblock=27025780&sort=asc&apikey=UVCMJ2PJ8CRISDAKNC7GB7I62K38U7G2DP")

                print("Done.")
                # Future If statement to evaluate previous snapshot state
                print("Snapshotting chain, please wait...\n")
                os.system("erc721-snapshot")

                prettyOS = json.dumps(responseOS.json(), indent=2)
                prettyES = json.dumps(responseES.json(), indent=2)

                resOS = open('resultOS.json', mode='w')
                resES = open('resultES.json', mode='w')

                resOS.write(prettyOS)
                resES.write(prettyES)

                print('OpenSea Collection Snapshot Data for Wallet ID ' + walletID + ' successfully written to "Desktop/resultOS.json"\n')
                print('Etherscan Snapshot Data for Wallet ID ' + walletID + ' successfully written to "Desktop/resultES.json"\n')


                time.sleep(0.3)
                print("Iterating through JSON object to enumerate Wallet Token ID's....\n")

                with open('balances/MetaZoo Games NFT Store.json', 'r') as f:
                    wallet_dict = json.load(f)

                for wallets in wallet_dict:


                    if wallets['wallet'] == walletID:   

                        print(wallets["tokenIds"])
                        

                        loop = False     

            else:
                print('Wallet ID does not start with "0x", please make sure there is an "0x" at the beginning of the wallet address.\n')           

        else:
            print("Wallet ID is not the correct number of characters, try again.\n")

    else:
        print("Incorrect wallet address, try again.\n")        
