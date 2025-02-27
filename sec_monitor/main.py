# sec_monitor/main.py
import logging
from collections import defaultdict
from sec_monitor.config import config
from sec_monitor.s3_manager import S3Manager
from sec_monitor.sec_client import fetch_filings
from sec_monitor.email_client import send_notification

logger = logging.getLogger(__name__)

# --- Configuration ---
IS_INITIAL_RUN = False

# Company CIKs to monitor
COMPANY_CIKS = {
    '0001747661': 'ADD',
    '0001546296': 'IPDN',
    '0001413745': 'ANTE',
    '0001527762': 'MFH',
    '0001957413': 'CJET',
    '0001769768': 'EJH',
}

def process_company_filings(cik, state):
    """Process filings for a single company and return new filings"""
    try:
        logger.info(f"Checking filings for CIK: {cik}")
        filings = fetch_filings(cik)

        if not filings:
            logger.warning(f"No filings data found for CIK: {cik}")
            return []

        accessions = filings.get('accessionNumber', [])
        forms = filings.get('form', [])
        dates = filings.get('filingDate', [])

        if not accessions:
            logger.info(f"No accessions found for CIK: {cik}")
            return []

        last_seen = state.get(cik)
        new_filings = []

        if last_seen and last_seen in accessions:
            last_index = accessions.index(last_seen)
            new_accessions = accessions[:last_index]
        else:
            new_accessions = accessions  # First run or reset state

        if new_accessions:
            # Update state to most recent accession
            state[cik] = new_accessions[0]

            # Collect new filings details
            for i in range(len(new_accessions)):
                accession = new_accessions[i]
                form_type = forms[i]
                filing_date = dates[i]

                # Generate SEC URL
                unpadded_cik = cik.lstrip('0')
                clean_accession = accession.replace('-', '')
                url = (f"https://www.sec.gov/Archives/edgar/data/{unpadded_cik}/"
                       f"{clean_accession}/{accession}-index.html")

                new_filings.append({
                    'form': form_type,
                    'date': filing_date,
                    'url': url
                })

            logger.info(f"Found {len(new_filings)} new filings for CIK: {cik}")

        return new_filings

    except Exception as e:
        logger.error(f"Error processing CIK {cik}: {str(e)}", exc_info=True)
        return []


def main():
    """Main execution flow"""
    try:
        logger.info("Starting SEC filings check")
        s3 = S3Manager()

        # Load state from S3
        state = s3.read_json(config.s3_bucket, 'sec_fillings/state.json')
        logger.debug("Loaded state from S3")

        all_new_filings = defaultdict(list)
        total_new = 0

        # Process each company
        for cik in COMPANY_CIKS.keys():
            if not cik.strip():
                continue

            new_filings = process_company_filings(cik.strip(), state)
            if new_filings:
                all_new_filings[cik] = new_filings
                total_new += len(new_filings)

        # Save updated state
        s3.write_json(config.s3_bucket, 'sec_fillings/state.json', state)
        logger.info(f"Saved updated state to S3. Total new filings: {total_new}")

        # Send notification if new filings found
        if not IS_INITIAL_RUN and total_new > 0:
            email_body = "New SEC filings detected:\n\n"
            for cik, filings in all_new_filings.items():
                name = COMPANY_CIKS.get(cik, cik)
                email_body += f"{name}:\n"
                for filing in filings:
                    email_body += (f"- {filing['form']} filed on {filing['date']}\n"
                                   f"  URL: {filing['url']}\n")
                email_body += "\n"

            send_notification(
                subject=f"New SEC Filings Alert ({total_new} new)",
                body=email_body,
                is_critical=True
            )
        else:
            send_notification(
                subject="No new SEC filings detected",
                body='',
                is_critical=False
            )

        logger.info("SEC filings check completed successfully")

    except Exception as e:
        logger.critical(f"Fatal error in main execution: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    from sec_monitor.logger import (setup_logging)

    setup_logging()

    try:
        main()
    finally:
        # Ensure all logs are flushed to S3
        logging.shutdown()