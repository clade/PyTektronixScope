from time import *
import numbers
import numpy as np

try:
    import visa
except ImportError:
    visa = None

class TektronixScopeError(Exception):
    """Exception raised from the TektronixScope class

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, mesg):
        self.mesg = mesg
    def __repr__(self):
        return self.mesg
    def __str__(self):
        return self.mesg



class TektronixScope(object):
    """Drive a TektronixScope instrument

    usage:
        scope = TektronixScope(instrument_resource_name)
        X,Y = scope.read_data_one_channel('CH2', t0 = 0, DeltaT = 1E-6, 
                                                            x_axis_out=True)

    Only a few functions are available, and the scope should
    be configured manually. Direct acces to the instrument can
    be made as any Visa Instrument :  scope.ask('*IDN?')
    """    
    def __init__(self, inst):
        """ Initialise the Scope

        argument : 
            inst : should be a string or an object with write and ask method

        """
        if not hasattr(inst, 'write'): 
            if isinstance(inst, str):
                if visa is not None:
                    rm = visa.ResourceManager()
                    inst = rm.open_resource(inst)
                else:
                    raise Exception('Visa is not install on your system')
            else:
                raise ValueError('First argument should be a string or an instrument')
        self._inst = inst

    def write(self, cmd):
        return self._inst.write(cmd)

    def ask(self, cmd):
        return self._inst.ask(cmd)

    def ask_raw(self, cmd):
        if hasattr(self._inst, 'ask_raw'):
            return self._inst.ask_raw(cmd)[:-1]
        else:
            return self._inst.ask(cmd)


###################################
## Method ordered by groups 
###################################

#Acquisition Command Group 
    def start_acq(self):
        """Start acquisition"""
        self.write('ACQ:STATE RUN')
    def stop_acq(self):
        """Stop acquisition"""
        self.write('ACQ:STATE STOP')
#Alias Command Group

#Bus Command Group

#Calibration and Diagnostic Command Group

#Cursor Command Group

#Display Command Group

#Ethernet Command Group

#File System Command Group

#Hard Copy Command Group

#Horizontal Command Group
    def get_horizontal_scale(self):
        return float(self.ask("HORizontal:SCAle?"))

    def set_horizontal_scale(self, val):
        return self.write("HORizontal:SCAle {val}".format(val=val))


#Mark Command Group

#Math Command Group

#Measurement Command Group

#Miscellaneous Command Group
    def load_setup(self):
        l = self.ask('SET?')
        dico = dict([e.split(' ', 1) for e in l.split(';')[1:]])
        self.dico = dico

    def get_setup_dict(self, force_load=False):
        """Return the dictionnary of the setup 
        
        By default, the method does not load the setup from the instrument
        unless it has not been loaded before or force_load is set to true.
        """
        if not hasattr(self, 'dico') or force_load:
            self.load_setup()
        return self.dico

    def get_setup(self, name, force_load=False):
        """Return the setup named 'name' 
        
        By default, the method does not load the setup from the instrument
        unless it has not been loaded before or force_load is set to true.
        """
        if not hasattr(self, 'dico') or force_load:
            self.load_setup()
        return self.dico[name]

    def number_of_channel(self):
        """Return the number of available channel on the scope (4 or 2)"""
        if ':CH4:SCA' in self.get_setup_dict().keys():
            return 4
        else:
            return 2

#Save and Recall Command Group

#Search Command Group

#Status and Error Command Group

#Trigger Command Group

#Vertical Command Group
    def channel_name(self, name):
        """Return and check the channel name
        
        Return the channel CHi from either a number i, or a string 'i', 'CHi'
        
        input : name is a number or a string
        Raise an error if the channel requested if not available 
        """
        n_max = self.number_of_channel()
        channel_list = ['CH%i'%(i+1) for i in range(n_max)]
        channel_listb = ['%i'%(i+1) for i in range(n_max)]
        if isinstance(name, numbers.Number):
            if name > n_max:
                raise TektronixScopeError("Request channel %i while channel \
number should be between %i and %i"%(name, 1, n_max))
            return 'CH%i'%name
        elif name in channel_list:
            return name
        elif name in channel_listb:
            return 'CH'+name
        else:
            raise TektronixScopeError("Request channel %s while channel \
should be in %s"%(str(name), ' '.join(channel_list)))

    def is_channel_selected(self, channel):
        return self.ask('SEL:%s?'%(self.channel_name(channel)))=='1'

    def get_channel_offset(self, channel):
        return float(self.ask('%s:OFFS?'%self.channel_name(channel)))

    def get_channel_position(self, channel):
        return float(self.ask('%s:POS?'%self.channel_name(channel)))

    def get_vertical_scale(self, channel):
        return float(self.ask('%s:SCA?'%self.channel_name(channel)))


    def set_impedance(self, channel, value):
        """Sets the input impedance of the channel"""
        liste_string = ['FIF', 'FIFty','SEVENTYF','SEVENTYFive','MEG','50','75','1.00E+06']
        liste_value = [50, 75, 1.00E6]
        if isinstance(value, str) or isinstance(value, unicode):
            if value.lower() not in map(lambda a:a.lower(),liste_string):
                raise TektronixScopeError("Impedance is %s. It should be in %s"%liste_string)
        elif isinstance(value, numbers.Number):
            if value not in liste_value:
                raise TektronixScopeError("Impedance is %s. It should be in %s"%liste_value)
            else:
                value = str(value) if value<100 else '1.00E+06'
        else:
            raise TektronixScopeError("Impedance is %s. It should be in %s"%liste_string)
        self.write("%s:IMPedance %s"%(self.channel_name(channel), value))
    def get_impedance(self, channel):
        """Returns the input impedance of the channel"""
        return self.ask('%s:IMPedance?'%self.channel_name(channel))

    def set_coupling(self, channel, value):
        """Sets the input coupling of the channel"""
        liste_string = ['AC','DC','GND']
        if isinstance(value, str) or isinstance(value, unicode):
            if value.lower() not in map(lambda a:a.lower(),liste_string):
                raise TektronixScopeError("Coupling is %s. It should be in %s"%liste_string)
        else:
            raise TektronixScopeError("Coupling is %s. It should be in %s"%liste_string)
        self.write("%s:COUPling %s"%(self.channel_name(channel), value))
    def get_coupling(self, channel):
        """Returns the input coupling of the channel"""
        return self.ask('%s:COUPling?'%self.channel_name(channel))



# Waveform Transfer Command Group
    def set_data_source(self, name):
        name = self.channel_name(name)
        self.write('DAT:SOUR '+str(name))

    def set_data_start(self, data_start):
        """Set the first data points of the waveform record
        If data_start is None: data_start=1
        """
        if data_start is None:
            data_start = 1
        data_start = int(data_start)
        self.write('DATA:START %i'%data_start)

    def get_data_start(self):
        return int(self.ask('DATA:START?'))

    def get_horizontal_record_length(self):
        return int(self.ask("horizontal:recordlength?"))

    def set_horizontal_record_length(self, val):
        self.write('HORizontal:RECOrdlength %s'%str(val))

    def set_data_stop(self, data_stop):
        """Set the last data points of the waveform record
        If data_stop is None: data_stop= horizontal record length
        """
        if data_stop is None:
            data_stop = self.get_horizontal_record_length()
        self.write('DATA:STOP %i'%data_stop)

    def get_data_stop(self):
        return int(self.ask('DATA:STOP?'))

    def get_out_waveform_horizontal_sampling_interval(self):
        return float(self.ask('WFMO:XIN?'))

    def get_out_waveform_horizontal_zero(self):
        return float(self.ask('WFMO:XZERO?'))

    def get_out_waveform_vertical_scale_factor(self):
        return float(self.ask('WFMO:YMUlt?'))

    def get_out_waveform_vertical_position(self):
        return float(self.ask('WFMO:YOFf?'))

    def read_data_one_channel(self, channel=None, data_start=None, 
                              data_stop=None, x_axis_out=False,
                              t0=None, DeltaT = None, booster=False):
        """Read waveform from the specified channel
        
        channel : name of the channel (i, 'i', 'chi'). If None, keep
            the previous channel
        data_start : position of the first point in the waveform
        data_stop : position of the last point in the waveform
        x_axis_out : if true, the function returns (X,Y)
                    if false, the function returns Y (default)
        t0 : initial position time in the waveform
        DeltaT : duration of the acquired waveform
            t0, DeltaT and data_start, data_stop are mutually exculsive 
        booster : if set to True, accelerate the acquisition by assuming
            that all the parameters are not change from the previous
            acquisition. If parameters were changed, then the output may
            be different than what is expected. The channel is the only
            parameter that is checked when booster is enable
        
        """
        # set booster to false if it the fist time the method is called
        # We could decide to automaticaly see if parameters of the method
        # are change to set booster to false. However, one cannot
        # detect if the setting of the scope are change
        # To be safe, booster is set to False by default.  
        if booster:  
            if not hasattr(self, 'first_read'): booster=False
            else: 
                if self.first_read: booster=False
        self.first_read=False
        if not booster:
            # Set data_start and data_stop according to parameters
            if t0 is not None or DeltaT is not None:
                if data_stop is None and data_start is None:
                    x_0 = self.get_out_waveform_horizontal_zero()
                    delta_x = self.get_out_waveform_horizontal_sampling_interval()
                    data_start = int((t0 - x_0)/delta_x)+1
                    data_stop = int((t0+DeltaT - x_0)/delta_x)
                else: # data_stop is not None or data_start is not None 
                    raise TektronixScopeError("Error in read_data_one_channel,\
t0, DeltaT and data_start, data_stop args are mutually exculsive")
            if data_start is not None:
                self.set_data_start(data_start)
            if data_stop is not None:
                self.set_data_stop(data_stop) 
            self.data_start = self.get_data_start()
            self.data_stop = self.get_data_stop()
        # Set the channel
        if channel is not None:
            self.set_data_source(channel)
        if not booster:
            if not self.is_channel_selected(channel):
                raise TektronixScopeError("Try to read channel %s which \
is not selectecd"%(str(channel)))
        if not booster:
            self.write("DATA:ENCDG RIB")
            self.write("WFMO:BYTE_NR 2")
            self.offset = self.get_out_waveform_vertical_position()
            self.scale = self.get_out_waveform_vertical_scale_factor()
            self.x_0 = self.get_out_waveform_horizontal_zero()
            self.delta_x = self.get_out_waveform_horizontal_sampling_interval()

        X_axis = self.x_0 + np.arange(self.data_start-1, self.data_stop)*self.delta_x

        buffer = self.ask_raw('CURVE?')
        res = np.frombuffer(buffer, dtype = np.dtype('int16').newbyteorder('>'),
                            offset=int(buffer[1])+2)
        # The output of CURVE? is scaled to the display of the scope
        # The following converts the data to the right scale
        Y = (res - self.offset)*self.scale
        if x_axis_out:
            return X_axis, Y
        else:
            return Y

#Zoom Command Group

                   
