import re
import os

##################################################################################################################################
# 																 #
#							   Chapter Cleaner V1 							 #
#												Created By: Daren Thoman 	 #
##################################################################################################################################


class CC:
    """
The Class CC Cleans a Raw Text files
That Have a Sieres of Chapter Timestamps  with a Episode # At The top
Example:
    ep1 or EP1 or Ep1 or 1
    2302 or 23:02
    23:94
    The Patern Repets

Parameters:
            input_file:
                    input_file is where the raw chapter ts text file goes
            ts_list:
                    ts_list is used for just using make_xml & make_txt functions
            chapter_file_type:
                    Used to select the chapter timestamp file type
    Functions:
            ts(Input_Timestamp)
            ep(Input_Episode)
            Input_anything(Input)
            make_xml(self, output_file=None, TS_Language="eng")
            make_txt(self, output_file=None)
            CoreV2(self)
            Create_output_files(self)"""

    def __init__(self, input_file, ts_list=None, chapter_file_type="txt"):
        self.input_file = input_file
		if input_file != None and os.path.exists(input_file) is False:
            raise FileNotFoundError
        self.ts_list = ts_list
        # xml and txt
        self.chapter_file_type = chapter_file_type

        # if self.chapter_file_type != "txt" or "xml":
        # 	raise ValueError("invalid mode: chapter_file_type is not: txt, xml")

    def ts(Input_Timestamp):
        """
        Returns a found Timestamp  using regex else None

        Paramiters:
                        Input_Timestamp (str)
        """
        Min = Sec = Mil = None

        ts_regex = r"(?P<Min>^\d\d?)[:| ]?(?P<Sec>\d\d)(.(?P<Mil>\d\d?))?"
        ts_prog = re.compile(ts_regex)
        ts_result = ts_prog .match(Input_Timestamp)

        try:
            Min = ts_result.group("Min")
            Sec = ts_result.group("Sec")
            Mil = ts_result.group("Mil")
        except AttributeError:
            pass

        if Min and Sec and Mil:
            Mil = Mil.ljust(3, '0')
            Min = Min.rjust(2, '0')
            return ('00:%s:%s.%s' % (Min, Sec, Mil))

        elif Min and Sec:
            Min = Min.ljust(2, '0')
            return ('00:%s:%s.000' % (Min, Sec))
        else:
            return None

    def ep(Input_Episode):
        """Returns a found Episode number using regex else None
                Paramiters:
                        Input_Episode (str)
                Returns:
                        "Ep_##" (str) else: None
        """

        EP_State = gr_three = gr_six = gr_four = None

        ep_regex = r'((ep|Ep|EP)(\d\d?))?(^\d\d?$)?([D|d]\w[\s|:](\d\d?))?'
        ep_prog = re.compile(ep_regex)
        ep_result = ep_prog.match(Input_Episode)
        try:
            gr_four = ep_result.group(4)
            gr_three = ep_result.group(3)
            gr_six = ep_result.group(6)
        except AttributeError:
            pass

        if gr_four or gr_three or gr_six:
            if gr_four == None:
                pass
            else:
                EP_State = ('Ep_%s' % (gr_four))
            if gr_three == None:
                pass
            else:
                EP_State = ('Ep_%s' % (gr_three))
            if gr_six == None:
                pass
            else:
                EP_State = ('Ep_%s' % (gr_six))
        else:
            EP_State = None
        return EP_State

    def Input_anything(Input):
        """Returns if the input is a TS. or EP. or neither and cleans it with ts() or ep()
                Paramiters:
                        Input (str)
                Returns:
                        State:
                                "EP" (str) or "TS" (str) or None
                        if a TS or EP Returns Result:
                                Result of ep() or ts() else None
        """
        r_ep = CC.ep(Input)
        r_ts = CC.ts(Input)
        if type(r_ep) == str:
            State = 'EP'
            return State, r_ep
        elif type(r_ts) == str:
            State = 'TS'
            return State, r_ts
        else:
            return None, None

    def make_xml(self, output_file=None, language="eng"):
        """Turns a List into a XML Chapter File
                Paramiters:
                        output_file=None:
                                outputs the TXT File if used alone you input CC(ts_list=input_list_here)
        """
        from xml.dom import minidom

        if output_file == None or False:
            print("WARNING! make_xml is not outputing to file.")

        root = minidom.Document()
        Chapters = root.createElement('Chapters')
        root.appendChild(Chapters)

        EditionEntry = root.createElement("EditionEntry")
        Chapters.appendChild(EditionEntry)

        for index, ts in enumerate(self.ts_list):
            ChapterAtom = root.createElement("ChapterAtom")
            EditionEntry.appendChild(ChapterAtom)

            ChapterTimeStart = root.createElement("ChapterTimeStart")
            ChapterTimeStart.appendChild(root.createTextNode(ts))
            ChapterAtom.appendChild(ChapterTimeStart)

            try:
                ChapterTimeEnd = root.createElement("ChapterTimeEnd")
                ChapterTimeEnd.appendChild(
                    root.createTextNode(self.ts_list[index + 1]))
                ChapterAtom.appendChild(ChapterTimeEnd)
            except IndexError:
                pass

            ChapterDisplay = root.createElement("ChapterDisplay")
            ChapterAtom.appendChild(ChapterDisplay)

            ChapterString = root.createElement("ChapterString")
            ChapterString.appendChild(
                root.createTextNode(f"Chapter {index + 1:02}"))
            ChapterDisplay.appendChild(ChapterString)

            ChapterLanguage = root.createElement("ChapterLanguage")
            ChapterLanguage.appendChild(root.createTextNode(language))
            ChapterDisplay.appendChild(ChapterLanguage)

        xml_str = root.toprettyxml(indent="  ")
        print(xml_str, file=output_file)

    def make_txt(self, output_file=None):
        """Turns a List into a XML Chapter File
                Paramiters:
                        output_file=None:
                                outputs the TXT File if used alone you input CC(ts_list=input_list_here)
        """

        if output_file == None or False:
            print("Xml is not writing to FILE!\n\n\n")

        i = -1
        L = len(self.ts_list)
        Chapter_number = 0
        for line in self.ts_list:
            Chapter_number = Chapter_number + 1
            Chapter_number2 = str(Chapter_number)
            Chapter_number2 = Chapter_number2.zfill(2)

            i = i + 1
            test = f"Chapter {Chapter_number2}"

            if L - 1 == i:
                test = "Ending"

            if test == "Chapter 01":
                test = "Intro"

            Formarted_Body = f"CHAPTER{Chapter_number2}={self.ts_list[i]}\nCHAPTER{Chapter_number2}NAME={test}"

            print(Formarted_Body, file=output_file)

    def CoreV2(self):
        """This Function does the created naming of the files"""

        exten = self.chapter_file_type
        self.ts_list = []
        with open(self.input_file, 'r') as File:
            for line in File:
                State, Temp = CC.Input_anything(line)
                if State == 'EP':
                    if self.ts_list > []:
                        print(self.ts_list)
                        if exten == "txt":
                            CC.make_txt(self, output_file=ep_f)
                        elif exten == "xml":
                            CC.make_xml(self, output_file=ep_f)
                        ep_f.close()

                    print(f"Creating: {Temp}.{exten}")
                    ep_f = open(f"{Temp}.{exten}", "w")

                    self.ts_list = list()
                elif State == 'TS':
                    self.ts_list.append(Temp)
                else:
                    pass
            print(self.ts_list)
            if exten == "txt":
                CC.make_txt(self, output_file=ep_f)
            elif exten == "xml":
                CC.make_xml(self, output_file=ep_f)

    def Create_output_files(self, output_file=None):
        """This the Main function creates the output folder
                Paramiters:
                        output_file="C:\\Users\\Username\\Documents\\"
                                is were the folder will output to
        """
        if output_file is None:
            output_file = os.path.join(
                os.path.expanduser("~"), "\\Documents\\")

        # Takes the path off the File.
        striped_file = os.path.basename(self.input_file)
        title, exten = striped_file.split('.')
        output_folder_name = title + "_Split & Cleaned"
        output_folderpath = os.path.join(output_file, output_folder_name)

        if os.path.exists(output_folderpath):
    		print('WARNING!: this output folder: ',
                  output_folderpath, 'already Exist\n')
			raise FileExistsError
	else:
		os.mkdir(output_folderpath)

        print(striped_file)
        print(output_folderpath)
        os.chdir(output_folderpath)
        CC.CoreV2(self)
        os.startfile(output_folderpath)


if __name__ == '__main__':
    f = os.path.join(os.getcwd(), "Sources\\Test Chapter File.txt")
    # Timestamps = ["00:11:11.000", "00:22:00.000", "00:33:00.000", "00:44:00.000", "00:55:00.000"]
    print("input file:", f)
    f1 = CC(input_file=f, chapter_file_type="txt")
    f1.Create_output_files(output_file=os.getcwd())
    # with open(f, "r") as file:
    # print(file.readline())
