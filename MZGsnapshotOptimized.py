import requests
import json
import time
from datetime import datetime
from etherscan import Etherscan
from deepdiff import DeepDiff
import pip
import os
import config #Configuration file import for api_key
contractIDMZG = "0xA0529c325e2594dcc599BA6E39aA4d6b28834c53" #Assign MetaZoo Genesis Contract ID to variable
contractIDMZGT = "0x2D366Be8fA4D15c289964dD4Adf7Be6Cc5e896E8" #Assign MetaZoo Games Token Contract ID to a variable


#Clear console before starting Main loop

def clear_console():
    os.system('clear')    

def queryAPI(walletID, contractID, snapshotDate, snapshotDateBlockNumber, currentBlockNumber, timestampStr):

    try:
        walletLength = len(walletID) #Get length of wallet ID for error checking
        wallet1stchars = walletID[0:2] #Get first 2 characters of wallet ID for error checking
        print("Requested Wallet ID is:" + walletID)
        print("Requested Contract ID is: " + contractName + " @ address " + selectedContract)
        print("Is this correct?")
        answer = input("Y/N?:\n")

        if answer == "Y" or answer == "y": #Verify Everything is A-OK thus far

            if walletLength == 42 : #Verify Wallet ID is at least 42 characters in length

                if wallet1stchars == "0x" : #Verify Wallet ID begins with "0x"

                    print("Wallet ID appears to be valid.\n")
                    time.sleep(0.3)
                    print("Querying Etherscan API for Wallet info...\n")
                    time.sleep(0.3)

                    #Query Etherscan API for Historical ERC721 Token Transfer events, filtered by input Wallet ID and Snapshot Date. 
                    try:
                        getERC721TxEventsSnapshot = es.get_erc721_token_transfer_events_by_address(address=(walletID), startblock=0, endblock=(snapshotDateBlockNumber), sort="asc")
                    except:
                        print("Error querying Etherscan API for historical ERC721 Transaction events by address for end block:" + snapshotDateBlockNumber)
                        loop = False   

                    #Query Etherscan API for ERC721 Token Transfer events, filtered by input Wallet ID and Snapshot Date. 
                    try:
                        getERC721TxEventsCurrent = es.get_erc721_token_transfer_events_by_address(address=(walletID), startblock=0, endblock=(currentBlockNumber), sort="asc")
                    except:
                        print("Error querying Etherscan API for ERC721 Transaction events by address for end block:" + currentBlockNumber)
                        loop = False
     
                    #Open a .JSON file called "resultES2.json" and prepare for writing
                    try:
                        with open('resultES2.json', "w") as outfile3:   
                            #Dump data from getERC721TxEventsSnapshot into json file and prettify
                            json.dump(getERC721TxEventsSnapshot, outfile3, indent=2)
                            print('Etherscan Historical Snapshot Data for Wallet ID ' + walletID + ' at ' + snapshotDate + ' successfully written to "Desktop/resultES2.json"\n')
                    except:
                        print("Error creating .JSON file from getERC721TxEventsSnapshot data")

                    #Open a .JSON file called "resultES2.json" and prepare for writing
                    try:
                        with open('resultES2Current.json', "w") as outfile4:   
                            #Dump data from getERC721TxEventsCurrent into json file and prettify
                            json.dump(getERC721TxEventsCurrent, outfile4, indent=2)
                            print('Etherscan Current Wallet Snapshot Data for Wallet ID' + walletID + ' at ' + timestampStr + ' successfully written to "Desktop/resultES2Current.json"\n')

                    except:
                        print("Error creating .JSON file from getERC721TxEventsCurrent data\n")    

    ######################################################################TESTING COMPARE FEATURES###################################################################################

    #Experimenting with comparing ONLY MZG/MZGT tokens here, currently it reports everything within the wallet that differs between snapshot and current date.
    #We want it to only compare MZG/MZGT tokens between those dates

                    #Run DeepDiff on two unformatted JSON strings, getERC721TxEventsSnapshot and getERC721TxEventsCurrent and write output to variable jsonCompare
                    try:
                        jsonCompare = DeepDiff(getERC721TxEventsSnapshot, getERC721TxEventsCurrent, ignore_order=True)
                        with open('snapshotVsCurrentJsonCompare.json', "w") as outfile5:   
                            #Dump data from getERC721TxEventsSnapshot into a json file and prettify
                            json.dump(jsonCompare, outfile5, indent=2)
                            print("JSON Comparison Successful! Written to: 'Desktop/snapshotVsCurrentJsonCompare.json'\n")

                    except:
                        print("JSON Comparison failed for some reason or another...\n")
                            

    ######################################################################END COMPARE FEATURE TESTING################################################################################

                        
                    #Re-open resultES2.json (auto-closes when done being read from)
                    with open('resultES2.json', 'r') as f:   
                        #Convert JSON data to dict for Python querying 
                        resultES2_dict = json.load(f) 

                        time.sleep(1)
                        #clear_console()

                        print("The following " + contractName + " TokenID's entered this wallet on or before " + snapshotDate + " at the following times:\n") 

                        #Iterate through each item in dict
                        for toAddress in resultES2_dict:

                            recvAddr = toAddress.get('to') #Retrieve "to" address from JSON object
                            recvTime = toAddress.get('timeStamp') #Retrieve "timestamp" information from JSON object
                            contractAddr = toAddress.get('contractAddress') #Retrieve "contract Address" information from JSON object
                            blockNumber = toAddress.get('blockNumber') #Retrieve block number info from JSON object
                            intRecvTime = int(recvTime) #Convert to integer
                            correctedDate = datetime.fromtimestamp(intRecvTime) #Convert to datetime from epoch
                            recvTimeStr = str(recvTime) #Convert to string

                            if recvAddr.casefold() == walletID.casefold(): #Compare if "to" address of a transaction matches input wallet (and ignores upper/lowercase)
                                if contractAddr.casefold() == selectedContract.casefold(): #Compares if the contract address from input matches data in JSON
                                    if recvTimeStr <= correctedEpochInput: #Compares Tx Received time to Snapshot Input time    
                                                
                                        print("TokenID:")   
                                        print(toAddress['tokenID'])
                                        print("Received Date:")
                                        print(correctedDate) 
                                        print("Received in Block:")
                                        print(blockNumber) #Print all eligible Token ID's
                                        print("\n")

                                        loop = False
                                    loop = False
                                loop =  False        
                                                       
                else:
                    print('Wallet ID does not start with "0x", please make sure there is an "0x" at the beginning of the wallet address.\n')           
            else:
                print("Wallet ID is not the correct number of characters, try again.\n")
        else:
            print("Incorrect wallet address, try again.\n") 
    except:
        print("Error doing.....something")


