import pandas as pd
import openpyxl
from openpyxl.styles import Font, Alignment
import os
import logging
from datetime import datetime

class ExcelGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_excel_file(self, university_name, organizations_data):
        """Create an Excel file for a university's organizations"""
        try:
            # Create filename
            safe_name = self.sanitize_filename(university_name)
            filename = f"{safe_name} - Organizations.xlsx"
            
            # Create DataFrame
            from config import ORGANIZATION_FIELDS
            df = pd.DataFrame(organizations_data, columns=ORGANIZATION_FIELDS)
            
            # Write to Excel
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Organizations', index=False)
                
                # Format the Excel file
                workbook = writer.book
                worksheet = writer.sheets['Organizations']
                
                # Style the header row
                header_font = Font(bold=True)
                header_alignment = Alignment(horizontal='center', vertical='center')
                
                for cell in worksheet[1]:
                    cell.font = header_font
                    cell.alignment = header_alignment
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    
                    adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            self.logger.info(f"Created Excel file: {filename} with {len(organizations_data)} organizations")
            return filename
            
        except Exception as e:
            self.logger.error(f"Failed to create Excel file for {university_name}: {e}")
            return None
    
    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        import re
        # Remove invalid characters for Windows/Unix file systems
        sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
        return sanitized.strip()
    
    def validate_organizations_data(self, organizations_data):
        """Validate and clean organization data before Excel creation"""
        if not organizations_data:
            return []
        
        from config import ORGANIZATION_FIELDS
        cleaned_data = []
        
        for org in organizations_data:
            # Ensure all required fields exist
            cleaned_org = {}
            for field in ORGANIZATION_FIELDS:
                value = org.get(field, '')
                # Clean the value
                if isinstance(value, str):
                    value = value.strip()
                    # Remove excessive whitespace
                    value = ' '.join(value.split())
                cleaned_org[field] = value
            
            # Only add if organization has a name
            if cleaned_org.get('Organization Name'):
                cleaned_data.append(cleaned_org)
        
        return cleaned_data
    
    def create_summary_report(self, results):
        """Create a summary report of all scraping results"""
        try:
            summary_data = []
            total_organizations = 0
            
            for university_name, data in results.items():
                org_count = len(data.get('organizations', []))
                total_organizations += org_count
                
                summary_data.append({
                    'University': university_name,
                    'Organizations Found': org_count,
                    'Organizations URL': data.get('organizations_url', 'N/A'),
                    'Status': data.get('status', 'Unknown'),
                    'Scraping Time': data.get('scraping_time', 'N/A')
                })
            
            # Create summary DataFrame
            df = pd.DataFrame(summary_data)
            
            # Create summary file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Scraping_Summary_{timestamp}.xlsx"
            
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Add a total row
                worksheet = writer.sheets['Summary']
                total_row = len(summary_data) + 2
                worksheet[f'A{total_row}'] = 'TOTAL'
                worksheet[f'B{total_row}'] = total_organizations
                
                # Style the file
                header_font = Font(bold=True)
                for cell in worksheet[1]:
                    cell.font = header_font
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            self.logger.info(f"Created summary report: {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Failed to create summary report: {e}")
            return None