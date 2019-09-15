import re, os, urllib2, sys
from Components.ConfigList import ConfigListScreen, ConfigList
from Components.config import ConfigSubsection, ConfigYesNo, ConfigText, config, configfile
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText
from Components.Label import Label
from Components.Sources.StaticText import StaticText
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor
from enigma import *
from downloader import DownloadSetting, ConverDate
from Components.Console import Console as iConsole
from Components.Harddisk import harddiskmanager
from Tools.Directories import fileExists, pathExists, resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Components.NimManager import nimmanager
from settinglist import *
from restore import *
from history import *
import os
import skin
import base64

config.pud = ConfigSubsection()
config.pud.autocheck = ConfigYesNo(default=False)
config.pud.showmessage = ConfigYesNo(default=True)
config.pud.lastdate = ConfigText(visible_width = 200)
config.pud.satname = ConfigText(visible_width = 200, default='Enigma2 D 19E FTA')
config.pud.update_question = ConfigYesNo(default=False)
config.pud.just_update = ConfigYesNo(default=False)

sorteo = "aHR0cDovL3NwYWluZTItZXh0cmEuZXMvZTJjaGFubmVsL2Rlc2NhcmdhLnBocA=="
URL = base64.decodestring(sorteo)

def chekiptv():
	import ssl
	context = ssl._create_unverified_context()
	url = 'https://raw.githubusercontent.com/jungla-team/satellite/master/streamTDT.tv'
	f = urllib2.urlopen(url,context=context)
	data = f.read()
	if not os.path.exists("/etc/enigma2/streamTDT.tv"):
		chek = 'no tiene lista stream tdt instalada'
	elif os.path.exists("/etc/enigma2/streamTDT.tv"):
		data2 = open("/etc/enigma2/streamTDT.tv", "r").read()
		if data != data2:
			chek = 'Actualizacion stream tdt disponible'
		else:
			chek = 'Su stream tdt esta actualizado'
	return chek


class MenuListSetting(MenuList):

    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        font, size = skin.parameters.get("KoalaIsettingsListFont", ('Regular',25))
        self.l.setFont(0, gFont(font, size))

