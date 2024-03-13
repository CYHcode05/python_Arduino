from serial import Serial
import time # time 모듈을 수입: 시간 관련 함수의 집합체
import psycopg2
import statistics as stat
import matplotlib.pyplot as plt
import pandas as pd

class PythonHub:
    __defComName = 'COM3'
    __defComBps = 9600
    __defWaitTime = 0.5

    
    def waitSerial(): # self가 없음 -> 클래스의 정적(static) 멤버: 인스턴스 멤버에 접근하지 않음
        time.sleep(PythonHub.__defWaitTime) # 단위: 초; 클래스 멤버에 접근할 때는 클래스명.(PythonHub.)
    def wait(delaySec):
        time.sleep(delaySec)

    # 생성자(constructor): 이름은 __init__로 고정
    def __init__(self, comName = __defComName, comBps = __defComBps): # comName: Serial 이름, comBps: Serial 속도
        #print('생성자 호출됨')
        # 멤버 변수 생성: 변수를 선언하지 않고 self.으로 변수를 추가; self는 클래스(PythonHub)로 만든 인스턴스에 접근하기 위한 키워드
        # Serial 클래스의 인스턴스 생성 -> self.ard에 할당
        self.ard = Serial(comName, comBps) # C++ 경우: Serial ard;
        self.clearSerial() # Serial 입력 버퍼 초기화
    # 소멸자(destructor): 이름은 __del__으로 고정
        self.volts = ()  # volts 속성 초기화
        self.voltTimes = ()  # voltTimes 속성 초기화
        self.lights = () # lights 속성 초기화
        self.lightsteps = () # lightsteps 속성 초기화
        self.lightTimes = () # lightTimes 속성 초기화
        self.conn = None # conn 속성 초기화
        self.cur = None # cur 속성 초기화
        self.sum = 0 # sum 속성 초기화
        self.variances = 0  # variances 속성 초기화
    
    def __del__(self):
        if self.ard.isOpen(): # Serial이 열려(open)있는가?
            self.ard.close() # Serial을 닫음(close)
        
         # Serial 메소드(멤버 함수)
    def writeSerial(self, sCmd): # 인스턴스 접근하기 위한 self 추가
        btCmd = sCmd.encode()
        nWrite = self.ard.write(btCmd) # 인스턴스의 멤버인 ard에 접근: self.ard
        self.ard.flush()
        return nWrite
    
    def readSerial(self):
        nRead = self.ard.in_waiting
        if nRead > 0:
            btRead = self.ard.read(nRead)
            sRead = btRead.decode()
            return sRead
        else: return ''

    def clearSerial(self): # Serial 버퍼를 비우는 메소드
        PythonHub.waitSerial()
        self.readSerial()
    
    def talk(self, sCmd):
        return self.writeSerial(sCmd + '\n')
    
    def listen(self):
        PythonHub.waitSerial() # 클래스의 정적 멤버인 waitSerial() 호출
        sRead = self.readSerial()
        return sRead.strip()
    
    def talkListen(self, sCmd):
        self.talk(sCmd)
        return self.listen()
    
#----------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------
    # db의 관련된 함수들
    def conncetdb(self):
        self.conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='2023', port='5432')
        self.cur = self.conn.cursor()
    
    def closedb(self):
        self.cur.close()
        self.conn.close()

    def writeDb(self, cmd): # DB에 명령어 cmd 쓰기
        sCmd = str(cmd) # string으로 type casting
        self.cur.execute(sCmd) # cursor에 명령어(SQL) 실행
        self.conn.commit() # connection에 기록하기 -> cursor 명령어를 DB가 수행

#-------------------------------------------------------------------------------------------------------------------
# 통계 관련 함수들(평균, 분산, 표준편차)

    def mean(self, *values):
        for value in values:
            self.sum += value
        return self.sum/len(values)
    
    def variance(self, *values):
        mean = self.mean(*values)
        for value in values:
            self.variances += (value - mean)**2
        return self.variances/len(values)

    def stdev(self, *values):
        return self.variance(*values)**0.5
    

