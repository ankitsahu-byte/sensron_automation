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
pytest tests/ui --html=reports/html/results.html --self-contained-html
pytest tests/ui/test_network_config.py --html=reports/html/network_config.html -v -s
pytest tests/ui/test_das_interrogator_page.py -v -s
pytest tests/ui/test_configuration_database_page.py -v -s
pytest tests/ui/test_anomoly_server_page.py -v -s
pytest tests/ui/test_das_interrogator_page.py --html=reports/html/das_interrogator_report.html -v -s

For htmlReport creation
------------------------
pytest tests/ui --junitxml=reports/xml/results.xml

To find the locator
------------------
playwright codegen http://10.101.54.90:4200/home/dashboard