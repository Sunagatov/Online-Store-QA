import pytest


link = "https://iced-latte.uk/"
first_name = "Test"
last_name = "Testtest"
email = "ilsinyakovmo4@gmail.com"
password = "80000005a"
'''Positive values of Names: 2 symbols with UPPERCASE letter, 3 symbols lowercase letters, 13 symbols with hyphens and space,
                             127 symbols with hyphens and UPPERCASE letters in the middle,
                             128 symbols with spase
'''
new_first_name_127sym = "vfmpevqkeukeukidxtyxWSqzhdpstrahexbgtmypsmmtqv-ebupnzrslccysaduwtgncthlraykruyqcaqchoelsfiktzvdaewbwymapkfmwxfgbrqqwrsdhoamiyto"
new_first_name_128sym = "vfmpevqkeukeukidxtyxwsqzhdpstrahexbgtmypsmmtqvfebupnzrslccys duwtgncthlraykruyqcaqchoelsfiktzvdaewbwymapkfmwxfgbrqqwrsdhoamiytob"
new_first_name_positive = ["Il", "ily", "Ann-Mary Kate",
                           pytest.param(new_first_name_127sym, marks=pytest.mark.xfail(reason='BE bug (>55 symbols) is not fixed')),
                           pytest.param(new_first_name_128sym, marks=pytest.mark.xfail(reason='BE bug (>55 symbols) is not fixed'))
                           ]
new_last_name_127sym = "qwertvqkeukeukidxtyxWSqzhdpstrahexbgtmypsmmtqv-ebupnzrslccysaduwtgncthlraykruyqcaqchoelsfiktzvdaewbwymapkfmwxfgbrqqwrsdhoamiyto"
new_last_name_128sym = "qwertvqkeukeukidxtyxWSqzhdpstrahexbgtmypsmmtqvs ebupnzrslccysaduwtgncthlraykruyqcaqchoelsfiktzvdaewbwymapkfmwxfgbrqqwrsdhoamiyto"
new_last_name_positive = ["Si", "sin",
                          pytest.param("Sinyak-Yak Ov", marks=pytest.mark.xfail(reason='FE bug "-" & "space" is not fixed')),
                          pytest.param(new_last_name_127sym, marks=pytest.mark.xfail(reason='Bugs: BE (>55 symbols) & FE (- & space) is not fixed')),
                          pytest.param(new_last_name_128sym, marks=pytest.mark.xfail(reason='Bugs: BE (>55 symbols) & FE (- & space) is not fixed')),
                          ]
'''Positive values of email: regular email, local-part with hyphen, local-part with equals, 
                             local-part with dots in the middle not consecutively and with digits,  
                             63 symbols in local-part with UPPERCASE letter, 
                             64 symbols in local-part with +,
                             62 symbols in domain's label with UPPERCASE letter,
                             63 symbols in domain's label with hyphen in the middle,                             
                             254 symbols in domain with digits
                             255 symbols in domain
'''
new_email_254sym_domain = "new@n7j0tgu3g7okrllb9xa4iv7ayg0pukoszdd4gh.7yiskyid8oh3z2s05vwlsrj8j60t46wouptvp13x6otrqiqcftk0sn23pkm5gbaigtgb3os3t261w0mmubnlfzdykivy7pycwf9nu4qif9oelw31i1girpyec6ibowvre5gvpeprlx9lnlqwkh3syfnt30bdppeyk9joeaki7nf1co9klhj4c7irhe2wqi7zts2hqqrcdyb1tbequpv.com"
new_email_255sym_domain = "new@xplglafelnbmkqxbwbukobzbeluzgpyluienzysdvybnnfhmmtdvazsnabvhqblnbgchfjspvoexvtlqakzgugrwtuvacjawutfxsgcuadgdztdtqkokutkkbqnqfcchfjnahteycosdfeccwfzxvsqlgtdgsxhylevtumtiokqarbrzbjhryhuljnpbgrafadczeohpdgrmpdjvgtxxwelffirhczrtnahwnypdxjiwingluiczlagafyx.net"
new_email_positive = ["new@gmail.com", "new-new@gmail.com", 
                      pytest.param("new=new@gmail.com", marks=pytest.mark.xfail(reason='There is not completed requirements')),
                      "new.ne.w9@gmail.com",
                      "wsqegnurpzlzxxfjlaeorHzniwfysavbczdktcxvpvkaqpalzveppsoofuurmbd@gmail.com",
                      "wsqegnurpzlzxxfjlaeorhzniwfysavbczdktcxvpvkaqpalzveppsoofuu+rmbd@gmail.com",
                      "new@wsqegnurpzlzxxfjlaeorhzniwfysavbczdTcxvpvkaqpalzveppsoofuurmbd.com",
                      "new@wsqegnurpzlzxxfjlaeorhzniwfysavbczdktcxvpvka-palzveppsoofuurmbd.net",
                      pytest.param(new_email_254sym_domain, marks=pytest.mark.xfail(reason='There is not completed requirements')),
                      pytest.param(new_email_255sym_domain, marks=pytest.mark.xfail(reason='There is not completed requirements'))
                      ]
