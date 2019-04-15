This repo details an API that receives requests in the form of JSON files containing a URL and a token, and returns a JSON file containing a count of the number of times that token appears in the text from the URL.

The input JSON file format is:
```
{
  "url":"foo.com",
  "word":"bar"
 }
 ```
 
 To execute the program, call it from the command line like this:
 ```
 > python wordcount.py somefile.json
 ```
 
 The output JSON file will open in port 5002 in the following format:
 ```
 {
  "status":"OK",
  "count":"1"
 }
 ```
 
 In the event that the program is unable to execute properly, it will give the following output:
  ```
 {
  "status":"FAIL - [description of error]",
  "count":""
 }
 ```
 
 The folder "test" contains the unit tests (tests.py) I wrote to check wordcount.py. The folder "data" contains the various JSON files I used in tests.py. To run those tests, execute this command:
 ```
 > python tests.py
 ```
