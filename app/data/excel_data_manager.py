"""
Excel Data Manager
Stores all test data in Excel/CSV files with complete logs
"""

import pandas as pd
import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class ExcelDataManager:
    """Manages test data storage in Excel/CSV format"""
    
    def __init__(self, 
                 excel_path: str = "test_history.xlsx",
                 logs_dir: str = "test_logs",
                 screenshots_dir: str = "screenshots"):
        """
        Initialize data manager
        
        Args:
            excel_path: Path to main Excel file
            logs_dir: Directory for detailed JSON logs
            screenshots_dir: Directory for screenshots
        """
        self.excel_path = excel_path
        self.logs_dir = logs_dir
        self.screenshots_dir = screenshots_dir
        
        # Create directories
        os.makedirs(logs_dir, exist_ok=True)
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Initialize Excel file if not exists
        self._init_excel()
    
    def _init_excel(self):
        """Create Excel file with proper structure"""
        if not os.path.exists(self.excel_path):
            df = pd.DataFrame(columns=[
                'test_id',
                'timestamp',
                'instruction',
                'status',
                'passed',
                'duration_seconds',
                'steps_count',
                'browser_opened',
                'url_visited',
                'login_checked',
                'login_status',
                'screenshots_taken',
                'errors',
                'code_file_path',
                'log_file_path'
            ])
            df.to_excel(self.excel_path, index=False, sheet_name='Test History')
            print(f" Created Excel file: {self.excel_path}")
    
    def save_test_result(self, 
                        instruction: str,
                        state: Dict,
                        execution_result: Dict) -> str:
        """
        Save complete test result to Excel and JSON log
        
        Args:
            instruction: User's natural language instruction
            state: Final LangGraph state
            execution_result: Test execution results
            
        Returns:
            test_id: Unique identifier for this test
        """
        # Generate test ID
        test_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Extract data from state
        parsed_steps = state.get("parsed_steps", [])
        browser_open = state.get("browser_open", False)
        current_url = state.get("current_url", "")
        logged_in = state.get("logged_in", False)
        generated_code = state.get("generated_code", "")
        code_file_path = state.get("code_file_path", "")
        
        # Extract execution data
        status = execution_result.get("status", "unknown")
        passed = execution_result.get("return_code", 1) == 0
        output = execution_result.get("output", "")
        errors = execution_result.get("errors", "")
        
        # Calculate duration from output
        duration = self._extract_duration(output)
        
        # Count steps and features
        steps_count = len(parsed_steps)
        login_checked = any(s.get("action") == "CHECK_LOGIN" for s in parsed_steps)
        screenshots_taken = sum(1 for s in parsed_steps if s.get("action") == "SCREENSHOT")
        
        # Prepare row for Excel
        new_row = {
            'test_id': test_id,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'instruction': instruction,
            'status': status,
            'passed': passed,
            'duration_seconds': duration,
            'steps_count': steps_count,
            'browser_opened': browser_open,
            'url_visited': current_url,
            'login_checked': login_checked,
            'login_status': 'Logged In' if logged_in else 'Not Logged In' if login_checked else 'N/A',
            'screenshots_taken': screenshots_taken,
            'errors': errors[:500] if errors else "",  # Truncate long errors
            'code_file_path': code_file_path,
            'log_file_path': f"{self.logs_dir}/{test_id}.json"
        }
        
        # Append to Excel
        try:
            df = pd.read_excel(self.excel_path)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_excel(self.excel_path, index=False, sheet_name='Test History')
            print(f" Saved to Excel: {self.excel_path}")
        except Exception as e:
            print(f" Excel save error: {e}")
        
        # Save detailed JSON log
        log_data = {
            'test_id': test_id,
            'timestamp': datetime.now().isoformat(),
            'instruction': instruction,
            'parsed_steps': parsed_steps,
            'browser_state': {
                'browser_open': browser_open,
                'current_url': current_url,
                'logged_in': logged_in
            },
            'generated_code': generated_code,
            'code_file_path': code_file_path,
            'execution': {
                'status': status,
                'passed': passed,
                'duration_seconds': duration,
                'output': output,
                'errors': errors,
                'return_code': execution_result.get("return_code", -1)
            },
            'metadata': {
                'steps_count': steps_count,
                'login_checked': login_checked,
                'screenshots_taken': screenshots_taken
            }
        }
        
        log_file = os.path.join(self.logs_dir, f"{test_id}.json")
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        print(f" Saved JSON log: {log_file}")
        
        return test_id
    
    def _extract_duration(self, output: str) -> float:
        """Extract duration from test output"""
        import re
        # Look for patterns like "5.2s" or "(5.2s)"
        match = re.search(r'(\d+\.?\d*)\s*s', output)
        if match:
            return float(match.group(1))
        return 0.0
    
    def get_all_tests(self) -> pd.DataFrame:
        """Get all test history"""
        try:
            return pd.read_excel(self.excel_path)
        except:
            return pd.DataFrame()
    
    def get_test_by_id(self, test_id: str) -> Optional[Dict]:
        """Get detailed test data from JSON log"""
        log_file = os.path.join(self.logs_dir, f"{test_id}.json")
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def get_statistics(self) -> Dict:
        """Calculate statistics from Excel data"""
        df = self.get_all_tests()
        
        if df.empty:
            return {
                'total_tests': 0,
                'passed': 0,
                'failed': 0,
                'pass_rate': 0.0,
                'avg_duration': 0.0,
                'total_steps': 0,
                'login_checks': 0,
                'screenshots': 0
            }
        
        return {
            'total_tests': len(df),
            'passed': int(df['passed'].sum()),
            'failed': int((~df['passed']).sum()),
            'pass_rate': float(df['passed'].mean() * 100) if len(df) > 0 else 0.0,
            'avg_duration': float(df['duration_seconds'].mean()),
            'total_steps': int(df['steps_count'].sum()),
            'login_checks': int(df['login_checked'].sum()),
            'screenshots': int(df['screenshots_taken'].sum())
        }
    
    def export_to_csv(self, output_path: str = "test_history.csv"):
        """Export Excel data to CSV"""
        df = self.get_all_tests()
        df.to_csv(output_path, index=False)
        print(f" Exported to CSV: {output_path}")
        return output_path
    
    def search_tests(self, query: str) -> pd.DataFrame:
        """Search tests by instruction"""
        df = self.get_all_tests()
        if df.empty:
            return df
        
        mask = df['instruction'].str.contains(query, case=False, na=False)
        return df[mask]
    
    def get_recent_tests(self, limit: int = 10) -> pd.DataFrame:
        """Get most recent tests"""
        df = self.get_all_tests()
        if df.empty:
            return df
        
        return df.sort_values('timestamp', ascending=False).head(limit)
    
    def clear_all_data(self):
        """Clear all test data (use with caution!)"""
        if os.path.exists(self.excel_path):
            os.remove(self.excel_path)
        
        # Clear logs
        for file in os.listdir(self.logs_dir):
            os.remove(os.path.join(self.logs_dir, file))
        
        # Reinitialize
        self._init_excel()
        print(" All data cleared")


# Global instance
data_manager = ExcelDataManager()