from sec_monitor.s3_manager import S3Manager
from sec_monitor.config import config
import logging

COMPANY_CIKS = {
    '0001747661': 'ADD',
    '0001546296': 'IPDN',
    '0001413745': 'ANTE',
    '0001527762': 'MFH',
    '0001957413': 'CJET'
}

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    s3 = S3Manager()
    state = s3.read_json(config.s3_bucket, 'sec_fillings/state.json')
    for cik, accession in state.items():
        ticker = COMPANY_CIKS.get(cik, cik)
        print(f"CIK: {cik} ({ticker}) - Last Accession: {accession}")

    log = s3.read_file(config.s3_bucket, 'sec_fillings/logs.txt')
    print('\n--- Recent Logs ---')
    print(log)
