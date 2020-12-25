# Chapter_Timestamp_Cleanier
```
Inputs a Raw Chapter Timestamps for a seasion txt file and outputs the chapter files as a TXT or XML Chapter File.
```

# Examples:
## Input
### Test Chapter File.txt
```
ep1
11:40
21:09
35:06
2
1140
20:10
30:15
```

## Output
### raw_input_chapter_FIXED Folder
```
EP_1(.txt or .xml) chapter file type
EP_2(.txt or .xml) chapter file type
```

# Output Types
```Both formats where basied for MKVToolNix's supported types```
* TXT output example: [Sources/TXT_OUTPUT.txt](https://github.com/DaringT/Chapter_Timestamp_Cleanier/blob/main/Sources/TXT_OUTPUT.txt)
* XML output example: [Sources/XML_OUTPUT.xml](https://github.com/DaringT/Chapter_Timestamp_Cleanier/blob/main/Sources/XML_OUTPUT.xml)


# Code Examples:
```
f1 = CC(input_file=f, chapter_file_type="txt")
# f1 = CC(input_file=f, chapter_file_type="xml", language="eng")
f1.Create_output_files(output_file=os.getcwd())
```

