# Chạy ứng dụng

## Cách đơn giản nhất trên Windows

Chạy file `run_app.bat` ở thư mục gốc của project bằng cách nhấp đúp vào file
trong File Explorer.

Hoặc mở PowerShell tại thư mục gốc của project và chạy:

```powershell
.\run_app.bat
```

Không chạy file này bằng nút **Run Python File** trong VS Code. File `.bat` là
file lệnh Windows, không phải file Python; nếu chạy bằng Python sẽ xuất hiện
lỗi `SyntaxError: invalid syntax` tại dòng `@echo off`.

File này tự động:

1. Tìm thư mục ứng dụng tương đối theo vị trí của chính nó.
2. Tạo môi trường Python `.venv` nếu chưa có.
3. Cài các thư viện trong `requirements.txt`.
4. Khởi động ứng dụng Streamlit.

Vì dùng đường dẫn tương đối, người khác có thể tải hoặc clone toàn bộ project
vào bất kỳ thư mục nào rồi chạy `run_app.bat`.

## Điều kiện

Máy cần cài Python 3 và chọn **Add Python to PATH** khi cài đặt. Có thể tải
Python tại <https://www.python.org/downloads/>.

## Chạy thủ công

```powershell
cd "matlab1\colour_science_uyen_thy"
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run "Khoa_hoc_Mau_sac.py"
```
