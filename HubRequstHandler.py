from http.server import SimpleHTTPRequestHandler
import time
from urllib import parse

class HubRequestHandler(SimpleHTTPRequestHandler): # SimpleHTTPRequestHandler를 상속받아 HubRequestHandler 클래스를 구현
    def do_GET(self):
        print(self.path)
        result = parse.urlsplit(self.path)
        if result.path == '/': self.writeHome() # 홈
        elif result.path == '/meas_one_volt': self.writeMeasOneVolt() 
        elif result.path == '/sample_volt': self.writeSampleVolt(result.query)
        elif result.path == '/meas_one_light': self.writeMeasOneLight()
        elif result.path == '/sample_light': self.writeSampleLight(result.query)
        elif result.path == '/serveo_move_0': self.writeServeoMove(0)
        elif result.path == '/serveo_move_90': self.writeServeoMove(90)
        elif result.path == '/serveo_move_180': self.writeServeoMove(180)
        elif result.path == '/serveo_move': self.writeSampleServeoMove(result.query)
        elif result.path == '/led': self.writeLedOn(result.query)
        elif result.path == '/buzeer': self.writeBuzeerOn(result.query)
        else: self.writeNotFound() # 404 에러
    
    def writeHead(self, nStatus): # response의 header
        self.send_response(nStatus)
        self.send_header('content-type', 'text/html') # 속성(attribute), 값 순으로 입력
        self.end_headers()
    
    def writeHtml(self, html):
        self.wfile.write(html.encode()) # html(유니코드) -> 바이트로 변경(encode() 함수 역할)
    
    def writeHome(self): # 홈용 HTLM을 쓰기
        self.writeHead(200) # 200: 성공
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>Python Web Server</title>'
        html += '<style>'
        html += 'body { background-color: #f5f5f5; font-family: "Arial", sans-serif; }'
        html += 'h3 { color: #333;}'
        html += 'a { color: #007bff; text-decoration: none; }'
        html += 'a:hover { color: #0056b3; }'  
        html += '</style>'
        html += '</head><body>'
        html += '<div style="margin-bottom: 20px;">'
        html += '<p><h6>작성자: 추영호</h6></p></div>'
        html += '<p> 이 홈페이지는 아두이노와 Pyhton을 이용하여 IOT를 실습을 위한 것입니다</p>'
        html += '<div><img src="data:image/png;base64,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"></div>'
        html += '<p> 아래의 링크를 클릭하여 각각의 기능을 사용할 수 있습니다.</p>'
        html += '<div style="display:inline-block; margin-right: 20px; border: 1px solid #000; padding: 10px; border-color: #ff0000;">'
        html += '<p><h3>전압 센서 제어</h3></p>'
        html += '<p><a href="/meas_one_volt">한번 전압 측정</a></p>'
        html += '<form action="/sample_volt" method="get">'
        html += '<p>측정 횟수: <input type="text" name="count"></p>'
        html += '<p>측정 간격: <input type="text" name="delay"></p>'
        html += '<p><input type="submit" value="전압 측정"></p>'
        html += '</form></div>'
        html += '<div style="display:inline-block; margin-right: 20px; border: 1px solid #000; padding: 10px; border-color: #ffa500;">'
        html += '<p><h3>조도 센서 제어</h3></p>'
        html += '<p><a href="/meas_one_light">한번 조도 측정</a></p>'
        html += '<form action="/sample_light" method="get">'
        html += '<p>측정 횟수: <input type="text" name="count"></p>'
        html += '<p>측정 간격: <input type="text" name="delay"></p>'
        html += '<p><input type="submit" value="조도 측정"></p>'
        html += '</form></div>'
        html += '<div style="display:inline-block; margin-right: 20px; border: 1px solid #000; padding: 10px; border-color: #00ff00;">'
        html += '<p><h3>모터 제어</h3></p>'
        html += '<p><a href="/serveo_move_0">모터 0도로 이동</a></p>'
        html += '<p><a href="/serveo_move_90">모터 90도로 이동</a></p>'
        html += '<p><a href="/serveo_move_180">모터 180도로 이동</a></p>'
        html += '<form action="/serveo_move" method="get">'
        html += '<p>모터 각도: <input type="text" name="ang"></p>'
        html += '<p><input type="submit" value="모터 이동"></p>'
        html += '</form></div>'
        html += '<div style="display:inline-block; margin-right: 20px; border: 1px solid #000; padding: 10px; border-color: #0000ff;">'
        html += '<p><h3>led 제어</h3></p>'
        html += '<form action="/led" method="get">'
        html += '<p>led 색상: <input type="text" name="led"></p>'
        html += '<p><input type="submit" value="led 제어"></p>'
        html += '</form></div>'
        html += '<div style="display:inline-block; margin-right: 20px; border: 1px solid #000; padding: 10px;">'
        html += '<p><h3>buzeer 제어</h3></p>'
        html += '<form action="/buzeer" method="get">'
        html += '<p>buzeer 음: <input type="text" name="buzeer"></p>'
        html += '<p>buzeer 시간: <input type="text" name="delay"></p>'
        html += '<p><input type="submit" value="buzeer 제어"></p>'
        html += '</form></div>'
        html += '</body></html>'
        self.writeHtml(html)

    def writeNotFound(self):
        self.writeHead(404)
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>페이지 없음</title>'
        html += '</head><body>'
        html += '<div><p><h1>페이지를 찾을 수 없습니다.</hl></p>'
        html += f'<div><h3>{self.path}에 대한 페이지는 존재하지 않습니다</h3></div>'
        html += '</body></html>'
        self.writeHtml(html)
