#!/usr/bin/env python3.5

from messaging.sms import SmsSubmit, SmsDeliver
'''
pdu = '0891683110701105F0600DA1019680310516F50019711150411275238C0500035C030262DB80585BA38BB24F1AFF0C003100316708003865E5665A003770B9FF0C534E4E2D79D1628059275B66516B53F7697C4E8C697C591A529F80FD5385FF0C73B0573A63A565367B805386FF0C4E8689E3804C4F4D8BE660C5629590127B8053868BF7767B9646FF1A0068007400740070003A002F002F00630061006D007000750073002E0035'
'''
def decodepdu(pdu):

    list =[]
    reci = SmsDeliver(pdu)
    #print(reci.number)
    #print(reci.date)
    date = reci.date.strftime("%Y-%m-%d %H:%M:%S")
    #print(date)
    #print(reci.text)
    #print("hello world!")
    list.append(reci.number)
    list.append(date)
    list.append(reci.text)
    return list


