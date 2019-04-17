import os
import hou
from PySide2 import QtCore, QtUiTools, QtWidgets

class lipSync(QtWidgets.QWidget):
    def __init__(self):
        super(lipSync, self).__init__()
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        
        # Connect to UI from QtDesigner
        ui_file = '{}/ui_lipSync.ui'.format(os.environ['TOOLBAR_PATH'])
        self.ui = QtUiTools.QUiLoader().load(ui_file, self)
        
        # Add functionality to the file selector
        audioFld = self.ui.audioPathField
        audioBtn = self.ui.audioBrowseBtn
        audioBtn.clicked.connect(lambda: audioFld.setText(hou.ui.selectFile()))
        phoneFld = self.ui.phonemesPathField
        phoneBtn = self.ui.phonemesBrowseBtn
        phoneBtn.clicked.connect(lambda: phoneFld.setText(hou.ui.selectFile()))
        
        # Create CHOP Network on click
        self.ui.createNetBtn.clicked.connect(self.createNetwork)
    
    
    def createNetwork(self):          
        # Voice CHOP Network
        voiceChopnet = hou.node('/obj/').createNode('chopnet', 'voice')
        
        # Phonemes audio source for making a phoneme library
        phonemes = voiceChopnet.createNode('file', 'phonemes')
        # Convert to mono
        delete1 = voiceChopnet.createNode('delete')
        delete1.setParms({'delscope': 'chan1'})
        delete1.setInput(0, phonemes)
        # Node for reducing sample rate
        resample1 = voiceChopnet.createNode('resample')
        resample1.setInput(0, delete1)
        
        # Split voiced and non-voiced channels
        voiceSplit = voiceChopnet.createNode('voicesplit')
        voiceSplit.setInput(0, resample1)
        # Node for getting voiced channels
        voiced = voiceChopnet.createNode('delete', 'voiced')
        voiced.setInput(0, voiceSplit)
        # Node for getting non-voiced channels
        nonVoiced = voiceChopnet.createNode('delete', 'non_voiced')
        nonVoiced.setParms({'discard': 1}) # Non-Scoped Channels
        nonVoiced.setInput(0, voiceSplit)
        
        # Node for getting source audio
        audioIn = voiceChopnet.createNode('file', 'audio_in')
        # Convert to mono
        delete2 = voiceChopnet.createNode('delete')
        delete2.setParms({'delscope': 'chan1'})
        delete2.setInput(0, audioIn)
        # Node for reducing sample rate
        resample2 = voiceChopnet.createNode('resample')
        resample2.setInput(0, delete2)
        
        # Match phonemes with channels in phoneme library
        voiceSync = voiceChopnet.createNode('voicesync')
        voiceSync.setInput(0, resample2)
        voiceSync.setInput(1, voiced)
        voiceSync.setInput(2, nonVoiced)
        
        # Filter for smoothening the discrete signals
        filter = voiceChopnet.createNode('filter')
        filter.setInput(0, voiceSync)
        
        # Connect to the blend SOPs of the face rig
        rename = voiceChopnet.createNode('rename', 'to_SOPs')
        rename.setInput(0, filter)
        rename.setExportFlag(True)
        
        # Pack arguments in a tuple
        # NOTE: Order of nodes is important!
        nodes = (phonemes, resample1, voiceSplit, resample2, voiced, nonVoiced,
                 audioIn, filter, rename)
        
        # Set parmeters from UI
        self.updateParms(*nodes)
        
        # Connect the Update Button for future updates
        self.ui.updateParmsBtn.clicked.connect(lambda: self.updateParms(*nodes))
        
        def moveAllToGoodPosition(root):
            """Recursively apply moveToGoodPosition() to all nodes in a network"""
            for child in root.children():
                child.moveToGoodPosition()
                moveAllToGoodPosition(child)
        # Organize nodes
        moveAllToGoodPosition(hou.node('/obj'))


    def updateParms(self, phonemes, resample1, voiceSplit, resample2, voiced,
                    nonVoiced, audioIn, filter, rename):
        # Create simple Rig
        if self.ui.useSimplemale.isChecked():
            simpleMale = hou.node('/obj/').createNode('simplemale')
        
        # Set parameters from UI
        phonemes.setParms({'file': self.ui.phonemesPathField.text()})
        resample1.setParms({'rate': self.ui.audioSampleRate.value()})
        voiceSplit.setParms({
            'sillevel': self.ui.silLevel.value(),
            'names': self.ui.phonemeChannels.text()
        })
        resample2.setParms({'rate': self.ui.audioSampleRate.value()})
        voiced.setParms({'delscope': self.ui.nonVoicedPhonemes.text()})
        nonVoiced.setParms({'delscope': self.ui.nonVoicedPhonemes.text()})
        audioIn.setParms({'file': self.ui.audioPathField.text()})
        filter.setParms({'width': self.ui.filterWidth.value()})
        rename.setParms({'renameto': self.ui.targetBlendChannels.text()})


def run():
    win = lipSync()
    win.show()