#-----------------------------------------------------------------------------------------------------------------'
# 전압 측정을 보여주는 html
    def writeMeasOneVolt(self):
        self.writeHead(200)
        bresult = self.server.gateway.insertVoltTable()
        nMeasCount, voltmean, voltstd, voltvar, voltmedian = self.server.gateway.describeVoltTable()
        self.server.gateway.clearVoltTuple()
        self.server.gateway.loadVoltTableToTuple()
        ntime = time.time()
        if bresult: sResult = '성공'
        else: sResult = '실패'
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>writeMeasOneVolt</title>'
        html += '</head><body>'
        html += '<a href="/">홈으로</a>'
        html += f'<div>측정시간: {time.ctime(ntime)} </div>'
        html += f'<div>측정전압: {sResult} </div>'
        html += f'<div>테이블 정보: {nMeasCount} </div>'
        html += f'<div>평균:{voltmean}, 분산:{voltvar}, 표준편차:{voltstd}, 중앙값:{voltmedian} </div>'
        html += self.server.gateway.writeHtmlVoltTuple()
        html += '</body></html>'
        self.writeHtml(html)

    def writeSampleVolt(self, qs):
        self.writeHead(200) 
        qdict = parse.parse_qs(qs)
        Count = int(qdict['count'][0])
        delay = float(qdict['delay'][0]) 
        nTime = time.time()
        bresult = self.server.gateway.insertVoltTable()
        self.server.gateway.clearVoltTuple()
        self.server.gateway.sampleVoltTuple(Count, delay)
        self.server.gateway.saveVoltTupleToTable()
        self.server.gateway.loadVoltTableToTuple()
        nMeasCount, voltmean, voltstd, voltvar, voltmedian = self.server.gateway.describeVoltTable()
        if bresult: sResult = '성공'
        else: sResult = '실패'
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>전압 여러번 측정</title>'
        html += '</head><body>'
        html += '<a href="/">홈으로</a>'
        html += f'<div><h5>측정 시간: {time.ctime(nTime)}</h5></div>'
        html += f'<div><h5>측정 횟수: {Count}</h5></div>'
        html += f'<div><p>전압 측정이 {sResult}했습니다.</p>'
        html += f'<p>현재까지 {nMeasCount}번 측정했습니다.</div>'
        html += f'<div>평균:{voltmean}, 분산:{voltvar}, 표준편차:{voltstd}, 중앙값:{voltmedian} </div>'
        html += self.server.gateway.writeHtmlVoltTuple()
        html += '</body></html>'
        self.writeHtml(html)