#-------------------------------------------------------------------------------------
    #전압과 관련된 함수들
    
    def getVolt(self):
        try:
            sVolt = self.talkListen('get volt')
            volt = float(sVolt)
            return volt 
        except:
            print('getVolt() 오류')
            return -1
        
    # 전압에 대한 튜플 함수
    def printVoltsTuple(self):
        for(volt, measTime) in zip(self.volts, self.voltTimes):
            print(f'volt: {volt}, @ time: {time.ctime(measTime)}')
    
    def sampleVoltTuple(self, nCount, ndelay):
        self.volts = ()
        self.voltTimes = ()
        Count = int(nCount)
        delay = float(ndelay)
        for i in range(Count):
            volt = self.getVolt()
            measTime = time.time()
            self.volts += (volt,)
            self.voltTimes += (measTime,)
            PythonHub.wait(delay)
        return self.volts, self.voltTimes
    
    def addvoltToTuple(self):
        volt = self.getVolt()
        measTime = time.time() #현재 시간 읽기: 에포크 타임(기원후 시간: epoch time)
        if volt >= 0:
            self.volts += (volt,) # 튜플은 한 번 생성되면 크기 변경 불가
            self.voltTimes += (measTime,)
            return True
        else:
            return False # 측정 실패

    def clearVoltTuple(self):
        self.volts = () # 현재 변수를 튜플로 초기화
        self.voltTimes = ()
        
    # 전압에 대한 DB 함수

    def countvoltTable(self):
        self.conncetdb()
        self.cur.execute("SELECT COUNT(*) FROM volt_table")
        ncount = self.cur.fetchone()[0]
        self.closedb
        return ncount

    def insertVoltTable(self):
        volt = self.getVolt()
        meastime = time.time()
        self.conncetdb()
        if volt >= 0:
            self.writeDb(f'INSERT INTO volt_table(meas_time, volt) VALUES({meastime}, {volt})')
            self.closedb()
            return True
        else:
            print('insertVoltTable() 오류')
            return False
        
    def clearVoltTable(self):
        self.conncetdb()
        self.writeDb("TRUNCATE TABLE volt_table")
        self.closedb()
       
    def saveVoltTupleToTable(self):# volts, voltTimes 튜플을 DB에 저장; volts, voltTimes는 clear
        self.conncetdb()
        for i in range(len(self.volts)):
            self.writeDb(f'INSERT INTO volt_table(meas_time, volt) VALUES({self.voltTimes[i]}, {self.volts[i]})')
        self.clearVoltTuple()
        self.closedb()
        return self.volts, self.voltTimes

    def loadVoltTableToTuple(self):
        self.conncetdb()
        self.writeDb("SELECT * FROM volt_table")
        result = self.cur.fetchall()
        for i in range(len(result)):
            self.voltTimes += (result[i][0],)
            self.volts += (result[i][1],)
        self.closedb()
        return self.volts, self.voltTimes

    # 전압에 대한 통계 함수
    def getVoltMean(self):
        return stat.mean(self.volts)
    
    def getVoltVariance(self):
        return stat.variance(self.volts)
    
    def getVoltStdev(self):
        return stat.stdev(self.volts)
    
    # 전압에 대한 그래프 함수

    def plotVolt(self):
        plt.plot(self.voltTimes, self.volts)
        plt.show()

    #pandas를 이용한 volt 통계
    def describeVoltTable(self):
        self.conncetdb()
        self.writeDb("SELECT volt FROM volt_table")
        result = self.cur.fetchall()

        df = pd.DataFrame(result, columns = ['Volt'])
        self.closedb()
        self.voltcount = df.shape[0]
        self.voltmean = df['Volt'].mean().item()
        self.voltstd = df['Volt'].std().item()
        self.voltvar = df['Volt'].var().item()
        self.voltmedian = df['Volt'].median().item()
        return self.voltcount, self.voltmean, self.voltstd, self.voltvar, self.voltmedian
    
