import unittest
from temperature import Temperature


class TestSetDefaultScale(unittest.TestCase):
    def test_c(self):
        Temperature.set_default_scale("c")
        self.assertEquals(Temperature.DEFAULT_SCALE, 'C')

    def test_C(self):
        Temperature.set_default_scale("C")
        self.assertEquals(Temperature.DEFAULT_SCALE, 'C')

    def test_f(self):
        Temperature.set_default_scale("f")
        self.assertEquals(Temperature.DEFAULT_SCALE, 'F')

    def test_F(self):
        Temperature.set_default_scale("F")
        self.assertEquals(Temperature.DEFAULT_SCALE, 'F')

    def test_k(self):
        Temperature.set_default_scale("k")
        self.assertEquals(Temperature.DEFAULT_SCALE, 'K')

    def test_K(self):
        Temperature.set_default_scale("K")
        self.assertEquals(Temperature.DEFAULT_SCALE, 'K')


class TestSetDefaultScaleErrors(unittest.TestCase):
        def test_type_error1(self):  # not a str
            with self.assertRaises(TypeError):
                Temperature.set_default_scale([1, 2, 3])

        def test_type_error2(self):  # not a str
            with self.assertRaises(TypeError):
                Temperature.set_default_scale((1, 2, 3))

        def test_type_error3(self):  # not a str
            with self.assertRaises(TypeError):
                Temperature.set_default_scale(6)

        def test_value_error1(self):  # not a single char str
            with self.assertRaises(ValueError):
                Temperature.set_default_scale("33")

        def test_value_error2(self):  # not a single char str
            with self.assertRaises(ValueError):
                Temperature.set_default_scale("")

        def test_value_error3(self):  # not in ["c", "C", "f", "F", "k", "K"]
            with self.assertRaises(ValueError):
                Temperature.set_default_scale("a")


class TestConstructor(unittest.TestCase):
    def setUp(self):
        self.__oldDefaultScale = Temperature.DEFAULT_SCALE
        Temperature.set_default_scale("C")

    def tearDown(self):
        Temperature.set_default_scale(self.__oldDefaultScale)

    def test_1(self):  # no value specified, 0 degree default scale
        t = Temperature()
        self.assertEquals(str(t), "0C")

    def test_2(self):  # int, default scale
        t = Temperature(100)
        self.assertEquals(str(t), "100C")

    def test_3(self):  # int string, default scale
        t = Temperature("100")
        self.assertEquals(str(t), "100C")

    def test_4(self):  # float string, default scale
        t = Temperature("100.")
        self.assertEquals(str(t), "100.0C")

    def test_5(self):  # float with scale
        t = Temperature("100.k")
        self.assertEquals(str(t), "100.0K")

    def test_6(self):
        Temperature.set_default_scale("f")
        t = Temperature("100")
        self.assertEquals(str(t), "100F")
        Temperature.set_default_scale("k")
        t = Temperature("-50")
        self.assertEquals(str(t), "-50K")

    def test_7(self):  # leading & trailing spaces
        t = Temperature("   100   ")
        self.assertEquals(str(t), "100C")


class TestConstructorErrors(unittest.TestCase):
    def test_type_error1(self):  # not a int, float, str
        with self.assertRaises(TypeError):
            t = Temperature((1, 2))

    def test_type_error2(self):  # not a int, float, str
        with self.assertRaises(TypeError):
            t = Temperature([1, 2])

    def test_value_error1(self):  # empty string
        with self.assertRaises(ValueError):
            t = Temperature("")

    def test_value_error2(self):  # empty string
        with self.assertRaises(ValueError):
            t = Temperature("     ")

    def test_value_error3(self):  # invalid scale
        with self.assertRaises(ValueError):
            t = Temperature("xyz")

    def test_value_error4(self):  # invalid scale
        with self.assertRaises(ValueError):
            t = Temperature("100u")

    def test_value_error5(self):  # invalid number string
        with self.assertRaises(ValueError):
            t = Temperature("10..0f")


