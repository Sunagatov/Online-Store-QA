text_review_750_char = (
    "The coffee presents a harmonious blend of boldness"
    " and nuanced flavors, making it an exceptional choice "
    "for both novices and connoisseurs.   Upon opening the "
    "bag, a rich and inviting aroma fills the room, hinting at"
    " the complex experience awaiting each cup. The initial sip "
    "reveals a robust flavor profile, characterized by a perfect "
    "balance between its bright acidity and deep, earthy undertones. "
    "The acidity is pleasantly crisp, enhancing the coffee's vibrant "
    "character without overpowering the palate. This coffee boasts a "
    "full body, providing a velvety mouthfeel that lingers, making "
    "each sip more satisfying than the last. The aftertaste is equally "
    "remarkable, leaving a subtle hint of cocoa and nuts that entices you to savor "
    "just one more cup."
)

text_review_1499_char = f"{text_review_750_char}This coffee boasts a full body, providing a velvety mouthfeel that lingers, making each sip more satisfying than the last. The aftertaste is equally remarkable, leaving a subtle hint of cocoa and nuts that entices you to savor just one more cup.Great care has been taken in sourcing and roasting these beans, resulting in a coffee that stands out for its quality and complexity. Whether enjoyed as a morning ritual or a midday pick-me-up, this coffee promises a richly rewarding experience. In conclusion, this coffee is a true testament to the art of coffee making, from the meticulous selection of beans to the precision in roasting. It’s a brew that not only energizes but also inspires, making it a must-try for anyone who appreciates the finder"
text_review_1_char = "T"
text_review_2_char = "Th"
text_review_1500_char = f"{text_review_750_char}This coffee boasts a full body, providing a velvety mouthfeel that lingers, making each sip more satisfying than the last. The aftertaste is equally remarkable, leaving a subtle hint of cocoa and nuts that entices you to savor just one more cup.Great care has been taken in sourcing and roasting these beans, resulting in a coffee that stands out for its quality and complexity. Whether enjoyed as a morning ritual or a midday pick-me-up, this coffee promises a richly rewarding experience. In conclusion, this coffee is a true testament to the art of coffee making, from the meticulous selection of beans to the precision in roasting. It’s a brew that not only energizes but also inspires, making it a must-try for anyone who appreciates the finders"
text_review_with_emojy = "Just one more cup ☕️☕️☕️☕️☕️"
text_review_with_allowed_symbols = "Just one more cup.,&!()"
text_review_with_extended_latin_letters = "Čafé Lùmièrė stånds øut ås a trùė gem ìn the hēart òf the cìty. Frõm the mōment yøu stėp insìde, yõu're ēngrõssed bý its cõzy ambiånçe ånd wëlcōming atmòsphęre. Thē cåfé bõasts an ēxceptiõnål variety of cõffées and tēas, each with its ûnique flåvor prõfile thåt promises tõ delight your tåste buds.Thē barristas are nõthing shôrt of artísts, cråfting each bēverage with prècisîon and cāre. Whēther ÿou prefer a clássic èspresso or sõmething mōre avant-garde, like their signåture Lávender Latté, yõu're sûre tõ be plēased."
text_review_with_digits = "Just one more cup 5, 10, 20"
# PARAMETERS FOR TEST REVIEW - TEXT, LENGTH OF TEXT, RATING OF PRODUCT
parameterize_text_review_positive = [
    (text_review_750_char, 750, 5),
    (text_review_1500_char, 1500, 4),
    (text_review_1499_char, 1499, 3),
    (text_review_2_char, 2, 2),
    (text_review_1_char, 1, 1),
    (text_review_with_emojy, None, 2),
    (text_review_with_allowed_symbols, None, 1),
    (text_review_with_extended_latin_letters, None, 5),
    (text_review_with_digits, None, 5),
]

