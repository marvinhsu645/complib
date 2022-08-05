# this is the very basic component library
from tagsys import Component
from sympy import *
from sympy.physics.units import *

############## define our own convenient units #############

mA = milli*ampere
uA = micro*ampere
nA = nano*ampere
mT = milli*tesla
uT = micro*tesla
dps = degrees/seconds
MHz = mega*hertz
kHz = kilo*hertz
GHz = giga*hertz
mm = milli*meter


######## Trivial ones for basic testing, not realistic ##########
Component('c1', { 'BM' },
            { 'pwr': { 'DC3V'}, 'stat': {'I2C'} })
Component('c2', { 'Acc' },
            { 'aout': {'Analog', 'Output'}})
Component('c3', { 'MCU', 'CPU', 'SPI', 'I2C' },
            {'usart': {'SPI', 'SPI.Master', 'I2C', 'I2C.Master',
                'SPI.Master-1', 'SPI.Master-2', 'SPI.Master-3',
                'SPI.Slave'} })
Component('c4', { 'MCU', 'CPU', 'SPI', 'I2C', 'ADC' },
            {'usart': {'SPI', 'SPI.Master', 'I2C', 'I2C.Master',
                'SPI.Master-1', 'SPI.Master-2', 'SPI.Master-3',
                'SPI.Slave'},
             'ain': { 'Analog', 'Input' }})
Component('c5', { 'ADC', 'SPI' },
            { 'ain': { 'Analog', 'Input' },
              'dout': {'SPI', 'SPI.Slave'}})
Component('c6', { 'Acc', 'ADC', 'SPI', 'I2C' },
             { 'spi': { 'SPI', 'SPI.Slave'}, 
               'i2c': { 'I2C', 'I2C.Slave'} })

Component('MPU9250', { 'Acc', 'Gyro', 'Mag', 'ADC', 'SPI', 'I2C' },
            { 'spi': { 'SPI', 'SPI.Slave'},
              'i2c': { 'I2C', 'I2C.Slave' }})

Component('EFR32', { 'MCU', 'CPU', 'SPI', 'I2C', 'ADC', 'BLE' },
            { 'usart0': { 'SPI', 'SPI.Master', 'I2C',
                'I2C.Master', 'SPI.Master-1', 'SPI.Master-2',
                'SPI.Master-3', 'SPI.Slave', 'UART'}, 
              'usart1': { 'SPI', 'SPI.Master', 'I2C',
                'I2C.Master', 'SPI.Master-1', 'SPI.Master-2',
                'SPI.Master-3', 'SPI.Slave', 'UART'}}) 

Component('MT29', { 'Flash', 'SPI' }, 
            { 'spi': { 'SPI', 'SPI.Slave'}})

####################### real ones for EcoMini ############
Component(name='TPS62740DSS', tagset={'buck_converter'}, 
        portdict={'p_in': {'power', 'DC', 'input',
                           '@V_in=Interval(2.2*volt, 5.5*volt)',
                           '@V_in_absmax=Interval(-3*volt, 6*volt)'},
                 'p_out': {'power', 'DC', 'output', 'regulated',
                            'switched',
                            '@V_out=Interval(-3*volt,3.7*volt)'}},
        attrdict={'V_in': Interval(2.2*volt, 5.5*volt), 
            'I_q': 360*nA,
            'I_out': Interval(0*mA, 300*mA),
            'V_out': {(i/10)*volt for i in range(18, 34)},
            'T_stg': Interval(-65, 150), #degrees C
            'V_esd_hbm': 2000*volt, #V max
            'V_esd_cdm': 2000*volt,
            'url':'https://www.ti.com/lit/ds/symlink/tps62740.pdf'}) # regulator
Component(name='MRMS301A', tagset={'magswitch'},
        portdict={'p_in': {'power', 'DC', 'input'},
                  'out': {'signal', 'output'}},
        attrdict={'V_in':Interval(1.6*volt, 3.5*volt),
                  'I_avg': 5*uA,
                  'sensitivity': Interval(0.5*mT, 2.5*mT), #mT
                  'temperature': Interval(-40, 85), # degC
                  'url': 'https://media.digikey.com/pdf/Data%20Sheets/Murata%20PDFs/MRx_Sensors.pdf' })    # magnetic switch
Component(name='M41T62', tagset={'RTC', 'I2C'},
        portdict={'i2c': {'I2C', 'I2C.Slave',
                    '@voltage=Interval(1.3*volt, 4.4*volt)',
                    '@frequency=400*hertz', '@I_consume=350*nA'}, #nA at 3V
                  'irq': {'IRQ', 'signal' 'output', 'opendrain'},
                  'sqwe': {'signal', 'output', 'squarewave',
                      '@frequency=32*kilo*hertz'},
                  'p_in': {'power', 'DC', 'input'}},
        attrdict={'url': 'https://www.st.com/resource/en/datasheet/m41t62.pdf'})      # RTC