class TestConverters(unittest.TestCase):
    def test_c2c(self):
        self.assertEquals(Temperature.c2c(100), 100)

    def test_c2f(self):
        self.assertEquals(Temperature.c2f(20), 68)

    def test_c2k(self):
        self.assertEquals(Temperature.c2k(10), 283.15)

    def test_f2c(self):
        self.assertEquals(Temperature.f2c(68), 20)

    def test_f2f(self):
        self.assertEquals(Temperature.f2f(100), 100)

    def test_f2k(self):
        self.assertAlmostEquals(Temperature.f2k(60), 288.705556, 6)

    def test_k2c(self):
        self.assertEquals(Temperature.k2c(283.15), 10)

    def test_k2f(self):
        self.assertAlmostEquals(Temperature.k2f(288.705556), 60, 5)

    def test_k2k(self):
        self.assertEquals(Temperature.k2k(100), 100)


class Test_dscale(unittest.TestCase):
    def test_1(self):
        t = Temperature("100c")
        self.assertEquals(t.dscale, "C")
        t.dscale = "k"
        self.assertEquals(t.dscale, "K")


class Test_dscale_SetterError(unittest.TestCase):
    def setUp(self):
        self.t = Temperature(100)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            self.t.dscale = 9

    def test_value_error1(self):
        with self.assertRaises(ValueError):
            self.t.dscale = "asdf"

    def test_value_error2(self):
        with self.assertRaises(ValueError):
            self.t.dscale = "  "

    def test_value_error3(self):
        with self.assertRaises(ValueError):
            self.t.dscale = "y"


class Test_dscale_Setter(unittest.TestCase):
    def test_1(self):
        t = Temperature(100)
        self.assertEquals(t._Temperature__dscale, Temperature.DEFAULT_SCALE)
        t.dscale = "k"
        self.assertEquals(t._Temperature__dscale, "K")

    def test_2(self):
        Temperature.set_default_scale("F")
        t = Temperature(32)
        self.assertEquals(str(t), "32F")
        t.dscale = "c"
        self.assertEquals(str(t), "0C")


class Test_dvalue(unittest.TestCase):
    def test_1(self):
        t = Temperature("0C")
        self.assertEquals(t.dvalue, 0)

    def test_2(self):
        t = Temperature("32.F")
        self.assertEquals(t.dvalue, 32)
        t.dscale = "C"
        self.assertEquals(t.dvalue, 0)

    def test_3(self):
        t = Temperature("0k")
        self.assertEquals(t.dvalue, 0)
        t.dscale = "c"
        self.assertEquals(t.dvalue, -273.15)

class Test_scale(unittest.TestCase):
    def test_1(self):
        t = Temperature("100c")
        self.assertEquals(t.scale, "C")
        t.scale = "k"
        self.assertEquals(t.scale, "K")


class Test_scale_SetterError(unittest.TestCase):
    def setUp(self):
        self.t = Temperature(100)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            self.t.scale = 9

    def test_value_error1(self):
        with self.assertRaises(ValueError):
            self.t.scale = "asdf"

    def test_value_error2(self):
        with self.assertRaises(ValueError):
            self.t.scale = "  "

    def test_value_error3(self):
        with self.assertRaises(ValueError):
            self.t.scale = "y"


class Test_scale_Setter(unittest.TestCase):
    def test_1(self):
        t = Temperature(100)
        self.assertEquals(t._Temperature__scale, Temperature.DEFAULT_SCALE)
        t.scale = "k"
        self.assertEquals(t._Temperature__scale, "K")

    def test_2(self):
        Temperature.set_default_scale("F")
        t = Temperature(32)
        self.assertEquals(str(t), "32F")
        t.scale = "c"
        self.assertEquals(t.scale, "C")


class TestValue(unittest.TestCase):
    def test_1(self):
        t = Temperature("-50.5F")
        self.assertEquals(t.value, -50.5)
        t.value = "90k"
        self.assertEquals(t.value, 90)