class koala_Isettings(Screen,ConfigListScreen):

    skin =  """
        <screen name="koala_Isettings" zPosition="2" position="0,0" size="1280,720" title="Plugins" flags="wfNoBorder" backgroundColor="#ff000000">
    <widget source="key_red" render="Label" position="130,387" size="276,30" zPosition="1" font="Regular; 21" halign="left" valign="center" backgroundColor="#00000000" transparent="1" foregroundColor="#00ffffff" noWrap="1" />
 <widget name="MenuListSetting" position="500,130" size="710,315" itemHeight="45" backgroundColorSelected="background" foregroundColorSelected="yellow" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/boton50-fs8.png" scrollbarMode="showOnDemand" transparent="1"/>
<widget source="key_blue" render="Label" position="130,434" size="276,30" zPosition="1" font="Regular; 21" halign="left" valign="center" backgroundColor="#00000000" transparent="1" foregroundColor="#00ffffff" noWrap="1" />
<widget source="key_yellow" render="Label" position="130,481" size="276,30" zPosition="1" font="Regular; 21" halign="left" valign="center" backgroundColor="#00000000" transparent="1" foregroundColor="#00ffffff" noWrap="1" />
<widget source="key_green" render="Label" position="130,528" size="276,30" zPosition="1" font="Regular; 21" halign="left" valign="center" backgroundColor="#00000000" transparent="1" foregroundColor="#00ffffff" noWrap="1" />
<ePixmap name="botonamarillo" position="89,477" size="39,39" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/botamarillo-fs8.png" zPosition="20" />
<ePixmap name="botonverde" position="89,524" size="39,39" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/botverde-fs8.png" zPosition="20" />
<widget source="home" render="Label" position="100,40" size="500,30" zPosition="11" font="Regular; 21" halign="left" valign="center" backgroundColor="#140b1" foregroundColor="white" transparent="1" noWrap="1" />
 <ePixmap name="arriba" position="0,0" size="1280,720" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/windows-fs8.png" zPosition="-5" />
 <ePixmap name="botonrojo" position="89,383" size="39,39" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/botrojo-fs8.png" zPosition="20" />
<ePixmap name="botonazul" position="89,430" size="39,39" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/botazul-fs8.png" zPosition="20" />
<ePixmap name="lateral" position="0,260" size="42,128" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/HasSub.png" zPosition="20" />
    <ePixmap name="fondoazul" position="0,0" size="1280,720" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/fondotv-fs8.png" zPosition="-35" alphatest="blend" />
    <ePixmap name="fondoarriba" position="0,0" size="1280,125" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/infobararriba70-fs8.png" zPosition="-30" alphatest="blend" />
    <ePixmap name="fondoabajo" position="-2,603" size="1280,125" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/fondopie-fs8.png" zPosition="-31" alphatest="blend" />
    <ePixmap name="playpie" position="50,635" size="24,24" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/tv24-fs8.png" zPosition="30" alphatest="blend" />
   <ePixmap name="menu_1" position="400,640" size="30,29" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/key_menu.png" zPosition="30" alphatest="blend" />
  <ePixmap name="menu_2" position="360,640" size="30,29" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/key_info.png" zPosition="30" alphatest="blend" />
<ePixmap name="iconohome" position="50,28" size="40,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/icon_home.png" zPosition="30" alphatest="blend" />
  <ePixmap name="menu_3" position="580,650" size="48,48" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/tdt.png" zPosition="30" alphatest="blend" />
    <widget source="session.CurrentService" render="Label" position="80,633" size="481,32" font="Bold; 20" transparent="1" valign="center" zPosition="11" backgroundColor="#10101010" noWrap="1" halign="left" foregroundColor="#007c8286">
      <convert type="ServiceName">Name</convert>
    </widget>
	<ePixmap name="logo_menu" position="500,330" size="700,204" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/Koala_.png" zPosition="19" />
<widget source="global.CurrentTime" render="Label" position="900,18" size="251,55" backgroundColor="#140b1" foregroundColor="white" transparent="1" zPosition="2" font="Regular;24" valign="center" halign="right" shadowColor="#000000" shadowOffset="-2,-2">
      <convert type="ClockToText">Format:%-H:%M</convert>
    </widget>
<widget source="global.CurrentTime" render="Label" position="900,40" size="300,55" backgroundColor="#140b1" foregroundColor="white" transparent="1" zPosition="2" font="Regular;16" valign="center" halign="right" shadowColor="#000000" shadowOffset="-2,-2">
      <convert type="ClockToText">Date</convert>
    </widget>
    	<widget source="aciptv" render="Label" position="625,635" size="600,60" zPosition="11" font="Regular; 26" halign="left" valign="center" backgroundColor="#10101010" foregroundColor="white" transparent="1" noWrap="1" />
<widget source="Title" render="Label" position="481,96" size="717,32" font="Bold; 24" halign="center" foregroundColor="#00faa900" backgroundColor="#101a2024" transparent="1" noWrap="1" zPosition="12" />
    <eLabel name="marcopip" position="82,117" size="344,186" backgroundColor="#00373737" />
    <widget source="session.VideoPicture" render="Pig" position="83,118" size="342,184" zPosition="50" backgroundColor="#ff000000" />
	            <widget name="description" transparent="1" backgroundColor="#140b1" foregroundColor="yellow" position="500,530" size="660,60" font="Regular;22" halign="center" valign="center" />
            <widget name="update" position="600,55" size="200,25" transparent="1" backgroundColor="#140b1" foregroundColor="white" font="Regular;22" halign="center" valign="center" />
			<widget source="textoupdate" render="Label" transparent="1" backgroundColor="#140b1" foregroundColor="red" position="450,55" size="200,25" font="Regular;22" halign="center" valign="center" />
	</screen>

        """

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self["description"] = Label("description")
        self['MenuListSetting'] = MenuListSetting([])
        self.skinName = "koala_Isettings"
        self.setup_title = _("Listas Canales by jungle-team")
        self.setTitle(self.setup_title)
        self["description"] = Label(_("Lista Instalada") + ":" + "n/a")
        self["update"] = Label(_("disabled"))


        self["key_red"] = StaticText(_("Exit"))
        self["key_green"] = StaticText(_("Install"))
        self["key_blue"] = StaticText(_("Koala InfoPanel"))
        self["key_yellow"] = StaticText(_("AutoUpdate"))
        self["textoupdate"] = StaticText(_("AutoUpdate:"))
        self["home"] = StaticText(_("Koala ISettings - Menu Principal"))
        self["aciptv"] = StaticText(_("Check Iptv: %s") % chekiptv())



        self["ColorActions"] = ActionMap(['OkCancelActions', 'MenuActions', 'ShortcutActions',"ColorActions","InfobarEPGActions"],
            {
            "red": self.keyCancel,
            "green": self.keyOk,
            "yellow" : self.keyAutoUpdate,
            "blue" : self.keyinfopanel,
            "cancel" : self.keyCancel,
            "ok" : self.keyOk,
            "menu" : self.keyMenu,
            "InfoPressed" : self.keyHistory,
            })

        self.List = DownloadSetting(URL)
        self.SettingsMenu()
        self.onShown.append(self.Info)
        config.pud.showmessage.value = True

    def keyMenu(self):
        if os.path.exists(Directory + '/Settings/enigma2'):
            self.session.open(koala_Restore)

    def keyinfopanel(self):
		self.session.open(koalaInfopanel)    

    def keyHistory(self):
        self.session.open(Koala_History)

    def keyCancel(self):
        configfile.save()
        self.close()

    def keyAutoUpdate(self):
        iTimerClass.StopTimer()
        if config.pud.autocheck.value and config.pud.just_update.value:
            self['update'].setText(_("disabled"))
            config.pud.autocheck.value = False
        else:
            if config.pud.just_update.value:
                self['update'].setText(_("enabled"))
                config.pud.just_update.value = False               
            else:
                self['update'].setText(_("update"))
                config.pud.just_update.value = True 
            if config.pud.lastdate.value == '':
                self.session.open(MessageBox, _('No se ha encontrado instalacion canales instalada !!\n\nPor favor instale una de las listas'), MessageBox.TYPE_INFO, timeout=15)
            config.pud.autocheck.value = True
            iTimerClass.TimerSetting()
        
        config.pud.save()

    def keyOk(self):
        self.name = self['MenuListSetting'].getCurrent()[0][3]
        self.date = self['MenuListSetting'].getCurrent()[0][4]
        self.link = self['MenuListSetting'].getCurrent()[0][2]
        self.session.openWithCallback(self.CBselect, MessageBox, _('Lista Canales Seleccionada:\n\nVersion: %s\nDate: %s\n\nEstas seguro de instalar esta lista canales?') % (self.name, self.date), MessageBox.TYPE_YESNO)

    def CBselect(self, req):
        if req:
            iTimerClass.startDownload(self.name, self.link, self.date)
        

    def Info(self):
        if not os.path.exists(Directory + '/Settings/enigma2'):
            os.system('mkdir -p ' + Directory + '/Settings/enigma2')

        if config.pud.autocheck.value:
            if config.pud.just_update.value:
                self['update'].setText(_("update"))
            else:
                self['update'].setText(_("enabled"))
        else:
            self['update'].setText(_("disabled"))
        if config.pud.lastdate.value == '':
            self["description"].setText(_("Lista Instalada") + ":" + "n/a")
        else:
            self["description"].setText(_("Lista Instalada") + ":" + config.pud.satname.value + " " + config.pud.lastdate.value)

    def ListEntryMenuSettings(self, name, date, link, name1, date1):
        res = [(name, date, link, name1, date1)]
        try:
            x, y, w1, w2, h = skin.parameters.get("KoalaIsettingsList", (15,7,420,210,40))
        except ValueError:
            x, y, w1, w2, h = (15,7,420,210,40)
        res.append(MultiContentEntryText(pos=(x, y), size=(w1, h), font=0, text=name, flags=RT_HALIGN_LEFT))
        res.append(MultiContentEntryText(pos=(x+w1, y), size=(w2, h), font=0, color=16777215, text=date1, flags=RT_HALIGN_RIGHT))
        res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=link, flags=RT_HALIGN_LEFT))
        res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=name1, flags=RT_HALIGN_LEFT))
        res.append(MultiContentEntryText(pos=(0, 0), size=(0, 0), font=0, text=date, flags=RT_HALIGN_LEFT))
        return res

    def SettingsMenu(self):
        self.listB = []        
        for date, name, link in self.List:
            self.listB.append(self.ListEntryMenuSettings(str(name.title()), str(date), str(link), str(name), ConverDate(str(date))))
        if not self.listB:
            self.listB.append(self.ListEntryMenuSettings(_('Servidor caido'), '', '', '', ''))
        self['MenuListSetting'].setList(self.listB)

