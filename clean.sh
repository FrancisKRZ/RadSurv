# Clean cache(s)
rm -r $(find . -type d | grep __pycache__)
# Clean logs
echo "" > log/rfserver.log
echo "" > log/server.log
