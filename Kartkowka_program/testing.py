tests = []  # [otput_vars{}, input_vars{}]
 
 
# zmienna1=23;zmienna2=5;ciag1#3=[5,4,7];n=7;ciag2#n=[1,2,3,4,5,6,7] ::: out1=12;
 
def load_tests():
    global tests
    with open('tests.txt', 'r') as f:
        for line in f:
            input_vars = {}
            output_vars = {}
            line = ''.join(line.split())
            input_str, output_str = line.split(':::')
            inp_varstr = input_str.split(';')
            for var in inp_varstr:
                nazwa, wartosc = var.split('=')
                if '#' in nazwa:
                    try:
                        nazwa, rozmiar = nazwa.split('#')
                        nazwa = '#' + nazwa
                        wartosc = wartosc[1:-1]
                        wartosc = wartosc.split(',')
                        wartosc = [int(x) for x in wartosc]
                        try:
                            rozmiar = int(rozmiar)
                        except:
                            try:
                                rozmiar = input_vars[rozmiar]
                            except:
                                print("Error, zły rozmiar ciągu")
                        wartosc.insert(0, rozmiar)
                        input_vars[nazwa] = wartosc
 
                    except:
                        print('Error źle zadeklarowany ciąg {} {}'.format(nazwa, wartosc))
                else:
                    input_vars[nazwa] = int(wartosc)
 
            outp_varstr = output_str.split(';')
            for var in outp_varstr:
                if var:
                    nazwa, wartosc = var.split('=')
                    if '#' in nazwa:
                        try:
                            nazwa, rozmiar = nazwa.split('#')
                            nazwa = '#' + nazwa
                            wartosc = wartosc[1:-1]
                            wartosc = wartosc.split(',')
                            wartosc = [int(x) for x in wartosc]
                            try:
                                rozmiar = int(rozmiar)
                            except:
                                try:
                                    rozmiar = output_vars[rozmiar]
                                except:
                                    print("Error, zły rozmiar ciągu")
                            wartosc.insert(0, rozmiar)
                            output_vars[nazwa] = wartosc
 
                        except:
                            print('Error źle zadeklarowany ciąg {} {}'.format(nazwa, wartosc))
                    else:
                        output_vars[nazwa] = int(wartosc)
 
            test = [input_vars, output_vars]
            tests.append(test)
 
 
print(tests)