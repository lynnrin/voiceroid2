import sys
import pywinauto
import subprocess
from time import sleep

def search_child_byclassname(class_name, uiaElementInfo, target_all = False):
    target = []
    # 全ての子要素検索
    for childElement in uiaElementInfo.children():
        # ClassNameの一致確認
        if childElement.class_name == class_name:
            if target_all == False:
                return childElement
            else:
                target.append(childElement)
    if target_all == False:
        # 無かったらFalse
        return False
    else:
        return target


def search_child_byname(name, uiaElementInfo):
    # 全ての子要素検索
    for childElement in uiaElementInfo.children():
        # Nameの一致確認
        if childElement.name == name:
            return childElement
    # 無かったらFalse
    return False


def eraseTextEditorView(textBoxEditControl):
    #textを消す＆終わるまで待つ
    while True:
        try:
            textBoxEditControl.set_edit_text("")
            break
        except:
            sleep(0.2)


def startVOICEROID2():
    parentUIAElement = pywinauto.uia_element_info.UIAElementInfo()
    if search_child_byname("VOICEROID2",parentUIAElement) == False \
            and search_child_byname("VOICEROID2*",parentUIAElement) == False:
        subprocess.Popen("C:\Program Files (x86)\AHS\VOICEROID2\VoiceroidEditor.exe")
        # 起動完了するまで待つ
        while search_child_byname("VOICEROID2",parentUIAElement) == False:
            sleep(0.1)

def talkVOICEROID2(speakPhrase):
    startVOICEROID2()
    # デスクトップのエレメント
    parentUIAElement = pywinauto.uia_element_info.UIAElementInfo()

    voiceroid2 = search_child_byname("VOICEROID2*",parentUIAElement)
    if voiceroid2 == False:
        voiceroid2 = search_child_byname("VOICEROID2",parentUIAElement)

    TextEditViewElement = search_child_byclassname("TextEditView",voiceroid2)
    textBoxElement = search_child_byclassname("TextBox",TextEditViewElement)

    textBoxEditControl = pywinauto.controls.uia_controls.EditWrapper(textBoxElement)

    textBoxEditControl.set_edit_text(speakPhrase)

    buttonsElement = search_child_byclassname("Button",TextEditViewElement,target_all = True)
    playButtonElement = ""
    for buttonElement in buttonsElement:
        # テキストブロックを捜索
        textBlockElement = search_child_byclassname("TextBlock",buttonElement)
        if textBlockElement.name == "再生":
            playButtonElement = buttonElement
            break

    playButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(playButtonElement)

    playButtonControl.click()

    eraseTextEditorView(textBoxEditControl)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        args = sys.argv
        talkVOICEROID2(args[1])