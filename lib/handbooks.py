#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# файл сборник справочников никаких кастомных обьектов только стандартные типы данных
#from handbooks import *
#глоссарий:
#	зона аропорта

#набор координат
coord={
'KSC_West'  :{'name':'KSC West Dot',       'lat':-0.04855056049336841, 'lng':-74.72449313835466000, 'alt':70.0000000000},
'KSC_East'  :{'name':'KSC East Dot',       'lat':-0.05025878770915180, 'lng':-74.48951284451766242, 'alt':70.0000000000},
'KSC_BP'    :{'name':'KSC Begin Position', 'lat':-0.04859355505160000, 'lng':-74.72465205780000000, 'alt':70.3741567462},
'recursive_dot'  :{'name':'recursive_dot', 'lat':-0.02022509861205912, 'lng':-72.18951284451766242, 'alt':1000.0},
'recursive_dot1' :{'name':'recursive_dot', 'lat':-0.02022509861205912, 'lng':-76.18951284451766242, 'alt': 600.0},
'two_dot'        :{'name':'two_dot',       'lat': 1.35022509861205912, 'lng':-70.48951284451766242, 'alt':1000.0}
}


#диспетчерский пункт
#типы диспетчерских пунктов
#0 главный диспетчер хоста выдает информацию о диспетчерах и зонах, ведет диспетчеризацию аварийных ситуаций, максимальный приоритет указаний
#1-10 диспетчера аэропортов и отдельностоящих впп
#1 главный диспетчер аэропорта выдает информацию о диспетчерах зон аэропорта, ведет диспетчеризацию аварийных ситуаций в зоне аэропорта и/или впп, ведет диспетчерезацию движения во всей зоне при отсутствии вспомогательных диспетчеров
#2 вспомогательный
tc_type={0:'information and Emergency',1:'airports main TC', 5:'airports secondary TC', 11:'SPAN zone TC', 255:'non TC'}
#имя,тип,порт
mainTC ={'name':'Main', 'type':0,'port':5000}
KSC_TC ={'name':'KSC' , 'type':1,'port':5001}



#Взлетно Посадочные Полосы
#вспомогательные данные для описания полос
#материалы покрытия полос (добавить словать описаний на разных языках)
VPP_cover = {0:None,1:'concrete',2:'priming'}
#классы ВПП зависит от покрытия, длинны, ширины, наличия подсветки, угла глиссады, максимальной дальности прямой для глиссады(не расчитывается свыше 50км), если нет подсветки то класс снижается до ближайшего где подсветка не является обязательной)
VPP_classes = {
0: {'name':None,'cover':0,'min_length':0,'lighting':False},
1: {'Name':'Class','cover':1,'min_length':2000.0,'lighting':True},
2: {'Name':'Class','cover':1,'min_length':1500.0,'lighting':True},
3: {'Name':'Class','cover':1,'min_length':1000.0,'lighting':True},
4: {'Name':'Class','cover':1,'min_length':750.0, 'lighting':False},
5: {'Name':'Class','cover':1,'min_length':500.0, 'lighting':False},
11:{'Name':'Class','cover':2,'min_length':2000.0,'lighting':True},
12:{'Name':'Class','cover':2,'min_length':1500.0,'lighting':True},
13:{'Name':'Class','cover':2,'min_length':1000.0,'lighting':False},
14:{'Name':'Class','cover':2,'min_length':750.0, 'lighting':False},
15:{'Name':'Class','cover':2,'min_length':500.0, 'lighting':False}
}
#имя, класс, номер, направление, длинна, координаты начала и завершения, диспетчерский пункт подлета, пролета, диспетчерский пункт взлета
KSC27 = {'name':'KSC27','vpp_class':1,'number':27,'direction':270.4165, 'length':2460.77,'edge1':coord.get('KSC_West'),'edge2':coord.get('KSC_East'),'tc_STAR':KSC_TC,'tc_SPAN':KSC_TC,'tc_SID':KSC_TC}
KSC9  = {'name':'KSC9', 'vpp_class':1,'number':9, 'direction':90.41651, 'length':2460.77,'edge2':coord.get('KSC_West'),'edge1':coord.get('KSC_East'),'tc_STAR':KSC_TC,'tc_SPAN':KSC_TC,'tc_SID':KSC_TC}
 



type_message={
0:{'name':'Ping', 'isLogging':False,'log_mess':'', 'isParammetric':False}, #просто пинг для проверки
1:{'name':'Hello','isLogging':False,'log_mess':'', 'isParammetric':False}, #начало общения просто для проверки что получатель отвечает хоть как то)))
2:{'name':'OK',   'isLogging':False,'log_mess':'', 'isParammetric':False}, #подтверждение 
3:{'name':'Bad',  'isLogging':False,'log_mess':'', 'isParammetric':False},  #отказ при нормальном получении
255:{'name':'test param',  'isLogging':False,'log_mess':'', 'isParammetric':True}
}

name_message={
'Ping' :0,
'Hello':1,
'OK'   :2,
'Bad'  :3,
'test param':255
}




