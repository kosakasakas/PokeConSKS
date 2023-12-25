#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Direction, Hat, Stick
from Commands.PythonCommandBase import ImageProcPythonCommand
import time

######################################################
#
# SKSBase
# ベースとなる機能ライブラリクラス
# これを継承し、組み合わせて実際のコマンドを作る
#
######################################################
class SKSBase(ImageProcPythonCommand):
    NAME = 'SVベース実装'
    
    def __init__(self, cam):
        super().__init__(cam)
        self.isDebug = True
        self.showNoMatchTemplate = True
        self.showTemplateMatchVal = False
        self.commandWaitTime = 0.02
        self.frameWaitTime = 1.0/30.0

    ######################################################
    # Utility
    ######################################################
    def DoAction(self, cmds):
        for cmd in cmds:
            self.press(cmd, wait=self.commandWaitTime)

    def DoActionUntilMatchTemplate(self, template, useGray, duration, bootCmds, thresholdValue=0.9):
        timeStart = time.time()
        while not self.isContainTemplate(template, threshold=thresholdValue, use_gray=useGray, show_value=self.showTemplateMatchVal):
            self.wait(self.frameWaitTime)
            timeEnd = time.time()
            timeSpend = timeEnd - timeStart
            if timeSpend > duration :
                self.DoAction(bootCmds)
                if self.showNoMatchTemplate:
                    msg = '{:.2f}sマッチしないので再操作. [{}]'.format(timeSpend, template)
                    print(msg)
                timeStart = time.time()
        return True

    def OpenMenu(self):
        self.press(Button.X, wait=1.0)
        self.DoActionUntilMatchTemplate(template='SKS/SV/Common/check_menu.png', duration=1.0, useGray=True, bootCmds = [Button.X])
        return True

    def Test(self):
        if self.OpenMenu():
            self.press(Button.X, wait=1.0)
            print('=========================')
            print('準備完了')
            print('=========================')
        return True

    ######################################################
    # 具体機能実装
    ######################################################
    def SV_DoFlyingTA_Begginer(self):
        n = 0
        c = 0
        while True:
            time_sta = time.time()
            # コース選択までA
            while not self.isContainTemplate('SKS/SV/FlyingTA/select_course_begginer.png', threshold=0.85, use_gray=False, show_value=self.showTemplateMatchVal):
                self.press(Button.A, wait=0.4)
            self.press(Button.A, wait=0.8)
            self.press(Button.A, wait=0.8)
            self.press(Button.A, wait=0.8)
            # タイムアタック開始チェック
            while not self.isContainTemplate('SKS/SV/FlyingTA/timer.png', threshold=0.9, use_gray=True, show_value=self.showTemplateMatchVal):
                self.wait(1.0/30.0)
            self.wait(6.0)
            # ちょい右上
            self.press(Direction(Stick.LEFT, 80), duration=0.8, wait=0.0)
            self.wait(2.5)
            # ちょい左上
            self.press(Direction(Stick.LEFT, 125), duration=2.8, wait=0.0)
            self.wait(4.2)
            # ゴール方向に向きなおす
            self.press(Direction(Stick.LEFT, 0), duration=0.7, wait=0.0)
            self.wait(0.5)
            # ゴールへ降下
            self.press(Direction(Stick.LEFT, -90), duration=0.1, wait=0.0)
            self.wait(18.6)
            # 旋回して無理やりゴールする
            self.press(Direction(Stick.LEFT, 0), duration=1.6, wait=0.1)
            # ゴールポスト手前で旋回してしまった場合の対策としてもっかいゴール目指して曲がる
            self.press(Direction(Stick.LEFT, 180), duration=3.2, wait=0.1)
            # TA終了判定
            while True:
                if self.isContainTemplate('SKS/SV/FlyingTA/clear.png', threshold=0.95, use_gray=True, show_value=self.showTemplateMatchVal):
                    c = c + 1
                    break
                elif self.isContainTemplate('SKS/SV/FlyingTA/fail.png', threshold=0.95, use_gray=True, show_value=self.showTemplateMatchVal):
                    break
            tim = time.time() - time_sta
            n = n + 1
            msg = '{}/{}回クリア {}s {}BP'.format(c,n,tim,10*c)
            print(msg)
        return True

######################################################
# こっからがコマンド
######################################################               
class SKSSV_FlyingTA_BG(SKSBase):
    NAME = 'SKSSV_そらとぶTA_初級'
    def __init__(self, cam):
        super().__init__(cam)
    def do(self):
        if self.Test():
            self.SV_DoFlyingTA_Begginer()
