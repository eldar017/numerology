import cv2
import numpy as np
from datetime import datetime

class Person:
    def __init__(self, firstName, lastName, dateofBirth):
        self.firstName = firstName
        self.lastName = lastName
        self.dateofBirth = dateofBirth
        self.calcTable = {'א': 1, 'י': 1, 'ק': 1, 'ב': 2, 'כ': 2, 'ך': 2, 'ר': 2, 'ג': 3, 'ל': 3, 'ף': 3,
                          'ש': 3, 'ד': 4, 'מ': 4, 'ם': 4, 'ת': 4, 'ה': 5, 'נ': 5, 'ן': 5, 'ו': 6, 'ס': 6, 'ז': 7, 'ע': 7,
                          'ח': 8, 'פ': 8, 'ף': 8, 'ט': 9, 'צ': 9, 'ץ': 9}
        self.risks = [7, 16, 25, 34, 52, 61, 70, 79, 88, 92]
        self.highrisks = [29, 40, 43]
        self.problematic = 0

    # קוד המחלקה הנוסף כאן...

def plant_parameters(image, parameters, locations):
    """Plants the given parameters at the given locations in the image.

    Args:
        image: The image to plant the parameters in.
        parameters: The parameters to plant.
        locations: The locations to plant the parameters at.

    Returns:
        The image with the parameters planted.
    """
    for location, parameter in zip(locations, parameters):
        cv2.putText(image, str(parameter), location, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
    return image

class Person:
    def __init__(self, firstName, lastName, dateofBirth):
        self.firstName = firstName
        self.lastName = lastName
        self.calcTable = {'א': 1, 'י': 1, 'ק': 1, 'ב': 2, 'כ': 2, 'ך': 2, 'ר': 2, 'ג': 3, 'ל': 3, 'ף': 3,
                          'ש': 3, 'ד': 4, 'מ': 4, 'ם': 4, 'ת': 4, 'ה': 5, 'נ': 5, 'ן': 5, 'ו': 6, 'ס': 6, 'ז': 7, 'ע': 7,
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
                raise KeyError(f"The letter {letter} is not in the calcTable dictionary.")

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
        day = dateofBirth.split("/")[0]
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
        day = dateofBirth.split("/")[0]
        if day[0] == "0":
            day = day[1:]
        month = dateofBirth.split("/")[1]
        if month[0] == "0":
            month = month[1:]
        year = dateofBirth.split("/")[2]
        year = int(year[0]) + int(year[1]) + int(year[2]) + int(year[3])
        total = int(day) + int(month) + int(year)
        reduced = self.calculate_value(total)
        result = f"{total}/{reduced}"
        # red_total = str(total)[0] + str(total)[1]
        # print(f"{str(total)[0]} nad {str(total)[1]}")
        # result = f"{total}\\{red_total}"
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


if __name__ == "__main__":
    firstName = input("הכנס שם פרטי: ")
    lastName = input("הכנס שם משפחה: ")
    dateofBirth = input("הכנס תאריך לידה (בפורמט dd/mm/yyyy): ")

    try:
        birth_date = datetime.strptime(dateofBirth, "%d/%m/%Y")
        day = birth_date.day
        month = birth_date.month
        year = birth_date.year

        person = Person(firstName, lastName, dateofBirth)
        head = person.gethead()
        calHead = person.calculate_value(head)
        hand = person.gethand()
        calHand = person.calculate_value(hand)
        legs = person.getLegs()
        calLegs = person.calculate_value(legs)
        rightLeg = person.getRightLeg()
        calRightLeg = person.calculate_value(rightLeg)
        spirala = person.getSpirala()
        calSpirala = person.calculate_value(spirala)
        leftLeg = person.getLeftLeg()
        calLeftLeg = person.calculate_value(leftLeg)

        print(f"שם מלא: {firstName} {lastName}")
        print(f"תאריך לידה: {day}/{month}/{year}")

        image = np.zeros((300, 600, 3), dtype=np.uint8)
        image = plant_parameters(image, [calFirsrtPeak, calFirsrtPeriod, calSecondPeak, calSecondPeriod, calThirdPeak, calThirdPeriod, calFourthPeak, calFourthPeriod], [(447, 63), (275, 63), (447, 104), (275, 104), (447, 146), (276, 146), (447, 196), (276, 196)])

        cv2.imshow("table.jpg", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except ValueError:
        print("תאריך לידה לא תקין")


        font_face = cv2.FONT_HERSHEY_COMPLEX
        font_scale = 0.55
        font_thickness = 1
        image2 = cv2.imread("table.jpg")

        #   הוספת הטקסטים לתמונה של מפה נומרולוגית
        parameters = [calFirsrtPeak, calFirsrtPeriod, calSecondPeak, calSecondPeriod, calThirdPeak, calThirdPeriod, calFourthPeak, calFourthPeriod]
        locations = [(447, 63), (275, 63), (447, 104), (275, 104), (447, 146), (276, 146), (447, 196), (276, 196)]
        color = (0, 0, 0)  # צבע שחור

        for parameter, location in zip(parameters, locations):
            text = str(parameter)
            position = location
            cv2.putText(image, text, position, font_face, font_scale, color, font_thickness, cv2.LINE_AA, False)