# text review for negative test
text_review_1501_char = (
    "I recently decided to purchase espresso online, and I must say, the experience has been exceptional. I ordered a bag of freshly roasted espresso beans from [Brand Name], and from start to finish, everything exceeded my expectations."
    "First, the website was easy to navigate, making the ordering process a breeze. I appreciated the detailed descriptions of each blend, which helped me make an informed decision. The customer reviews and ratings were also very helpful in guiding my choice. I ended up selecting their signature espresso blend, which promised rich, bold flavors and a smooth finish."
    "Shipping was incredibly fast. I received my order within two days, which is impressive considering the usual delays with online orders. The packaging was top-notch, too. The beans came in a resealable bag with a one-way valve to ensure freshness. There was even a personal note from the roaster, which added a nice touch and made the purchase feel special."
    "Now, let’s talk about the espresso itself. The moment I opened the bag, I was greeted with an amazing aroma that instantly filled my kitchen. The beans were roasted to perfection, with a deep, rich color and a slight sheen from the natural oils. Grinding the beans was effortless, and the aroma only intensified, promising a fantastic cup of coffee."
    "Brewing the espresso was a delightful experience. I used my home espresso machine, and the results were outstanding. The shot pulled beautifully, with a thick, golden crema on top. I am so so happy!!!))"
)

text_review_1857_char = (
    "I recently decided to purchase espresso online, and I must say, the experience has been exceptional. I ordered a bag of freshly roasted espresso beans from [Brand Name], and from start to finish, everything exceeded my expectations."
    "First, the website was easy to navigate, making the ordering process a breeze. I appreciated the detailed descriptions of each blend, which helped me make an informed decision. The customer reviews and ratings were also very helpful in guiding my choice. I ended up selecting their signature espresso blend, which promised rich, bold flavors and a smooth finish."
    "Shipping was incredibly fast. I received my order within two days, which is impressive considering the usual delays with online orders. The packaging was top-notch, too. The beans came in a resealable bag with a one-way valve to ensure freshness. There was even a personal note from the roaster, which added a nice touch and made the purchase feel special."
    "Now, let’s talk about the espresso itself. The moment I opened the bag, I was greeted with an amazing aroma that instantly filled my kitchen. The beans were roasted to perfection, with a deep, rich color and a slight sheen from the natural oils. Grinding the beans was effortless, and the aroma only intensified, promising a fantastic cup of coffee."
    "Brewing the espresso was a delightful experience. I used my home espresso machine, and the results were outstanding. The shot pulled beautifully, with a thick, golden crema on top. I am so so happy!!!))"
    "Shipping was incredibly fast. I received my order within two days, which is impressive considering the usual delays with online orders. The packaging was top-notch, too. The beans came in a resealable bag with a one-way valve to ensure freshness. There was even a personal note from the roaster, which added a nice touch and made the purchase feel special."
)

text_review_non_latin_letters = (
    "Купил эспрессо онлайн, и был в восторге от качества. Аромат свежесмолотых зерен наполнил кухню, а вкус готового напитка был богатым и сбалансированным, с нотками шоколада и фруктов."
    "Отличный сервис и быстрая доставка — обязательно закажу снова "
)

text_review_with_not_allowed_symbols = "I'm so happy # % + = - / @ $ *  ; : ' "
text_review_with_empty_text = ""
text_review_with_whitespaces = "          "

# PARAMETERS FOR TEST REVIEW - TEXT, EXPECTED LENGTH, RATING OF PRODUCT, EXPECTED HTTP CODE, EXPECTED MESSAGE
parameterize_text_review_negative = [
    (text_review_non_latin_letters, None, 1, 400, "Invalid data"),
    (text_review_with_not_allowed_symbols, None, 2, 400, "Invalid data"),
    (
        text_review_with_empty_text,
        None,
        3,
        400,
        "ErrorMessage: size must be between 1 and 1500",
    ),
    (
        text_review_1501_char,
        1501,
        4,
        400,
        "ErrorMessage: size must be between 1 and 1500",
    ),
    (
        text_review_1857_char,
        1857,
        4,
        400,
        "ErrorMessage: size must be between 1 and 1500",
    ),
    (text_review_with_whitespaces, None, 5, 400, "Invalid data"),
]

# PARAMETERS FOR TEST REVIEW WITH EMPTY TEXT AND RATING - TEXT, RATING, EXPECTED HTTP CODE, EXPECTED MESSAGE
parameterize_text_review_with_empty_text_and_rating = [
    (text_review_750_char, "", 400, "Rating or review should be filled in"),
    ("", 1, 400, "Rating or review should be filled in"),
    ("", "", 400, "Rating or review should be filled in"),
]
