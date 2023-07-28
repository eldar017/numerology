from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
import cv2
import sys
import time
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
import numpy as np

app = Flask(__name__, static_folder='static')
font1 = TTFont('font/Roboto-Regular.ttf')

# שמור את קובץ הפונט בתבנית המתאימה ל-OpenCV
font1.save('font/converted_robert.xml')

class Person:
    def __init__(self, firstName, lastName, dateofBirth):  # הוספת משתנה 'dateofBirth' למחלקה
        self.firstName = firstName
        self.lastName = lastName
        self.dateofBirth = dateofBirth
        # כאן יש קוד נוסף למחלקה...
        self.calcTable = {'א': 1, 'י': 1, 'ק': 1, 'ב': 2, 'כ': 2, 'ך': 2, 'ר': 2, 'ג': 3, 'ל': 3, 'ף': 3,
                          'ש': 3, 'ד': 4, 'מ': 4, 'ם': 4, 'ת': 4, 'ה': 5, 'נ': 5, 'ן': 5, 'ו': 6, 'ס': 6, 'ז': 7,
                          'ע': 7,'ח': 8, 'פ': 8, 'ף': 8, 'ט': 9, 'צ': 9, 'ץ': 9, ' ': 0}
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
        for letter in name:
            if letter == 'א' or letter == 'י' or letter == 'ה' or letter == 'ו':
                continue
            else:
                value = self.calcTable[letter]
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
                raise KeyError(f"The letter {letter} is not in the calcTable dictionary.")

        return total

    def reduce(self, number):
        number = int(number)
        """Reduce gross numbers to netto numbers."""
        if number == 11 or number == 22 or number == 13 or number == 14 or number == 16 or number == 19 or number == 33:  # Numbers 11 or 22 should not be reduced.
            total = number
        else:
            total = number
            size = len(str(total))
            if size > 1:
                while size > 1:  # Repeats until the number is not fully reduced to one digit only.
                    word = str(total)
                    word = list(word)
                    total = 0
                    for letter in word:
                        total = total + int(letter)
                    size = len(str(total))

            else:
                total = number
            # total = self.reduce_value(total)
        return total

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
        # fname = self.reduce(fname)
        lname = self.ahviChar(self.lastName)
        lname = self.reduce(lname)
        total = fname + lname
        total = self.reduce_value(total)
        return (total)

    def gethand(self):
        fname = self.ncalc(self.firstName)
        self.fname = self.reduce(fname)
        lname = self.ncalc(self.lastName)
        lname = self.reduce(lname)
        total = fname + lname
        total = self.reduce_value(total)
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
        total = self.reduce_value(total)
        return (total)

    def getRightLeg(self):
        """Return the number for the right legs ."""
        day = self.dateofBirth.split("/")[0]
        if day[0] == "0":
            day = day[1:]
        return day

    def getLeftLeg(self):
        """Return the number for the right legs ."""
        total = int(self.reduce_value(self.getSpirala())) + int(self.reduce_value(self.gethand()))
        return total

    def getHeart(self):
        """Return the number for the right legs ."""
        spirala = self.reduce_value(self.getSpirala())
        spirala = self.getCrematic(spirala)
        hand = self.reduce_value(self.gethand())
        hand = self.getCrematic(hand)
        if(spirala > hand):
            total = int(spirala) - int(hand)
        else:
            total = int(hand) - int(spirala)
        return total

    def getCrematic(self, value):
        new_var = 0
        if value == 11 or value == 22 or value == 13 or value == 14 or value == 16 or value == 19 or value == 33:
            for digit in str(value):
                new_var += int(digit)
            value = str(new_var)
        else:
            for digit in str(value):
                new_var += int(digit)
            value = str(new_var)
        return value

    def getSpirala(self):
        """Return the number for the spirala ."""
        day = self.dateofBirth.split("/")[0]
        if day[0] == "0":
            day = day[1:]
        self.day = self.reduce_value(day)
        month = self.dateofBirth.split("/")[1]
        if month[0] == "0":
            month = month[1:]
        self.month = self.reduce_value(month)
        year = self.dateofBirth.split("/")[2]
        year = int(year[0]) + int(year[1]) + int(year[2]) + int(year[3])
        self.year = self.reduce_value(year)
        total = int(self.day) + int(self.month) + int(self.year)
        # print(f"day is {int(day)}, month is : {int(month)}, years is: {int(year)}, total is : {total}")
        total = self.reduce_value(total)
        self.spirala = total
        # print(total)
        return self.spirala

    def getSpirala2(self):
        """Return the number for the spirala ."""
        day = self.dateofBirth.split("/")[0]
        if day[0] == "0":
            day = day[1:]
        day = self.reduce_value(day)
        month = self.dateofBirth.split("/")[1]
        if month[0] == "0":
            month = month[1:]
        month = self.reduce_value(month)
        year = self.dateofBirth.split("/")[2]
        year = int(year[0]) + int(year[1]) + int(year[2]) + int(year[3])
        year = self.reduce_value(year)
        total = int(day) + int(month) + int(year)
        total = self.reduce_value(total)
        return total

    def calculate_value(self, value):
        new_var = 0

        if int(value) < 10:
            result = value
        elif int(value) == 19:
            for digit in str(value):
                new_var += int(digit)
            str_var = str(new_var)
            result = f"{value}/{str_var[0]}"
        else:
            for digit in str(value):
                new_var += int(digit)
            result = f"{value}/{new_var}"
        return result

    def calculate_challenge(self, value):
        new_var = 0
        for digit in str(value):
            new_var += int(digit)
        result = -new_var
        return result

    def reduce_value(self, value):
        val = self.reduce(value)
        new_var = 0
        if val == 11 or val == 22 or val == 13 or val == 14 or val == 16 or val == 19 or val == 33:
            result = val
        elif int(val) < 10:
            result = val
        else:
            for digit in str(val):
                new_var += int(digit)
            result = new_var
        return result

    def sum_value(self, value):
        val = self.reduce(value)
        new_var = 0
        for digit in str(val):
            new_var += int(digit)
        result = new_var
        return result

    def first_peak(self):
        day = self.dateofBirth.split("/")[0]
        if day[0] == "0":
            day = day[1:]
        day = self.reduce_value(day)
        month = self.dateofBirth.split("/")[1]
        if month[0] == "0":
            month = month[1:]
        month = self.reduce_value(month)
        total = int(day) + int(month)
        total = self.reduce_value(total)
        return total

    def first_period(self):
        month = self.dateofBirth.split("/")[1]
        if month[0] == "0":
            month = month[1:]
        month = self.reduce_value(month)
        month = self.reduce_value(month)
        return month

    def second_peak(self):
        day = self.dateofBirth.split("/")[0]
        if day[0] == "0":
            day = day[1:]
        day = self.reduce_value(day)
        year = self.dateofBirth.split("/")[2]
        year = int(year[0]) + int(year[1]) + int(year[2]) + int(year[3])
        year = self.reduce_value(year)
        total = int(day) + int(year)
        total = self.reduce_value(total)
        return total

    def second_period(self):
        day = self.dateofBirth.split("/")[0]
        if day[0] == "0":
            day = day[1:]
        day = self.reduce_value(day)
        return day

    def third_peak(self):
        total = self.reduce_value(self.first_peak()) + self.reduce_value(self.second_peak())
        total = self.reduce_value(total)
        return total

    def third_period(self):
        day = self.dateofBirth.split("/")[0]
        if day[0] == "0":
            day = day[1:]
        day = self.reduce_value(day)
        return day

    def fourth_peak(self):
        month = self.dateofBirth.split("/")[1]
        if month[0] == "0":
            month = month[1:]
        month = self.reduce_value(month)
        year = self.dateofBirth.split("/")[2]
        year = int(year[0]) + int(year[1]) + int(year[2]) + int(year[3])
        year = self.reduce_value(year)
        total = int(month) + int(year)
        total = self.reduce_value(total)
        return total

    def fourth_period(self):
        year = self.dateofBirth.split("/")[2]
        year = int(year[0]) + int(year[1]) + int(year[2]) + int(year[3])
        year = self.reduce_value(year)
        year = self.reduce_value(year)
        return year

    def first_challenge(self):
        if(self.month > self.day):
            self.first_chal = self.month - self.day
        else:
            self.first_chal = self.day - self.month
        self.first_chal = self.reduce_value(self.first_chal)

        return self.first_chal

    def second_challenge(self):
        if(self.year > self.day):
            self.second_chal = self.year - self.day
        else:
            self.second_chal = self.day - self.year
        self.second_chal = self.reduce_value(self.second_chal)

        return self.second_chal

    def third_challenge(self):
        if(self.first_chal > self.second_chal):
            self.third_chal = self.first_chal - self.second_chal
        else:
            self.third_chal = self.second_chal - self.first_chal
        self.third_chal = self.reduce_value(self.third_chal)

        return self.third_chal

    def fourth_challenge(self):
        if (self.year > self.month):
            self.fourth_chal = self.year - self.month
        else:
            self.fourth_chal = self.month - self.year
        self.fourth_chal = self.reduce_value(self.fourth_chal)

        return self.fourth_chal


    def personal_year(self):

        # Assuming the date of birth is in the format "DD/MM/YYYY"
        date_of_birth = self.dateofBirth


        # Parse the date of birth string into a datetime object
        dob = datetime.strptime(date_of_birth, "%d/%m/%Y")

        # Get the current date
        current_date = datetime.now()

        # Compare the month and day of the date of birth with the current month and day
        if (dob.month, dob.day) <= (current_date.month, current_date.day):
            # The person has already celebrated their birthday this year
            actual_years = current_date.year
            self.actual_age = current_date.year - dob.year
            print("Celebrated birthday in", current_date.year,"actual years: " ,actual_years,"(", self.actual_age, "years old)")
        else:
            # The person has not celebrated their birthday this year yet
            actual_years = current_date.year -1
            self.actual_age = current_date.year - 1 - dob.year
            print("Did not celebrate birthday in", current_date.year,"actual years: " ,actual_years, "(", self.actual_age, "years  old)")
        # total = actual_years + current_date.month
        #self.peron_year = self.reduce_value(actual_years) + self.reduce_value(self.month) + self.reduce_value(self.day)
        self.peron_year = self.reduce_value(actual_years) + self.reduce_value(self.first_peak())
        print(f"personal_year is : {self.peron_year}")
        return self.peron_year

    def personal_month(self):
        date_of_birth = self.dateofBirth

        # Parse the date of birth string into a datetime object
        dob = datetime.strptime(date_of_birth, "%d/%m/%Y")

        # Get the current date
        current_date = datetime.now()
        self.peron_month = self.peron_year + self.reduce_value(current_date.month)
        print(f"personal_month is : {self.peron_month}")
        return self.reduce_value(self.peron_month)

    def personal_day(self):
        date_of_birth = self.dateofBirth

        # Parse the date of birth string into a datetime object
        dob = datetime.strptime(date_of_birth, "%d/%m/%Y")
        # Get the current date
        self.firstAge = 36 - self.spirala
        self.printFirstAge = f"0-{self.firstAge}"
        current_date = datetime.now()
        self.peron_day = self.reduce_value(self.peron_month) + self.reduce_value(current_date.day)
        print(f"personal_day is : {self.peron_day}")
        print(f"first age is : {self.printFirstAge}")
        return self.reduce_value(self.peron_day)

    def personal_age(self):
        date_of_birth = self.dateofBirth
        dob = datetime.strptime(date_of_birth, "%d/%m/%Y")
        current_date = datetime.now()
        # self.actual_age = current_date.year - dob.year
        return self.actual_age

    def first_age(self):
        self.firstAge = 36 - self.sum_value(self.spirala)
        print(f"*****{self.sum_value(self.spirala)}")
        self.printFirstAge = f"0-{self.firstAge}"
        print(self.printFirstAge)
        return self.printFirstAge

    def second_age(self):
        self.secondAge = int(self.firstAge)+9
        self.printSecondAge = f"{self.firstAge}-{self.secondAge}"
        return self.printSecondAge

    def third_age(self):
        self.thirdAge = int(self.secondAge) + 9
        self.printThirdAge = f"{self.secondAge}-{self.thirdAge}"
        return self.printThirdAge

    def fourth_age(self):
        self.fourthAge = 120
        self.printFourthAge = f"{self.thirdAge}-{self.fourthAge}"
        return self.printFourthAge

    def _firstName(self):
        print(f"first name number is:{self.fname}")
        return self.fname

    def dayofBirth(self):
        return self.day

    def astrologia(self):
        day = self.dateofBirth.split("/")[0]
        month = self.dateofBirth.split("/")[1]
        astro_sign = ''
        if month == '12':
            astro_sign = 'תשק' if (int(day) < 22) else 'ידג'
        elif month == '01':
            astro_sign = 'ידג' if (int(day) < 20) else 'ילד'
        elif month == '02':
            astro_sign = 'ילד' if (int(day) < 19) else 'םיגד'
        elif month == '03':
            astro_sign = 'םיגד' if (int(day) < 21) else 'הלט'
        elif month == '04':
            astro_sign = 'הלט' if (int(day) < 20) else 'רוש'
        elif month == '05':
            astro_sign = 'רוש' if (int(day) < 21) else 'םימואת'
        elif month == '06':
            astro_sign = 'םימואת' if (int(day) < 21) else 'ןטרס'
        elif month == '07':
            astro_sign = 'ןטרס' if (int(day) < 23) else 'הירא'
        elif month == '08':
            astro_sign = 'הירא' if (int(day) < 23) else 'הלותב'
        elif month == '09':
            astro_sign = 'הלותב' if (int(day) < 23) else 'םיינזאמ'
        elif month == '10':
            astro_sign = 'םיינזאמ' if (int(day) < 23) else 'ברקע'
        elif month == '11':
            astro_sign = 'ברקע' if (int(day) < 22) else 'תשק'
        # print(astro_sign)
        print("Your Astrological sign is :", astro_sign)
        return astro_sign

