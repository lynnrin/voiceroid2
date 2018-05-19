import sys
import pywinauto
import subprocess
from time import sleep

class talkVOICEROID():
    def __init__(self):
        self.__startVOICEROID2()

    def __search_child_byclassname(self, class_name, uiaElementInfo, target_all=False):
        target = []
        for childElement in uiaElementInfo.children():
            if childElement.class_name == class_name:
                if target_all == False:
                    return childElement
                else:
                    target.append(childElement)
        if target_all == False:
            return False
        else:
            return target

    def __search_child_byname(self, name, uiaElementInfo):
        for childElement in uiaElementInfo.children():
            if childElement.name == name:
                return childElement
        return False

    def __startVOICEROID2(self):
        parentUIAElement = pywinauto.uia_element_info.UIAElementInfo()
        if self.__search_child_byname("VOICEROID2", parentUIAElement) == False \
                and self.__search_child_byname("VOICEROID2*", parentUIAElement) == False:
            subprocess.Popen("C:\Program Files (x86)\AHS\VOICEROID2\VoiceroidEditor.exe")
            # 起動完了するまで待つ
            while self.__search_child_byname("VOICEROID2", parentUIAElement) == False:
                sleep(0.1)

    def talkVOICEROID2(self, speakPhrase):
        parentUIAElement = pywinauto.uia_element_info.UIAElementInfo()

        voiceroid2 = self.__search_child_byname("VOICEROID2*", parentUIAElement)
        if voiceroid2 == False:
            voiceroid2 = self.__search_child_byname("VOICEROID2", parentUIAElement)

        TextEditViewElement = self.__search_child_byclassname("TextEditView", voiceroid2)
        textBoxElement = self.__search_child_byclassname("TextBox", TextEditViewElement)

        textBoxEditControl = pywinauto.controls.uia_controls.EditWrapper(textBoxElement)

        textBoxEditControl.set_edit_text(speakPhrase)

        buttonsElement = self.__search_child_byclassname("Button", TextEditViewElement, target_all=True)
        playButtonElement = ""
        for buttonElement in buttonsElement:
            textBlockElement = self.__search_child_byclassname("TextBlock", buttonElement)
            if textBlockElement.name == "再生":
                playButtonElement = buttonElement
                break

        playButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(playButtonElement)

        playButtonControl.click()

        self.__eraseTextEditorView(textBoxEditControl)

    def __eraseTextEditorView(self, textBoxEditControl):
        # textを消す＆終わるまで待つ
        while True:
            try:
                textBoxEditControl.set_edit_text("")
                break
            except:
                sleep(0.2)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        args = sys.argv
        talkVOICEROID().talkVOICEROID2(args[1])

