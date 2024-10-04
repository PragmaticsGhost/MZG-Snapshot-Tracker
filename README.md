# MetaZoo NFT Snapshot Eligibility Checker

## Overview
The **MetaZoo NFT Snapshot Eligibility Checker** is a Python script that allows users to check their eligibility for owning specific MetaZoo NFTs at a given snapshot date. The tool queries the Etherscan API to retrieve ERC721 token transfer data for a specific wallet and checks whether the wallet held any MetaZoo Genesis or MetaZoo Games Tokens on or before a provided snapshot date. The comparison feature highlights differences in token holdings between the snapshot date and the current date.

## Features
- Accepts ETH wallet addresses and snapshot date as input.
- Fetches and compares NFT transaction data from Etherscan for two contracts:
  - MetaZoo Genesis (MZG)
  - MetaZoo Games Token (MZGT)
- Outputs comparison of NFTs between the snapshot date and the current date using DeepDiff.
- Saves results in `.json` files for both the snapshot date and the current date.
- Supports both historical and current snapshot data retrieval.

## Prerequisites
Ensure you have the following installed:
- Python 3.x
- Required Python packages (use `pip` to install):
  ```bash
  pip install requests etherscan-python deepdiff
  ```

## Configuration
To configure the script, add your Etherscan API key to a `config.py` file. The file should look like this:

```python
api_key = "YOUR_ETHERSCAN_API_KEY"
```

## Usage
1. **Clear Console**: The console will be cleared at the start of each run.
2. **Input Wallet ID**: The user is prompted to input their Ethereum wallet address.
3. **Snapshot Date**: The user provides a snapshot date in the format `YYYY-MM-DD HH:MM`.
4. **Contract Selection**: Choose either MetaZoo Genesis or MetaZoo Games Token contract.
5. **Check Eligibility**: The script will check if the wallet held NFTs on or before the snapshot date.
6. **Compare Results**: The script will compare token holdings between the snapshot date and the current date.
7. **Outputs**:
   - `resultES2.json`: Snapshot data.
   - `resultES2Current.json`: Current data.
   - `snapshotVsCurrentJsonCompare.json`: Comparison between snapshot and current data.

### Run the Script
To execute the script, run:

```bash
python3 MZGsnapshot.py
```

## Error Handling
The script handles a variety of errors such as:
- Invalid Wallet ID format.
- Invalid snapshot date format.
- API errors when querying Etherscan.
- Issues while writing `.json` files.

## Additional Information
- This project relies on the **Etherscan API** for fetching Ethereum blockchain data.
- **DeepDiff** is used to compare the JSON outputs of NFT transaction data.

## Future Improvements (probably not, RIP MetaZoo)
- Enhance token filtering to focus specifically on MZG/MZGT tokens in the comparison.
- Add functionality to support other MetaZoo contracts or blockchains.
  
---

Developed with love by **Pragmatic**

ReadMe generated with GenAI....don't hate me, this project is old and will very likely never see use by anybody. 