#-----------------------------------------------------------------------------------------------------------------'
# 조도 센서 제어를 보여주는 html
    def writeMeasOneLight(self):
        self.writeHead(200)
        bresult = self.server.gateway.insertlightTable()
        lightcount, lightmean, lightstd, lightvar, lightmedian = self.server.gateway.describeLightTable()
        self.server.gateway.clearlightTuple()
        self.server.gateway.loadLightTableToTuple()
        ntime = time.time()
        if bresult: sResult = '성공'
        else: sResult = '실패'
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>writeMeasOneVolt</title>'
        html += '</head><body>'
        html += '<a href="/">홈으로</a>'
        html += f'<div>측정시간: {time.ctime(ntime)} </div>'
        html += f'<div>측정 조도: {sResult} </div>'
        html += f'<div>테이블 정보: {lightcount} </div>'
        html += f'<div>평균:{lightmean}, 분산:{lightvar}, 표준편차:{lightstd}, 중앙값:{lightmedian} </div>'
        html += self.server.gateway.writeHtmlLightTuple()
        html += '</body></html>'
        self.writeHtml(html)

    def writeSampleLight(self, qs):
        self.writeHead(200) 
        qdict = parse.parse_qs(qs)
        Count = int(qdict['count'][0])
        delay = float(qdict['delay'][0]) 
        nTime = time.time()
        bresult = self.server.gateway.insertlightTable()
        self.server.gateway.clearlightTuple()
        self.server.gateway.samplelightTuple(Count, delay)
        self.server.gateway.saveLightTupleIntoTable()
        self.server.gateway.loadLightTableToTuple()
        lightcount, lightmean, lightstd, lightvar, lightmedian = self.server.gateway.describeLightTable()
        if bresult: sResult = '성공'
        else: sResult = '실패'
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>조도 센서 여러번 측정</title>'
        html += '</head><body>'
        html += '<a href="/">홈으로</a>'
        html += f'<div><h5>측정 시간: {time.ctime(nTime)}</h5></div>'
        html += f'<div><h5>측정 횟수: {Count}</h5></div>'
        html += f'<div><p>조도 측정이 {sResult}했습니다.</p>'
        html += f'<p>현재까지 {lightcount}번 측정했습니다.</div>'
        html += f'<div>평균:{lightmean}, 분산:{lightvar}, 표준편차:{lightstd}, 중앙값:{lightmedian} </div>'
        html += self.server.gateway.writeHtmlLightTuple()
        html += '</body></html>'
        self.writeHtml(html)

#-----------------------------------------------------------------------------------------------------------------'
# 모터 제어를 보여주는 html
    def writeServeoMove(self, ang):
        self.writeHead(200)
        self.server.gateway.setServo(ang)
        nTime = time.time()
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>모터 이동</title>'
        html += '</head><body>'
        html += '<a href="/">홈으로</a>'
        html += f'<div><h5>모터를 {ang}도로 이동했습니다.</h5></div>'
        html += f'<div><h5>측정 시간: {time.ctime(nTime)}</h5></div>'
        html += '</body></html>'    
        self.writeHtml(html)

    def writeSampleServeoMove(self, qs):
        self.writeHead(200)
        qdict = parse.parse_qs(qs)
        ang = int(qdict['ang'][0])
        self.server.gateway.setServo(ang)
        nTime = time.time()
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>모터 이동</title>'
        html += '</head><body>'
        html += '<a href="/">홈으로</a>'
        html += f'<div><h5>모터를 {ang}도로 이동했습니다.</h5></div>'
        html += f'<div><h5>측정 시간: {time.ctime(nTime)}</h5></div>'
        html += '</body></html>'    
        self.writeHtml(html)

#-----------------------------------------------------------------------------------------------------------------'
# led 제어를 보여주는 html

    def writeLedOn(self, qs):
        self.writeHead(200)
        qdict = parse.parse_qs(qs)
        led = str(qdict['led'][0])
        self.server.gateway.setLedColor(led)
        nTime = time.time()
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>Led 제어</title>'
        html += '</head><body>'
        html += '<a href="/">홈으로</a>'
        html += f'<div><h5>Led를 {led}로 제어했습니다.</h5></div>'
        html += f'<div><h5>측정 시간: {time.ctime(nTime)}</h5></div>'
        html += '</body></html>'    
        self.writeHtml(html)

#-----------------------------------------------------------------------------------------------------------------'
# buzeer 제어를 보여주는 html
    def writeBuzeerOn(self, qs):
        self.writeHead(200)
        qdict = parse.parse_qs(qs)
        buzzer = str(qdict['buzeer'][0])
        delay = int(qdict['delay'][0])
        ndelay = delay*1000
        self.server.gateway.setBuzzerNote(buzzer, ndelay)
        nTime = time.time()
        html = '<html><head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>Buzzer 제어</title>'
        html += '</head><body>'
        html += '<a href="/">홈으로</a>'
        html += f'<div><h5>Buzeer를 {buzzer}로 제어했습니다.</h5></div>'
        html += f'<div><h5>측정 시간: {time.ctime(nTime)}</h5></div>'
        html += '</body></html>'    
        self.writeHtml(html)
        