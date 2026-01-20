
import sys
import pymongo

def check_analysis(analysis_id):
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['biasscope']
    # Try both _id and analysis_id fields
    analysis = db.analyses.find_one({'analysis_id': analysis_id})
    if not analysis:
        analysis = db.analyses.find_one({'_id': analysis_id})
    if not analysis:
        print(f"Analysis not found: {analysis_id}")
        return
    print(f"Analysis ID: {analysis_id}")
    print(f"Status: {analysis.get('status')}")
    print(f"Results present: {'results' in analysis and bool(analysis['results'])}")
    print(f"Report generated: {analysis.get('report_generated')}")
    print(f"Report path: {analysis.get('report_path')}")
    if 'error_message' in analysis:
        print(f"Error: {analysis['error_message']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_analysis.py <analysis_id>")
        sys.exit(1)
    check_analysis(sys.argv[1])