class TestValueSetter(unittest.TestCase):
    def test_1(self):
        t = Temperature("64f")
        self.assertEquals(t.value, 64)
        self.assertEquals(t._Temperature__scale, "F")
        t.value = "100k"
        self.assertEquals(t.value, 100)
        self.assertEquals(t._Temperature__scale, "K")


class TestValueSetterError(unittest.TestCase):
    def test_1(self):
        t = Temperature("100C")
        with self.assertRaises(TypeError):
            t.value = [1, 2]

    def test_2(self):
        t = Temperature()
        with self.assertRaises(ValueError):
            t.value = "30h"


class TestAdd(unittest.TestCase):
    def setUp(self):
        Temperature.set_default_scale("C")

    def test_1(self):
        t = Temperature(90+5)
        t += 5
        self.assertEquals(t.dvalue, 100)
        self.assertEquals(t.value, 100)

    def test_2(self):
        t = Temperature("32F")
        t.dscale = "c"
        t += 32.
        self.assertEquals(t.value, 64)

    def test_3(self):  # Fahrenheit + Fahrenheit
        t1 = Temperature("32F")
        t2 = Temperature("32F")
        t3 = t1 + t2
        self.assertEquals(t3.value, 64)

    def test_4(self):  # Fahrenheit + Celsius
        t1 = Temperature("32F")
        t2 = Temperature("0C")
        t1.dscale = "K"
        t2.dscale = "K"
        t3 = t1 + t2
        self.assertEquals(t3.value, 546.3)
        self.assertEquals(t3.scale, "K")
        self.assertEquals(t3.dscale, "K")

    def test_5(self):  # Kelvin + Celsius
        t1 = Temperature("273.15K")
        t2 = Temperature("0C")
        t3 = t1 + t2
        self.assertEquals(t3.value, 546.3)
        self.assertEquals(t3.scale, "K")
        self.assertEquals(t3.dscale, "K")

    def test_6(self):
        Temperature.set_default_scale("f")
        t1 = Temperature("1")
        t2 = Temperature("2")
        t3 = t1 + t2
        t4 = t2 + t3
        t5 = t3 + t4
        for i in range(1, 6):
            self.assertEquals(str(eval("t"+str(i)))[-1], "F")
        self.assertEquals(t1.dvalue, 1)
        self.assertEquals(t2.dvalue, 2)
        self.assertEquals(t3.dvalue, 3)
        self.assertEquals(t4.dvalue, 5)
        self.assertEquals(t5.dvalue, 8)

    def test_7(self):
        t1 = Temperature(10)
        t2 = t1 + t1 + t1
        t2 += Temperature(-10)
        self.assertEquals(t2.value, 20)

    def test_8(self):
        t = Temperature("10") - Temperature("30") + Temperature("20")
        self.assertEquals(t.value, 0)


class TestAddError(unittest.TestCase):
    def test_1(self):
        with self.assertRaises(TypeError):
            t = Temperature("33.3 k")
            t += ""


class TestSub(unittest.TestCase):
    def test_1(self):
        t = Temperature(90+5)
        t -= 5
        self.assertEquals(t.dvalue, 90)
        self.assertEquals(t.value, 90)

    def test_2(self):
        t = Temperature("32F")
        t.dscale = "c"
        t -= 32.
        self.assertEquals(t.value, 0)

    def test_3(self):  # Fahrenheit + Fahrenheit
        t1 = Temperature("32F")
        t2 = Temperature("32F")
        t3 = t1 - t2
        self.assertEquals(t3.value, 0)

    def test_4(self):  # Fahrenheit + Celsius
        t1 = Temperature("32F")
        t2 = Temperature("0C")
        t1.dscale = "K"
        t2.dscale = "K"
        t3 = t1 - t2
        self.assertEquals(t3.value, 0)
        self.assertEquals(t3.scale, "K")
        self.assertEquals(t3.dscale, "K")

    def test_5(self):  # Kelvin + Celsius
        t1 = Temperature("273.15K")
        t2 = Temperature("0C")
        t3 = t1 - t2
        self.assertEquals(t3.value, 0)
        self.assertEquals(t3.scale, "K")
        self.assertEquals(t3.dscale, "K")

    def test_6(self):
        Temperature.set_default_scale("k")
        t1 = Temperature("10")
        t2 = Temperature("20")
        t3 = t1 - t2
        t4 = t2 - t3
        t5 = t3 - t4
        for i in range(1, 6):
            self.assertEquals(str(eval("t"+str(i)))[-1], "K")
        self.assertEquals(t1.dvalue, 10)
        self.assertEquals(t2.dvalue, 20)
        self.assertEquals(t3.dvalue, -10)
        self.assertEquals(t4.dvalue, 30)
        self.assertEquals(t5.dvalue, -40)


