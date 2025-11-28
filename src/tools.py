import os

class Tools:  
    def get_current_path():
        """Hàm lấy thư mục hiện tại
        """
        current_dir = os.getcwd()
        return current_dir
    
    def get_excel_in_dir(directory):
        """Hàm lấy tất cả tên file excel trong một thư mục
        """
        excel_files = [f for f in os.listdir(directory) if f.endswith(('.xlsx', '.xls'))]
        return excel_files
    
    def get_path_excel_in_dir(directory):
        """Hàm lấy tất cả đường dẫn file excel trong một thư mục
        """
        path_excel_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(('.xlsx', '.xls'))]
        return path_excel_files
    
    def get_xml_in_dir(directory):
        """Hàm lấy tất cả tên file xml trong một thư mục
        """
        xml_files = [f for f in os.listdir(directory) if f.endswith(('.xml'))]
        return xml_files
    
    def get_path_xml_in_dir(directory):
        """Hàm lấy tất cả đường dẫn file xml trong một thư mục
        """
        path_xml_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(('.xml'))]
        return path_xml_files