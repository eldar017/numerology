from flask import Flask, request, render_template
import cv2
from datetime import datetime
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def generate_image():
    if request.method == 'POST':
        firstName = request.form.get('firstName', '').strip().replace(' ', '')
        lastName = request.form.get('lastName', '').strip().replace(' ', '')
        birthDay = request.form.get('birthDay')
        birthMonth = request.form.get('birthMonth')
        birthYear = request.form.get('birthYear')
        dateofBirth = f"{birthDay.zfill(2)}/{birthMonth.zfill(2)}/{birthYear}"

        # הוסף את כל הקוד של המחלקה Person כאן
        class Person:

            def __init__(self, firstName, lastName, dateofBirth):
                self.firstName = firstName
                self.lastName = lastName
                self.dateofBirth = dateofBirth
                self.calcTable = {'א': 1, 'י': 1, 'ק': 1, 'ב': 2, 'כ': 2, 'ך': 2, 'ר': 2, 'ג': 3, 'ל': 3, 'ף': 3,
                                  'ש': 3, 'ד': 4, 'מ': 4, 'ם': 4, 'ת': 4, 'ה': 5, 'נ': 5, 'ן': 5, 'ו': 6, 'ס': 6, 'ז': 7,
                                  'ע': 7,
                                  'ח': 8, 'פ': 8, 'ף': 8, 'ט': 9, 'צ': 9, 'ץ': 9}
                self.risks = [7, 16, 25, 34, 52, 61, 70, 79, 88, 92]
                self.highrisks = [29, 40, 43]
                self.problematic = 0

            def ahviChar(self, word):
                self.name = word
                calcTable2 = {'א': 1, 'י': 1, 'ה': 5, 'ו': 6}
                name = list(word)
                total = 0
                for letter in name:
                    if letter == 'א' or letter == 'י' or letter == 'ה' or letter == 'ו':
                        value = calcTable2[letter]
                        total = total + value
                return (total)

            def not_ahviChar(self, word):
                self.name = word
                calcTable2 = {'א': 1, 'י': 1, 'ה': 5, 'ו': 6}
                name = list(word)
                total = 0
                print(name)
                for letter in name:
                    if letter == 'א' or letter == 'י' or letter == 'ה' or letter == 'ו':
                        continue
                    else:
                        # print(letter)
                        value = self.calcTable[letter]
                        # print(value)
                        total = total + value
                return (total)

            def gcalc(self, word):
                """Calculate the gross number from the word."""
                word = list(word)
                total = 0
                for letter in word:
                    if letter in self.calcTable:
                        value = self.calcTable[letter]
                        total += value
                    else:
                        # דלג על תווים לא חוקיים (כמו רווחים, תווים זרים וכו')
                        continue
                return total

            def reduce(self, number):
                """Reduce gross numbers to netto numbers."""
                if number == 11 or number == 22 or number == 13 or number == 14 or number == 16 or number == 19 or number == 33:  # Numbers 11 or 22 should not be reduced.
                    total = number
                else:
                    total = number
                    size = len(str(total))
                    if size > 1:
                        while size > 1:  # Repeats until the number is not fully reduced to one digit only.
                            if total == 11 or total == 22 or total == 13 or total == 14 or total == 16 or total == 19:  # Numbers 11,13,14,16,19,22 should not be reduced.
                                break
                            word = str(total)
                            word = list(word)
                            total = 0
                            for letter in word:
                                total = total + int(letter)
                            size = len(str(total))

                    else:
                        total = number
                return (total)

            def ncalc(self, word):
                """Calculate the netto numbers."""
                word = list(word)
                total = self.gcalc(word)
                total = self.reduce(total)
                return (total)

            def getInNum(self):
                """Return the numeric value of the first letter in a name."""
                nletter = list(self.name)
                nletter = nletter[0]
                total = self.calcTable[nletter]
                return (total)

            def getIsNum(self):
                """Return the numeric values of the first letter in a surname."""
                sletter = list(self.surname)
                sletter
                sletter = sletter[0]
                total = self.calcTable[sletter]
                return (total)

            def gethead(self):
                """ Retuen the numeric value of the head"""
                fname = self.ahviChar(self.firstName)
                fname = self.reduce(fname)
                lname = self.ahviChar(self.lastName)
                lname = self.reduce(lname)
                total = fname + lname
                # print(f'name {sname}, surname {gname}')
                return (total)

            def gethand(self):
                fname = self.ncalc(self.firstName)
                # sname = self.reduce(sname)
                lname = self.ncalc(self.lastName)
                lname = self.reduce(lname)
                total = fname + lname
                return (total)

            def getWest(self):
                """Return the number for the western part of cross."""
                west = self.ncalc(self.surname)
                west = self.reduce(west)
                return (west)

            def getLegs(self):
                """Return the number for the legs part of cross."""
                fname = self.not_ahviChar(self.firstName)
                fname = self.reduce(fname)
                lname = self.not_ahviChar(self.lastName)
                lname = self.reduce(lname)
                total = fname + lname
                # print(f'name {sname}, surname {gname}')
                return (total)

            def getRightLeg(self):
                """Return the number for the right legs ."""
                try:
                    birth_date = datetime.strptime(self.dateofBirth, "%d/%m/%Y")
                    day = birth_date.day
                except ValueError:
                    day = None
                print(f"{self.dateofBirth}")
                day = self.dateofBirth.split("/")[0]
                if day[0] == "0":
                    day = day[1:]
                return day

            def getLeftLeg(self):
                """Return the number for the right legs ."""
                # day = dateofBirthe.split("/")[0]
                # if day[0] == "0":
                #     day = day[1:]
                # month = dateofBirthe.split("/")[1]
                # if month[0] == "0":
                #     month = month[1:]
                # year = dateofBirthe.split("/")[2]
                # year = int(year[0]) + int(year[1]) + int(year[2]) + int(year[3])
                # total1 = int(day) + int(month) + int(year)
                total = int(self.reduce_value(spirala)) + int(self.reduce_value(hand))
                return total

            def getSpirala(self):
                """Return the number for the spirala ."""
                day = self.dateofBirth.split("/")[0]
                if day[0] == "0":
                    day = day[1:]
                month = self.dateofBirth.split("/")[1]
                if month[0] == "0":
                    month = month[1:]
                year = self.dateofBirth.split("/")[2]
                year = int(year[0]) + int(year[1]) + int(year[2]) + int(year[3])
                total = int(day) + int(month) + int(year)
                reduced = self.calculate_value(total)
                result = f"{total}/{reduced}"
                return total

            def calculate_value(self, value):
                new_var = 0
                if int(value) < 10:
                    result = value
                else:
                    for digit in str(value):
                        new_var += int(digit)
                    result = f"{value}/{new_var}"
                return result

            def reduce_value(self, value):
                new_var = 0
                if int(value) < 10:
                    result = value
                else:
                    for digit in str(value):
                        new_var += int(digit)
                    result = new_var
                return result

        # incoming = "שון לוי"
        # dateofBirthe = "04/09/1990"

        # incoming = incoming.upper()
        # incoming = incoming.split(" ")

        # firstName = incoming[0]
        # lastName = incoming[1]

        person = Person(firstName, lastName, dateofBirth)
        print(dateofBirth)
        # print(name)
        # print(surname)
        head = (person.gethead())
        calHead = (person.calculate_value(head))
        hand = (person.gethand())
        calHand = (person.calculate_value(hand))
        legs = (person.getLegs())
        calLegs = (person.calculate_value(legs))
        rightLeg = (person.getRightLeg())
        calRightLeg = (person.calculate_value(rightLeg))
        spirala = (person.getSpirala())
        calSpirala = (person.calculate_value(spirala))
        leftLeg = (person.getLeftLeg())
        calLeftLeg = (person.calculate_value(leftLeg))

        print(
            f"head is: {calHead}, hand is :{calHand}, legs is: {calLegs}, rightLeg is : {calRightLeg}, spirala is: {calSpirala}, leftLeg is : {calLeftLeg}")


        def plant_parameters(image, parameters, locations):
            """Plants the given parameters at the given locations in the image."""
            from PIL import Image, ImageDraw, ImageFont
            # המרת התמונה מ-cv2 ל-PIL
            image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(image_pil)
            try:
                font = ImageFont.truetype("font/Roboto-Regular.ttf", 19)
            except Exception:
                font = ImageFont.load_default()
            for location, parameter in zip(locations, parameters):
                x, y = location
                # קונטור לבן
                draw.text((x, y), str(parameter), font=font, fill="white", stroke_width=4, stroke_fill="white")
                # טקסט שחור מעל
                draw.text((x, y), str(parameter), font=font, fill="black")
            # המרת התמונה חזרה ל-cv2
            image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
            return image

        image = cv2.imread("background.jpg")
        parameters = [calHead, calHand, calHand, calLegs, calRightLeg, calLeftLeg, calSpirala]
        locations = [(302, 38), (509, 408), (75, 410), (283, 727), (540, 726), (25, 726), (312, 208)]
        planted_image = plant_parameters(image, parameters, locations)

        output_path = "static/output_image.jpg"
        cv2.imwrite(output_path, planted_image)

        return render_template('result.html', image=output_path)

    return render_template('form.html')

if __name__ == "__main__":
    app.run()