jsession = None

######################################################################################
class koalaInfopanel(Screen):

	skin = """
<screen name="koalaInfopanel" zPosition="2" position="0,0" size="1280,720" title="Plugins" flags="wfNoBorder" backgroundColor="#ff000000">
    <widget source="key_red" render="Label" position="130,387" size="276,30" zPosition="1" font="Regular; 21" halign="left" valign="center" backgroundColor="#00000000" transparent="1" foregroundColor="#00ffffff" noWrap="1" />
<widget source="key_blue" render="Label" position="130,434" size="276,30" zPosition="1" font="Regular; 21" halign="left" valign="center" backgroundColor="#00000000" transparent="1" foregroundColor="#00ffffff" noWrap="1" />
<ePixmap name="botonazul" position="89,430" size="39,39" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/botazul-fs8.png" zPosition="20" />
<widget source="key_yellow" render="Label" position="130,481" size="276,30" zPosition="1" font="Regular; 21" halign="left" valign="center" backgroundColor="#00000000" transparent="1" foregroundColor="#00ffffff" noWrap="1" />
<ePixmap name="botonamarillo" position="89,477" size="39,39" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/botamarillo-fs8.png" zPosition="20" />
<widget source="key_green" render="Label" position="130,527" size="276,30" zPosition="1" font="Regular; 21" halign="left" valign="center" backgroundColor="#00000000" transparent="1" foregroundColor="#00ffffff" noWrap="1" />
<ePixmap name="botonverde" position="89,524" size="39,39" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/botverde-fs8.png" zPosition="20" />
 <ePixmap name="arriba" position="0,0" size="1280,720" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/windows-fs8.png" zPosition="-5" />
<widget source="homeinfo" render="Label" position="100,40" size="500,30" zPosition="11" font="Regular; 21" halign="left" valign="center" backgroundColor="#140b1" foregroundColor="white" transparent="1" noWrap="1" />
 <ePixmap name="botonrojo" position="89,383" size="39,39" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/botrojo-fs8.png" zPosition="20" />
<ePixmap name="lateral" position="0,260" size="42,128" alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/HasSub.png" zPosition="20" />
    <ePixmap name="fondoazul" position="0,0" size="1280,720" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/fondotv-fs8.png" zPosition="-35" alphatest="blend" />
    <ePixmap name="fondoarriba" position="0,0" size="1280,125" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/infobararriba70-fs8.png" zPosition="-30" alphatest="blend" />
    <ePixmap name="fondoabajo" position="-2,603" size="1280,125" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/fondopie-fs8.png" zPosition="-31" alphatest="blend" />
<ePixmap name="iconoinfo" position="50,28" size="40,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/icon_info.png" zPosition="30" alphatest="blend" />
    <ePixmap name="playpie" position="50,635" size="24,24" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/tv24-fs8.png" zPosition="30" alphatest="blend" />
<widget source="global.CurrentTime" render="Label" position="900,18" size="251,55" backgroundColor="#140b1" foregroundColor="white" transparent="1" zPosition="2" font="Regular;24" valign="center" halign="right" shadowColor="#000000" shadowOffset="-2,-2">
      <convert type="ClockToText">Format:%-H:%M</convert>
    </widget>
<widget source="global.CurrentTime" render="Label" position="900,40" size="300,55" backgroundColor="#140b1" foregroundColor="white" transparent="1" zPosition="2" font="Regular;16" valign="center" halign="right" shadowColor="#000000" shadowOffset="-2,-2">
      <convert type="ClockToText">Date</convert>
    </widget>
    <widget source="session.CurrentService" render="Label" position="80,633" size="481,32" font="Bold; 20" transparent="1" valign="center" zPosition="11" backgroundColor="#10101010" noWrap="1" halign="left" foregroundColor="#007c8286">
      <convert type="ServiceName">Name</convert>
    </widget>
<widget source="Title" render="Label" position="481,96" size="717,32" font="Bold; 24" halign="center" foregroundColor="#00faa900" backgroundColor="#101a2024" transparent="1" noWrap="1" zPosition="12" />
    <eLabel name="marcopip" position="82,117" size="344,186" backgroundColor="#00373737" />
    <widget source="session.VideoPicture" render="Pig" position="83,118" size="342,184" zPosition="50" backgroundColor="#ff000000" />
	<widget source="CPULabel" render="Label" position="460,160" zPosition="2" size="180,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#03307dc3" transparent="1" />
	<widget source="CPU" render="Label" position="675,160" zPosition="2" size="390,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="MemoryLabel" render="Label" position="540,500" size="150,22" font="Regular; 20" halign="right" backgroundColor="background" foregroundColor="#03307dc3" transparent="1" />
	<widget source="publicidad" render="Label" position="670,635" size="600,60" zPosition="11" font="Regular; 26" halign="left" valign="center" backgroundColor="#10101010" foregroundColor="white" transparent="1" noWrap="1" />
	<widget source="SwapLabel" render="Label" position="540,524" size="150,22" font="Regular; 20" halign="right" backgroundColor="background" foregroundColor="#03307dc3" transparent="1" />
	<widget source="FlashLabel" render="Label" position="540,548" size="150,22" font="Regular; 20" halign="right" backgroundColor="background" foregroundColor="#03307dc3" transparent="1" />
	<widget source="memTotal" render="Label" position="700,500" zPosition="2" size="420,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="swapTotal" render="Label" position="700,524" zPosition="2" size="420,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="flashTotal" render="Label" position="700,548" zPosition="2" size="420,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="device" render="Label" position="540,430" zPosition="2" size="580,66" font="Regular;20" halign="left" valign="top" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="Hardware" render="Label" position="675,135" zPosition="2" size="390,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="ipLabel" render="Label" position="460,185" zPosition="2" size="180,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#03307dc3" transparent="1" />
	<widget source="ipInfo" render="Label" position="675,185" zPosition="2" size="390,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="macLabel" render="Label" position="460,210" zPosition="2" size="180,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#03307dc3" transparent="1" />
	<widget source="macInfo" render="Label" position="675,210" zPosition="2" size="390,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="Image" render="Label" position="675,235" zPosition="2" size="390,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="Kernel" render="Label" position="675,270" zPosition="2" size="390,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="HardwareLabel" render="Label" position="460,135" zPosition="2" size="180,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#03307dc3" transparent="1" />
	<widget source="ImageLabel" render="Label" position="460,235" zPosition="2" size="180,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#03307dc3" transparent="1" />
	<widget source="KernelLabel" render="Label" position="460,270" zPosition="2" size="180,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#03307dc3" transparent="1" />
	<widget source="nim" render="Label" position="550,340" zPosition="2" size="580,70" font="Regular;20" halign="left" valign="top" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="driver" render="Label" position="675,295" zPosition="2" size="390,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="driverLabel" render="Label" position="460,295" zPosition="2" size="180,22" font="Regular;20" halign="right" valign="center" backgroundColor="background" foregroundColor="#03307dc3" transparent="1" />
<ePixmap name="menu_3" position="320,640" size="30,29" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/key_1.png" zPosition="30" alphatest="blend" />
<ePixmap name="menu_4" position="360,640" size="30,29" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/key_2.png" zPosition="30" alphatest="blend" />
<ePixmap name="menu_4" position="400,640" size="30,29" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/koala_Isettings/confluence/menu/key_3.png" zPosition="30" alphatest="blend" />


			
</screen>"""
	
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.skinName = "koalaInfopanel"
		self.setTitle(_("Koala Info Panel"))
		self.iConsole = iConsole()
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions", "NumberActions"],
		{
			"cancel": self.cancel,
			"back": self.cancel,
			"red": self.cancel,
			"blue": self.koalaippublica,
			"yellow": self.koalalibmemoria,
			"green": self.koalaresetpass,
			"1": self.koalasatelite,
			"2": self.koalaiptv,
			"3": self.serviceapptest,
			"ok": self.cancel,
			})
		self["homeinfo"] = StaticText(_("Koala Isettings- Panel Info"))
		self["publicidad"] = StaticText(_("Soporte by jungle-team.com"))
		self["key_red"] = StaticText(_("Cerrar"))
		self["key_blue"] = StaticText(_("IP Publica"))
		self["key_yellow"] = StaticText(_("Liberar Memoria"))
		self["key_green"] = StaticText(_("Resetear Password"))
		self["MemoryLabel"] = StaticText(_("Memoria:"))
		self["SwapLabel"] = StaticText(_("Swap:"))
		self["FlashLabel"] = StaticText(_("Flash:"))
		self["memTotal"] = StaticText()
		self["swapTotal"] = StaticText()
		self["flashTotal"] = StaticText()
		self["device"] = StaticText()
		self["Hardware"] = StaticText()
		self["Image"] = StaticText()
		self["CPULabel"] = StaticText(_("Procesador:"))
		self["CPU"] = StaticText()
		self["Kernel"] = StaticText()
		self["nim"] = StaticText()
		self["ipLabel"] = StaticText(_("Interna IP:"))
		self["ipInfo"] = StaticText()
		self["macLabel"] = StaticText(_("MAC (lan/wlan):"))
		self["macInfo"] = StaticText()
		self["EnigmaVersion"] = StaticText()
		self["HardwareLabel"] = StaticText(_("Hardware:"))
		self["ImageLabel"] = StaticText(_("Imagen:"))
		self["KernelLabel"] = StaticText(_("Kernel Version:"))
		self["EnigmaVersionLabel"] = StaticText(_("Last Upgrade:"))
		self["driver"] = StaticText()
		self["driverLabel"] = StaticText(_("Driver Version:"))
		self.memInfo()
		self.FlashMem()
		self.devices()
		self.mainInfo()
		self.cpuinfo()
		self.network_info()

    	def koalaippublica(self):
		os.popen("wget -qO /tmp/.mostrarip http://icanhazip.com/")
		f = open("/tmp/.mostrarip")
		mostrarip = f.readline()
		f.close()
		self.mbox = self.session.open(MessageBox,_("Mi IP Publica: %s") % (mostrarip), MessageBox.TYPE_INFO, timeout = 10 )

	def koalalibmemoria(self):
		os.system("sync ; echo 3 > /proc/sys/vm/drop_caches")
		os.system("free | awk '/Mem:/ {print int(100*$4/$2) ;}' >/tmp/.memory")
		f = open("/tmp/.memory")
		mused = f.readline()
		f.close()
		self.mbox = self.session.open(MessageBox,_("Porcentaje Memoria libre despues de la ejecucion: %s ") % (mused), MessageBox.TYPE_INFO, timeout = 20 )

	def koalaresetpass(self):
		os.system("passwd -d root")
		self.mbox = self.session.open(MessageBox,_("Tu Password ha sido borrada"), MessageBox.TYPE_INFO, timeout = 10 )

	def koalasatelite(self):
		nuevo = "/etc/tuxbox/satellites.xml"
		copia = "/etc/tuxbox/satellites.xml.old"
		os.rename(nuevo, copia)
		url = 'https://raw.githubusercontent.com/jungla-team/satellite/master/satellites.xml'
		f = urllib2.urlopen(url)
		data = f.read()
		with open("/etc/tuxbox/satellites.xml", "wb") as code:
			code.write(data)
		self.mbox = self.session.open(MessageBox,_("Satellite.xml ha sido actualizado"), MessageBox.TYPE_INFO, timeout = 10 )
		
	def serviceapptest(self):
		service = os.system('opkg list-installed | grep serviceapp')
		if service !=0:
			os.system('opkg update && opkg install enigma2-plugin-systemplugins-serviceapp')
			self.mbox = self.session.open(MessageBox,_("Se procede a instalar serviceapp"), MessageBox.TYPE_INFO, timeout = 10 )
		else:
			self.mbox = self.session.open(MessageBox,_("Ya tienes serviceapp instalado"), MessageBox.TYPE_INFO, timeout = 10 )	
		
	def koalaiptv(self):
		url = 'https://raw.githubusercontent.com/jungla-team/satellite/master/streamTDT.tv'
		f = urllib2.urlopen(url)
		data = f.read()
		with open("/etc/enigma2/streamTDT.tv", "wb") as code:
			code.write(data)
			
		myfile = open("/etc/enigma2/bouquets.tv",'r')
		find="0"
		for line in myfile:
			if line.find('streamTDT.tv') >= 0:
				find=line
				
		myfile.close()
		if (find != "0"):
			self.strReplace('/etc/enigma2/bouquets.tv', find, '#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "streamTDT.tv" ORDER BY bouquet')
		else:
			myfile = open ("/etc/enigma2/bouquets.tv", "a")
			myfile.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "streamTDT.tv" ORDER BY bouquet\n')
			myfile.close()
			eDVBDB.getInstance().reloadServicelist()
			eDVBDB.getInstance().reloadBouquets()
		self.mbox = self.session.open(MessageBox,_("instalado favorito iptv"), MessageBox.TYPE_INFO, timeout = 10 )
		
	def strReplace(self, file, search, replace):
		with open(file,'r') as f:
			newlines = []
			for line in f.readlines():
				newlines.append(line.replace(search, replace))
		with open(file, 'w') as f:
			for line in newlines:
				f.write(line)
		
	def network_info(self):
		self.iConsole.ePopen("ifconfig -a", self.network_result)
		
	def network_result(self, result, retval, extra_args):
		if retval is 0:
			ip = ''
			mac = []
			if len(result) > 0:
				for line in result.splitlines(True):
					if 'HWaddr' in line:
						mac.append('%s' % line.split()[-1].strip('\n'))
					elif 'inet addr:' in line and 'Bcast:' in line:
						ip = line.split()[1].split(':')[-1]
				self["macInfo"].text = '/'.join(mac)
			else:
				self["macInfo"].text =  _("unknown")
		else:
			self["macInfo"].text =  _("unknown")
		if ip is not '':
			self["ipInfo"].text = ip
		else:
			self["ipInfo"].text = _("unknown")


		
	def cpuinfo(self):
		if fileExists("/proc/cpuinfo"):
			cpu_count = 0
			processor = cpu_speed = cpu_family = cpu_variant = temp = ''
			core = _("core")
			cores = _("cores")
			for line in open('/proc/cpuinfo'):
				if "system type" in line:
					processor = line.split(':')[-1].split()[0].strip().strip('\n')
				elif "cpu MHz" in line:
					cpu_speed =  line.split(':')[-1].strip().strip('\n')
					#cpu_count += 1
				elif "cpu type" in line:
					processor = line.split(':')[-1].strip().strip('\n')
				elif "model name" in line:
					processor = line.split(':')[-1].strip().strip('\n').replace('Processor ', '')
				elif "cpu family" in line:
					cpu_family = line.split(':')[-1].strip().strip('\n')
				elif "cpu variant" in line:
					cpu_variant = line.split(':')[-1].strip().strip('\n')
				elif line.startswith('processor'):
					cpu_count += 1
			if not cpu_speed:
				try:
					cpu_speed = int(open("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq").read()) / 1000
				except:
					cpu_speed = '-'
			if fileExists("/proc/stb/sensors/temp0/value") and fileExists("/proc/stb/sensors/temp0/unit"):
				temp = "%s%s%s" % (open("/proc/stb/sensors/temp0/value").read().strip('\n'), unichr(176).encode("latin-1"), open("/proc/stb/sensors/temp0/unit").read().strip('\n'))
			elif fileExists("/proc/stb/fp/temp_sensor_avs"):
				temp = "%s%sC" % (open("/proc/stb/fp/temp_sensor_avs").read().strip('\n'), unichr(176).encode("latin-1"))
			if cpu_variant is '':
				#self["CPU"].text = _("%s, %s Mhz (%d %s) %s") % (processor, cpu_speed[:-1], cpu_count, cpu_count > 1 and cores or core, temp)
				self["CPU"].text = _("%s, %s Mhz (%d %s) %s") % (processor, cpu_speed, cpu_count, cpu_count > 1 and cores or core, temp)
			else:
				self["CPU"].text = "%s(%s), %s %s" % (processor, cpu_family, cpu_variant, temp)
		else:
			self["CPU"].text = _("undefined")

	def status(self):
		status = ''
		if fileExists("/usr/lib/opkg/status"):
			status = "/usr/lib/opkg/status"
		elif fileExists("/usr/lib/ipkg/status"):
			status = "/usr/lib/ipkg/status"
		elif fileExists("/var/lib/opkg/status"):
			status = "/var/lib/opkg/status"
		elif fileExists("/var/opkg/status"):
			status = "/var/opkg/status"
		return status
		
			
	def devices(self):
		list = ""
		hddlist = harddiskmanager.HDDList()
		hddinfo = ""
		if hddlist:
			for count in range(len(hddlist)):
				hdd = hddlist[count][1]
				if int(hdd.free()) > 1024:
					list += ((_("%s  %s  (%d.%03d GB free)\n") % (hdd.model(), hdd.capacity(), hdd.free()/1024 , hdd.free()%1024)))
				else:
					list += ((_("%s  %s  (%03d MB free)\n") % (hdd.model(), hdd.capacity(),hdd.free())))
		else:
			hddinfo = _("none")
		self["device"].text = list
		
	def HardWareType(self):
		if os.path.isfile("/proc/stb/info/boxtype"):
			return open("/proc/stb/info/boxtype").read().strip().upper()
		if os.path.isfile("/proc/stb/info/vumodel"):
			return "VU+" + open("/proc/stb/info/vumodel").read().strip().upper()
		if os.path.isfile("/proc/stb/info/model"):
			return open("/proc/stb/info/model").read().strip().upper()
		return _("unavailable")
		
	def getImageTypeString(self):
		try:
			if os.path.isfile("/etc/issue"):
				for line in open("/etc/issue"):
					if not line.startswith('Welcom') and '\l' in line:
						return line.capitalize().replace('\n', ' ').replace('\l', ' ').strip()
		except:
			pass
		return _("undefined")
		
	def getKernelVersionString(self):
		try:
			return open("/proc/version").read().split()[2]
		except:
			return _("unknown")
			
	def getImageVersionString(self):
		try:
			if os.path.isfile('/var/lib/opkg/status'):
				st = os.stat('/var/lib/opkg/status')
			elif os.path.isfile('/usr/lib/ipkg/status'):
				st = os.stat('/usr/lib/ipkg/status')
			elif os.path.isfile('/usr/lib/opkg/status'):
				st = os.stat('/usr/lib/opkg/status')
			elif os.path.isfile('/var/opkg/status'):
				st = os.stat('/var/opkg/status')
			tm = time.localtime(st.st_mtime)
			if tm.tm_year >= 2011:
				return time.strftime("%Y-%m-%d %H:%M:%S", tm)
		except:
			pass
		return _("unavailable")
		
	def listnims(self):
		tuner_name = {'0':'Tuner A:', '1':'Tuner B:', '2':'Tuner C:', '3':'Tuner D:', '4':'Tuner E:', '5':'Tuner F:', '6':'Tuner G:', '7':'Tuner H:', '8':'Tuner I:', '9':'Tuner J:'}
		nimlist = ''
		if fileExists("/proc/bus/nim_sockets"):
			for line in open("/proc/bus/nim_sockets"):
				if 'NIM Socket' in line:
					nimlist += tuner_name[line.split()[-1].replace(':', '')] + ' '
				elif 'Type:' in line:
					nimlist += '(%s)' % line.split()[-1].replace('\n', '').strip() + ' '
				elif 'Name:' in line:
					nimlist += '%s' % line.split(':')[1].replace('\n', '').strip() + '\n'
			return nimlist
		else:
			return _("unavailable")
			
	def mainInfo(self):
		package = 0
		self["Hardware"].text = self.HardWareType()
		self["Image"].text = self.getImageTypeString()
		self["Kernel"].text = self.getKernelVersionString()
		self["EnigmaVersion"].text = self.getImageVersionString()
		self["nim"].text = self.listnims()
		if fileExists(self.status()):
			for line in open(self.status()):
				if "-dvb-modules" in line and "Package:" in line:
					package = 1
				elif "kernel-module-player2" in line and "Package:" in line:
					package = 1
				elif "formuler-dvb-modules" in line and "Package:" in line:
					package = 1
				elif "vuplus-dvb-proxy-vusolo4k" in line and "Package:" in line:
					package = 1
				if "Version:" in line and package == 1:
					package = 0
					self["driver"].text = line.split()[-1]
					break

	def memInfo(self):
		for line in open("/proc/meminfo"):
			if "MemTotal:" in line:
				memtotal = line.split()[1]
			elif "MemFree:" in line:
				memfree = line.split()[1]
			elif "SwapTotal:" in line:
				swaptotal =  line.split()[1]
			elif "SwapFree:" in line:
				swapfree = line.split()[1]
		self["memTotal"].text = _("Total: %s Kb  Free: %s Kb") % (memtotal, memfree)
		self["swapTotal"].text = _("Total: %s Kb  Free: %s Kb") % (swaptotal, swapfree)
		
	def FlashMem(self):
		size = avail = 0
		st = os.statvfs("/")
		avail = st.f_bsize * st.f_bavail / 1024
		size = st.f_bsize * st.f_blocks / 1024
		self["flashTotal"].text = _("Total: %s Kb  Free: %s Kb") % (size , avail)
		
			
	def cancel(self):
		self.close()
#############################################################

def SessionStart(reason, **kwargs):
    if reason == 0:
        iTimerClass.gotSession(kwargs['session'], URL)
    jsession = kwargs['session']

iTimerClass = CheckTimer(jsession)

def AutoStart(reason, **kwargs):
    if reason == 1:
        iTimerClass.StopTimer()

def Main(session, **kwargs):
    session.open(koala_Isettings)

def Plugins(**kwargs):
    if nimmanager.hasNimType("DVB-S"):
        return [
            PluginDescriptor(name=_("Koala Isettings"), description=_("Instala lista canales jungle-team.com"), icon="plugin.png", where=PluginDescriptor.WHERE_PLUGINMENU, fnc=Main),
            PluginDescriptor(where=PluginDescriptor.WHERE_SESSIONSTART, fnc=SessionStart),
            PluginDescriptor(where=PluginDescriptor.WHERE_AUTOSTART, fnc=AutoStart)]
    else:
        return []
