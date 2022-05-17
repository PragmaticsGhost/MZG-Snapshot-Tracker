import requests
import json
import time
from datetime import datetime
from etherscan import Etherscan


loop = True

while loop:

    es = Etherscan('UVCMJ2PJ8CRISDAKNC7GB7I62K38U7G2DP')
    walletID = input("Please enter the Wallet ID you would like to query the OpenSea API about:\n") #TESTING
    snapshotDate = str(input('Enter date you would like to check eligibility on/before(yyyy-mm-dd hh:mm): ')) #TESTING
    print("")
    dt = datetime.strptime(snapshotDate, '%Y-%m-%d %H:%M')
    epoch = dt.timestamp() 
    epochFloat = epoch
    epochString = str(epochFloat)
    correctedEpoch = epochString.replace(".0","")
    


    print("1 = MetaZoo Games Tokens")
    print("2 = Metazoo Genesis\n")
    contractID = input("Please select the Contract ID you would like to query:\n") #TESTING
    if contractID == "1":
        contractIDMZG = "0xA0529c325e2594dcc599BA6E39aA4d6b28834c53"
        

        walletLength = len(walletID)
        wallet1stchars = walletID[0:2]
        print("Requested Wallet ID is:" + walletID + ", is this correct?\n")
        time.sleep(0.3)
        answer = input("Y/N?:\n") #TESTING

        if answer == "Y":

            if walletLength == 42 : 

                if wallet1stchars == "0x" :

                    print("Wallet ID appears to be valid.\n")
                    time.sleep(0.3)
                    print("Querying OpenSea & Etherscan APIs for Wallet info...\n")
                    time.sleep(0.3)

                    getERC721TxEvents = es.get_erc721_token_transfer_events_by_address(address=(walletID), startblock=0, endblock=27025780, sort="asc")
             
                    print("Done.\n")

                    with open('resultES2.json', "w") as outfile:   
                        json.dump(getERC721TxEvents, outfile, indent=2)

                    print('Etherscan Snapshot Data for Wallet ID ' + walletID + ' at ' + snapshotDate + ' successfully written to "Desktop/resultES2.json"\n')

                    time.sleep(0.3)
                    print("Iterating through JSON object to enumerate Wallet Token ID's....\n")

                    with open('resultES2.json', 'r') as f:   
                        resultES2_dict = json.load(f) 

                        for toAddress in resultES2_dict:

                            recvAddr = toAddress.get('to') 
                            recvTime = toAddress.get('timeStamp')
                            contractAddr = toAddress.get('contractAddress')
                            intRecvTime = int(recvTime)
                            correctedDate = datetime.fromtimestamp(intRecvTime)
                            recvTimeStr = str(recvTime)
                            

                            #print("recvAddr")                          #DEBUG
                            #print(recvAddr.casefold(), len(recvAddr))  #DEBUG
                            #print("")                                  #DEBUG
                            #print("walletID")                          #DEBUG
                            #print(walletID.casefold(), len(walletID))  #DEBUG
                            #rint("")                                   #DEBUG
                            #print("contractAddr")                      #DEBUG
                            #print(contractAddr.casefold(), len(contractAddr)) #DEBUG
                            #print("")                                  #DEBUG
                            #print("contractIDMZG")                     #DEBUG
                            #print(contractIDMZG.casefold(), len(contractIDMZG)) #DEBUG
                            #print("")                                  #DEBUG
                            #print("recvTimeStr")                       #DEBUG
                            #print(recvTimeStr, len(recvTimeStr))  #DEBUG
                            #print("")                             #DEBUG
                            #print("correctedEpoch")               #DEBUG
                            #print(correctedEpoch, len(correctedEpoch)) #DEBUG      
                            #print("")                              #DEBUG

                            if recvAddr.casefold() == walletID.casefold():
                                if contractAddr.casefold() == contractIDMZG.casefold():
                                    if recvTimeStr <= correctedEpoch:

                                        print("The following MZG Genesis TokenID's entered this wallet before " + snapshotDate + " at the following times:")    
                                        print(toAddress['tokenID'], correctedDate)
                                        print("")
                        
                                    loop = False   

                    loop = False          

                else:
                    print('Wallet ID does not start with "0x", please make sure there is an "0x" at the beginning of the wallet address.\n')           

            else:
                print("Wallet ID is not the correct number of characters, try again.\n")

        else:
            print("Incorrect wallet address, try again.\n")        
    elif contractID == "2":
        contractIDMZGT = "0x2D366Be8fA4D15c289964dD4Adf7Be6Cc5e896E8"

        walletLength = len(walletID)
        wallet1stchars = walletID[0:2]
        print("Requested Wallet ID is:" + walletID + ", is this correct?\n")
        time.sleep(0.3)
        answer = input("Y/N?:\n") #TESTING

        if answer == "Y":

            if walletLength == 42 : 

                if wallet1stchars == "0x" :

                    print("Wallet ID appears to be valid.\n")
                    time.sleep(0.3)
                    print("Querying OpenSea & Etherscan APIs for Wallet info...\n")
                    time.sleep(0.3)

                    getERC721TxEvents = es.get_erc721_token_transfer_events_by_address(address=(walletID), startblock=0, endblock=27025780, sort="asc")
             
                    print("Done.\n")

                    with open('resultES2.json', "w") as outfile:   
                        json.dump(getERC721TxEvents, outfile, indent=2)

                    print('Etherscan Snapshot Data for Wallet ID ' + walletID + ' at ' + snapshotDate + ' successfully written to "Desktop/resultES2.json"\n')

                    time.sleep(0.3)
                    print("Iterating through JSON object to enumerate Wallet Token ID's....\n")

                    with open('resultES2.json', 'r') as f:   
                        resultES2_dict = json.load(f) 

                        for toAddress in resultES2_dict:

                            recvAddr = toAddress.get('to') 
                            recvTime = toAddress.get('timeStamp')
                            contractAddr = toAddress.get('contractAddress')
                            intRecvTime = int(recvTime)
                            correctedDate = datetime.fromtimestamp(intRecvTime)
                            recvTimeStr = str(recvTime)
                            

                            #print("recvAddr")                          #DEBUG
                            #print(recvAddr.casefold(), len(recvAddr))  #DEBUG
                            #print("")                                  #DEBUG
                            #print("walletID")                          #DEBUG
                            #print(walletID.casefold(), len(walletID))  #DEBUG
                            #rint("")                                   #DEBUG
                            #print("contractAddr")                      #DEBUG
                            #print(contractAddr.casefold(), len(contractAddr)) #DEBUG
                            #print("")                                  #DEBUG
                            #print("contractIDMZG")                     #DEBUG
                            #print(contractIDMZG.casefold(), len(contractIDMZG)) #DEBUG
                            #print("")                                  #DEBUG
                            #print("recvTimeStr")                       #DEBUG
                            #print(recvTimeStr, len(recvTimeStr))  #DEBUG
                            #print("")                             #DEBUG
                            #print("correctedEpoch")               #DEBUG
                            #print(correctedEpoch, len(correctedEpoch)) #DEBUG      
                            #print("")                              #DEBUG

                            if recvAddr.casefold() == walletID.casefold():
                                if contractAddr.casefold() == contractIDMZGT.casefold():
                                    if recvTimeStr <= correctedEpoch:

                                        print("The following MZGT TokenID's entered this wallet before " + snapshotDate + " at the following times:\n")    
                                        print(toAddress['tokenID'], correctedDate)
                                        print("")
                        
                                    loop = False   

                    loop = False  



    else:
        print("Error, only enter 1 or 2...")    

