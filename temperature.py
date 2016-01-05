class Temperature(object):
    """
    Celsius: "c" or "C", this is the class default
    Fahrenheit: "f" or "F"
    Kelvin: "k" or "K"
    """

    DEFAULT_SCALE = "C"

    def __init__(self, value=None):
        """
        Valid value types are None, int, float, and str

        Temperature() -> "0C"
        Temperature(3) -> "3C"
        Temperature(3.0) -> "3.0C"
        Temperature("10.5f") -> "10.5F"
       """
        if value is None:  # default to 0 degree with default scale
            self.__value = 0
            self.__scale = Temperature.DEFAULT_SCALE
        elif isinstance(value, int) or isinstance(value, float):
            self.__value = value
            self.__scale = Temperature.DEFAULT_SCALE
        else:
            if not isinstance(value, str):
                raise TypeError("Init value must be numeric or a valid temperature string. Example: '100C', '72F'")
            value = value.strip()  # get rid of potential spaces
            if len(value) == 0:  # empty string
                raise ValueError("Invalid init string. Example: '100C', '72F'")

            try:  # is this an integer
                self.__value = int(value)
                self.__scale = Temperature.DEFAULT_SCALE
            except ValueError:
                try:  # is this a float
                    self.__value = float(value)
                    self.__scale = Temperature.DEFAULT_SCALE
                except ValueError:  # expecting a scale qualifier
                    scale = value[-1]
                    if scale not in ["c", "C", "f", "F", "k", "K"]:
                        raise ValueError("Invalid temperature scale. Valid scales are : 'c', 'C', 'f', 'F', 'k', 'K'")

                    temperature = value[:-1]
                    if "." in temperature:  # there's a period, parse temperature as a float
                        try:
                            self.__value = float(temperature)
                        except ValueError:
                            raise ValueError("Invalid temperature '{0}'".format(temperature))
                    else:  # no period, parse temperature as an int
                        try:
                            self.__value = int(temperature)
                        except ValueError:
                            raise ValueError("Invalid temperature '{0}'".format(temperature))

                    self.__scale = scale.upper()

        self.__dscale = self.__scale  # display scale defaults to scale

    def __str__(self):
        return "{0}{1}".format(self.dvalue, self.__dscale)

    def __repr__(self):
        return "{0}{1}".format(self.value, self.__scale)

    def __add__(self, other):
        """
        If other is int or float, new value = __value + other, __scale is old value
        If other is not Temperature, raise TypeError.
        If both self & value are of the same scale, new value = __value + other.__value, __scale is old value
        For the rest, convert __value & other.__value to Kelvin, sum them, set __scale to "K"
        """

        new_t = Temperature()
        new_t.__value = self.__value
        new_t.__scale = self.__scale
        new_t.__dscale = self.__dscale

        # simple addition, __scale & __dscale stay the same
        if isinstance(other, int) or isinstance(other, float):
            new_t.__value += other
            return new_t

        # value must be a Temperature object
        if not isinstance(other, Temperature):
            raise TypeError("int, float or Temperature object expected.")

        # adding 2 Temperature objects with the same scale, __dscale = self.__dscale
        if self.__scale == other.__scale:
            new_t.__value += other.__value
            return new_t

        # adding 2 Temperatures objects with mixed scale, __scale & __dscale set to "K"
        from_ = self.__scale.lower()
        func = "Temperature." + from_ + "2k"
        sum_ = eval(func)(self.__value)  # convert self to Kelvin
        from_ = other.__scale.lower()
        func = "Temperature." + from_ + "2k"
        sum_ += eval(func)(other.__value)  # convert other to Kelvin and add
        new_t.__value = sum_
        new_t.__scale = new_t.__dscale = "K"

        return new_t

    def __sub__(self, other):
        """
        If other is int or float, new value = __value - other, __scale is old value
        If other is not Temperature, raise TypeError.
        If both self & value are of the same scale, new value = __value - other.__value, __scale is old value
        For the rest, convert __value & other.__value to Kelvin, subtract them, set __scale to "K"
        """

        new_t = Temperature()
        new_t.__value = self.__value
        new_t.__scale = self.__scale
        new_t.__dscale = self.__dscale

        # simple subtraction, __scale & __dscale stay the same
        if isinstance(other, int) or isinstance(other, float):
            new_t.__value -= other
            return new_t

        # value must be a Temperature object
        if not isinstance(other, Temperature):
            raise TypeError("int, float or Temperature object expected.")

        # adding 2 Temperature objects with the same scale, __dscale = self.__dscale
        if self.__scale == other.__scale:
            new_t.__value -= other.__value
            return new_t

        # adding 2 Temperatures objects with mixed scale, __scale & __dscale set to "K"
        from_ = self.__scale.lower()
        func = "Temperature." + from_ + "2k"
        diff = eval(func)(self.__value)  # convert self to Kelvin
        from_ = other.__scale.lower()
        func = "Temperature." + from_ + "2k"
        diff -= eval(func)(other.__value)  # convert other to Kelvin and subtract
        new_t.__value = diff
        new_t.__scale = new_t.__dscale = "K"

        return new_t

    def __eq__(self, other):
        left = "Temperature." + self.__scale.lower() + "2k"
        right = "Temperature." + other.__scale.lower() + "2k"
        return eval(left)(self.__value) == eval(right)(other.__value)

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        left = "Temperature." + self.__scale.lower() + "2k"
        right = "Temperature." + other.__scale.lower() + "2k"
        return eval(left)(self.__value) < eval(right)(other.__value)

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        left = "Temperature." + self.__scale.lower() + "2k"
        right = "Temperature." + other.__scale.lower() + "2k"
        return eval(left)(self.__value) > eval(right)(other.__value)

    def __ge__(self, other):
        return self > other or self == other

    @property
    def dscale(self):
        """
        returns the display scale
        """
        return self.__dscale

    @dscale.setter
    def dscale(self, scale):
        """
        sets the display scale
        """
        if not isinstance(scale, str):
            raise TypeError('Display scale muse be one of ["c", "C", "f", "F", "k", "K"]')
        scale = scale.strip()
        if len(scale) != 1:
            raise ValueError('Display scale muse be one of ["c", "C", "f", "F", "k", "K"]')
        if scale not in ["c", "C", "f", "F", "k", "K"]:
            raise ValueError('Display scale muse be one of ["c", "C", "f", "F", "k", "K"]')
        self.__dscale = scale.upper()

    @property
    def dvalue(self):
        from_ = self.__scale.lower()
        to = self.__dscale.lower()
        func = "Temperature." + from_ + "2" + to
        return eval(func)(self.__value)

    @property
    def scale(self):
        """
        returns the scale
        """
        return self.__scale

    @scale.setter
    def scale(self, scale):
        """
        sets the scale
        """
        if not isinstance(scale, str):
            raise TypeError('Temperature scale muse be one of ["c", "C", "f", "F", "k", "K"]')
        scale = scale.strip()
        if len(scale) != 1:
            raise ValueError('Temperature scale muse be one of ["c", "C", "f", "F", "k", "K"]')
        if scale not in ["c", "C", "f", "F", "k", "K"]:
            raise ValueError('Temperature scale muse be one of ["c", "C", "f", "F", "k", "K"]')
        self.__scale = scale.upper()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        """
        reinitialize object with value
        """
        self.__init__(value)

    @staticmethod
    def c2c(c): return c

    @staticmethod
    def c2f(c): return c * 1.8 + 32

    @staticmethod
    def c2k(c): return c + 273.15

    @staticmethod
    def f2c(f): return (f - 32) * 5/9

    @staticmethod
    def f2f(f): return f

    @staticmethod
    def f2k(f): return (f + 459.67) * 5/9

    @staticmethod
    def k2c(k): return k - 273.15

    @staticmethod
    def k2f(k): return k * 1.8 - 459.67

    @staticmethod
    def k2k(k): return k

    @staticmethod
    def set_default_scale(scale):
        if not isinstance(scale, str):
            raise TypeError("Invalid scale. Valid scales are : 'c', 'C', 'f', 'F', 'k', 'K'")
        if len(scale) != 1:
            raise ValueError("Invalid temperature scale. Valid scales are : 'c', 'C', 'f', 'F', 'k', 'K'")
        if scale not in ["c", "C", "f", "F", "k", "K"]:
            raise ValueError("Invalid temperature scale. Valid scales are : 'c', 'C', 'f', 'F', 'k', 'K'")
        Temperature.DEFAULT_SCALE = scale.upper()

import random

def main():
    l = []
    Temperature.set_default_scale("K")
    for i in range(9, -1, -1):
        l.append(Temperature(i))

    for i in l:
        i.dscale = "F"

    l[5].dscale = "k"
    for i in l:
        print i

    print l
    print sorted(l)
    for i in sorted(l):
        print i,
    print

    print "----------------------------"
    temp_list = []
    for i in range(20):
        value = random.randint(-200, 300)
        scale = random.choice(["C", "F", "K"])
        t = Temperature(str(value)+scale)
        t.dscale = "c"
        temp_list.append(t)

    print temp_list
    print sorted(temp_list)
    temp_dvale_list = []
    for t in sorted(temp_list):
        temp_dvale_list.append(t.dvalue)
        print t,
    print
    print temp_dvale_list

    for t in sorted(temp_list):
        print t.value,t.scale, "        ", t.dvalue, "      ", Temperature.f2c(t.value)

    temp_list[2].haha = "haha"
    print temp_list[2].__dict__

    t10 = Temperature("37c")
    t10.dscale="F"
    print t10
    print 1.8*37+32

    print Temperature.c2f(Temperature.f2c(99.9999))

    print Temperature()
    print Temperature("0c") + Temperature("32f")


if __name__ == "__main__":
    main()