#-------------------------------------------------------------------------------------------------
# 조도와 관련된 함수들

    def getLight(self):
        try:
            sLight = self.talkListen('get light')
            light = str(sLight)
            return light

        except:
            print('getLight() 오류')
            return -1
    
    def getLightstep(self):
        try:
            sLightstep = self.talkListen('get lightstep')
            lightstep = int(sLightstep)
            return lightstep

        except:
            print('getLightstep() 오류')
            return -1
        
    # 조도에 대한 튜플 함수

    def addlightToTuple(self):
        light = self.getLight()
        lightstep = self.getLightstep()
        measTime = time.time()
        if light >= 0:
            self.lights += (light,)
            self.lightsteps += (lightstep,)
            self.lightTimes += (measTime,)
            return True
        else:
            return False
        
    def samplelightTuple(self, nCount, ndelay):
        self.lights = ()
        self.lightsteps = ()
        self.lightTimes = ()
        Count = int(nCount)
        delay = float(ndelay)
        for i in range(Count):
            light = self.getLight()
            lightstep = self.getLightstep()
            measTime = time.time()
            self.lights += (light,)
            self.lightsteps += (lightstep,)
            self.lightTimes += (measTime,)
            PythonHub.wait(delay)
        return self.lightTimes, self.lights, self.lightsteps
    
    def clearlightTuple(self):
        self.lights = ()
        self.lightsteps = ()
        self.lightTimes = ()

    # 조도에 대한 DB 함수
    def countlightTable(self):
        self.conncetdb()
        self.cur.execute("SELECT COUNT(*) FROM light_table")
        ncount = self.cur.fetchone()[0]
        self.closedb
        return ncount
    
    def insertlightTable(self):
        light = self.getLight()
        lightstep = self.getLightstep()
        meastime = time.time()
        self.conncetdb()
        if lightstep >= 0:
            self.writeDb(f"INSERT INTO light_table(meas_time, light, light_step) VALUES({meastime}, '{light}', {lightstep})")
            self.closedb()
            return True
        else:
            print('insertlightTable() 오류')
            return False
        
    def clearlightTable(self):
        self.conncetdb()
        self.writeDb("TRUNCATE TABLE light_table")
        self.closedb()
    
    def saveLightTupleIntoTable(self):
        self.conncetdb()
        for i in range(len(self.lights)):
            self.writeDb(f"INSERT INTO light_table(meas_time, light, light_step) VALUES({self.lightTimes[i]}, '{self.lights[i]}', {self.lightsteps[i]})")
        self.clearlightTuple()
        self.closedb()
        return self.lightTimes, self.lights, self.lightsteps
        

    def loadLightTableToTuple(self):
        self.conncetdb()
        self.writeDb("SELECT * FROM light_table")
        result = self.cur.fetchall()
        for i in range(len(result)):
            self.lightTimes += (result[i][0],)
            self.lights += (result[i][1],)
            self.lightsteps += (result[i][2],)
        self.closedb()
        return self.lightTimes, self.lights, self.lightsteps   
    
    # 조도에 대한 통계 함수
    def getLightMean(self):
        return stat.mean(self.lightsteps)
    
    def getLightVariance(self):
        return stat.variance(self.lightsteps)
    
    def getLightStdev(self):
        return stat.stdev(self.lightsteps)
    
    # 조도에 대한 그래프 함수
    def plotLight(self):
        plt.plot(self.lightTimes, self.lightsteps)
        plt.show()

    #pandas를 이용한 light 통계
    def describeLightTable(self):
        self.conncetdb()
        self.writeDb("SELECT light_step FROM light_table")
        result = self.cur.fetchall()

        df = pd.DataFrame(result, columns = ['Light'])
        self.closedb()
        self.lightcount = df.shape[0]
        self.lightmean = df['Light'].mean().item()
        self.lightstd = df['Light'].std().item()
        self.lightvar = df['Light'].var().item()
        self.lightmedian = df['Light'].median().item()
        return self.lightcount, self.lightmean, self.lightstd, self.lightvar, self.lightmedian
    
#-------------------------------------------------------------------------------------------------
    #servo와 관련된 함수들
    def setServo(self,ang):
        try:
            nAng = int(ang)
            nAng = str(nAng)
            self.talk('set servo ' + nAng)

        except:
            print('setServo() 오류') 
            return -1

#-------------------------------------------------------------------------------------------------
    #led와 관련된 함수들
    def setLedColor(self, color):
        try:
            nColor = str(color)
            self.talk('set led ' + nColor)

        except:
            print('setLedColor() 오류')
            return -1

#-------------------------------------------------------------------------------------------------
    #buzzer와 관련된 함수들
    def setBuzzerNote(self, note, delay): # 부저 음정을 note로 설정하고 delay만큼 울림
        try:
            sNote = str(note)
            nDelay = int(delay)
            self.talk(f'set buzzer {sNote} {nDelay}')
        except:
            print('부저 설정 오류')

#-------------------------------------------------------------------------------------------------
    #html과 관련된 함수들
    def writeHtmlVoltTuple(self):
        html = '<table width="100%" border="1"><thead><tr><th>번호</th><th>전압 측정값</th><th>측정 일시</th></tr></thead>'
        i = 1
        for (volt, voltTime) in zip(self.volts, self.voltTimes):
            html += f'<tr><td>{i}</td><td>{volt} V</td><td>{time.ctime(voltTime)}</td></tr>'
            i += 1
        html += '</table>'
        return html
    
    def writeHtmlLightTuple(self):
        html = '<table width="100%" border="1"><thead><tr><th>번호</th><th>조도</th><th>조도 측정값</th><th>측정 일시</th></tr></thead>'
        i = 1
        for (light, lightstep ,lightTime) in zip(self.lights ,self.lightsteps, self.lightTimes):
            html += f'<tr><td>{i}</td><td>{light}</td><td>{lightstep}</td><td>{time.ctime(lightTime)}</td></tr>'
            i += 1
        html += '</table>'
        return html