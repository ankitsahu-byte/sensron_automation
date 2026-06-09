create a vertual env
-------------------
python -m venv {myenv_name}

.\{myenv_name}\Scripts\activate.bat

pip install -r requirements.txt

playwright install

For htmlReport creation
------------------------
pytest tests/ui/test_01_login.py --html=reports/html/login_report.html --self-contained-html
pytest tests/ui/test_02_dashboard.py --html=reports/dashboard_report.html --self-contained-html


For htmlReport creation
------------------------
pytest tests/ui --junitxml=reports/xml/results.xml