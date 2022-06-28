from unittest import TestCase

import code_tokenize as ctok

class PythonTokenizationTestCase(TestCase):
    
    def test_tokenize1(self):
        tokens = ctok.tokenize("def my_func():\n    bar()", lang = "python")
        expected = ["def", "my_func", "(", ")", ":", "#INDENT#", "bar", "(", ")", "#NEWLINE#", "#DEDENT#"]
        self.assertEqual(expected, [str(t) for t in tokens])

    def test_tokenize2(self):
        tokens = ctok.tokenize("def my_func(x):\n   x = x + 1\n    return x", lang = "python")
        expected = ["def", "my_func", "(", "x", ")", ":", "#INDENT#", "x", "=", "x", "+", "1", "#NEWLINE#", "return", "x", "#NEWLINE#", "#DEDENT#"]
        self.assertEqual(expected, [str(t) for t in tokens])

    def test_error_handling(self):
        self.assertRaises(SyntaxError, ctok.tokenize, "def my_func(x):\n   x = x + 1    return x", lang = "python")
    
    def test_error_handling2(self):
        tokens = ctok.tokenize("def my_func(x):\n   x = x + 1    return x", lang = "python", syntax_error = "ignore")
        expected = ["def", "my_func", "(", "x", ")", ":",  "x", "=", "x", "+", "1", "#INDENT#", "return", "x", "#NEWLINE#", "#DEDENT#"]
        self.assertEqual(expected, [str(t) for t in tokens])
        


class JavaTokenizationTestCase(TestCase):
    
    def test_tokenize1(self):
        tokens = ctok.tokenize("public class Test {\npublic void myFunc(){\n    bar();\n}\n}", lang = "java")
        expected = ["public", "class", "Test", "{", "public", "void", "myFunc", "(", ")", "{", "bar", "(", ")", ";", "}", "}"]
        self.assertEqual(expected, [str(t) for t in tokens])

    def test_tokenize2(self):
        tokens = ctok.tokenize("public class Test {\npublic int myFunc(int x){\n    x = x + 1;\n    return x;\n}\n}", lang = "java")
        expected = ["public", "class", "Test", "{", "public", "int", "myFunc", "(", "int", "x", ")", "{", "x", "=", "x", "+", "1", ";", "return", "x", ";", "}", "}"]
        self.assertEqual(expected, [str(t) for t in tokens])

    def test_error_handling(self):
        self.assertRaises(SyntaxError, ctok.tokenize, "public int myFunc(int x){\n    x = x + 1;\n    return x;\n}", lang = "java")
    
    def test_error_handling2(self):
        tokens = ctok.tokenize("public int myFunc(int x){\n    x = x + 1;\n    return x;\n}", lang = "java", syntax_error = "ignore")
        expected = ["public", "int", "myFunc", "", "(", "int", "x", ")", "{", "x", "=", "x", "+", "1", ";", "return", "x", ";", "}"]
        self.assertEqual(expected, [str(t) for t in tokens])


class GoTokenizationTest(TestCase):

    def test_tokenize1(self):
        tokens = ctok.tokenize('func main(){\n    tip1 := "test"\n}', lang = "go")
        expected = ["func", "main", "(", ")", "{", "tip1", ":=", '"test"', "#NEWLINE#", "}"]

        self.assertEqual(expected, [str(t) for t in tokens])