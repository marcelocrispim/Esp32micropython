# tenta importar o umqtt, caso não estiver instalado ele faz a instalacao
try:
    import uasyncio
except:
    import upip

    upip.install('uasyncio')
    print('umqtt Instalado !!!')
    import uasyncio

try:
    from umqtt.simple import MQTTClient
except:
    import upip

    upip.install('micropython-umqtt.simple')
    print('umqtt Instalado !!!')
    from umqtt.simple import MQTTClient

from urandom import randint
from ujson import loads
from machine import Pin
import network
import ubinascii


async def main(numero, tempo):
    # print('entrou = ', numero)
    while True:
        print('entrou = ', numero, 'tempo = ', tempo)
        await uasyncio.sleep(tempo)


############################
def sub_cb(topic, msg):
    print(1)
    print((topic.decode(), loads(msg.decode())))


async def mainMqtt(c):
    c.subscribe('hmi/#'.encode())
    print("Client %s - Connected to %s, subscribed to %s topic" % (nome, 'autbackup', 'hmi/#'))

    try:
        while True:
            # print( micropython.mem_info())
            if c.check_msg():
                print('Tem Mensagem')
                c.wait_msg()
            await uasyncio.sleep(.2)
            # print('re-loop mqtt')
    except Exception as e:
        print(e)


############################
def callBack(x, c, mac):
    c.publish('hmi/{}/b0'.format(mac), str(x.value()).encode())


async def mainButton(c, mac):
    b0 = Pin(0, Pin.IN)
    b0.irq(handler=lambda x: callBack(b0, c, mac), trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)


############################
mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
nome = "umqtt_client_{}".format(mac)
c = MQTTClient(nome, '192.168.30.253')
# Subscribed messages will be delivered to this callback
c.set_callback(sub_cb)
c.connect()
loop = uasyncio.get_event_loop()
loop.create_task(mainButton(c, mac))
loop.create_task(mainMqtt(c))
loop.run_forever()
