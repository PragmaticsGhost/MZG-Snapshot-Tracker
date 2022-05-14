import requests
import json
import time
import os.path



loop = True

while loop:

    #print("Would you like to look up a specific token or ")
    walletID = input("Please enter the Wallet ID you would like to query the OpenSea API about:\n")
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
                print("Querying OpenSea API for Wallet info...\n")
                time.sleep(0.3)

                response = requests.get(f"https://api.opensea.io/api/v1/collections?asset_owner={walletID}&limit=300")
                pretty = json.dumps(response.json(), indent=2)
                res = open('result.json', mode='w')
                res.write(pretty)
                print('OpenSea Collection Snapshot Data for Wallet ID ' + walletID + ' successfully written to "Desktop/result.json"\n')

                time.sleep(0.3)
                print("Iterating through JSON object to enumerate Wallet Token ID's....\n")

                with open('MZGStore.json', 'r') as f:
                    wallet_dict = json.load(f)

                for wallets in wallet_dict:

                    #if wallets['wallet'] == walletID:   

                        print(wallets)
                        

                        loop = False     

            else:
                print('Wallet ID does not start with "0x", please make sure there is an "0x" at the beginning of the wallet address.\n')           

        else:
            print("Wallet ID is not the correct number of characters, try again.\n")

    else:
        print("Incorrect wallet address, try again.\n")
        


#0x5558AED91F04C83bb9dd7201181634997D96a912
    
        