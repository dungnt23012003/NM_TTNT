# NM_TTNT

1. Cài đặt Miniconda (https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html) tải chỗ Dowload the installer rồi chạy file
   * chú ý từ giờ có 2 cái khác nhau: anaconda command != command prompt
  vào anaconda command = thanh tìm kiếm, cài đặt anaconda navigation bằng câu lệnh:
            conda install anaconda-navigator
     gặp câu hỏi proceed ([y]/n) thì chọn y
   
3. Kết nối Miniconda với VS Code (https://saturncloud.io/blog/activating-anaconda-environment-in-vscode-a-guide-for-data-scientists/)
   + TH nếu làm bước 5 hiện lỗi đỏ thì:
     - (https://stackoverflow.com/questions/44515769/conda-is-not-recognized-as-internal-or-external-command)
     - ở bước add new path thì thêm lần lượt các path lần lượt là các câu lệnh sinh ra từ bước 'where conda' ở phía trên nhưng bỏ đi \ cuối
     - ví dụ ở bước where conda hiện ra dòng C:\Users\Admin\miniconda3\condabin\conda.bat thì lúc thêm new path ở bước 6 thì chỉ thêm
                                             C:\Users\Admin\miniconda3\condabin
    + sau khi thay đổi environment variables thì tắt vscode đi bật lại.
   
5.  Cài package Shapely bằng conda:
   Mở anaconda command gõ lệnh           conda install -c anaconda shapely
  proceed([y]/n)? chọn y

7. Cài một số package khác = requirement.txt
   + yêu cầu có file requirement.txt (mới đẩy lên github) trên máy cá nhân
   + tìm file geos_c.dll trên máy, copy paste vào mục C:\Users\Admin\miniconda3\Library\lib
   + tìm file requirement.txt trên máy cá nhân và copy đường dẫn tới file này, giả sử là "C:\Users\Admin\Desktop\requirements3.txt"
   + mở anaconda command gõ 2 lệnh:
       - conda install pip
       - pip install -r C:\Users\Admin\Desktop\requirements3.txt

8. Kiểm tra
   Vào lại VSCode, mở terminal = Ctrl + `.
   Chú ý đã chọn conda làm interpreter của chương trình, theo bước 1 mục 3.
   gõ lệnh conda list thấy có đủ các package đã cài trong file requirement + Shapely là xong.  
                                
9. Bo sung PyQt6 cho GUI moi
      pip install PyQt6