class TestSubError(unittest.TestCase):
    def test_1(self):
        with self.assertRaises(TypeError):
            t = Temperature("33.3 k")
            t = t - " "


class TestLogicalOperators(unittest.TestCase):
    def setUp(self):
        Temperature.set_default_scale("C")

    def test_equal(self):
        t1 = Temperature()
        t2 = Temperature("273.15k")
        t3 = Temperature("32F")
        t4 = Temperature("100")
        t5 = Temperature("100F")
        self.assertEquals(t1==t2, True)
        self.assertEquals(t1==t3, True)
        self.assertEquals(t2==t3, True)
        self.assertEquals(t3==t4, False)
        self.assertEquals(t3==t5, False)
        self.assertEquals(t4==t5, False)

    def test_notequal(self):
        t1 = Temperature()
        t2 = Temperature("273.15k")
        t3 = Temperature("32F")
        t4 = Temperature("100")
        t5 = Temperature("100F")
        self.assertEquals(t1!=t2, False)
        self.assertEquals(t1!=t3, False)
        self.assertEquals(t2!=t3, False)
        self.assertEquals(t3<>t4, True)
        self.assertEquals(t3<>t5, True)
        self.assertEquals(t4<>t5, True)

    def test_less_than(self):
        t1 = Temperature()
        t2 = Temperature("273.15k")
        t3 = Temperature("32F")
        t4 = Temperature("100")
        t5 = Temperature("100F")
        self.assertEquals(t1<t2, False)
        self.assertEquals(t1<t3, False)
        self.assertEquals(t2<t3, False)
        self.assertEquals(t5<t3, False)
        self.assertEquals(t3<t5, True)
        self.assertEquals(t1<t4, True)

    def test_less_than_or_equal(self):
        t1 = Temperature()
        t2 = Temperature("273.15k")
        t3 = Temperature("32F")
        t4 = Temperature("100")
        t5 = Temperature("100F")
        self.assertEquals(t1<=t2, True)
        self.assertEquals(t1<=t3, True)
        self.assertEquals(t2<=t3, True)
        self.assertEquals(t5<=t3, False)
        self.assertEquals(t4<=t1, False)
        self.assertEquals(t4<=t2, False)

    def test_greater_than(self):
        t1 = Temperature()
        t2 = Temperature("273.15k")
        t3 = Temperature("32F")
        t4 = Temperature("100")
        t5 = Temperature("100F")
        self.assertEquals(t1>t2, False)
        self.assertEquals(t1>t3, False)
        self.assertEquals(t2>t3, False)
        self.assertEquals(t4>t1, True)
        self.assertEquals(t4>t3, True)
        self.assertEquals(t5>t3, True)

    def test_greater_than_or_equal(self):
        t1 = Temperature()
        t2 = Temperature("273.15k")
        t3 = Temperature("32F")
        t4 = Temperature("100")
        t5 = Temperature("100F")
        self.assertEquals(t1>=t2, True)
        self.assertEquals(t1>=t3, True)
        self.assertEquals(t2>=t3, True)
        self.assertEquals(t3>=t4, False)
        self.assertEquals(t3>=t5, False)
        self.assertEquals(t5>=t4, False)

if __name__ == "__main__":
    unittest.main()