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
 
 The output JSON file will be of the following format:
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
