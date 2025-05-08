Step1 先拉最新版本（每次開始前都要）
終端機輸入git pull

Step2 開始coding

Step3 儲存並推送修改：

git add .
git commit -m "說明這次修改了什麼（例如：完成首頁排版）"
git push# ticket-system

## Git
所有操作在終端機執行
### 第一次拉資料夾
```
git clone git@github.com:Aurororara/ticket-system.git
```
### 每次編輯時更新 git
```
git pull origin main
```
### 上 git
`git add .` -> 代表所有檔案都要上傳上去
```
git add .
git commit -m "說明這次修改了什麼（例如：完成首頁排版）"
git push origin main
```

## Python
### 後端 python 安裝套件
```
pip install -r requirements.txt
```

### 執行服務
```
python app.py
```