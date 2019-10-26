import smbus
from datetime import datetime
from time import sleep


def getTwosComplement(raw_val, length):
        """Get two's complement of `raw_val`.

        Args:
            raw_val (int): Raw value
            length (int): Max bit length

        Returns:
            int: Two's complement
        """
        val = raw_val
        if raw_val & (1 << (length - 1)):
            val = raw_val - (1 << length)
        return val


class DPS310:
    """Class of DPS310, Pressure and Temperature sensor.
    """
    __bus = smbus.SMBus(1)
    __addr = 0x77

    # Compensation Scale Factors
    # Oversampling Rate          | Scale Factor (kP or kT)
    # ---------------------------|------------------------
    #   1       (single)         |  524288
    #   2 times (Low Power)      | 1572864
    #   4 times                  | 3670016
    #   8 times                  | 7864320
    #  16 times (Standard)       |  253952
    #  32 times                  |  516096
    #  64 times (High Precision) | 1040384  <- Configured
    # 128 times                  | 2088960
    __kP = 1040384
    __kT = 1040384


    def __init__(self):
        """Initial setting.

        Execute `self.correctTemperature()` and `self.setOversamplingRate()`.
        """
        self.__correctTemperature()
        self.__setOversamplingRate()


    def __correctTemperature(self):
        """Correct temperature.

        DPS310 sometimes indicates a temperature over 60 degree Celsius
        although room temperature is around 20-30 degree Celsius.
        Call this function to fix.
        """
        # Correct Temp
        DPS310.__bus.write_byte_data(DPS310.__addr, 0x0E, 0xA5)
        DPS310.__bus.write_byte_data(DPS310.__addr, 0x0F, 0x96)
        DPS310.__bus.write_byte_data(DPS310.__addr, 0x62, 0x02)
        DPS310.__bus.write_byte_data(DPS310.__addr, 0x0E, 0x00)
        DPS310.__bus.write_byte_data(DPS310.__addr, 0x0F, 0x00)


    def __setOversamplingRate(self):
        """Set oversampling rate.

        Pressure measurement rate    :  4 Hz
        Pressure oversampling rate   : 64 times
        Temperature measurement rate :  4 Hz
        Temperature oversampling rate: 64 times
        """
        # Oversampling Rate Setting (64time)
        DPS310.__bus.write_byte_data(DPS310.__addr, 0x06, 0x26)
        DPS310.__bus.write_byte_data(DPS310.__addr, 0x07, 0xA6)
        DPS310.__bus.write_byte_data(DPS310.__addr, 0x08, 0x07)
        # Oversampling Rate Configuration
        DPS310.__bus.write_byte_data(DPS310.__addr, 0x09, 0x0C)


    def __getRawPressure(self):
        """Get raw pressure from sensor.

        Returns:
            int: Raw pressure
        """
        p1 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x00)
        p2 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x01)
        p3 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x02)

        p = (p1 << 16) | (p2 << 8) | p3
        p = getTwosComplement(p, 24)
        return p


    def __getRawTemperature(self):
        """Get raw temperature from sensor.

        Returns:
            int: Raw temperature
        """
        t1 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x03)
        t2 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x04)
        t3 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x05)

        t = (t1 << 16) | (t2 << 8) | t3
        t = getTwosComplement(t, 24)
        return t


    def __getPressureCalibrationCoefficients(self):
        """Get pressure calibration coefficients from sensor.

        Returns:
            int: Pressure calibration coefficient (c00)
            int: Pressure calibration coefficient (c10)
            int: Pressure calibration coefficient (c20)
            int: Pressure calibration coefficient (c30)
            int: Pressure calibration coefficient (c01)
            int: Pressure calibration coefficient (c11)
            int: Pressure calibration coefficient (c21)
        """
        src13 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x13)
        src14 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x14)
        src15 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x15)
        src16 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x16)
        src17 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x17)
        src18 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x18)
        src19 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x19)
        src1A = DPS310.__bus.read_byte_data(DPS310.__addr, 0x1A)
        src1B = DPS310.__bus.read_byte_data(DPS310.__addr, 0x1B)
        src1C = DPS310.__bus.read_byte_data(DPS310.__addr, 0x1C)
        src1D = DPS310.__bus.read_byte_data(DPS310.__addr, 0x1D)
        src1E = DPS310.__bus.read_byte_data(DPS310.__addr, 0x1E)
        src1F = DPS310.__bus.read_byte_data(DPS310.__addr, 0x1F)
        src20 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x20)
        src21 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x21)

        c00 = (src13 << 12) | (src14 << 4) | (src15 >> 4)
        c00 = getTwosComplement(c00, 20)

        c10 = ((src15 & 0x0F) << 16) | (src16 << 8) | src17
        c10 = getTwosComplement(c10, 20)

        c20 = (src1C << 8) | src1D
        c20 = getTwosComplement(c20, 16)

        c30 = (src20 << 8) | src21
        c30 = getTwosComplement(c30, 16)

        c01 = (src18 << 8) | src19
        c01 = getTwosComplement(c01, 16)

        c11 = (src1A << 8) | src1B
        c11 = getTwosComplement(c11, 16)

        c21 = (src1E < 8) | src1F
        c21 = getTwosComplement(c21, 16)

        return c00, c10, c20, c30, c01, c11, c21


    def __getTemperatureCalibrationCoefficients(self):
        """Get temperature calibration coefficients from sensor.

        Returns:
            int: Temperature calibration coefficient (c0)
            int: Temperature calibration coefficient (c1)
        """
        src10 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x10)
        src11 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x11)
        src12 = DPS310.__bus.read_byte_data(DPS310.__addr, 0x12)

        c0 = (src10 << 4) | (src11 >> 4)
        c0 = getTwosComplement(c0, 12)

        c1 = ((src11 & 0x0F) << 8) | src12
        c1 = getTwosComplement(c1, 12)

        return c0, c1


    def calcScaledPressure(self):
        """Calculate scaled pressure.

        Returns:
            float: Scaled pressure
        """
        raw_p = self.__getRawPressure()
        scaled_p = raw_p / DPS310.__kP
        return scaled_p


    def calcScaledTemperature(self):
        """Calculate scaled temperature.

        Returns:
            float: Scaled temperature
        """
        raw_t = self.__getRawTemperature()
        scaled_t = raw_t / DPS310.__kT
        return scaled_t


    def calcCompTemperature(self, scaled_t):
        """Calculate compensated temperature.

        Args:
            scaled_t (float): Scaled temperature

        Returns:
            float: Compensated temperature [C]
        """
        c0, c1 = self.__getTemperatureCalibrationCoefficients()
        comp_t = c0 * 0.5 + scaled_t * c1
        return comp_t


    def calcCompPressure(self, scaled_p, scaled_t):
        """Calculate compensated pressure.

        Args:
            scaled_p (float): Scaled pressure
            scaled_t (float): Scaled temperature

        Returns:
            float: Compensated pressure [Pa]
        """
        c00, c10, c20, c30, c01, c11, c21 = \
            self.__getPressureCalibrationCoefficients()
        comp_p = (c00 + scaled_p * (c10 + scaled_p * (c20 + scaled_p * c30))
                + scaled_t * (c01 + scaled_p * (c11 + scaled_p * c21)))
        return comp_p


def main():
    dps310 = DPS310()

    try:
        standard_timestamp = datetime.today().timestamp()
        while True:
            scaled_p = dps310.calcScaledPressure()
            scaled_t = dps310.calcScaledTemperature()
            p = dps310.calcCompPressure(scaled_p, scaled_t)
            t = dps310.calcCompTemperature(scaled_t)
            now_timestamp = datetime.today().timestamp()
            delta_timestamp = now_timestamp - standard_timestamp
            #print(f'{delta_timestamp}: {p:8.1f} Pa {t:4.1f} C')
            print(f'{delta_timestamp}\t{p}')
            sleep(0.1)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
