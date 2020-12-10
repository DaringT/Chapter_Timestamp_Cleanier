# Chapter_Timestamp_Cleanier
Timestamp_Chapter_Cleaner_Creator

Inputs a Raw Chapter Timestamps for a seasion txt file and outputs the chapter files as a TXT or XML Chapter File.

#Examples:
Input
  raw_input_chapter.txt
    ep1
    11:40
    21:09
    35:06

    ep2
    11:40
    20:10
    30:15
    
Output
  raw_input_chapter_FIXED Folder
    # Sources/TXT_OUTPUT.txt
    EP_1(.txt or .xml) chapter file type
    EP_2(.txt or .xml) chapter file type
    .
    .

Both formats where basied for MKVToolNix 
  TXT Format
    https://github.com/DaringT/Chapter_Timestamp_Cleanier/blob/main/Sources/TXT_OUTPUT.txt

  XML Format
    https://github.com/DaringT/Chapter_Timestamp_Cleanier/blob/main/Sources/XML_OUTPUT.xml

#Code Examples:
  f1 = CC(input_file=f, chapter_file_type="txt")
  # f1 = CC(input_file=f, chapter_file_type="xml", language="eng")
  f1.Create_output_files(output_file=os.getcwd())
  
  
