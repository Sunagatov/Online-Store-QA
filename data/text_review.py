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
