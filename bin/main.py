#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PIL import Image,ImageDraw,ImageFont  #引入图片处理库
import os,sys,re,json,time,datetime  #引入系统相关库
from borax.calendars.lunardate import LunarDate #农历日期以及天干地支纪年法的 Python 库
import logging  #日志库
import subprocess
import os
from threading import Timer
import requests
white = 255 #颜色
black = 0
logging.basicConfig(level=logging.DEBUG)
################################引入配置文件开始################################################
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir): 
    sys.path.append(libdir)#将引入文件添加到环境变量
    from waveshare_epd import epd2in13_V2  #引入墨水屏驱动文件
logging.debug("Loading Fonts")
font01 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20) #字体文件
font02 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15) #字体文件
font03 = ImageFont.truetype(os.path.join(picdir, 'DSEG7Modern-Bold.ttf'), 38) #字体文件
font04 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 10) #字体文件
font05 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12) #字体文件
font06 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 13) #字体文件
################################引入配置文件结束################################################
def Local_strong_brush(): #局部强制刷新显示
     i = 0
     while i < 5:
         epd.displayPartial(epd.getbuffer(info_image.rotate(180)))#局刷开始
         i = i + 1
def getWeath(city='101270108'): #天气函数,下载json天气至本地
     headers = {
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50',
         'Referer':'http://www.weather.com.cn/'
     }
     response = requests.get('http://d1.weather.com.cn/sk_2d/'+city+'.html',headers=headers)
     response.encoding = 'utf-8'
     Weath=response.text[11:]
     fileHandle=open('weather.json','w')
     fileHandle.write(str(Weath))
     fileHandle.close()
     Timer(1800, getWeath).start() #定时器函数,间隔三分钟下载文件至本地
     print("天气文件更新")
def gey_yiyan(): #一言API
     response = requests.get("https://international.v1.hitokoto.cn/?c=k&c=f&c=d&c=a&encode=text&min_length=7&max_length=19") 
     response.encoding = 'utf-8'
     yiyan=response.text
     return yiyan
def get_date():#返回当前年月日及星期几
    date = datetime.datetime.now()
    today=LunarDate.today()
    week_day_dict = {0: '星期一',1: '星期二',2: '星期三',3: '星期四',4: '星期五',5: '星期六',6: '星期日',}
    day = date.weekday()
    return time.strftime('%Y年%m月%d日')+'  '+week_day_dict[day]+'  '+today.strftime('农 %M月%D')
def get_time():#返回当前时间,不到秒,大写
    return time.strftime('%H:%M')
def Get_address():#获取当前的IP地址
     return (subprocess.check_output(u"hostname -I | cut -d\' \' -f1 | head --bytes -1", shell = True ).decode('gbk'))
def CPU_temperature():#CPU温度获取
     temperatura = os.popen('vcgencmd measure_temp').readline()
     temperatura = temperatura.replace('temp=','').strip()
     return str(temperatura)
def Memory_footprint():#显示内存占用百分比
     return(subprocess.check_output(u"free -m | awk -F '[ :]+' 'NR==2{printf \"%d\", ($3)/$2*100}'", shell = True ).decode('gbk'))
