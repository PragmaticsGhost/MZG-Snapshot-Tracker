import requests
import json
import time
from datetime import datetime
from etherscan import Etherscan

#Begin Main loop
loop = True
while loop:

    #Generate Etherscan client using API KEY
    es = Etherscan('UVCMJ2PJ8CRISDAKNC7GB7I62K38U7G2DP') 

    #Title/Greeting
    print("Welcome to the MetaZoo NFT Snapshot Eligibility Checker.")
    print("Written with love by Pragmatic\n")

    #Initial inputs
    walletID = input("To begin, please enter your Wallet ID:\n") #Enter Wallet ID
    snapshotDate = str(input('Enter date you would like to check eligibility on/before (yyyy-mm-dd hh:mm): ')) #Enter Snapshot Date & Time
    
    #Convert input datetime to epoch
    try:
        dt = datetime.strptime(snapshotDate, '%Y-%m-%d %H:%M') #Format input timestamp
        epoch = dt.timestamp() #Generate Epoch time from input datetime
        epochFloat = epoch #Just a placeholder variable
        epochString = str(epochFloat) #Convert to string
        correctedEpoch = epochString.replace(".0","") #Remove trailing ".0" that the datetime convert function adds 
    except:   
        print("Incorrect datetime format entered. Please be sure to enter date and time in (yyyy-mm-dd hh:mm) format\n")
        loop = False
        break

    #Query Etherscan API for closest blocknumber to input time & date, will choose a block "before" input datetime if forced.
    try:
        snapshotDateBlockNumber = es.get_block_number_by_timestamp(timestamp=(correctedEpoch), closest="before")

    except:
        print("Error querying Etherscan API...")
        loop = False
        break


    #Open blank .JSON file titled "snapshotDateBlockNumber.json" and prepare for writing
    with open('snapshotDateBlockNumber.json', "w") as outfile:   

        #Dump unformatted JSON data from snapshotDateBlockNumber into JSON file and write to disk
        json.dump(snapshotDateBlockNumber, outfile, indent=2)

    #Choose MZG or MZGT contract to query
    print("1 = MetaZoo Genesis")
    print("2 = Metazoo Games Token\n")
    contractID = input("Please select the Contract ID you would like to query:\n") #TESTING

    if contractID == "1":
        contractIDMZG = "0xA0529c325e2594dcc599BA6E39aA4d6b28834c53" #Assign MZG Contract ID to variable
        

        walletLength = len(walletID) #Get length of wallet ID for error checking
        wallet1stchars = walletID[0:2] #Get first 2 characters of wallet ID for error checking
        print("Requested Wallet ID is:" + walletID)
        print("Requested Contract ID is: MetaZoo Genesis @ address" + contractIDMZG)
        print("Is this correct?")
        time.sleep(0.3)
        answer = input("Y/N?:\n")

        if answer == "Y": #Verify Everything is A-OK thus far

            if walletLength == 42 : #Verify Wallet ID is at least 42 characters in length

                if wallet1stchars == "0x" : #Verify Wallet ID begins with "0x"

                    print("Wallet ID appears to be valid.\n")
                    time.sleep(0.3)
                    print("Querying Etherscan API for Wallet info...\n")
                    time.sleep(0.3)

                    #Query Etherscan API for ERC721 Token Transfer events, filtered by input Wallet ID and Snapshot Date. 
                    getERC721TxEvents = es.get_erc721_token_transfer_events_by_address(address=(walletID), startblock=0, endblock=(snapshotDateBlockNumber), sort="asc")
             

                    #Open a .JSON file called "resultES2.json" and prepare for writing
                    with open('resultES2.json', "w") as outfile:   
                        #Dump data from getERC721TXEvents into json file and prettify
                        json.dump(getERC721TxEvents, outfile, indent=2)

                    print('Etherscan Snapshot Data for Wallet ID ' + walletID + ' at ' + snapshotDate + ' successfully written to "Desktop/resultES2.json"\n')

                    #Re-open resultES2.json (it auto-closes when done being read from)
                    with open('resultES2.json', 'r') as f:   
                        #Convert JSON data to dict for Python querying 
                        resultES2_dict = json.load(f) 

                        #Iterate through each item in dict
                        for toAddress in resultES2_dict:

                            recvAddr = toAddress.get('to') #Retrieve "to" address from JSON object
                            recvTime = toAddress.get('timeStamp') #Retrieve "timestamp" information from JSON object
                            contractAddr = toAddress.get('contractAddress') #Retrieve "contract Address" information from JSON object
                            intRecvTime = int(recvTime) #Convert to integer
                            correctedDate = datetime.fromtimestamp(intRecvTime) #Convert to datetime from epoch
                            recvTimeStr = str(recvTime) #Convert to string
                            

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

                            if recvAddr.casefold() == walletID.casefold(): #Compare if "to" address of a transaction matches input wallet (and ignores upper/lowercase)
                                if contractAddr.casefold() == contractIDMZG.casefold(): #Compares if the contract address from input matches data in JSON
                                    if recvTimeStr <= correctedEpoch: #Compares Tx Received time to Snapshot Input time

                                        print("The following MZG Genesis TokenID's entered this wallet on or before " + snapshotDate + " at the following times:")    
                                        print(toAddress['tokenID'], correctedDate, snapshotDateBlockNumber) #Print all eligible Token ID's
                                        print("")
                        
                                    loop = False  #End loop 

                    loop = False   #End loop prematurely if errors       

                else:
                    print('Wallet ID does not start with "0x", please make sure there is an "0x" at the beginning of the wallet address.\n')           

            else:
                print("Wallet ID is not the correct number of characters, try again.\n")

        else:
            print("Incorrect wallet address, try again.\n") 

    elif contractID == "2":
        contractIDMZGT = "0x2D366Be8fA4D15c289964dD4Adf7Be6Cc5e896E8" #Assign MZGT Contract ID to a variable

        walletLength = len(walletID) #Get length of wallet ID
        wallet1stchars = walletID[0:2] #Parse first two characters of wallet ID
        print("Requested Wallet ID is:" + walletID)
        print("Requested Contract ID is: MetaZoo Games Token @ address " + contractIDMZGT)
        print("Is this correct?")
        time.sleep(0.3)
        answer = input("Y/N?:\n") #TESTING

        if answer == "Y":

            if walletLength == 42 : #Verify wallet is 42 characters

                if wallet1stchars == "0x" : #Verify wallet begins with "0x"

                    print("Wallet ID appears to be valid.\n")
                    time.sleep(0.3)
                    print("Querying Etherscan API for Wallet info...\n")
                    time.sleep(0.3)

                    #Query Etherscan API for ERC721 transfer events by input wallet address/datetime and store returned data in variable
                    getERC721TxEvents = es.get_erc721_token_transfer_events_by_address(address=(walletID), startblock=0, endblock=(snapshotDateBlockNumber), sort="asc")
             

                    #Open .json file and prep for writing
                    with open('resultES2.json', "w") as outfile:   
                        #Dump data from variable into .JSON and prettify
                        json.dump(getERC721TxEvents, outfile, indent=2)

                    print('Etherscan Snapshot Data for Wallet ID ' + walletID + ' at ' + snapshotDate + ' successfully written to "Desktop/resultES2.json"\n')

                    #RE-open resultES2.json and load as dict
                    with open('resultES2.json', 'r') as f:   
                        resultES2_dict = json.load(f) 

                        #Iterate through objects in json
                        for toAddress in resultES2_dict:

                            recvAddr = toAddress.get('to') #Retrieve "to" address of Transactions from JSON
                            recvTime = toAddress.get('timeStamp') #Retrieve timestamp of transactions from JSON
                            contractAddr = toAddress.get('contractAddress') #Retrieve contract address of transactions from data
                            intRecvTime = int(recvTime) #Convert to integer
                            correctedDate = datetime.fromtimestamp(intRecvTime) #Convert to datetime
                            recvTimeStr = str(recvTime) #Convert to string
                            

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

                            if recvAddr.casefold() == walletID.casefold(): #Compare if receive address and input wallet ID is the same to verify this is an incoming Tx
                                if contractAddr.casefold() == contractIDMZGT.casefold(): #Compare if Contract ID of tokens are the desired MetaZoo contract ID
                                    if recvTimeStr <= correctedEpoch: #Check snapshot date against receive time of token tx 

                                        print("The following MetaZoo Games Token TokenID's entered this wallet before " + snapshotDate + " at the following times:\n")    
                                        print(toAddress['tokenID'], correctedDate, snapshotDateBlockNumber) #Print all eligible TokenID's, the incoming Tx date, and the blocknumber the Tx happened in
                                        print("")
                        
                                    loop = False  #End Loop

                    loop = False  #End Loop



    else:
        print("Error, only two options playa...")