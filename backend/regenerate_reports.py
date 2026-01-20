#!/usr/bin/env python
"""
Utility script to regenerate PDF reports for all completed analyses
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.mongodb import get_database
from app.services.report_generator import ReportGenerator
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


async def regenerate_reports():
    """Regenerate PDF reports for all completed analyses"""
    try:
        db = await get_database()
        report_gen = ReportGenerator()
        
        # Get all completed analyses with results
        cursor = db.analyses.find({
            "status": "completed",
            "results": {"$exists": True}
        })
        analyses = await cursor.to_list(None)
        
        if not analyses:
            print("No completed analyses found")
            return
        
        print(f"Found {len(analyses)} completed analyses\n")
        
        success_count = 0
        error_count = 0
        
        for analysis in analyses:
            analysis_id = analysis['_id']
            print(f"Processing: {analysis_id}")
            
            try:
                # Generate the PDF report
                report_path = await report_gen.generate_report(analysis_id, analysis['results'])
                
                # Update the database with the report path
                result = await db.analyses.update_one(
                    {"_id": analysis_id},
                    {"$set": {
                        "report_generated": True,
                        "report_path": report_path
                    }}
                )
                
                print(f"  ✓ Report generated: {report_path}")
                success_count += 1
                
            except Exception as e:
                print(f"  ✗ Error: {str(e)}")
                error_count += 1
                logger.error(f"Error generating report for {analysis_id}: {str(e)}", exc_info=True)
        
        print(f"\n{'='*60}")
        print(f"Report Generation Complete!")
        print(f"  Successful: {success_count}")
        print(f"  Failed: {error_count}")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        logger.error(f"Fatal error in regenerate_reports: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        # Close database connection
        pass


if __name__ == "__main__":
    print("BiasScope Report Regeneration Utility")
    print("="*60)
    print()
    
    asyncio.run(regenerate_reports())
