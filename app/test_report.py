from report import loadJSON, getTable, getDescription, descriptionToMD

def test_report():
    vulnerabilities = loadJSON("/seed/exploit/test.json")
    assert vulnerabilities == {}