def CPU_usage(): #显示CPU占用百分比
     return(str(int(float(os.popen("top -b -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))))
def power_battery():#获取当前电池电量
     return(str(int(subprocess.check_output(u"echo \"get battery\" | nc -q 0 127.0.0.1 8423|awk -F':' '{print int($2)}'", shell = True ).decode('gbk')))+u'%')      
def Bottom_edge():  #在图片中添加底边内容
     draw.rectangle((0, 105, 250, 122), 'black', 'black')
     '''电池图标画图'''
     draw.line((126,109,154,109),fill=255, width=1) #电池顶边
     draw.line((126,110,126,119),fill=255, width=1) #电池左边
     draw.line((127,119,154,119),fill=255, width=1) #电池下边
     draw.line((154,110,154,118),fill=255, width=1)
     draw.line((155,112,157,112),fill=255, width=1)
     draw.line((155,116,157,116),fill=255, width=1)
     draw.line((157,113,157,115),fill=255, width=1)
     global power_str
     power_str=power_battery()
     draw.text((131,108),power_str,font = font04,fill =255) #显示当前电量百分比
     '''电池图标画图'''
     '''添加一言API'''
     global Time_keeping
     Time_keeping =0
     draw.text((4,84),gey_yiyan(),font = font06,fill =0)
     '''添加一言API end'''     
     draw.ellipse((192, 107, 207, 120), 0, 255)# 时钟图标
     draw.line((199,109,199,114),fill=255, width=1)
     draw.line((200,114,204,114),fill=255, width=1)
     global local_addr  #获取当前IP地址
     local_addr= Get_address()  #获取当前IP地址
     draw.text((10,107),"IP:"+local_addr,font = font05,fill =255)#显示当前IP地址
def Weather(): #在图片中添加天气内容
     Weather_json = open('weather.json','r')
     Weather_data = Weather_json.read()
     Weather_json.close()
     Weather_text=json.loads(Weather_data)
     global Weather_position
     global temperature
     global weather
     global wind_direction
     global weather_update
     global weather_date
     global humidity
     Weather_position = Weather_text['cityname'] #定位位置
     temperature=Weather_text['temp']+u'°C' #温度
     weather = Weather_text['weather'] #天气情况
     wind_direction = Weather_text['WD'] #风向
     weather_update = Weather_text['time'] #天气更新时间
     weather_date =  Weather_text['date'] #日期
     humidity =  Weather_text['SD'] #湿度
     draw.text((150,25),"天气:",font = font06,fill =0)#显示当前天气前缀
     draw.text((150,45),"温度:",font = font06,fill =0)#显示当前温度前缀
     draw.text((150,65),"湿度:",font = font06,fill =0)#显示当前湿度前缀
     draw.text((191,25),weather,font = font06,fill =0)
     draw.text((191,45),temperature,font = font06,fill =0)
     draw.text((191,65),humidity,font = font06,fill =0)
     draw.text((211,107),weather_update,font = font05,fill =255) #显示天气更新时间

def Basic_refresh(): #全刷函数
    logging.info("Refresh and prepare the basic content before starting the canvas")#开始画布前刷新准备基础内容
    epd.init(epd.PART_UPDATE)
    epd.Clear(0xFF)
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    global get_date_var
    get_date_var=get_date() #记录开始数据
    draw.text((2,2),get_date_var,font = font02,fill =0)#将日期及星期几显示到屏幕
    global local_time
    local_time=get_time()
    draw.text((5,40),local_time,font = font03,fill =0)#显示当前时间
    Bottom_edge() #添加底边内容
    Weather() #天气内容
    epd.display(epd.getbuffer(info_image.rotate(180)))
def Partial_full_brush(): #局部定时全刷函数
     Basic_refresh() #全局刷新
     logging.debug("局部定时全局刷新")
     epd.init(epd.PART_UPDATE)
def Partial_refresh():#局刷函数
     logging.info("Partial content update, this update is recommended to be synchronized with the minute to save the life of the ink screen")#局部内容更新,此更新建议与分钟同步,以节省墨水屏寿命
     epd.displayPartBaseImage(epd.getbuffer(info_image.rotate(180)))
     epd.init(epd.PART_UPDATE)
     while (True):
         global local_time
         local_time1=get_time()
         if (local_time1==local_time) ==False:
             draw.rectangle((5, 40, 133, 82), fill = 255) #时间局刷区域
             draw.text((5,40),local_time1,font = font03,fill =0)#刷新当前时间
             local_time=local_time1
             Local_strong_brush() #局部强刷
         get_date_var1=get_date()  #局刷判断,如果时间与前一次不一致说明内容变化,需要刷新显示
         global get_date_var #再次声明这个是全局变量
         if(get_date_var1==get_date_var) ==False:
             draw.rectangle((2, 2, 250, 16), fill = 255) #设置头部刷新区域
             draw.text((2,2),get_date_var,font = font02,fill =0)#将日期及星期几刷新显示到屏幕
             get_date_var=get_date_var1 #将更新的值保存到初始变量,直到下一次变化时执行该刷新操作
             logging.debug("头部日期部位发生刷新变化.")
             Local_strong_brush() #局部强刷
         global local_addr #当前IP地址
         local_addr1 = Get_address()
         if (local_addr1==local_addr) ==False:
             draw.rectangle((1, 107, 94, 120), fill = 0) #设置头部刷新区域
             draw.text((10,107),"IP:"+local_addr1,font = font05,fill =255)#显示当前IP地址
             local_addr=local_addr1
             Local_strong_brush() #局部强刷
         '''天气局部更新函数'''
         Weather_json = open('weather.json','r')
         Weather_data = Weather_json.read()
         Weather_json.close()
         Weather_text=json.loads(Weather_data)
         global Weather_position
         global temperature
         global weather
         global wind_direction
         global weather_update
         global weather_date
         global humidity
         Weather_position1 = Weather_text['cityname'] #定位位置
         temperature1=Weather_text['temp']+u'°C' #温度
         weather11 = Weather_text['weather'] #天气情况
         wind_direction1 = Weather_text['WD'] #风向
         weather_update1 = Weather_text['time'] #天气更新时间
         weather_date1 =  Weather_text['date'] #日期
         humidity1 =  Weather_text['SD'] #湿度
         if (weather11==weather) ==False:
             draw.rectangle((191, 25, 249, 38), fill = 255) #天气局刷区域
             draw.text((191,25),weather11,font = font06,fill =0)
             weather=weather11
             logging.info("天气局部刷新")
             Local_strong_brush() #局部强刷
         if (temperature1==temperature) ==False:
             draw.rectangle((191, 45, 249, 57), fill = 255) #局刷区域
             draw.text((191,45),temperature1,font = font06,fill =0)
             temperature=temperature1
             logging.info("温度局部刷新")
             Local_strong_brush() #局部强刷
         if (humidity1==humidity) ==False:
             draw.rectangle((191, 65, 249, 77), fill = 255) #局刷区域
             draw.text((191,65),humidity1,font = font06,fill =0)
             humidity = humidity1
             logging.info("湿度局部刷新")
             Local_strong_brush() #局部强刷
         if (weather_update1==weather_update) ==False:
             draw.rectangle((211, 107, 248, 118), fill = 0) #设置更新时间刷新区域
             draw.text((211,107),weather_update1,font = font05,fill =255) #显示天气更新时间
             weather_update=weather_update1
             logging.info("天气更新时间局部刷新")
             Local_strong_brush() #局部强刷
         '''天气局部更新函数'''
         global power_str
         power_str1 =power_battery()
         if (power_str1==power_str) ==False:
             draw.rectangle((128, 110, 153, 117), fill = 0) #设置更新时间刷新区域
             draw.text((130,108),power_battery(),font = font04,fill =255) #显示当前电量百分比
             power_str=power_str1
             Local_strong_brush() #局部强刷
             logging.info("电源电量局部刷新")
         '''一言API显示'''
         global Time_keeping
         Time_keeping+=1
         if Time_keeping == 300 : #一言API局刷,当变量Time_keeping数据为10即开始执行
             draw.rectangle((1, 82, 248, 101), fill = 255)
             draw.text((4,84),gey_yiyan(),font = font06,fill =0)
             Time_keeping=0
             Local_strong_brush() #局部强刷
             logging.info("一言API局部刷新")
         '''一言API显示'''
         #epd.displayPartial(epd.getbuffer(info_image.rotate(180)))#局刷开始
         time.sleep(2)
         #if time.strftime('%H%M%S')=='000000': #如果时间是晚上00点,执行全局刷新
             #Partial_full_brush() #每天全局刷新一次
try:
##################屏幕初始化#########################
    getWeath()#天气获取函数开始运行
    epd = epd2in13_V2.EPD() #初始化
    epd.init(epd.FULL_UPDATE)#设定屏幕刷新模式
    epd.Clear(0xFF) #清除屏幕内容
##################屏幕初始化#########################   
    logging.info("Width = %s, Height = %s", format(epd.width), format(epd.height)) #打印屏幕高度及宽度
    logging.info("Initialize and clear the display")#屏幕开始准备相关展示
    info_image = Image.new('1', (epd.height, epd.width), 255) #画布创建准备
    draw = ImageDraw.Draw(info_image)
    Basic_refresh() #全局刷新
    Partial_refresh() #局部刷新
    epd.init(epd.FULL_UPDATE)
    #epd.Clear(0xFF)
    epd.sleep()
except IOError as e:
    logging.info(e)   
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd.init(epd.FULL_UPDATE)
    epd.sleep()
    epd2in13_V2.epdconfig.module_exit()
    exit()