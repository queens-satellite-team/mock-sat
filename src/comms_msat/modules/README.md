### Running the tests
To run the test suite make sure that pytest module is installed. This can be 
done with:
```
pip3 install -U pytest
```
and checking that the insallation was completed successfully:
```
$ pytest --version
pytest 6.2.1
```

The tests are run by calling `pytest`. I like to use the command:
```
clear && pytest -rA
```
which clears the previous output and displays a more detailed log of which
tests passed and what they wrote to standard out.
