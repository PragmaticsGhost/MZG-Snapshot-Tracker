import requests
import json
import time
from datetime import datetime
import os


loop = True

while loop:

    
    walletID = "0x5558AED91F04C83bb9dd7201181634997D96a912" #input("Please enter the Wallet ID you would like to query the OpenSea API about:\n") Faster for testing 
    contractID = "0xA0529c325e2594dcc599BA6E39aA4d6b28834c53" #input("Please enter the Contract ID you would like to query:\n") Faster for testing 
    snapshotDate = "2022-02-28 11:59" #str(input('Enter date(yyyy-mm-dd hh:mm): ')) Faster for testing 

    dt = datetime.strptime(snapshotDate, '%Y-%m-%d %H:%M')
    epoch = dt.timestamp() 
    print(epoch)



    walletLength = len(walletID)
    wallet1stchars = walletID[0:2]
    print("Requested Wallet ID is:" + walletID + ", is this correct?\n")
    time.sleep(0.3)
    answer = "Y" #input("Y/N?:\n") Faster for testing 

    if answer == "Y":

        if walletLength == 42 : 

            if wallet1stchars == "0x" :

                print("Wallet ID appears to be valid.\n")
                time.sleep(0.3)
                print("Querying OpenSea & Etherscan APIs for Wallet info...\n")
                time.sleep(0.3)

                #responseOS = requests.get(f"https://api.opensea.io/api/v1/collections?asset_owner={walletID}&limit=300")
                #responseES2 = requests.get(f"https://api.etherscan.io/api?module=account&action=tokennfttx&contractaddress={contractID}&address={walletID}&page=1&offset=100&startblock=0&endblock=27025780&sort=asc&apikey=UVCMJ2PJ8CRISDAKNC7GB7I62K38U7G2DP")

                print("Done.")
                # Future If statement to evaluate previous snapshot state
                #print("Snapshotting chain, please wait...\n")
                #os.system("erc721-snapshot")

                #prettyOS = json.dumps(responseOS.json(), indent=2)
                #prettyES2 = json.dumps(responseES2.json(), indent=2)

                #resOS = open('resultOS.json', mode='w')
                #resES2 = open('resultES2.json', mode='w')

                #resOS.write(prettyOS)
                #resES2.write(prettyES2)

                #print('OpenSea Collection Snapshot Data for Wallet ID ' + walletID + ' successfully written to "Desktop/resultOS.json"\n')
                print('Etherscan Snapshot Data for Wallet ID ' + walletID + ' successfully written to "Desktop/resultES2.json"\n')


                time.sleep(0.3)
                print("Iterating through JSON object to enumerate Wallet Token ID's....\n")

                with open('resultES2.json', 'r') as f:
                    
                    resultES2_dict = json.load(f)
                    

                    for toAddress in resultES2_dict:


                        recvAddr = toAddress.get('to') 
                        recvTime = toAddress.get('timeStamp')
                        intRecvTime = int(recvTime)
                        correctedDate = datetime.fromtimestamp(intRecvTime)

                        #print(recvAddr.casefold(), len(recvAddr))  DEBUG
                        #print(walletID.casefold(), len(walletID))  DEBUG
                    
                        if recvAddr.casefold() == walletID.casefold():


                            print("The following MZG Token ID's entered this wallet at the following times")    
                            print(toAddress['tokenID'], correctedDate)
                        
                            loop = False   
                    loop = False          

            else:
                print('Wallet ID does not start with "0x", please make sure there is an "0x" at the beginning of the wallet address.\n')           

        else:
            print("Wallet ID is not the correct number of characters, try again.\n")

    else:
        print("Incorrect wallet address, try again.\n")        
