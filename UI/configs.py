import pytest


link = "https://iced-latte.uk/"
first_name = "Sarah"
last_name = "Testtest"
email = "sarah@example.com"
password = "P@ssw0rd"

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
                          "Sinyak-Yak Ov",
                          new_last_name_127sym,
                          new_last_name_128sym
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

# Negative values of Names: special characters, non-Latin letters, 1 symbol, empty, 129 symbols, 200 symbols
new_first_name_129sym = "kqijmbiwghdqyflvberhuyzzduezixhzgbtqeeizljzggxbrpgukjfdvsgwzarexwcauuhurnukwtsgqtpqtdwjxdpkaqcwmhobykrksbgppbmoasvwqbcrrkrjljkoev"
new_first_name_200sym = "jsopivxfqnkjjyoskwadzzjxisnbbmjsyxdqetkqnhsduatqhlrfzdlxuniecpbvmyvdfzjvflknsimaxbnwyeeifpyxjnyxevmfnbuvcvjnnwachecpcioveipbsidujhcbjdgevbwwtmuxybulzzvgdrwktxtdcrixrrbnqpqpzqcigegtlkhcvskrgvfhxczimrkm"
new_first_name_negative = ["An&na!", "Петя",
                           pytest.param("R", marks=pytest.mark.xfail(reason='Bug 1 symbol is not fixed')),
                           "", new_first_name_129sym, new_first_name_200sym
                           ]

new_last_name_129sym = "kqijmbiwghdqyflvberhuyzzduezixhzgbtqeeizljzggxbrpgukjfdvsgwzarexwcauuhurnukwtsgqtpqtdwjxdpkaqcwmhobykrksbgppbmoasvwqbcrrkrjljkoev"
new_last_name_200sym = "jsopivxfqnkjjyoskwadzzjxisnbbmjsyxdqetkqnhsduatqhlrfzdlxuniecpbvmyvdfzjvflknsimaxbnwyeeifpyxjnyxevmfnbuvcvjnnwachecpcioveipbsidujhcbjdgevbwwtmuxybulzzvgdrwktxtdcrixrrbnqpqpzqcigegtlkhcvskrgvfhxczimrkm"
new_last_name_negative = ["Sm&it!", "Иванов",
                          pytest.param("Q", marks=pytest.mark.xfail(reason='Bug 1 symbol is not fixed')),
                          "", new_last_name_129sym, new_last_name_200sym
                          ]

'''Negative values of email: non-latin local-part,
                             local-part with dot at the beginning,
                             dot at the end,
                             consecutively dots,
                             65 symbols in local-part,
                             100 symbols in local-part,
                             domain with dot at the beginning, dot at the end, consecutively dots,
                             @@, domain with hyphen at the beginning, hyphen at the end,
                             domain with all-numeric top-level, domain with special char,
                             64 symbols in domain's label,
                             100 symbols in domain's label,
                             256 symbols in domain,
                             300 symbols in domain
'''
new_email_100sym_local = "lloqzpmzpmaluojzvfllivrgrgcypehpnevjquiohvaubtetrjwhmuvqhayayarbdkijwbrtkcabypmurovrcdojxqxtuqfedrxx@mail.com"
new_email_100sym_dom_label = "new@toellyubpniiukppyhzjcylzlnlciqlgggrhssraowrvopspmywgidblkclerrdvdgozarbgtecpjtddktocopxfejnocmxtlmvy.com"
new_email_256sym_domain = "new@nrr7j0tgu3g7okrllb9xa4iv7ayg0pukoszdd4gh.7yiskyid8oh3z2s05vwlsrj8j60t46wouptvp13x6otrqiqcftk0sn23pkm5gbaigtgb3os3t261w0mmubnlfzdykivy7pycwf9nu4qif9oelw31i1girpyec6ibowvre5gvpeprlx9lnlqwkh3syfnt30bdppeyk9joeaki7nf1co9klhj4c7irhe2wqi7zts2hqqrcdyb1tbequpv.com"
new_email_300sym_domain = "new@xtoyfxqjz0bb9p6jtu3lgc0bcs0ck5mga30o7vhgxw4qxmid8gd4gge5vh0ai7y4cirti6a1dhi6c4r29nh5edipn2i73e8snfgii4dkjqt1ws3fhyc93rb5q8zn0mv5vbziqxilfksuad8gaw5181f24qfw59ed3yew2j1me3kiowdy66znahvuslud2zfa80g65ddmfzeskzz8x8i5vf2wkqd64tnky334z67yhvgaohgb2rqvecs2g4v0y4fj80x2ut0zqqmjttphizs76a7zs8a5lnj49848i7og.al7"
new_email_negative = ["иванов@gmail.com",
                      pytest.param(".new@gmail.com", marks=pytest.mark.xfail(reason='Bug incomplete validation local-part is not fixed')),
                      pytest.param("new.@gmail.com", marks=pytest.mark.xfail(reason='Bug incomplete validation local-part is not fixed')),
                      pytest.param("ne..w@gmail.com", marks=pytest.mark.xfail(reason='Bug incomplete validation local-part is not fixed')),
                      pytest.param("wsqegnurpzlzxxfjlaeorhzniwfysavbczdktcxvpvkaqpalzveppsoofuu.rmbde@gmail.com", marks=pytest.mark.xfail(reason='Bug incomplete validation local-part is not fixed')),
                      pytest.param(new_email_100sym_local, marks=pytest.mark.xfail(reason='Bug incomplete validation local-part is not fixed')),
                      "new@.gmail.com", "new@gmail.com.", "new@gmail..com",
                      "new@@gmail.com", "new@-gmail.com", "new@gmail-.com",
                      "new@gmail.999", "new@gmail.c!om",
                      "new@jclyojnoffuidebygkxtspoyuzqhudjqfopugbtgcteiatylxavwdtmxkikbiwse.com",
                      new_email_100sym_dom_label,
                      new_email_256sym_domain,
                      new_email_300sym_domain
                      ]