#Title/Greeting
try:
    print("Welcome to the MetaZoo NFT Snapshot Eligibility Checker.")
    print("Written with love by Pragmatic\n")
    es = Etherscan(config.api_key)  #Generate Etherscan client using API Key given in config.py
except:
    print("Unable to generate Etherscan client, ending...") 

#Begin Main loop
loop = True
while loop:
  
    #Initial inputs
    walletID = input("Please enter your Wallet ID:\n") #Enter Wallet ID
    snapshotDate = str(input('Please enter the date you would like to check eligibility on/before (yyyy-mm-dd hh:mm): \n')) #Enter Snapshot Date & Time
    
    #Convert input datetime to epoch
    try:
        dt = datetime.strptime(snapshotDate, '%Y-%m-%d %H:%M') #Format input timestamp
        epoch = dt.timestamp() #Generate Epoch time from input datetime
        epochString = str(epoch) #Convert to string for processing
        correctedEpochInput = epochString.replace(".0","") #Remove trailing ".0" that the datetime convert function adds 
    
    except:   
        print("Incorrect datetime format entered. Please be sure to enter date and time in (yyyy-mm-dd hh:mm)format. Ending....\n")
        loop = False
        break

    #Obtain current datetime and convert to epoch
    try:
        dateTimeObj = datetime.now() #Get current time
        timestampStr = dateTimeObj.strftime("%Y-%m-%d %H:%M") #Format datetime to YYYY-MM-DD HH-MM
        dt2 = datetime.strptime(timestampStr, '%Y-%m-%d %H:%M') #Write formatted datetime to variable
        currentEpochTime = dt2.timestamp() #Generate epoch time from datetime
        currentEpochTimeStr = str(currentEpochTime) #Convert to string for processing
        correctedEpochCurrent = currentEpochTimeStr.replace(".0","") #Remove trailing ".0" that the datetime convert function adds 

    except:
        print("Unable to convert current datetime to epoch, ending...\n")
        loop = False
        break

    #Query Etherscan API for closest blocknumber to current system time & date and assign to variable. Will always choose a block "before" current datetime if forced to choose.
    try:
        currentBlockNumber = es.get_block_number_by_timestamp(timestamp=(correctedEpochCurrent), closest="before")
    except:
        print("Error querying Etherscan API for current blocknumber, ending...\n")
        loop = False
        break

    #Query Etherscan API for closest blocknumber to input system time & date and assign to variable. Will always choose a block "before" input datetime if forced to choose.
    try:
        snapshotDateBlockNumber = es.get_block_number_by_timestamp(timestamp=(correctedEpochInput), closest="before")
    except:
        print("Error querying Etherscan API for blocknumber at input Snapshot time, ending...\n")
        loop = False
        break

#Choose MZG or MZGT contract to query
    print("1 = MetaZoo Genesis")
    print("2 = Metazoo Games Token\n")
    contractID = input("Please select the Contract ID you would like to query:\n") #TESTING
    
    if contractID == "1":
        selectedContract = contractIDMZG
        contractName = "Metazoo Genesis"
        queryAPI(walletID, contractID, snapshotDate, snapshotDateBlockNumber, currentBlockNumber, timestampStr)

    elif contractID == "2":
        selectedContract = contractIDMZGT
        contractName = "Metazoo Games Tokens"
        queryAPI(walletID, contractID, snapshotDate, snapshotDateBlockNumber, currentBlockNumber, timestampStr)
    else:
        print("Contract ID Selection error\n")
    