Component(name='MPU-9250', tagset={'IMU', 'Accelerometer',
            'Gyroscope', 'Magnetometer', 'SPI', 'I2C', 'ADC' },
          portdict={'pwr': {'power', 'DC', 'input',
                        '@voltage=Interval(2.4*volt, 3.6*volt)'},
                    'spi': {'SPI', 'SPI.Slave',
                            '@frequency=1*MHz',},
                    'i2c': {'I2C', 'I2C.Slave',
                            '@frequency=400*kHz'}}, 
          attrdict={'acc_range': {Interval(-i*gee, i*gee) \
                        for i in [2, 4, 8, 16]},
                    'gyro_range':{Interval(-i*dps, i*dps)\
                        for i in [250,500,1000,2000]},
                    'mag_range': Interval(-4800*uT, 4800*uT),
                    'bitres': 16},
          portchild={'pwr': {'VDD', 'VDDIO'},
                     'spi': {'SDA/SDI', 'SDO', 'SCL/SCLK', 'nCS'},
                     'i2c': {'SDA/SDI', 'SCL/SCLK'}},
          pindict={'VDD': {'power', 'input'},
                   'SCL/SCLK': {'input', 'signal', 'clock'},
                   'SDA/SDI': {'inout', 'signal', 'data'},
                   'INT': {'output', 'IRQ'}},
          pinnum={1:'RESV',
                  12:'INT',
                  13:'VDD',
                  23:'SCL/SCLK',
                  24:'SDA/SDI'},
          patch="(export (version D) \
                    (components \
                      (comp (ref #PWR1) \
                        (value GND) \
                        (libsource (lib power) (part GND)) \
                        (sheetpath (names /top/9252463163646315502) (tstamps /top/9252463163646315502))) \
                      (comp (ref #PWR2) \
                        (value VCC) \
                        (libsource (lib power) (part VCC)) \
                        (sheetpath (names /top/5533475186907887364) (tstamps /top/5533475186907887364))) \
                      (comp (ref C1) \
                        (value 0.1muF) \
                        (libsource (lib Device) (part C)) \
                        (sheetpath (names /top/15864663021404307731) (tstamps /top/15864663021404307731))) \
                      (comp (ref C2) \
                        (value 0.1muF) \
                        (libsource (lib Device) (part C)) \
                        (sheetpath (names /top/4757838341044565466) (tstamps /top/4757838341044565466))) \
                      (comp (ref C3) \
                        (value 10nF) \
                        (libsource (lib Device) (part C)) \
                        (sheetpath (names /top/2814596574783560753) (tstamps /top/2814596574783560753))) \
                      (comp (ref U1) \
                        (value MPU-9250) \
                        (libsource (lib MPU-9250) (part MPU-9250)) \
                        (sheetpath (names /top/14013186969592232737) (tstamps /top/14013186969592232737)))) \
                  (nets \
                    (net (code 1) (name N$1) \
                      (node (ref #PWR1) (pin 1)) \
                      (node (ref C1) (pin 2)) \
                      (node (ref C2) (pin 2)) \
                      (node (ref C3) (pin 2)) \
                      (node (ref U1) (pin 18)) \
                      (node (ref U1) (pin 20))) \
                    (net (code 2) (name N$2) \
                      (node (ref #PWR2) (pin 1)) \
                      (node (ref C2) (pin 1)) \
                      (node (ref U1) (pin 13))) \
                    (net (code 3) (name N$3) \
                      (node (ref #PWR2) (pin 1)) \
                      (node (ref U1) (pin 1))) \
                    (net (code 4) (name N$4) \
                      (node (ref C1) (pin 1)) \
                      (node (ref U1) (pin 10))) \
                    (net (code 5) (name N$5) \
                      (node (ref #PWR2) (pin 1)) \
                      (node (ref C3) (pin 1)) \
                      (node (ref U1) (pin 8)))) \
                )") # IMU
Component(name='CC2541-SOC-KGD',
          tagset={'MCU', 'CPU', '8051', 'BLE', 'ADC', 'SPI',
                  'I2C', 'UART', 'GPIO', 'DMA', 'SRAM', 'Flash',
                  'Timer', 'LDO' },
          portdict={'usart0': {'SPI', 'SPI.Master', 'SPI.Slave',
                                'UART'},
                    'usart1':{'SPI', 'SPI.Master', 'SPI.Slave',
                                'UART'},
                    'i2c': {'I2C', 'I2C.Master', 'I2C.Slave'},
                    'p_in': {'power', 'DC', 'input'},
                    'ant': {'Antenna', '@frequency=2.4*GHz'}},
          attrdict={'ADC_bitres': 12, }) # MCU+BLE
Component(name='WAN2012', 
          tagset={'Antenna', },
          attrdict={'frequency_central': 2450*MHz,
              'bandwidth_min': 85* MHz,
              'return_loss_max': -6.5, # dB
              'gain_peak': 1.72, # dBi
              'impedance': 50*ohm,
              'temperature_op': Interval(-40, 110), #degC
              'power_max': 4*watt,
              'length': 2.5*mm,
              'width': 1.23*mm,
              'height': 0.45*mm,
              })     # Antenna

Component(name='NE555', 
          tagset={'Timer'})
Component(name='R', 
          tagset={'R'})
Component(name='C', 
          tagset={'C'})
Component(name='PWR', 
          tagset={'Power', 'supply'})
Component(name='GND', 
          tagset={'Power', 'load'})