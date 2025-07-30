import pandas as pd
import io

def exceltolist(input_file):
    """reads only first column of Excel file."""
    xls=pd.ExcelFile(input_file)
    sheets=xls.sheet_names
    for sheet in sheets:
        data=pd.read_excel(input_file,sheet_name=sheet)
        data = data.to_dict('list')
    dct = {}
    return data[list(data.keys())[0]]

def file_to_list(file_obj, filename):
    """
    Convert uploaded file (Excel, CSV, TXT) to a list of non-empty values.
    Reads all non-empty cells from all columns.
    
    Args:
        file_obj: Streamlit uploaded file object
        filename: Name of the uploaded file
    
    Returns:
        list: List of non-empty strings from the file
    """
    try:
        if filename.endswith(('.xlsx', '.xls')):
            # Handle Excel files - read all non-empty cells from all columns
            import tempfile
            import os
            
            temp_path = None
            try:
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                    tmp_file.write(file_obj.getbuffer())
                    temp_path = tmp_file.name
                
                # Read Excel file
                df = pd.read_excel(temp_path)
                
                # Extract all non-empty values from all columns
                all_values = []
                for col in df.columns:
                    col_values = df[col].dropna().astype(str).tolist()
                    all_values.extend(col_values)
                
                return [x.strip() for x in all_values if x.strip()]
                
            finally:
                # Clean up temporary file
                if temp_path and os.path.exists(temp_path):
                    try:
                        os.unlink(temp_path)
                    except (PermissionError, OSError):
                        import time
                        time.sleep(0.1)
                        try:
                            os.unlink(temp_path)
                        except:
                            pass
                            
        elif filename.endswith('.csv'):
            # Handle CSV files - read all non-empty cells from all columns
            df = pd.read_csv(io.StringIO(file_obj.getvalue().decode('utf-8')), header=None)
            
            # Extract all non-empty values from all columns
            all_values = []
            for col in df.columns:
                col_values = df[col].dropna().astype(str).tolist()
                all_values.extend(col_values)
            
            return [x.strip() for x in all_values if x.strip()]
            
        elif filename.endswith('.txt'):
            # Handle TXT files - support both comma-separated and line-separated
            content = file_obj.getvalue().decode('utf-8')
            
            if ',' in content:
                # Comma-separated values
                values = [x.strip() for x in content.split(',') if x.strip()]
            else:
                # Line-separated values
                values = [x.strip() for x in content.split('\n') if x.strip()]
            
            return values
            
        else:
            raise ValueError(f"Unsupported file format: {filename}")
            
    except Exception as e:
        raise Exception(f"Error processing file '{filename}': {str(e)}")