def plant_parameters(image, parameters, locations):
    """
    Plants the given parameters at the given locations in the image.

    Args:
        image: The image to plant the parameters in.
        parameters: The parameters to plant.
        locations: The locations to plant the parameters at.

    Returns:
        The image with the parameters planted.
    """
    fontPath = 'font/Roboto-Regular.ttf'
    for parameter, location in zip(parameters, locations):

        cv2.putText(image, str(parameter), location, cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0), 1)

    return image

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        dateOfBirth = request.form['dateOfBirth']

        # ... בצע את כל החישובים על פי הקלט המתקבל מהמשתמש ...
        person = Person(firstName, lastName, dateOfBirth)
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
        hearth = (person.getHeart())
        calHearth = (person.calculate_value(hearth))
        leftLeg = (person.getLeftLeg())
        calLeftLeg = (person.calculate_value(leftLeg))
        firstPeak = (person.first_peak())
        calFirsrtPeak = (person.calculate_value(firstPeak))
        secondPeak = (person.second_peak())
        calSecondPeak = (person.calculate_value(secondPeak))
        thirdPeak = (person.third_peak())
        calThirdPeak = (person.calculate_value(thirdPeak))
        fourthPeak = (person.fourth_peak())
        calFourthPeak = (person.calculate_value(fourthPeak))
        firstPeriod = (person.first_period())
        calFirsrtPeriod = (person.calculate_value(firstPeriod))
        secondPeriod = (person.second_period())
        calSecondPeriod = (person.calculate_value(secondPeriod))
        thirdPeriod = (person.third_period())
        calThirdPeriod = (person.calculate_value(thirdPeriod))
        fourthPeriod = (person.fourth_period())
        calFourthPeriod = (person.calculate_value(fourthPeriod))
        firstChallenge = (person.first_challenge())
        calFirstChallenge = (person.calculate_challenge(firstChallenge))
        secondChallenge = (person.second_challenge())
        calSecondChallenge = (person.calculate_challenge(secondChallenge))
        thirdChallenge = (person.third_challenge())
        calThirdChallenge = (person.calculate_challenge(thirdChallenge))
        fourthChallenge = (person.fourth_challenge())
        calFourthChallenge = (person.calculate_challenge(fourthChallenge))
        calFirstAge = (person.first_age())
        calSecondAge = (person.second_age())
        calThirdAge = (person.third_age())
        calFourthAge = (person.fourth_age())
        persoanlYears = (person.personal_year())
        calPersonalYears = (person.calculate_value(persoanlYears))
        persoanlMonth = (person.personal_month())
        calPersonalMonth = (person.calculate_value(persoanlMonth))
        persoanlDay = (person.personal_day())
        calPersonalDay = (person.calculate_value(persoanlDay))
        calPersoanlAge = (person.personal_age())
        firstName = (person._firstName())
        calFirstName = (person.calculate_value(firstName))

        dayOfBirth = (person.dayofBirth())
        calDayOfBirth = (person.calculate_value(dayOfBirth))
        calAstrology = (person.astrologia())
        # calPersonalAge = (person.calculate_value(self.actual_age))

        print(
            f"firstPeak: {calFirsrtPeak}, firstPeriod :{calFirsrtPeriod}, secondPeak: {calSecondPeak}, secondPeriod : {calSecondPeriod}, thirdPeak is: {calThirdPeak}, thirdPeriod is : {calThirdPeriod} , fourthPeak is: {calFourthPeak}, fourthPeriod is : {calFourthPeriod}, personal_yaers is {calPersonalYears}")
        # כאן יש קוד נוסף עם החישובים...

        font_path = 'font/Roboto-Regular.ttf'  # הגדר את הנתיב לקובץ ה-ttf של הפונט
        font_face = cv2.FONT_HERSHEY_COMPLEX
        # font_face = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        font_scale = 0.55
        font_thickness = 1
        image = cv2.imread("background.jpg")

        #   הוספת הטקסטים לתמונה של מפה נומרולוגית
        parameters = [calHead, calHand, calHand, calLegs, calRightLeg, calLeftLeg, calHearth, calSpirala]
        locations = [(290, 38), (509, 408), (70, 410), (283, 727), (540, 726), (25, 726), (320, 210), (285, 298)]
        color = (0, 0, 0)  # צבע שחור



        for parameter, location in zip(parameters, locations):
            if location == (285, 298):
                # print("&&&&&&&&&&&&&&&")
                print(location)
                color = (90, 255, 10)
                font_scale = 0.65
                text = str(parameter)
                position = location
                cv2.putText(image, text, position, font_face, font_scale, color, font_thickness, cv2.LINE_AA, False)
            else:
                font_scale = 0.55
                text = str(parameter)
                position = location
                cv2.putText(image, text, position, font_face, font_scale, color, font_thickness, cv2.LINE_AA, False)

        image2 = cv2.imread("table.jpg")

        #   הוספת הטקסטים לתמונה של מפה נומרולוגית
        parameters2 = [calFirstAge, calSecondAge, calThirdAge, calFourthAge, calFirsrtPeriod, calFirsrtPeak, calSecondPeriod, calSecondPeak, calThirdPeriod, calThirdPeak,
                      calFourthPeriod, calFourthPeak, calFirstChallenge, calSecondChallenge, calThirdChallenge, calFourthChallenge,calPersonalYears, calPersonalMonth, calPersonalDay, calPersoanlAge]
        locations2 = [(667, 68), (667, 110), (667, 154), (667, 204), (447, 68), (275, 68), (447, 110), (275, 110), (447, 154), (276, 154), (447, 204), (276, 204), (87, 68), (87, 110), (87, 150), (87, 190), (374, 272), (374, 306), (374, 332), (374, 376)  ]
        color = (0, 0, 0)  # צבע שחור


        for parameter, location in zip(parameters2, locations2):
            font_scale = 0.55
            text = str(parameter)
            position = location
            cv2.putText(image2, text, position, font_face, font_scale, color, font_thickness, cv2.LINE_AA, False)


        ############
        image3 = cv2.imread("params.jpg")
        image_path = 'params.jpg'
        image3 = cv2.imread(image_path)

        # Define the font properties for Hebrew text
        font_path = 'font/Lunasima-Regular.ttf'
        font_size = 20
        font_color = (0, 0, 0)
        #   הוספת הטקסטים לתמונה של מפה נומרולוגית
        parameters3 = [calFirstName, calDayOfBirth, calAstrology]
        locations3 = [(86, 33), (86, 82), (86, 136)]
        color = (0, 0, 0)  # צבע שחור
        pil_image = Image.fromarray(cv2.cvtColor(image3, cv2.COLOR_BGR2RGB))
        font = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(pil_image)

        for parameter, location in zip(parameters3, locations3):

            text = str(parameter)
            position = location
            draw.text(position, text, font=font, fill=font_color)
        ############
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        output_path = 'static/param_table.jpg'


        cv2.imwrite("static/result.jpg", image)
        cv2.imwrite("static/result_table.jpg", image2)
        cv2.imwrite(output_path, cv_image)
        # cv2.imwrite("static/param_table.jpg", image3)
        return render_template('result.html')

    return render_template('index.html')

@app.route('/home')
def home():
    return redirect(url_for('index'))

@app.route('/result')
def show_result():
    # החישובים והקוד המתאים ליצירת התמונה result.jpg
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    date_of_birth = request.form['dateOfBirth']
    image_filename = 'static/result.jpg'
    image_filename2 = 'static/result_table.jpg'
    return render_template('result.html', image_filename=image_filename, image_filename2=image_filename2)
    #return render_template('result.html', image_filename=image_filename, image_filename2=image_filename2, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
